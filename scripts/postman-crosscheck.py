#!/usr/bin/env python3
"""Cross-check the Postman inventory (from postman-flatten.py) against the mirror:
endpoints missing from openapi.json, query params / body keys / response codes
present in Postman but absent from the spec, and body keys never mentioned in
the relevant api/*.md page. Prints a readable report for a human/LLM analyst.

Usage: postman-crosscheck.py <inventory.json> [openapi.json] [api-dir]
"""
import json, re, sys, pathlib

inv=json.load(open(sys.argv[1]))
spec=json.load(open(sys.argv[2] if len(sys.argv)>2 else "openapi.json"))
api=pathlib.Path(sys.argv[3] if len(sys.argv)>3 else "api")
FOLDER_PAGE={"Profiles":"profiles.md","Tags":"tags.md","Folders":"folders.md","Proxies":"proxies.md",
             "Local client API":"local-client.md","Teams":"teams.md","Fingerprint":"fingerprint.md",
             "Docker":"docker.md","Kubernetes":"docker.md","Automation Libraries":"automation.md",
             "Snippets":"automation.md","Action Log":"action-log.md","Proxy providers":"proxy-providers.md"}

def top_folder(f):
    # since 2026-11 the collection nests the cloud API under a "Public API" folder
    parts=f.split(" / ")
    return parts[1] if parts[0]=="Public API" and len(parts)>1 else parts[0]
pages={p.name:p.read_text() for p in api.glob("*.md")}
alltext="\n".join(pages.values())

def spec_op(path, method):
    for p,ops in spec["paths"].items():
        if re.sub(r"\{[^}]+\}","{}",p)==re.sub(r"\{[^}]+\}","{}",path) and method.lower() in ops:
            return p, ops[method.lower()]
    return None, None

def deref(s, depth=0):
    if depth>6 or not isinstance(s,dict): return s
    if "$ref" in s:
        t=spec
        for part in s["$ref"].lstrip("#/").split("/"): t=t.get(part,{})
        return deref(t, depth+1)
    return s

def schema_keys(s, prefix="", depth=0):
    s=deref(s); out=set()
    if depth>4 or not isinstance(s,dict): return out
    for comb in ("allOf","anyOf","oneOf"):
        for x in s.get(comb,[]): out|=schema_keys(x,prefix,depth+1)
    for k,v in (s.get("properties") or {}).items():
        out.add(prefix+k); out|=schema_keys(v,prefix+k+".",depth+1)
    if s.get("type")=="array" and "items" in s: out|=schema_keys(s["items"],prefix+"[].",depth+1)
    return out

def body_schema(op):
    rb=deref(op.get("requestBody",{})); c=rb.get("content",{})
    for ct in c.values(): return c and ct.get("schema",{})
    return {}

missing=[]; rows=[]
for r in inv:
    if top_folder(r["folder"]) in ("Automation Libraries","Snippets","Docker","Kubernetes"): continue
    page=FOLDER_PAGE.get(top_folder(r["folder"]),"")
    text=pages.get(page,"")
    sp,op=spec_op(r["path"],r["method"])
    issues=[]
    if op is None:
        if r["path"].startswith("/api/v2/"):
            missing.append(f"{r['method']} {r['path']}  ({r['folder']} / {r['name']})")
        # local client endpoints are documented in markdown only
        if r["path"] not in text and r["path"].replace("{","<").replace("}",">") not in text:
            issues.append(f"path not found in api/{page}")
    else:
        sq={p["name"] for p in op.get("parameters",[]) if deref(p).get("in")=="query"}
        xq=set(r["query"])-sq
        if xq: issues.append(f"query params not in spec: {sorted(xq)}")
        sk=schema_keys(body_schema(op)); top={k for k in r["body_keys"] if "." not in k and "[]" not in k}
        xb=top-{k for k in sk if "." not in k}
        if sk and xb: issues.append(f"body keys not in spec: {sorted(xb)}")
        codes={str(x["code"]) for x in r["responses"] if x["code"]}-set(op.get("responses",{}))
        if codes: issues.append(f"response codes not in spec: {sorted(codes)}")
    # markdown field coverage: top-level body keys and query params should be mentioned in the page
    for k in sorted({k for k in r["body_keys"] if "." not in k and "[]" not in k}|set(r["query"])):
        if k and not re.search(r"`"+re.escape(k)+r"`|\b"+re.escape(k)+r"\b", text):
            issues.append(f"`{k}` not mentioned in api/{page}")
    if issues: rows.append((f"{r['method']} {r['path']}  [{r['folder']} / {r['name']}]", issues))

print("# Postman ↔ mirror cross-check\n")
print(f"requests inspected: {len(inv)}")
print("\n## Postman endpoints missing from openapi.json")
print("\n".join("- "+m for m in missing) or "- none")
print("\n## Per-request discrepancies (Postman has it, mirror may not)")
for head,iss in rows:
    print(f"\n### {head}"); print("\n".join("- "+i for i in iss))
if not rows: print("- none")
