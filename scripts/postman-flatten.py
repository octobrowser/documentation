#!/usr/bin/env python3
"""Flatten a Postman collection (documenter JSON) into a deterministic, readable
Markdown document plus a structured inventory, so it can be diffed across fetches
and cross-checked against the mirror.

Usage: postman-flatten.py <collection.json> <out.md> [<inventory.json>]
"""
import html, json, re, sys
from html.parser import HTMLParser

VOLATILE = {"_postman_id", "id", "uid", "_exporter_id", "_postman_isSubFolder"}

class Text(HTMLParser):
    BLOCK = {"p","div","h1","h2","h3","h4","h5","h6","li","tr","br","pre","table","ul","ol","blockquote"}
    def __init__(self): super().__init__(); self.out=[]; self.pre=False
    def handle_starttag(self,t,a):
        if t=="pre": self.pre=True
        if t=="img": self.out.append("[img: %s]" % dict(a).get("src",""))
        if t=="li": self.out.append("\n- ")
        elif t in self.BLOCK: self.out.append("\n")
        elif t in ("td","th"): self.out.append(" | ")
    def handle_endtag(self,t):
        if t=="pre": self.pre=False
        if t in self.BLOCK: self.out.append("\n")
    def handle_data(self,d): self.out.append(d if self.pre else re.sub(r"\s+"," ",d))

def html2text(s):
    if not s: return ""
    p=Text(); p.feed(s); t=html.unescape("".join(p.out))
    return re.sub(r"\n{3,}","\n\n",t).strip()

def pretty(body):
    if body is None: return ""
    s=body if isinstance(body,str) else json.dumps(body)
    try: return json.dumps(json.loads(s), indent=2, sort_keys=True, ensure_ascii=False)
    except Exception: return s.strip()

def url_of(u):
    if isinstance(u,str): return u
    raw=u.get("raw") or ""
    if raw: return raw
    return "/".join(["/".join(u.get("host",[]) if isinstance(u.get("host"),list) else [u.get("host","")]),
                     "/".join(u.get("path",[]) if isinstance(u.get("path"),list) else [u.get("path","")])])

def norm_path(raw):
    raw=re.sub(r"^https?://[^/]+","",raw); raw=re.sub(r"^//","/",raw)
    raw=raw.split("?")[0]; raw=re.sub(r"\{\{[^}]+\}\}","",raw)
    raw=re.sub(r":([A-Za-z_]+)",r"{\1}",raw)
    return "/"+raw.strip("/")

def keys_of(s, prefix=""):
    """Flattened key paths of a JSON-ish string (for inventory)."""
    try: v=json.loads(s) if isinstance(s,str) else s
    except Exception: return set()
    out=set()
    def walk(x,p):
        if isinstance(x,dict):
            for k,val in x.items(): out.add(p+k); walk(val,p+k+".")
        elif isinstance(x,list):
            for val in x[:3]: walk(val,p+"[].")
    walk(v,prefix); return out

def body_text(b):
    if not b: return "", None
    mode=b.get("mode")
    if mode=="raw": return pretty(b.get("raw")), b.get("raw")
    if mode in ("urlencoded","formdata"):
        rows=[f"- `{x.get('key')}` = `{x.get('value','')}`" + (f" — {x['description']}" if x.get('description') else "") for x in b.get(mode,[])]
        return f"({mode})\n"+"\n".join(rows), None
    if mode=="file": return "(file upload)", None
    return pretty(b.get(mode)), None

def emit_request(it, depth, md, inv, crumb):
    r=it.get("request",{})
    if isinstance(r,str): r={"url":r}
    method=r.get("method","GET").upper(); raw=url_of(r.get("url",{})); path=norm_path(raw)
    md.append(f"\n{'#'*min(depth+1,6)} {method} {it['name']}\n")
    md.append(f"`{method} {raw}`\n")
    desc=r.get("description"); desc=desc.get("content") if isinstance(desc,dict) else desc
    if desc: md.append(html2text(desc)+"\n")
    u=r.get("url",{})
    q=[x for x in (u.get("query",[]) if isinstance(u,dict) else []) if not x.get("disabled")]
    if q:
        md.append("**Query**\n"); md += [f"- `{x.get('key')}` = `{x.get('value','')}`"+(f" — {html2text(x['description']) if isinstance(x.get('description'),str) else ''}" if x.get('description') else "") for x in q]; md.append("")
    hdrs=[h for h in r.get("header",[]) if not h.get("disabled")]
    if hdrs:
        md.append("**Headers**\n"); md += [f"- `{h.get('key')}`: `{h.get('value','')}`" for h in hdrs]; md.append("")
    bt,rawbody=body_text(r.get("body"))
    if bt: md.append("**Body**\n"); md.append("```json\n"+bt+"\n```\n")
    resps=it.get("response",[]) or []
    rinv=[]
    for resp in sorted(resps, key=lambda x:(str(x.get("code","")),x.get("name",""))):
        code=resp.get("code",""); md.append(f"**Response {code} — {resp.get('name','')}**\n")
        ru=resp.get("originalRequest",{}) or {}
        rb,_=body_text(ru.get("body")) if ru else ("",None)
        if rb and rb!=bt: md.append("_request:_\n```json\n"+rb+"\n```\n")
        body=pretty(resp.get("body"))
        if body: md.append("```json\n"+body+"\n```\n")
        rinv.append({"code":code,"name":resp.get("name",""),"keys":sorted(keys_of(resp.get("body")))})
    inv.append({"folder":" / ".join(crumb),"name":it["name"],"method":method,"path":path,"raw":raw,
                "query":sorted(x.get("key","") for x in q),"headers":sorted(h.get("key","") for h in hdrs),
                "body_keys":sorted(keys_of(rawbody)) if rawbody else [],"responses":rinv})

def walk(items, depth, md, inv, crumb):
    for it in items:
        if "item" in it:
            md.append(f"\n{'#'*min(depth+1,6)} 📁 {it['name']}\n")
            d=it.get("description"); d=d.get("content") if isinstance(d,dict) else d
            if d: md.append(html2text(d)+"\n")
            walk(it["item"], depth+1, md, inv, crumb+[it["name"]])
        else: emit_request(it, depth, md, inv, crumb)

def main():
    src,out=sys.argv[1],sys.argv[2]; invp=sys.argv[3] if len(sys.argv)>3 else None
    d=json.load(open(src)); c=d.get("collection",d); info=c.get("info",{})
    import datetime
    md=[f"# {info.get('name','Postman collection')}\n", f"<!-- fetched {datetime.date.today().isoformat()} -->\n"]
    if info.get("description"): md.append(html2text(info["description"])+"\n")
    if c.get("variable"):
        md.append("\n## Variables\n"); md += [f"- `{v.get('key')}` = `{v.get('value','')}`" for v in c["variable"]]; md.append("")
    inv=[]; walk(c.get("item",[]),1,md,inv,[])
    open(out,"w").write("\n".join(md).rstrip()+"\n")
    if invp: json.dump(inv, open(invp,"w"), indent=1, sort_keys=True)
    print(f"{len(inv)} requests -> {out}" + (f", inventory -> {invp}" if invp else ""))

if __name__=="__main__": main()
