# Octo Browser API

<!-- fetched 2026-11-18 -->

Swagger schemas

Swagger schemas can be found here.

General information

Get API Token

API tokens are managed in Team settings → API tokens. A team can have several named tokens, each with its own permissions (see API token permissions below).

The number of tokens depends on the subscription plan:

  | Plan  | API tokens

  | Base  | 1

  | Team  | 3

  | Advanced  | 5

The token issued in earlier versions keeps working and is shown in the list as API token with full permissions. It counts towards the limit.

On plans with a single team member, every token has full permissions.

Pass the token in the X-Octo-Api-Token header.

API token permissions

Each token can only call the endpoints allowed by its permissions. A request without the required permission returns 403:

{
    "success": false,
    "msg": "No permission",
    "code": "no_permission",
    "data": ""
}

Alternative API endpoints

You can use alternative API endpoints if your provider is blocking the recommended one

https://app.octobrowser-mirror1.com
https://app.octobrowser-mirror1.net
https://app.octobrowser-mirror1.org

Rate Limits and 429 errors.

Please check status codes for 429 code: different teams have different limits that depend on subscription level. All limits are shared within the team.

If you need higher limits, you can upgrade your subscription to a higher level.

If you need higher limits than those available with the Advanced subscription, please contact our Technical Support.

If you get code 429, stop all requests and pause for retry-after (from headers) seconds.

Not respecting or ignoring 429 responses may result in us enforcing stricter API limits for your team.

You can also check remaining requests and rate limit reset time by inspecting appropriate headers.

Certain API requests may involve more complex processing and, as a result, may cost more than one request point from the RPM (Requests Per Minute) or RPH (Requests Per Hour) limits for their execution. This serves to ensure fair usage and optimal performance for all users.

Retry-After: 0                       # if 0, you can send the next request
X-Ratelimit-Limit: 200               # RPM (requests per minute) limit
X-Ratelimit-Limit-Hour: 3000         # RPH (requests per hour) limit
X-Ratelimit-Remaining: 4             # remaining RPM
X-Ratelimit-Remaining-Hour: 2999     # remaining RPH
X-Ratelimit-Reset: 1671789217        # unix timestamp

Current limits for subscription plans

  | Plan  | RPM  | RPH

  | Base  | 50  | 500

  | Team  | 100  | 1500

  | Advanced  | 200, expandable up to 1,000  | 3,000, expandable up to 50,000

If you require limits exceeding 1,000 RPM and 50,000 RPH, please contact our Support.

Errors

Every error has the same format:

{
    "success": false,
    "msg": "Human-readable message",
    "code": "machine.readable_code",
    "data": ""
}

Use code in your code, msg may change. Some errors include details in data.

Validation errors return 400 with the invalid fields:

{
    "validation_error": {
        "body_params": [ ... ]
    }
}

(query_params, path_params or body_params, depending on where the invalid field is.) A request body with a non-JSON Content-Type returns 415.

Responses with status 400, 409 and 422 cost extra rate-limit points, so check your requests before retrying them.

Data types: prices and balances are strings with a decimal number ("12.5"), dates are ISO 8601 in UTC without a timezone suffix ("2026-10-27T12:00:00").

One-time profiles

Octo has support for one-time profiles that:

-
have faster creation/start time

-
are removed and not synchronized; they are faster to stop and don't clutter the profile list

-
are suitable for certain workloads, such as scraping tasks.

One request POST One-time profile is counted as 4 requests when calculating RPM/RPH limits.

How to run Octo Browser client in the "headless" mode:

Linux

-
open the Terminal in the folder where OctoBrowser.AppImage is located

-
run the command OCTO_HEADLESS=1 ./OctoBrowser.AppImage

Windows

-
open powershell terminal

-
run the command $env:OCTO_HEADLESS = "1"; start 'C:\Program Files\Octo Browser\Octo Browser.exe'

macOS

-
open the Terminal

-
run the command - OCTO_HEADLESS=1 open -a "Octo Browser"

How to run the Octo Browser client with a custom local port:

Linux

-
open the Terminal in the folder where OctoBrowser.AppImage is located

-
run the command OCTO_LOCAL_PORT=55555 ./OctoBrowser.AppImage

Windows

-
open powershell terminal

-
run the command $env:OCTO_LOCAL_PORT = "55555"; start 'C:\Program Files\Octo Browser\Octo Browser.exe'

macOS

-
open the Terminal

-
run the command - OCTO_LOCAL_PORT=55555 open -a "Octo Browser"

Logging into Octo Browser using an API Token

Windows

Open PowerShell and run the following command:

$env:OCTO_API_TOKEN = "YOUR_API_TOKEN"; start 'C:\Program Files\Octo Browser\Octo Browser.exe'

macOS

Open the Terminal and run the following command:

OCTO_API_TOKEN="YOUR_API_TOKEN" open -a "Octo Browser"

Linux

Open the terminal in the folder where OctoBrowser.AppImage is located, and run the following command:

OCTO_API_TOKEN=YOUR_API_TOKEN ./OctoBrowser.AppImage

The client works with the permissions of this token (see API token permissions). Local API requests that need a permission the token doesn't have fail with no_permission.

Actions made in the client are shown in the Action Log as (API).

Silent installation

Windows

To perform a "silent" Octo Browser installation using the terminal, run the .exe installer with the "qn" flag.
Example for Powershell:

& '.\Octo_Browser_latest_win.exe' /qn

macOS

hdiutil attach ./Octo_Browser_latest_mac_arm64.dmg
cp -R /Volumes/Octo\ Browser/Octo\ Browser.app /Applications
hdiutil unmount /Volumes/Octo\ BrowserEndFragment

## Variables

- `baseUrl` = `https://app.octobrowser.net`
- `API_TOKEN` = ``
- `localUrl` = `http://localhost:58888`
- `TAG_UUID` = `8e7c08beb89f4366aa854bdbd7473702`
- `PROFILE_UUID` = ``
- `PROXY_UUID` = `6cbecae429ba48d48836f22baf0e99a0`
- `USER_ACCOUNT` = ``
- `FOLDER_UUID` = ``
- `FOLDER_UUID_OR_NAME` = ``
- `PROVIDER_UUID` = ``
- `MOBILE_PROVIDER_UUID` = ``

## 📁 Public API

### 📁 Profiles

#### GET Get Profiles

`GET https://app.octobrowser.net/api/v2/automation/profiles?page_len=100&page=0&fields=title,description,folder,images_load_limit,launch_args,local_cache,extra_info,proxy,start_pages,tags,pinned_tag,status,last_active,version,storage_options,created_at,updated_at&ordering=active`

Note: if a request contains two tags in the search_tags field, its result will only show profiles containing both tags, not all profiles featuring one of the tags.

Visibility: only profiles available to the token are returned

Without the Edit profiles permission, description is returned masked as **.

status: 0 — not running, 1 — running, 2 — error.

**Response 200 — Get Profiles**

```json
{
  "code": null,
  "data": [
    {
      "uuid": "4bbdc824762342f485bed4968533b28a"
    },
    {
      "uuid": "4565940d5b9b41f99341fae6f5f3d855"
    },
    {
      "uuid": "ded609bdffaa4a6582b1b1d78454d28e"
    },
    {
      "uuid": "abfe707260e74e9aaa1ab7ca0df80caa"
    },
    {
      "uuid": "96516930574740538b0c733b74d68242"
    },
    {
      "uuid": "0e9c63e48099406987c266e72e994bb0"
    },
    {
      "uuid": "055ddebf0d414449be748b08f1ed2ddf"
    },
    {
      "uuid": "f61f8cfabb4c4ce6babf1ac61843b890"
    },
    {
      "uuid": "d9bdf0109e3e43febc28a0380ddf6c0b"
    },
    {
      "uuid": "184b52f2086b4aeba33cabfb8ecee961"
    },
    {
      "uuid": "a353e680e88646c688f9fcce92d00e5f"
    },
    {
      "uuid": "e952ff70362041a2a4045d7054f0c639"
    },
    {
      "uuid": "98e2d1dd14684205a710b9d25812b07e"
    },
    {
      "uuid": "21d471786f4e4038811e1e78371831d9"
    },
    {
      "uuid": "6663f622a8c1446c814d0bc3d0f6bb6e"
    },
    {
      "uuid": "9949a40a62274c11a9d2e8313337f257"
    },
    {
      "uuid": "9223ea89bdfc447aa71159e6d73fc99e"
    },
    {
      "uuid": "1abe52bc7e734ea39e105646ba57f105"
    },
    {
      "uuid": "7e4edc73405f4e4ca35b9640e293b1b3"
    },
    {
      "uuid": "0c53271685954184a18c478852abfc5f"
    },
    {
      "uuid": "eb4db359e99343dd8130a8cddd681e49"
    },
    {
      "uuid": "f631b60aa1c84daf8cfe63fd5aa897d7"
    },
    {
      "uuid": "28fe11f09e4746978db85f87529a1b40"
    },
    {
      "uuid": "d0acc7abc815435f85fe518680341e58"
    },
    {
      "uuid": "a76252cdf1bb4d3dbd9d8fbf706bd80a"
    }
  ],
  "msg": "",
  "page": 0,
  "success": true,
  "total_count": 25
}
```

#### POST Create Profile

`POST https://app.octobrowser.net/api/v2/automation/profiles`

Note: if you don't specify a given parameter, we will generate the best values for it on our servers. Change only the parameters you need to customize.

Required permission: Create profiles. Sending password also required Profile passwords.

Profile data

Note: if you are unsure about how to update or create a profile, you can always modify an existing profile in the browser and then check its data using the get profile API. In most cases, this will give you the information you need.

Proxy

The proxy field accepts three forms:

-
{"uuid": ""} — attach an existing proxy from the proxy list. A plain string, "proxy": "", is accepted and means the same.

-
{"type": ..., "host": ..., "port": ..., "login": ..., "password": ...} — a temporary proxy bound to this profile only: this creates it, or edits the profile's existing temporary proxy in place.

-
null — detach the proxy from the profile; a temporary proxy is deleted in this case, as is the old temporary proxy when a profile is switched from it to a proxy from the list.

Temporary proxies cannot be referenced by uuid, since they belong to a single profile: passing the uuid of a temporary proxy fails with 404 proxy not found, same as an unknown uuid.

Folder

The folder must be available to the token. Otherwise the request returns 403 with code no_permission.

WebRTC options

This feature aims to hide users' actual IP addresses, especially when they are using a proxy. This option makes it possible to disable the transmission of real IP addresses through the non-proxied UDP protocol in WebRTC.

{
  "webrtc": {
        "type": "disable_non_proxied_udp",
        "data": null
      },
    ]
  }
}

{
   "webrtc": {
        "type": "real",
        "data": null
      },
    ]
  }
}

{
   "webrtc": {
        "type": "ip",
        "data": null
      },
    ]
  }
}

Customize language, timezone and geolocation:

Example for language:

{
  "languages": {
    "type": "manual",
    "data": [
      "[ru-RU] Russian (Russia)",
      "[en-US] English (United States)"
    ]
  }
}

Example for timezone:

Note: currently you need to set daylight time manually (this will be fixed later)

{
  "timezone": {
    "type": "manual",
    "data": "America/Detroit"
  }
}

Example for geolocation:

{
"geolocation":{
    "type": "manual",
    "data":{
        "latitude": 41.40338,
        "longitude": 2.17403,
        "accuracy": 10
        }
}
}

Storage Options

{
  "storage_options" : {
    "cookies": true,
    "passwords": true,
    "extensions": true,
    "localstorage": false,
    "history": false,
    "bookmarks": true,
    "serviceworkers": false
   }
}

Cookies

The cookies field of the request body takes either a JSON array of cookie objects or a string in one of the supported formats. The examples below are values of that field, not whole request bodies. A string value may also be base64-encoded, and the string form is capped at 16 MiB.

{
  "cookies": "cookie of permitted format"
}

{
  "cookies": [...]
}

We accept the following cookie formats:

JSON

[
  {
    "domain":".google.com",
    "expirationDate":1639134293.313654,
    "hostOnly":false,
    "httpOnly":false,
    "name":"1P_JAR",
    "path":"/",
    "sameSite":"no_restriction",
    "secure":true,
    "value":"2021-11-10-11"
  }
]

Mozilla

[
  {
    "Path raw":"/",
    "Samesite raw":"no_restriction",
    "Name raw":"NID",
    "Content raw":"2021-11-10-11",
    "Expires raw":"1639134293",
    "Host raw":"https://.google.com/",
    "This domain only raw":"false",
    "HTTP only raw":"false",
    "Send for raw":"true"
  }
]

Netscape

.google.com    TRUE    /    TRUE    1639134293    1P_JAR    2021-11-10-1    544

Each value must be separated by a tab (\t).

.google.com\tTRUE\t/\tTRUE\t1639134293\t1P_JAR\t2021-11-10-1\t544

Bookmarks

{
"bookmarks": [
    {
      "name": "google",
      "url": "https://google.com"
    },
    {
      "name": "ebay",
      "url": "https://ebay.com"
    }
  ]
}

Accessing extra_info from extensions

Data passed to extra_info can be accessed from browser extensions:

-
Add "permissions": ["cookies"] to manifest.json

-
Use chrome.cookies.getOctoProfileExtraInfo (usually from extension's service-worker) to access extra_info as JSON-string:

chrome.cookies.getOctoProfileExtraInfo((extraInfo) => {
  console.log(extraInfo);
});

Fields

- tags — tag names, not UUIDs. Names that do not exist are ignored.

- pinned_tag — tag name, not UUID. Added to tags if missing. A name that does not exist is ignored.

- folder — folder UUID or name.

- image — image UUID, as in the image field of a profile. Unknown UUID falls back to the default image.

- extensions — <id>@<version>, as in the uuid field of Get Extensions.

- images_load_limit — image size limit in bytes, null disables the limit.

- proxy — also accepts a VPN object: {"type": "vpn", "vpn_protocol": "wireguard", "conf": "<base64 WireGuard config>"}.

**Body**

```json
{
    "title": "Test profile from api",
    "description": "test description",
    "start_pages": ["https://fb.com"],
    "password": "password",
    "tags": [
        "octo"
    ],
    "folder": "test",
    "launch_args": ["--start-maximized"],
    "pinned_tag": "octo", // [optional]
    "proxy": {
        "type": "socks5",
        "host": "1.1.1.1",
        "port": 5555,
        "login": "",
        "password": ""
    },
    "storage_options": {
        "cookies": true,
        "passwords": true,
        "extensions": true,
        "localstorage": false,
        "history": false,
        "bookmarks": true
    },
    "cookies": [
    {
      "domain": ".google.com",
      "expirationDate": 1639134293.313654,
      "hostOnly": false,
      "httpOnly": false,
      "name": "1P_JAR",
      "path": "/",
      "sameSite": "no_restriction",
      "secure": true,
      "value": "2021-11-10-11"
    }
    ],
    "image": "48a68cba76684e5c806132b8e461525f",
    "extensions": [],
    "images_load_limit": 10240,
    "local_cache": true,
    "fingerprint": {
        "os": "win",
        "os_version": "11",
        "os_arch": "x86",
        "renderer": "Nvidia GeForce GT 710",
        "screen": "1920x1080",
        "languages": {
            "type": "ip"
        },
        "timezone": {
            "type": "ip"
        },
        "geolocation": {
            "type": "ip"
        },
        "cpu": 4,
        "ram": 8,
        "noise": {
            "webgl": true,
            "canvas": false,
            "audio": true,
            "client_rects": false
        },
        "webrtc": {
            "type": "ip"
        },
        "dns": "1.1.1.1",
        "media_devices": {
            "video_in": 1,
            "audio_in": 1,
            "audio_out": 1
        }
    },
    "extra_info": {
        "any": "value"
    }
}
```

**Response 201 — Create Mobile Profile**

_request:_
```json
{
  "description": "Mobile profiles don't support extensions",
  "fingerprint": {
    "device_model": "SM-T870",
    "device_type": "tablet",
    "os": "android",
    "os_arch": "arm",
    "os_version": "13"
  },
  "title": "Test mobile profile from api"
}
```

**Response 201 — Create Profile**

_request:_
```json
{
  "bookmarks": [
    {
      "name": "example",
      "url": "https://example.com"
    }
  ],
  "cookies": [
    {
      "domain": ".google.com",
      "expirationDate": 1639134293.313654,
      "hostOnly": false,
      "httpOnly": false,
      "name": "1P_JAR",
      "path": "/",
      "sameSite": "no_restriction",
      "secure": true,
      "value": "2021-11-10-11"
    }
  ],
  "description": "test description",
  "extensions": [],
  "fingerprint": {
    "cpu": 4,
    "dns": "1.1.1.1",
    "geolocation": {
      "type": "ip"
    },
    "languages": {
      "type": "ip"
    },
    "media_devices": {
      "audio_in": 1,
      "audio_out": 1,
      "video_in": 1
    },
    "noise": {
      "audio": true,
      "canvas": false,
      "client_rects": false,
      "webgl": true
    },
    "os": "win",
    "os_arch": "x86",
    "os_version": "11",
    "ram": 8,
    "screen": "1920x1080 @1 SDR",
    "timezone": {
      "type": "ip"
    },
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "webrtc": {
      "type": "ip"
    }
  },
  "folder": "folder",
  "image": "36fb48f4e99d47d3b18383d0c27feac2",
  "images_load_limit": 10240,
  "launch_args": [
    "--start-maximized"
  ],
  "local_cache": true,
  "password": "password",
  "proxy": {
    "host": "1.1.1.1",
    "login": "",
    "password": "",
    "port": 5555,
    "type": "socks5"
  },
  "start_pages": [
    "https://fb.com"
  ],
  "storage_options": {
    "bookmarks": true,
    "cookies": true,
    "extensions": true,
    "history": false,
    "localstorage": false,
    "passwords": true,
    "serviceworkers": false
  },
  "tags": [
    "octo"
  ],
  "title": "Test profile from api"
}
```

```json
{
  "code": null,
  "data": {
    "uuid": "d9623a2be9a0431784aacc4500d7963a"
  },
  "msg": "",
  "success": true
}
```

**Response 201 — Create Profile with VPN Proxy**

_request:_
```json
{
  "fingerprint": {
    "os": "win"
  },
  "proxy": {
    "conf": "W0ludGVyZmFjZV0KIyBUaGUgaW50ZXJuYWwgSVAgYWRkcmVzcyBhc3NpZ25lZCB0byB0aGlzIHNwZWNpZmljIGNsaWVudApBZGRyZXNzID0gMTAuMC4wLjIvMjQsIGZkYzk6MjgxZjowNGQ3OjllZTk6OjIvNjQKIyBUaGUgY2xpZW50J3MgdW5pcXVlIHByaXZhdGUga2V5ClByaXZhdGVLZXkgPSA8Q0xJRU5UXzFfUFJJVkFURV9LRVk+CiMgT3B0aW9uYWw6IFRoZSBETlMgc2VydmVyIHRoZSBjbGllbnQgc2hvdWxkIHVzZSB3aGlsZSBjb25uZWN0ZWQKRE5TID0gMS4xLjEuMSwgOC41LjUuNQoKW1BlZXJdCiMgVGhlIHB1YmxpYyBrZXkgb2YgdGhlIFdpcmVHdWFyZCBzZXJ2ZXIKUHVibGljS2V5ID0gPFNFUlZFUl9QVUJMSUNfS0VZPgojIFRoZSBwdWJsaWMgSVAgYWRkcmVzcyBvciBkb21haW4gbmFtZSBhbmQgcG9ydCBvZiB0aGUgc2VydmVyCkVuZHBvaW50ID0gaHR0cDovL3lvdXJkb21haW4uY29tOjU2NzQ1CiMgVHJhZmZpYyB0byByb3V0ZSB0aHJvdWdoIHRoZSB0dW5uZWwuIAojIFVzZSAwLjAuMC4wLzAsIDo6LzAgdG8gcm91dGUgYWxsIGludGVybmV0IHRyYWZmaWMuIAojIFVzZSAxMC4wLjAuMC8yNCB0byBvbmx5IHJvdXRlIHRyYWZmaWMgZGVzdGluZWQgZm9yIHRoZSBWUE4gc3VibmV0LgpBbGxvd2VkSVBzID0gMC4wLjAuMC8wLCA6Oi8wCiMgT3B0aW9uYWw6IFNlbmRzIGEgcGFja2V0IGV2ZXJ5IDI1IHNlY29uZHMgdG8ga2VlcCB0aGUgY29ubmVjdGlvbiBhbGl2ZSBiZWhpbmQgTkFUcwpQZXJzaXN0ZW50S2VlcGFsaXZlID0gMjU=",
    "syn_mode": "profile_based",
    "type": "vpn",
    "vpn_protocol": "wireguard"
  },
  "title": "Test profile from api"
}
```

```json
{
  "code": null,
  "data": {
    "uuid": "e0f29146f19a4707970e2d82abf545e7"
  },
  "msg": "",
  "success": true
}
```

**Response 201 — Create Profile with netscape cookies**

_request:_
```json
{
  "cookies": "some.host\tTRUE\t/\tTRUE\t123\tname\tvalue\nsome2.host\tTRUE\t/\tTRUE\t111\tname2\tvalue2",
  "fingerprint": {
    "os": "win"
  },
  "title": "Test profile from api with netscape cookies"
}
```

```json
{
  "code": null,
  "data": {
    "uuid": "d9623a2be9a0431784aacc4500d7963a"
  },
  "msg": "",
  "success": true
}
```

**Response 201 — Simple Profile**

_request:_
```json
{
  "fingerprint": {
    "os": "win"
  },
  "title": "Test profile from api"
}
```

```json
{
  "code": null,
  "data": {
    "uuid": "21d471786f4e4038811e1e78371831d9"
  },
  "msg": "",
  "success": true
}
```

#### DELETE Delete Profiles

`DELETE https://app.octobrowser.net/api/v2/automation/profiles`

Deletes profiles by uuid, from 1 to 100 per request.

Required permission: Delete profiles.

skip_trash_bin is true by default: profiles are deleted permanently. This is faster and suits profiles you won't need later.

Pass "skip_trash_bin": false to move profiles to the trash bin instead. They can be found with Get Trash Bin and returned with Restore Profiles.

The response splits the requested UUIDs into four lists:

-
deleted_uuids — deleted;

-
active_uuids — running, not deleted;

-
protected_uuids — protected from deletion with the API, not deleted;

-
not_found_uuids — not found in your team or the token has no access to them.

If none of the requested profiles is accessible, the request returns 403 with code profiles.access_error. If nothing was deleted, it returns 404 with the same three lists in errors.

200 does not mean profiles were deleted: check deleted_uuids.

The request has a JSON body. Make sure your HTTP client sends a body with DELETE requests.

**Body**

```json
{
  "skip_trash_bin": true,
  "uuids": [
    "{PROFILE_UUID}"
  ]
}
```

**Response 200 — Delete Profiles**

_request:_
```json
{
  "skip_trash_bin": false,
  "uuids": [
    "8e62ef680ac94859a66ac671298be35c",
    "d7226450b9fb4bac8526c24fc3669814",
    "a4708a63d55742a09b7f1a600c248484"
  ]
}
```

```json
{
  "data": {
    "active_uuids": [
      "d7226450b9fb4bac8526c24fc3669814"
    ],
    "deleted_uuids": [
      "a4708a63d55742a09b7f1a600c248484"
    ],
    "not_found_uuids": [
      "9f0e1d2c3b4a49588776655443322110"
    ],
    "protected_uuids": []
  },
  "msg": "Profiles deleted",
  "success": true
}
```

#### GET Get Trash Bin

`GET https://app.octobrowser.net/api/v2/automation/profiles/trash_bin?page=0&page_len=10&search=`

Returns profiles in the team trash bin, newest first.

Required permission: Delete profiles

Each profile can be restored for free a limited number of times per period. After that, a restore costs tokens. The restore object shows the current terms:

-
paid — true if restoring this profile now costs tokens;

-
price — the price in tokens ("0" for a free restore);

-
free_at — when the next free restore becomes available (null if the restore is free now).

deleted_by is the email of the user who deleted the profile, or (API) if it was deleted with an API token. by_automation_api is true for profiles deleted through the API.

**Response 200 — Get Trash Bin**

```json
{
  "code": null,
  "data": [
    {
      "by_automation_api": true,
      "deleted_at": "2026-10-27T10:15:00",
      "deleted_by": "Scraper (API)",
      "restore": {
        "free_at": null,
        "paid": false,
        "price": "0"
      },
      "title": "Profile 1",
      "uuid": "4bbdc824762342f485bed4968533b28a"
    },
    {
      "by_automation_api": false,
      "deleted_at": "2026-10-26T18:40:00",
      "deleted_by": "user@example.com",
      "restore": {
        "free_at": "2026-10-28T18:40:00",
        "paid": true,
        "price": "1"
      },
      "title": "Profile 2",
      "uuid": "4565940d5b9b41f99341fae6f5f3d855"
    }
  ],
  "msg": "",
  "page": 0,
  "success": true,
  "total_count": 2
}
```

#### POST Restore Profiles

`POST https://app.octobrowser.net/api/v2/automation/profiles/trash_bin/restore`

Restores profiles from the trash bin, from 1 to 100 per request.

Required permission: Delete profiles.

Restores the profiles that can be restored and skips the rest. The response splits the requested UUIDs into three lists:

-
restored_uuids — restored;

-
payment_required_uuids — in the trash bin, but the restore costs tokens (see restore in Get Trash Bin). Paid restores are not available with the API: these profiles stay in the trash bin, restore them in the Octo Browser client;

-
not_found_uuids — not in the trash bin of your team.

  | Status  | Code  | When

  | 403  | profiles.maximum_saved_error  | Restoring would exceed the profile limit of the plan. Nothing is restored

200 does not mean profiles were restored: check restored_uuids.

**Body**

```json
{
  "uuids": [
    "{PROFILE_UUID}"
  ]
}
```

**Response 200 — Restore Profiles**

```json
{
  "data": {
    "not_found_uuids": [
      "9f0e1d2c3b4a49588776655443322110"
    ],
    "payment_required_uuids": [
      "4565940d5b9b41f99341fae6f5f3d855"
    ],
    "restored_uuids": [
      "4bbdc824762342f485bed4968533b28a"
    ]
  },
  "msg": "",
  "success": true
}
```

#### GET Get Profile

`GET https://app.octobrowser.net/api/v2/automation/profiles/:uuid`

status: 0 — not running, 1 — running, 2 — error.

**Response 200 — Get Profile**

```json
{
  "code": null,
  "data": {
    "bookmarks": [],
    "created_at": "2024-08-21T15:40:15",
    "description": "",
    "extensions": [],
    "fingerprint": {
      "cpu": 12,
      "dns": null,
      "fonts": [
        "Candara Light",
        "Sitka Banner",
        "Cascadia Code Regular",
        "Yu Gothic UI Semibold",
        "Symbol",
        "Wingdings",
        "Sitka",
        "Cascadia Mono SemiBold",
        "Microsoft Himalaya",
        "Yu Gothic Regular",
        "Myanmar Text",
        "Sitka Display",
        "Constantia",
        "Cascadia Code",
        "Yu Gothic UI Light",
        "Microsoft YaHei Light",
        "Calibri",
        "Lucida Sans Unicode",
        "Tahoma",
        "Microsoft YaHei UI",
        "Verdana",
        "Webdings",
        "Segoe UI Historic",
        "Sans-Serif",
        "Yu Gothic",
        "Leelawadee UI",
        "Corbel Light",
        "Georgia",
        "Serif",
        "Segoe UI Variable Small Light",
        "Sitka Small Semibold",
        "Microsoft JhengHei Light",
        "Calibri Light",
        "MingLiU-ExtB",
        "Segoe Print",
        "Segoe UI Variable Display Light",
        "Microsoft Yi Baiti",
        "MS UI Gothic",
        "Candara",
        "Cascadia Mono SemiLight",
        "SimSun-ExtB",
        "Courier New",
        "Microsoft New Tai Lue",
        "Corbel",
        "Microsoft JhengHei UI Light",
        "Cascadia Mono",
        "Cascadia Mono Italic",
        "Cascadia Code Light",
        "Segoe UI Variable Small",
        "Palatino Linotype",
        "Lucida Console",
        "Javanese Text",
        "Cascadia Mono SemiLight Italic",
        "Arial Black",
        "Cascadia Code Light Italic",
        "Microsoft Tai Le",
        "Segoe UI Variable",
        "Cascadia Mono Light Italic",
        "PMingLiU-ExtB",
        "Segoe Script",
        "Microsoft YaHei",
        "Segoe Fluent Icons",
        "MS PGothic",
        "Impact",
        "Comic Sans MS",
        "Cascadia Code Bold Italic",
        "Segoe UI Variable Text Light",
        "Monospace",
        "Sitka Text Semibold",
        "Ebrima",
        "Segoe MDL2 Assets",
        "Math",
        "MingLiU_HKSCS-ExtB",
        "Segoe UI Symbol",
        "Mongolian Baiti",
        "Yu Gothic UI Regular",
        "Segoe UI Black",
        "SimSun",
        "Sylfaen",
        "Segoe UI Variable Small Regular",
        "Cascadia Mono Regular",
        "Cascadia Mono Bold Italic",
        "Microsoft JhengHei Regular",
        "Gadugi",
        "Trebuchet MS",
        "Cascadia Code SemiBold",
        "Ink Free",
        "Cascadia Mono SemiBold Italic",
        "Sitka Subheading Semibold",
        "Cambria Math",
        "Microsoft PhagsPa",
        "Yu Gothic Light",
        "Helvetica",
        "Cascadia Code SemiLight",
        "Segoe UI Variable Display Semibold",
        "Emoji",
        "Yu Gothic Medium",
        "Segoe UI Variable Small Semibold",
        "Fantasy",
        "Franklin Gothic Medium",
        "Cascadia Mono Bold",
        "Gabriola",
        "Segoe UI",
        "Sitka Heading",
        "Cascadia Code Italic",
        "Times New Roman",
        "HoloLens MDL2 Assets",
        "Microsoft JhengHei",
        "System-UI",
        "Cascadia Code SemiLight Italic",
        "Cascadia Mono ExtraLight Italic",
        "Segoe UI Semibold",
        "Bahnschrift",
        "Plantagenet Cherokee",
        "Cascadia Code Bold",
        "Segoe UI Variable Text Semibold",
        "NSimSun",
        "Marlett",
        "MV Boli",
        "Microsoft JhengHei UI",
        "Microsoft Sans Serif",
        "Nirmala UI",
        "Segoe UI Variable Text",
        "Microsoft JhengHei UI Regular",
        "Sitka Small",
        "Sitka Subheading",
        "Cascadia Code ExtraLight",
        "Sitka Banner Semibold",
        "Sitka Display Semibold",
        "Cascadia Code ExtraLight Italic",
        "Courier",
        "Sitka Text",
        "Sitka Heading Semibold",
        "Cursive",
        "Segoe UI Variable Display",
        "Fangsong",
        "Cascadia Mono Light",
        "Arial",
        "Segoe UI Variable Display Regular",
        "MS Gothic",
        "Cascadia Code SemiBold Italic",
        "Cascadia Mono ExtraLight",
        "Segoe UI Variable Text Regular",
        "Cambria",
        "Malgun Gothic",
        "Segoe UI Light",
        "Microsoft YaHei UI Light",
        "Segoe UI Emoji",
        "Verdana Italic",
        "KodchiangUPC Bold",
        "Verdana Bold Italic",
        "Microsoft JhengHei UI Bold",
        "Gisha Bold",
        "Rockwell Nova Cond Bold",
        "FangSong",
        "Sakkal Majalla Bold",
        "EucrosiaUPC Bold",
        "Comic Sans MS Bold Italic",
        "MS Mincho",
        "Cambria Bold Italic",
        "IrisUPC Bold Italic",
        "Georgia Bold",
        "Tahoma Bold",
        "Meiryo Italic",
        "Sanskrit Text"
      ],
      "geolocation": {
        "data": null,
        "type": "ip"
      },
      "languages": {
        "data": null,
        "type": "ip"
      },
      "media_devices": {
        "audio_in": 1,
        "audio_out": 1,
        "video_in": 1
      },
      "noise": {
        "audio": false,
        "canvas": false,
        "client_rects": false,
        "webgl": false
      },
      "os": "win",
      "os_arch": "x86",
      "os_version": "11",
      "ram": 16,
      "renderer": "NVIDIA GeForce GT 710",
      "screen": "1440x900 @1 SDR",
      "timezone": {
        "data": null,
        "type": "ip"
      },
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
      "user_agent_changed_by_user": null,
      "webrtc": {
        "data": null,
        "type": "ip"
      }
    },
    "folder": null,
    "has_user_password": true,
    "image": "55e228c7227946b3889f370b54be26c1",
    "last_active": null,
    "local_cache": false,
    "password_set_at": "2024-08-21T15:41:11",
    "pinned_tag": null,
    "proxy": null,
    "start_pages": [],
    "status": 0,
    "storage_options": {
      "bookmarks": true,
      "cookies": true,
      "extensions": true,
      "history": false,
      "localstorage": false,
      "passwords": true,
      "serviceworkers": false
    },
    "tags": [],
    "title": "Quick befitting-sick",
    "updated_at": "2024-08-21T15:41:11",
    "uuid": "cfd673b04de3433caca327836ae69d19",
    "version": "0"
  },
  "msg": "",
  "success": true
}
```

#### PATCH Update Profile

`PATCH https://app.octobrowser.net/api/v2/automation/profiles/:uuid`

Note: It's possible to update running profiles; however, we recommend updating only stopped profiles for synchronization reasons.

Required permission: Edit profiles.

Proxy

The proxy field accepts three forms:

-
{"uuid": ""} — attach an existing proxy from the proxy list. A plain string, "proxy": "", is accepted and means the same.

-
{"type": ..., "host": ..., "port": ..., "login": ..., "password": ...} — a temporary proxy bound to this profile only: this creates it, or edits the profile's existing temporary proxy in place.

-
null — detach the proxy from the profile; a temporary proxy is deleted in this case, as is the old temporary proxy when a profile is switched from it to a proxy from the list.

Temporary proxies cannot be referenced by uuid, since they belong to a single profile: passing the uuid of a temporary proxy fails with 404 proxy not found, same as an unknown uuid.

Folder

The folder must be available to the token. Otherwise the request returns 403 with code no_permission.

Fields

- tags — tag names, not UUIDs. Names that do not exist are ignored. [] removes all tags.

- pinned_tag — tag name, not UUID. Added to tags if missing. A name that does not exist is ignored. null unpins the tag.

- folder — folder UUID or name. null removes the profile from its folder.

- image — image UUID, as in the image field of a profile.

- extensions — <id>@<version>, as in the uuid field of Get Extensions.

- images_load_limit — image size limit in bytes, null disables the limit.

- proxy — also accepts a VPN object: {"type": "vpn", "vpn_protocol": "wireguard", "conf": "<base64 WireGuard config>"}.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "title": "new title", // [optional]
    "description": "new description", // [optional]
    "start_pages": ["https://fb.com"],
        "bookmarks": [{
        "name": "example42",
        "url": "http://example.com"
    }],
    "tags": [ // [optional]
        "new_tag"
    ],
    "folder": "folder", // [optional]
    "launch_args": ["--start-maximized"],
    "pinned_tag": "octo", // [optional],
    "proxy": { // [optional]
        "type": "socks5",
        "host": "1.1.1.1",
        "port": 5555,
        "login": "",
        "password": ""
    },
    "storage_options": { // [optional]
        "cookies": true,
        "passwords": true,
        "extensions": true,
        "localstorage": false,
        "history": false,
        "bookmarks": true
    },
    "cookies": [ // [optional]
    {
      "domain": ".google.com",
      "expirationDate": 1639134293.313654,
      "hostOnly": false,
      "httpOnly": false,
      "name": "1P_JAR",
      "path": "/",
      "sameSite": "no_restriction",
      "secure": true,
      "value": "2021-11-10-11"
    }
    ],
    "image": "36fb48f4e99d47d3b18383d0c27feac2", // [optional]
    "extensions": [], // [optional]
    "local_cache": true, // [optional]
    "fingerprint": { // [optional]
        "os": "win", // [required]
        "os_version": "11", // [optional]
        "os_arch": "x86", // [optional]
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "screen": "1920x1080",
        "languages": {
            "type": "ip"
        },
        "timezone": {
            "type": "ip"
        },
        "geolocation": {
            "type": "ip"
        },
        "cpu": 4,
        "ram": 8,
        "noise": {
            "webgl": true,
            "canvas": false,
            "audio": true,
            "client_rects": false
        },
        "webrtc": {
            "type": "ip"
        },
        "dns": "1.1.1.1",
        "media_devices": {
            "video_in": 1,
            "audio_in": 1,
            "audio_out": 1
        }
    },
    "extra_info": {
        "any": "value"
    }
}
```

**Response 200 — Update Profile**

_request:_
```json
{
  "bookmarks": [
    {
      "name": "example",
      "url": "https://example.com"
    }
  ],
  "fingerprint": {
    "cpu": 4,
    "dns": "",
    "fonts": [
      "Adobe Caslon Pro",
      "Adobe Garamond",
      "Al Bayan",
      "Al Nile",
      "Al Tarikh",
      "American Typewriter",
      "Andale Mono",
      "Apple Braille",
      "Apple Chancery",
      "Apple Color Emoji",
      "Apple Sd Gothic Neo",
      "Apple Symbols",
      "Applegothic",
      "Applemyungjo",
      "Arial",
      "Arial Black",
      "Arial Hebrew",
      "Arial Hebrew Scholar",
      "Arial Narrow",
      "Arial Rounded Mt Bold",
      "Arial Unicode Ms",
      "Avenir",
      "Avenir Next",
      "Avenir Next Condensed",
      "Ayuthaya",
      "Baghdad",
      "Bangla Mn",
      "Bangla Sangam Mn",
      "Baskerville",
      "Baskerville Old Face",
      "Beirut",
      "Big Caslon",
      "Bodoni 72",
      "Bodoni 72 Oldstyle",
      "Bodoni 72 Smallcaps",
      "Bodoni Ornaments",
      "Bradley Hand",
      "Britannic Bold",
      "Brush Script Mt",
      "Candara",
      "Century Gothic",
      "Century Schoolbook",
      "Chalkboard",
      "Chalkboard Se",
      "Chalkduster",
      "Charter",
      "Cochin",
      "Comic Sans Ms",
      "Constantia",
      "Cooper Black",
      "Copperplate",
      "Copperplate Gothic Light",
      "Corbel",
      "Corsiva Hebrew",
      "Courier",
      "Courier New",
      "Damascus",
      "Decotype Naskh",
      "Devanagari Mt",
      "Devanagari Sangam Mn",
      "Didot",
      "Din Alternate",
      "Din Condensed",
      "Diwan Kufi",
      "Diwan Thuluth",
      "Engravers Mt",
      "Euphemia Ucas",
      "Fangsong",
      "Farah",
      "Farisi",
      "Futura",
      "Gb18030 Bitmap",
      "Geeza Pro",
      "Geneva",
      "Georgia",
      "Gill Sans",
      "Gill Sans Mt",
      "Gujarati Mt",
      "Gujarati Sangam Mn",
      "Gulim",
      "Gurmukhi Mn",
      "Gurmukhi Mt",
      "Gurmukhi Sangam Mn",
      "Heiti Sc",
      "Heiti Tc",
      "Helvetica",
      "Helvetica Neue",
      "Herculanum",
      "Hiragino Kaku Gothic Pron",
      "Hiragino Kaku Gothic Stdn",
      "Hiragino Maru Gothic Pron",
      "Hiragino Mincho Pron",
      "Hiragino Sans",
      "Hiragino Sans Gb",
      "Hoefler Text",
      "Impact",
      "Imprint Mt Shadow",
      "Inaimathi",
      "Itf Devanagari",
      "Itf Devanagari Marathi",
      "Kailasa",
      "Kaiti",
      "Kannada Mn",
      "Kannada Sangam Mn",
      "Kefa",
      "Khmer Mn",
      "Khmer Sangam Mn",
      "Kohinoor Bangla",
      "Kohinoor Devanagari",
      "Kohinoor Telugu",
      "Kokonor",
      "Krungthep",
      "Kufistandardgk",
      "Lao Mn",
      "Lao Sangam Mn",
      "Lucida Calligraphy",
      "Lucida Grande",
      "Lucida Sans Unicode",
      "Luminari",
      "Malayalam Mn",
      "Malayalam Sangam Mn",
      "Marker Felt",
      "Marlett",
      "Meiryo",
      "Menlo",
      "Microsoft Sans Serif",
      "Microsoft Yahei",
      "Mingliu_Hkscs",
      "Mishafi",
      "Mishafi Gold",
      "Monaco",
      "Ms Gothic",
      "Mshtakan",
      "Muna",
      "Myanmar Mn",
      "Myanmar Sangam Mn",
      "Nadeem",
      "New Peninim Mt",
      "Noteworthy",
      "Noto Nastaliq Urdu",
      "Onyx",
      "Optima",
      "Oriya Mn",
      "Oriya Sangam Mn",
      "Palatino",
      "Papyrus",
      "Party Let",
      "Phosphate",
      "Pingfang Hk",
      "Pingfang Sc",
      "Pingfang Tc",
      "Plantagenet Cherokee",
      "Princetown Let",
      "Pt Mono",
      "Pt Sans",
      "Pt Sans Caption",
      "Pt Sans Narrow",
      "Pt Serif",
      "Pt Serif Caption",
      "Raanana",
      "Rockwell",
      "Sana",
      "Sathu",
      "Savoye Let",
      "Shree Devanagari 714",
      "Signpainter",
      "Silom",
      "Sinhala Mn",
      "Sinhala Sangam Mn",
      "Skia",
      "Snell Roundhand",
      "Songti Sc",
      "Songti Tc",
      "Stencil",
      "Stixgeneral",
      "Stixintegralsd",
      "Stixintegralssm",
      "Stixintegralsup",
      "Stixintegralsupd",
      "Stixintegralsupsm",
      "Stixnonunicode",
      "Stixsizefivesym",
      "Stixsizefoursym",
      "Stixsizeonesym",
      "Stixsizethreesym",
      "Stixsizetwosym",
      "Stixvariants",
      "Stsong",
      "Sukhumvit Set",
      "Symbol",
      "Tahoma",
      "Tamil Mn",
      "Tamil Sangam Mn",
      "Telugu Mn",
      "Telugu Sangam Mn",
      "Thonburi",
      "Times",
      "Times New Roman",
      "Trajan Pro",
      "Trattatello",
      "Trebuchet Ms",
      "Verdana",
      "Waseem",
      "Webdings",
      "Wingdings",
      "Wingdings 2",
      "Wingdings 3",
      "Zapfino"
    ],
    "geolocation": {
      "type": "ip"
    },
    "languages": {
      "type": "ip"
    },
    "media_devices": {
      "audio_in": 1,
      "audio_out": 1,
      "video_in": 1
    },
    "noise": {
      "audio": true,
      "canvas": false,
      "client_rects": false,
      "webgl": true
    },
    "ram": 16,
    "renderer": "NVIDIA GeForce GT 750M",
    "screen": "2560x1440 @2 SDR P3",
    "timezone": {
      "type": "ip"
    },
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "webrtc": {
      "type": "ip"
    }
  },
  "folder": null,
  "launch_args": [
    "--start-maximized"
  ],
  "proxy": null,
  "tags": [
    "facebook"
  ]
}
```

```json
{
  "code": null,
  "data": {
    "uuid": "d9623a2be9a0431784aacc4500d7963a"
  },
  "msg": "",
  "success": true
}
```

#### POST Import Cookies

`POST https://app.octobrowser.net/api/v2/automation/profiles/:uuid/import_cookies`

Cookies are applied on the next profile start. Returns 409 (profiles.started) if the profile is running.

Required permission: Create profiles.

Cookies format

We accept the following cookie formats:

JSON

[
  {
    "domain":".google.com",
    "expirationDate":1639134293.313654,
    "hostOnly":false,
    "httpOnly":false,
    "name":"1P_JAR",
    "path":"/",
    "sameSite":"no_restriction",
    "secure":true,
    "value":"2021-11-10-11"
  }
]

Mozilla

[
  {
    "Path raw":"/",
    "Samesite raw":"no_restriction",
    "Name raw":"NID",
    "Content raw":"2021-11-10-11",
    "Expires raw":"1639134293",
    "Host raw":"https://.google.com/",
    "This domain only raw":"false",
    "HTTP only raw":"false",
    "Send for raw":"true"
  }
]

Netscape

.google.com    TRUE    /    TRUE    1639134293    1P_JAR    2021-11-10-1    544

Each value must be tab (\t) separated.

.google.com\tTRUE\t/\tTRUE\t1639134293\t1P_JAR\t2021-11-10-1\t544

Request format

JSON

cookies field allows a string or JSON-array

{
  "cookies": "cookie of permitted format"
}

{
  "cookies": [...]
}

File

you can send cookies in MultipartFormdata format in the cookies field

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "cookies": [
    {
      "domain": ".google.com",
      "expirationDate": 1639134293.313654,
      "hostOnly": false,
      "httpOnly": false,
      "name": "1P_JAR",
      "path": "/",
      "sameSite": "no_restriction",
      "secure": true,
      "value": "2021-11-10-11"
    }
  ]
}
```

**Response 200 — Cookies file**

_request:_
```json
(formdata)
- `cookies` = ``
```

```json
{
  "data": "",
  "msg": "Cookies imported",
  "success": true
}
```

**Response 200 — JSON Cookies**

```json
{
  "data": "",
  "msg": "Cookies imported",
  "success": true
}
```

**Response 200 — Mozilla Cookies**

_request:_
```json
{
  "cookies": [
    {
      "Content raw": "2021-11-10-11",
      "Expires raw": "1639134293",
      "HTTP only raw": "false",
      "Host raw": "https://.google.com/",
      "Name raw": "NID",
      "Path raw": "/",
      "Samesite raw": "no_restriction",
      "Send for raw": "true",
      "This domain only raw": "false"
    }
  ]
}
```

```json
{
  "data": "",
  "msg": "Cookies imported",
  "success": true
}
```

**Response 200 — Netscape Cookies**

_request:_
```json
{
  "cookies": "some.host\tTRUE\t/\tTRUE\t123\tname\tvalue\nsome2.host\tTRUE\t/\tTRUE\t111\tname2\tvalue2"
}
```

```json
{
  "data": "",
  "msg": "Cookies imported",
  "success": true
}
```

#### POST Transfer profiles

`POST https://app.octobrowser.net/api/v2/automation/profiles/transfer`

This transfers profiles from one account to another.

Note: The maximum profiles count limit is 100 entries at once.

Required permission: Transfer profiles.

200 means at least one profile was transferred, the rest are skipped without being listed.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "receiver_email": "",
  "transfer_proxy": true,
  "uuids": [
    ""
  ]
}
```

**Response 200 — Transfer with proxy**

_request:_
```json
{
  "receiver_email": "uywez34@mailto.plus",
  "transfer_proxy": true,
  "uuids": [
    "cb4de994eb5e4f2b9b56f7d0ac92d0ae"
  ]
}
```

```json
{
  "data": "",
  "msg": "Profiles transferred successfully",
  "success": true
}
```

**Response 200 — Transfer without proxy**

_request:_
```json
{
  "receiver_email": "uywez34@mailto.plus",
  "transfer_proxy": false,
  "uuids": [
    "cb4de994eb5e4f2b9b56f7d0ac92d0ae"
  ]
}
```

```json
{
  "data": "",
  "msg": "Profiles transferred successfully",
  "success": true
}
```

#### POST Force Stop Profile

`POST https://app.octobrowser.net/api/v2/automation/profiles/:uuid/force_stop`

Marks a running profile as stopped without syncing. Unsynced changes are lost.

version (optional, number or string): running session version, 409 on mismatch. Omit to stop the current session.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "version": 1 // [optional]
}
```

**Response 200 — Force Stop Profile**

_request:_
```json
{
  "version": null
}
```

```json
{
  "data": "",
  "msg": "Profile stopped",
  "success": true
}
```

**Response 200 — Force Stop Profile (with consistency check)**

_request:_
```json
{
  "version": 1
}
```

```json
{
  "data": "",
  "msg": "Profile stopped",
  "success": true
}
```

#### POST Mass Force Stop Profile

`POST https://app.octobrowser.net/api/v2/automation/profiles/force_stop`

Forcibly stops several running profiles, listed by uuid in the uuids field — from 1 to 100 per request. Unlike the single-profile endpoint, this one takes no version parameter and performs no version consistency check.

The failed field of the response lists the uuids that were not stopped (for example, profiles that weren't running). The response status is 200 when all requested profiles were stopped, 207 Multi-Status when only some were, and 400 when none were — in the last case the failed list is returned in errors.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "uuids": [
    "{PROFILE_UUID}"
  ]
}
```

**Response 200 — Force Stop Profile Success**

```json
{
  "data": {
    "failed": []
  },
  "msg": "Profiles stopped successfully",
  "success": true
}
```

**Response 400 — Force Stop Profile Stop Error**

```json
{
  "code": "profiles.stop_error",
  "data": {
    "failed": [
      "4b8afed25a524f5aa1dc2922279622f8"
    ]
  },
  "msg": "Bulk force stop error",
  "success": false
}
```

#### GET Get Export profiles

`GET https://app.octobrowser.net/api/v2/automation/profiles/export?page=0&page_len=10`

Required permission: Transfer profiles.

**Headers**

- `Content-Type`: `application/json`

**Response 200 — Get Export profiles**

```json
{
  "data": {
    "data": [
      {
        "data": "JGFlc19nY20kJFpkbkZ6WWlOTVROejNCRnhwVDBuanZJcWp6a0lLemNvV2VpWXEvLkdETC40WFF1QmdwYnlNampRcTRzZ1JSUmJqWHhKMjNWbnVITUxuL1ZTMTBCT1BmaVZZS0E=",
        "title": "{profile_title}",
        "uuid": "{UUID}"
      }
    ],
    "page": 0,
    "total": 1
  },
  "msg": "",
  "success": true
}
```

#### GET Get Export profile

`GET https://app.octobrowser.net/api/v2/automation/profiles/export/:uuid`

Required permission: Transfer profiles.

**Headers**

- `Content-Type`: `application/json`

**Response 200 — Get Export profile**

```json
{
  "data": {
    "data": "JGFlc19nY20kJDMvMzBKcW12d2tXYi91UlRNL1ZHNFNTZEROYUlKSC5wbDRwWTdkaFlac0pBRUE4dkpVOXVRclhnWnpPT3N5eUtUOUlKOGMveTZkekpmemRPMEFMd3Z0YnBsenM=",
    "title": "{profile_title}",
    "uuid": "{UUID}"
  },
  "msg": "",
  "success": true
}
```

#### POST Export profiles

`POST https://app.octobrowser.net/api/v2/automation/profiles/export`

Up to 100 profiles per request allowed.

In the event of duplicate UUIDs in a request, they will be disregarded without any notifications.

This is a paid-for action that costs 0,5 tokens per profile.

Required permission: Transfer profiles.

200 does not mean profiles were exported: check exported and failed.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "export_proxy": false,
  "uuids": [
    ""
  ]
}
```

**Response 200 — Export profiles with proxy**

_request:_
```json
{
  "export_proxy": true,
  "uuids": [
    ""
  ]
}
```

```json
{
  "data": {
    "exported": [
      {
        "data": "MEYCIQDcEhji9E69bcOC1853v0zlXIP8kq6ecKwdcejBYkagrwIhAPUU/65bZqoT74AiqKT4IVuKK26zkBN2M9HTFJoZC4rS",
        "title": "{profile_title}",
        "uuid": "{UUID}"
      }
    ],
    "failed": []
  },
  "msg": "Profiles exported successfully",
  "success": true
}
```

**Response 200 — Export profiles without proxy**

```json
{
  "data": {
    "exported": [
      {
        "data": "MEYCIQDcEhji9E69bcOC1853v0zlXIP8kq6ecKwdcejBYkagrwIhAPUU/65bZqoT74AiqKT4IVuKK26zkBN2M9HTFJoZC4rS",
        "title": "{profile_title}",
        "uuid": "{UUID}"
      }
    ],
    "failed": []
  },
  "msg": "Profiles exported successfully",
  "success": true
}
```

#### POST Import profiles

`POST https://app.octobrowser.net/api/v2/automation/profiles/import`

Up to 100 profiles per request allowed.

Required permission: Create profiles.

Folder

The folder must be available to the token. Otherwise the request returns 403 with code no_permission.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "data": [
        "<export_data>"
    ],
    "folder": "folder" //optional
}
```

**Response 200 — Import profiles encoded string**

_request:_
```json
{
    "data": [
        "JGFlc19nY20kJE1mUk9tVS5KUGhrZmZyeGVCcGpzQ1VDa2xOUWRtcGdtVXc2WGdnMldqNWU5bFdHcGFnME5LSzZQa1BZLndsdnZEMWRZdHRudG5GdW5xakk5aUxyRWIycHhWdw=="
    ],
    "folder": "folder" // [optional]
}
```

```json
{
  "data": {
    "failed": []
  },
  "msg": "Profiles imported successfully",
  "success": true
}
```

**Response 200 — Import profiles new file**

_request:_
```json
{
  "data": [
    {
      "data": "JGFlc19nY20kJE1mUk9tVS5KUGhrZmZyeGVCcGpzQ1VDa2xOUWRtcGdtVXc2WGdnMldqNWU5bFdHcGFnME5LSzZQa1BZLndsdnZEMWRZdHRudG5GdW5xakk5aUxyRWIycHhWdw==",
      "title": "[Imported] Quick bouncy-reception",
      "uuid": "761c6c15b2e44545851061555c665319"
    }
  ]
}
```

```json
{
  "data": {
    "failed": []
  },
  "msg": "Profiles imported successfully",
  "success": true
}
```

**Response 200 — Import profiles old file**

_request:_
```json
{
  "data": [
    {
      "data": "{\"title\": \"[Imported] Quick rosy-chairlift\", \"exported_at\": \"2023-12-06 08:58:38\", \"profile\": \"gAAAAABlcDhTKzTeRIj2pGHBg-zJggNGMsekvt2DT47uM_iZYua9yoEmov0x3ZQKOu-XSWjgMGLL3CAC8rN92zyj-qOBVw3bnA==\"}",
      "signature": "MEUCIQD4ynaphY6R0TjQPz6hb5cmPaN5W+5pguRT65a6KB4r/gIgDOOcLfRvhrmeYHSpRIKSnjaziXM6lrS1OvVm86vxKVk="
    }
  ]
}
```

```json
{
  "data": {
    "failed": []
  },
  "msg": "Profiles imported successfully",
  "success": true
}
```

#### POST Set Profiles Password

`POST https://app.octobrowser.net/api/v2/automation/profiles/set_password`

Required permission: Profile passwords.

Sets one and the same password on every profile listed in profiles.

old_password is also a single value: it must match the current password of every listed profile that already has one. It can be omitted when none of the listed profiles has a password yet.

The request is all-or-nothing: if the old password doesn't match for one of the profiles, or one of them is currently running on another machine, the whole request fails with 400 and no profile is changed.

password length: 4–255 characters.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "old_password": "old_password",
  "password": "password",
  "profiles": [
    "uuid",
    "uuid"
  ]
}
```

**Response 200 — Set Profiles Password**

```json
{
  "data": "",
  "msg": "Password has been set for selected profiles",
  "success": true
}
```

#### POST Clear Profile Password

`POST https://app.octobrowser.net/api/v2/automation/profiles/:uuid/clear_password`

Required permission: Profile passwords.

Unsets the password of the profile given by uuid. The profile's current password must be passed in the request body; if it doesn't match, the request fails with 400.

{
  "password": "current_profile_password"
}

**Response 200 — Clear Profile Password**

_request:_
```json
{
  "password": "current_profile_password"
}
```

```json
{
  "data": "",
  "msg": "Password has been cleared",
  "success": true
}
```

### 📁 Tags

#### GET Get Tags

`GET https://app.octobrowser.net/api/v2/automation/tags`

**Response 200 — Get Tags**

```json
{
  "data": [
    {
      "color": "grey",
      "name": "aaaa",
      "uuid": "3524ff6e3f0245ffbbcb5ea3d0446a8e"
    },
    {
      "color": "blue",
      "name": "facebook",
      "uuid": "07fd5038fc0743cd955d963a19edb3d9"
    },
    {
      "color": "yellow",
      "name": "google",
      "uuid": "ab1391ce01aa46fcbdd9d02a4569bec4"
    },
    {
      "color": "orange",
      "name": "octo",
      "uuid": "7891009afee84952a926b03e7bc0af52"
    }
  ],
  "msg": "",
  "success": true
}
```

#### POST Create Tag

`POST https://app.octobrowser.net/api/v2/automation/tags`

Required permission: Edit tags.

Available colors for tags:

grey blue cyan orange green purple red yellow

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "name": "supertag",
    "color": "blue" //optional
}
```

**Response 201 — Create Tag**

```json
{
  "data": {
    "color": "blue",
    "name": "supertag",
    "uuid": "ab003313e690425cb1f01e67b9b3a5da"
  },
  "msg": "",
  "success": true
}
```

#### DELETE Remove Tag

`DELETE https://app.octobrowser.net/api/v2/automation/tags/:uuid`

Required permission: Edit tags.

**Response 200 — Remove Tag**

```json
{
  "data": "",
  "msg": "",
  "success": true
}
```

#### PATCH Update Tag

`PATCH https://app.octobrowser.net/api/v2/automation/tags/:uuid`

Required permission: Edit tags.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "name": "supertag1",
    "color": "orange" //optional
}
```

**Response 200 — Update Tag**

_request:_
```json
{
  "color": "orange",
  "name": "supertag1"
}
```

```json
{
  "data": {
    "color": "orange",
    "name": "supertag1",
    "uuid": "ab003313e690425cb1f01e67b9b3a5da"
  },
  "msg": "",
  "success": true
}
```

### 📁 Folders

#### GET Get Folders

`GET https://app.octobrowser.net/api/v2/automation/folders`

Returns folders available to the token. A token with restricted folder access gets only its folders, possibly an empty list.

**Response 200 — Get Folders**

```json
{
  "data": [
    {
      "assignable_wo_permission": false,
      "name": "folder",
      "uuid": "b49b03b068c745ff88cfa3d3f1619e3c"
    }
  ],
  "msg": "",
  "success": true
}
```

#### POST Create Folder

`POST https://app.octobrowser.net/api/v2/automation/folders`

Required permission: Edit folders. Setting assignable_wo_permission also requires Manage team.

Available colors for tags:

grey blue cyan orange green purple red yellow

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "folders": [
        {
            "name": "folder",
            "assignable_wo_permission": true //optional
        }
    ]
}
```

**Response 201 — Create Folder**

```json
{
  "data": [
    {
      "assignable_wo_permission": true,
      "name": "folder",
      "uuid": "5ba18556ebe54f27b1d80a35043775a8"
    }
  ],
  "msg": "",
  "success": true
}
```

#### DELETE Remove Folder

`DELETE https://app.octobrowser.net/api/v2/automation/folders/:uuid_or_name`

Required permission: Edit folders. Setting assignable_wo_permission also requires Manage team.

**Response 200 — Remove Folder**

```json
{
  "data": "",
  "msg": "",
  "success": true
}
```

#### PATCH Update Folder

`PATCH https://app.octobrowser.net/api/v2/automation/folders/:uuid_or_name`

Required permission: Edit folders. Setting assignable_wo_permission also requires Manage team.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "name": "folder",  // optional
    "assignable_wo_permission": true // optional
}
```

**Response 200 — Update Folder**

_request:_
```json
{
  "assignable_wo_permission": "false",
  "name": "folder"
}
```

```json
{
  "data": {
    "assignable_wo_permission": false,
    "name": "folder",
    "uuid": "5ba18556ebe54f27b1d80a35043775a8"
  },
  "msg": "",
  "success": true
}
```

### 📁 Proxies

Proxies from the list are attached to profiles through the proxy field of profile create/update, by uuid.

#### GET Get Proxies

`GET https://app.octobrowser.net/api/v2/automation/proxies`

**Response 200 — Get Proxies**

```json
{
  "data": [
    {
      "change_ip_url": "https://localhost/api/v1/change-ip?uuid=c26dc4d6-0de7-4aeb-bbef-de3d98362f4e",
      "external_id": null,
      "host": "localhost",
      "login": "some_login",
      "password": "some_password",
      "port": 29801,
      "profiles_count": 0,
      "title": "example proxy",
      "type": "socks5",
      "uuid": "963d30cb2d7247c89da222c8a9dcab29"
    },
    {
      "change_ip_url": null,
      "conf": "W0ludGVyZmFjZV0KIyBUaGUgaW50ZXJuYWwgSVAgYWRkcmVzcyBhc3NpZ25lZCB0byB0aGlzIHNwZWNpZmljIGNsaWVudApBZGRyZXNzID0gMTAuMC4wLjIvMjQsIGZkYzk6MjgxZjowNGQ3OjllZTk6OjIvNjQKIyBUaGUgY2xpZW50J3MgdW5pcXVlIHByaXZhdGUga2V5ClByaXZhdGVLZXkgPSA8Q0xJRU5UXzFfUFJJVkFURV9LRVk+CiMgT3B0aW9uYWw6IFRoZSBETlMgc2VydmVyIHRoZSBjbGllbnQgc2hvdWxkIHVzZSB3aGlsZSBjb25uZWN0ZWQKRE5TID0gMS4xLjEuMSwgOC41LjUuNQoKW1BlZXJdCiMgVGhlIHB1YmxpYyBrZXkgb2YgdGhlIFdpcmVHdWFyZCBzZXJ2ZXIKUHVibGljS2V5ID0gPFNFUlZFUl9QVUJMSUNfS0VZPgojIFRoZSBwdWJsaWMgSVAgYWRkcmVzcyBvciBkb21haW4gbmFtZSBhbmQgcG9ydCBvZiB0aGUgc2VydmVyCkVuZHBvaW50ID0gaHR0cDovL3lvdXJkb21haW4uY29tOjU2NzQ1CiMgVHJhZmZpYyB0byByb3V0ZSB0aHJvdWdoIHRoZSB0dW5uZWwuIAojIFVzZSAwLjAuMC4wLzAsIDo6LzAgdG8gcm91dGUgYWxsIGludGVybmV0IHRyYWZmaWMuIAojIFVzZSAxMC4wLjAuMC8yNCB0byBvbmx5IHJvdXRlIHRyYWZmaWMgZGVzdGluZWQgZm9yIHRoZSBWUE4gc3VibmV0LgpBbGxvd2VkSVBzID0gMC4wLjAuMC8wLCA6Oi8wCiMgT3B0aW9uYWw6IFNlbmRzIGEgcGFja2V0IGV2ZXJ5IDI1IHNlY29uZHMgdG8ga2VlcCB0aGUgY29ubmVjdGlvbiBhbGl2ZSBiZWhpbmQgTkFUcwpQZXJzaXN0ZW50S2VlcGFsaXZlID0gMjU=",
      "external_id": "my_custom_id=1",
      "host": "http://yourdomain.com",
      "login": "",
      "password": "",
      "port": 56745,
      "profiles_count": 0,
      "syn_mode": "profile_based",
      "title": "my-vpn-proxy",
      "type": "vpn",
      "uuid": "23b512d979394d4097c5a6ddf04217b0",
      "vpn_protocol": "wireguard"
    }
  ],
  "msg": "",
  "success": true
}
```

#### POST Create Proxy

`POST https://app.octobrowser.net/api/v2/automation/proxies`

Required permission: Create proxies.

The request body has two forms, chosen by type: a regular proxy and a VPN one.

  | Field  | Type  | Required  | Description

  | type  | string  | yes  | ssh, http, https, socks5.

  | title  | string  | yes  | Proxy name, 1–255 characters.

  | host  | string  | yes  | IPv4 address, IPv6 address or domain name (4–253 characters).

  | port  | integer  | yes  | 0–65535

  | login  | string  | no  | Up to 255 characters.

  | password  | string  | no  | Same rules as login.

  | change_ip_url  | string  | no  | Any http/https url the provider gives you for rotating the ip.

  | external_id  | string  | no  | Your own identifier, up to 255 characters. Must be a string.

VPN proxies.

Send type: "vpn" and the request body switches to the VPN form below.

Request body (VPN form):

  | Field  | Type  | Required  | Description

  | type  | string  | yes  | vpn

  | title  | string  | yes  | Proxy name, 1–255 characters.

  | conf  | string  | yes  | WireGuard configuration file, base64-encoded. Must contain an Endpoint = host:port line. Up to 16 KB before encoding.

  | syn_mode  | string  | no  | TCP/IP fingerprint the tunnel emulates. Default profile_based. See the values below.

  | vpn_protocol  | string  | no  | wireguard the only supported value, and the default. For AWG configuration use wireguard too.

  | external_id  | string  | no  | Your own identifier, up to 255 characters.

host, port, login, password and change_ip_url are not accepted in the VPN form: the endpoint comes from the config, and a tunnel has no credentials or rotation url. Sending any of them returns 400.

syn_mode values:

  | Value  | Meaning

  | profile_based  | Follow the OS of the profile the proxy is attached to (default).

  | win / mac / android  | Always emulate this OS, whatever the profile is.

  | real  | Keep the real fingerprint of the machine running the browser.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "type": "socks",
    "host": "localhost",
    "port": 1081,
    "login": "user", // [optional]
    "password": "secret111", // [optional]
    "title": "super proxy",
    "change_ip_url": "http://example.com", // [optional]
    "external_id": "12345" // [optional]
}
```

**Response 201 — Create Proxy**

_request:_
```json
{
  "change_ip_url": "http://localhost:1082/change_ip",
  "external_id": "my_custom_id=1",
  "host": "localhost",
  "login": "user",
  "password": "secret111",
  "port": 1081,
  "title": "super proxy",
  "type": "socks"
}
```

```json
{
  "data": {
    "change_ip_url": "http://localhost:1082/change_ip",
    "external_id": "my_custom_id=1",
    "host": "localhost",
    "login": "user",
    "password": "secret111",
    "port": 1081,
    "profiles_count": 0,
    "title": "super proxy",
    "type": "socks",
    "uuid": "789f4d3f898d4e10acf2bebd249fcf95"
  },
  "msg": "",
  "success": true
}
```

**Response 201 — Create VPN Proxy**

_request:_
```json
{
  "conf": "W0ludGVyZmFjZV0KIyBUaGUgaW50ZXJuYWwgSVAgYWRkcmVzcyBhc3NpZ25lZCB0byB0aGlzIHNwZWNpZmljIGNsaWVudApBZGRyZXNzID0gMTAuMC4wLjIvMjQsIGZkYzk6MjgxZjowNGQ3OjllZTk6OjIvNjQKIyBUaGUgY2xpZW50J3MgdW5pcXVlIHByaXZhdGUga2V5ClByaXZhdGVLZXkgPSA8Q0xJRU5UXzFfUFJJVkFURV9LRVk+CiMgT3B0aW9uYWw6IFRoZSBETlMgc2VydmVyIHRoZSBjbGllbnQgc2hvdWxkIHVzZSB3aGlsZSBjb25uZWN0ZWQKRE5TID0gMS4xLjEuMSwgOC41LjUuNQoKW1BlZXJdCiMgVGhlIHB1YmxpYyBrZXkgb2YgdGhlIFdpcmVHdWFyZCBzZXJ2ZXIKUHVibGljS2V5ID0gPFNFUlZFUl9QVUJMSUNfS0VZPgojIFRoZSBwdWJsaWMgSVAgYWRkcmVzcyBvciBkb21haW4gbmFtZSBhbmQgcG9ydCBvZiB0aGUgc2VydmVyCkVuZHBvaW50ID0gaHR0cDovL3lvdXJkb21haW4uY29tOjU2NzQ1CiMgVHJhZmZpYyB0byByb3V0ZSB0aHJvdWdoIHRoZSB0dW5uZWwuIAojIFVzZSAwLjAuMC4wLzAsIDo6LzAgdG8gcm91dGUgYWxsIGludGVybmV0IHRyYWZmaWMuIAojIFVzZSAxMC4wLjAuMC8yNCB0byBvbmx5IHJvdXRlIHRyYWZmaWMgZGVzdGluZWQgZm9yIHRoZSBWUE4gc3VibmV0LgpBbGxvd2VkSVBzID0gMC4wLjAuMC8wLCA6Oi8wCiMgT3B0aW9uYWw6IFNlbmRzIGEgcGFja2V0IGV2ZXJ5IDI1IHNlY29uZHMgdG8ga2VlcCB0aGUgY29ubmVjdGlvbiBhbGl2ZSBiZWhpbmQgTkFUcwpQZXJzaXN0ZW50S2VlcGFsaXZlID0gMjU=",
  "external_id": "my_custom_id=1",
  "syn_mode": "profile_based",
  "title": "my-vpn-proxy",
  "type": "vpn",
  "vpn_protocol": "wireguard"
}
```

```json
{
  "code": null,
  "data": {
    "change_ip_url": null,
    "external_id": "my_custom_id=1",
    "host": "http://yourdomain.com",
    "login": "",
    "password": "",
    "port": 56745,
    "profiles_count": 0,
    "syn_mode": "profile_based",
    "title": "my-vpn-proxy",
    "type": "vpn",
    "uuid": "23b512d979394d4097c5a6ddf04217b0",
    "vpn_protocol": "wireguard"
  },
  "msg": "",
  "success": true
}
```

#### DELETE Remove Proxy

`DELETE https://app.octobrowser.net/api/v2/automation/proxies/:uuid`

Required permission: Delete proxies.

**Response 200 — Remove Proxy**

```json
{
  "data": "",
  "msg": "",
  "success": true
}
```

#### PATCH Update Proxy

`PATCH https://app.octobrowser.net/api/v2/automation/proxies/:uuid`

Required permission: Edit proxies.

Request body (regular form)

  | Field  | Type  | Description

  | type  | string  | New proxy type. Same values as in POST, plus vpn to convert the proxy see below.

  | title  | string  | 1–255 characters.

  | host  | string  | IPv4, IPv6 or domain name.

  | port  | integer  | 0–65535.

  | login, password  | string  | Up to 255 characters each. Pass an empty string to clear.

  | change_ip_url  | string  |

  | external_id  | string  | Up to 255 characters.

Request body (VPN form)

  | Field  | Type  | Description

  | type  | string  | vpn. Required only when converting a regular proxy into a VPN one. for a proxy that is already VPN it can be omitted.

  | title  | string  | 1–255 characters.

  | conf  | string  | New WireGuard/AWG configuration, base64-encoded, with an Endpoint = host:port line. Required when converting a regular proxy into a VPN one, optional otherwise. Replaces the stored config: host and port are re-read from it and the last check result is reset.

  | syn_mode  | string  | Fingerprint mode: profile_based, win, mac, android or real.

  | vpn_protocol  | string  | wireguard

  | external_id  | string  | Up to 255 characters.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "type": "socks", // [optional]
    "host": "localhost", // [optional]
    "port": 1081, // [optional]
    "login": "user", // [optional]
    "password": "secret111", // [optional]
    "title": "new title", // [optional]
    "change_ip_url": "http://example.com", // [optional]
    "external_id": "12345" // [optional]
}
```

**Response 200 — Update Proxy**

_request:_
```json
{
  "title": "new title"
}
```

```json
{
  "data": {
    "change_ip_url": null,
    "external_id": null,
    "host": "127.0.0.1",
    "login": "",
    "password": "",
    "port": 40000,
    "profiles_count": 0,
    "title": "renew title",
    "type": "socks5",
    "uuid": "5246b94778f549859e2e6577d98d90aa"
  },
  "msg": "",
  "success": true
}
```

**Response 200 — Update VPN Proxy**

_request:_
```json
{
  "conf": "W0ludGVyZmFjZV0KIyBUaGUgaW50ZXJuYWwgSVAgYWRkcmVzcyBhc3NpZ25lZCB0byB0aGlzIHNwZWNpZmljIGNsaWVudApBZGRyZXNzID0gMTAuMC4wLjIvMjQsIGZkYzk6MjgxZjowNGQ3OjllZTk6OjIvNjQKIyBUaGUgY2xpZW50J3MgdW5pcXVlIHByaXZhdGUga2V5ClByaXZhdGVLZXkgPSA8Q0xJRU5UXzFfUFJJVkFURV9LRVk+CiMgT3B0aW9uYWw6IFRoZSBETlMgc2VydmVyIHRoZSBjbGllbnQgc2hvdWxkIHVzZSB3aGlsZSBjb25uZWN0ZWQKRE5TID0gMS4xLjEuMSwgOC41LjUuNQoKW1BlZXJdCiMgVGhlIHB1YmxpYyBrZXkgb2YgdGhlIFdpcmVHdWFyZCBzZXJ2ZXIKUHVibGljS2V5ID0gPFNFUlZFUl9QVUJMSUNfS0VZPgojIFRoZSBwdWJsaWMgSVAgYWRkcmVzcyBvciBkb21haW4gbmFtZSBhbmQgcG9ydCBvZiB0aGUgc2VydmVyCkVuZHBvaW50ID0gaHR0cDovL3lvdXJkb21haW4uY29tOjU2NzQ1CiMgVHJhZmZpYyB0byByb3V0ZSB0aHJvdWdoIHRoZSB0dW5uZWwuIAojIFVzZSAwLjAuMC4wLzAsIDo6LzAgdG8gcm91dGUgYWxsIGludGVybmV0IHRyYWZmaWMuIAojIFVzZSAxMC4wLjAuMC8yNCB0byBvbmx5IHJvdXRlIHRyYWZmaWMgZGVzdGluZWQgZm9yIHRoZSBWUE4gc3VibmV0LgpBbGxvd2VkSVBzID0gMC4wLjAuMC8wLCA6Oi8wCiMgT3B0aW9uYWw6IFNlbmRzIGEgcGFja2V0IGV2ZXJ5IDI1IHNlY29uZHMgdG8ga2VlcCB0aGUgY29ubmVjdGlvbiBhbGl2ZSBiZWhpbmQgTkFUcwpQZXJzaXN0ZW50S2VlcGFsaXZlID0gMjU=",
  "type": "vpn"
}
```

```json
{
  "code": null,
  "data": {
    "change_ip_url": null,
    "external_id": "my_custom_id=1",
    "host": "http://yourdomain.com",
    "login": "",
    "password": "",
    "port": 56745,
    "syn_mode": "profile_based",
    "type": "vpn",
    "uuid": "23b512d979394d4097c5a6ddf04217b0",
    "vpn_protocol": "wireguard"
  },
  "msg": "",
  "success": true
}
```

### 📁 Proxy providers

Proxies from the proxy providers built into Octo Browser.

Proxy kinds: data_center, mobile, residential. Traffic is counted in bytes per provider and is bought with tokens from the team balance.

#### GET Get Proxy Providers

`GET https://app.octobrowser.net/api/v2/automation/proxy_providers`

Returns proxy providers available to the team.

-
kinds — proxy kinds the provider offers;

-
traffic — remaining team traffic for this provider, in bytes;

-
proxy_count — number of team proxies from this provider;

-
can_create_proxy, can_buy_traffic — whether these actions are currently available for the provider.

**Response 200 — Get Proxy Providers**

```json
{
  "data": [
    {
      "can_buy_traffic": true,
      "can_create_proxy": true,
      "kinds": [
        "mobile",
        "residential"
      ],
      "name": "Provider",
      "proxy_count": 3,
      "traffic": 5000000000,
      "uuid": "9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b"
    }
  ],
  "msg": "",
  "success": true
}
```

#### GET Get Provider Proxies

`GET https://app.octobrowser.net/api/v2/automation/proxy_providers/proxies`

Returns team proxies created from proxy providers. Filter by provider and kind if needed.

Paginated with page and page_len, the response contains total_count and page.

**Response 200 — Get Provider Proxies**

```json
{
  "code": null,
  "data": [
    {
      "change_ip_url": "https://proxy.example.com/change-ip?key=abc",
      "external_id": null,
      "geo": {
        "city": "los_angeles",
        "country": "US",
        "isp": "verizon",
        "region": "CA"
      },
      "host": "proxy.example.com",
      "kind": "mobile",
      "login": "some_login",
      "password": "some_password",
      "port": 29801,
      "profiles_count": 0,
      "provider": {
        "name": "Provider",
        "uuid": "9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b"
      },
      "syn_mode": null,
      "title": "US mobile 1",
      "type": "socks5",
      "uuid": "963d30cb2d7247c89da222c8a9dcab29",
      "vpn_protocol": null
    }
  ],
  "msg": "",
  "page": 0,
  "success": true,
  "total_count": 1
}
```

#### POST Create Provider Proxies

`POST https://app.octobrowser.net/api/v2/automation/proxy_providers/proxies`

Creates 1 to 100 proxies from a proxy provider.

provider: Provider uuid from GET /proxy_providers.

Required permission: Create paid proxies.

Take country, region, city and isp codes from the location requests of this folder. region, city and isp are optional. isp applies to mobile proxies only.

Returns 201 with the created proxies

  | Status  | Code  | When

  | 400  | proxy_providers.empty_balance  | No traffic left for this provider

  | 400  | proxy_providers.invalid  | The provider does not offer this kind

  | 400  | bad_request  | The provider is unavailable or the location is invalid (see msg)

  | 403  | proxy.limit_reached  | The plan limit of provider proxies is reached

**Body**

```json
{
    "provider": "9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b",
    "kind": "mobile",
    "country_code": "US",
    "region_code": "CA",     //optional
    "city_code": null,       //optional
    "isp_code": null,        //optional
    "quantity": 1
}
```

**Response 201 — Create Provider Proxies**

```json
{
  "data": [
    {
      "change_ip_url": "https://proxy.example.com/change-ip?key=abc",
      "external_id": null,
      "geo": {
        "city": "los_angeles",
        "country": "US",
        "isp": "verizon",
        "region": "CA"
      },
      "host": "proxy.example.com",
      "kind": "mobile",
      "login": "some_login",
      "password": "some_password",
      "port": 29801,
      "profiles_count": 0,
      "provider": {
        "name": "Provider",
        "uuid": "9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b"
      },
      "syn_mode": null,
      "title": "US mobile 1",
      "type": "socks5",
      "uuid": "963d30cb2d7247c89da222c8a9dcab29",
      "vpn_protocol": null
    }
  ],
  "msg": "",
  "success": true
}
```

**Response 400 — Create Provider Proxies Empty Balance**

```json
{
  "code": "proxy_providers.empty_balance",
  "data": "",
  "msg": "Proxy provider traffic balance is empty",
  "success": false
}
```

#### PATCH Update Provider Proxy

`PATCH https://app.octobrowser.net/api/v2/automation/proxy_providers/proxies/:proxy_uuid`

Renames a provider proxy. Only title can be changed (1–255 characters).

Required permission: Edit proxies.

**Body**

```json
{
  "title": "US mobile 1"
}
```

**Response 200 — Update Provider Proxy**

```json
{
  "data": {
    "change_ip_url": "https://proxy.example.com/change-ip?key=abc",
    "external_id": null,
    "geo": {
      "city": "los_angeles",
      "country": "US",
      "isp": "verizon",
      "region": "CA"
    },
    "host": "proxy.example.com",
    "kind": "mobile",
    "login": "some_login",
    "password": "some_password",
    "port": 29801,
    "profiles_count": 0,
    "provider": {
      "name": "Provider",
      "uuid": "9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b"
    },
    "syn_mode": null,
    "title": "US mobile 1",
    "type": "socks5",
    "uuid": "963d30cb2d7247c89da222c8a9dcab29",
    "vpn_protocol": null
  },
  "msg": "",
  "success": true
}
```

#### DELETE Delete Provider Proxy

`DELETE https://app.octobrowser.net/api/v2/automation/proxy_providers/proxies/:proxy_uuid`

Required permission: Delete proxies.

**Response 200 — Delete Provider Proxy**

```json
{
  "data": null,
  "msg": "",
  "success": true
}
```

#### GET Get Countries

`GET https://app.octobrowser.net/api/v2/automation/proxy_providers/:provider_uuid/:kind/countries`

Returns countries where the provider offers proxies of the given kind. Use code in the next requests and in Create Provider Proxies.

  | Status  | Code  | When

  | 400  | proxy_providers.not_exists  | The provider is not available

  | 400  | proxy_providers.invalid  | The provider does not offer this kind

**Response 200 — Get Countries**

```json
{
  "data": [
    {
      "code": "US",
      "name": "United States"
    },
    {
      "code": "DE",
      "name": "Germany"
    }
  ],
  "msg": "",
  "success": true
}
```

#### GET Get Mobile ISPs

`GET https://app.octobrowser.net/api/v2/automation/proxy_providers/:provider_uuid/mobile/countries/:country_code/isps`

Returns mobile carriers (ISPs) of the provider in the country.

Use code as :isp in Get Mobile Regions and as isp in Create Provider Proxies. The ISP is optional: skip it to get a proxy from any carrier in the country.

  | Status  | Code  | When

  | 400  | proxy_providers.not_exists  | The provider is not available

  | 400  | proxy_providers.invalid  | The provider does not offer mobile proxies

  | 400  | bad_request  | The provider API returned an error, try again later

**Response 200 — Get Mobile ISPs**

```json
{
  "data": [
    {
      "code": "verizon",
      "name": "Verizon"
    },
    {
      "code": "t-mobile",
      "name": "T-Mobile"
    }
  ],
  "msg": "",
  "success": true
}
```

#### GET Get Mobile Regions

`GET https://app.octobrowser.net/api/v2/automation/proxy_providers/:provider_uuid/mobile/countries/:country_code/isps/:isp_code/regions`

Returns regions where the mobile carrier (ISP) of the provider is available in the country.

Use code as :region in Get Mobile Cities and as region in Create Provider Proxies.

  | Status  | Code  | When

  | 400  | proxy_providers.not_exists  | The provider is not available

  | 400  | proxy_providers.invalid  | The provider does not offer mobile proxies

  | 400  | bad_request  | The provider API returned an error, try again later

**Response 200 — Get Mobile Regions**

```json
{
  "data": [
    {
      "code": "CA",
      "name": "California"
    },
    {
      "code": "NY",
      "name": "New York"
    }
  ],
  "msg": "",
  "success": true
}
```

#### GET Get Mobile Cities

`GET https://app.octobrowser.net/api/v2/automation/proxy_providers/:provider_uuid/mobile/countries/:country_code/isps/:isp_code/regions/:region_code/cities`

Returns cities where the mobile carrier (ISP) of the provider is available in the region.

Use code as city in Create Provider Proxies.

  | Status  | Code  | When

  | 400  | proxy_providers.not_exists  | The provider is not available

  | 400  | proxy_providers.invalid  | The provider does not offer mobile proxies

  | 400  | bad_request  | The provider API returned an error, try again later

**Response 200 — Get Mobile Cities**

```json
{
  "data": [
    {
      "code": "los_angeles",
      "name": "Los Angeles"
    },
    {
      "code": "san_francisco",
      "name": "San Francisco"
    }
  ],
  "msg": "",
  "success": true
}
```

#### GET Get Residential Regions

`GET https://app.octobrowser.net/api/v2/automation/proxy_providers/:provider_uuid/residential/countries/:country_code/regions`

Returns regions where the provider offers residential proxies in the country.

Use code as :region in Get Residential Cities and as region in Create Provider Proxies. Residential proxies have no ISP level.

  | Status  | Code  | When

  | 400  | proxy_providers.not_exists  | The provider is not available

  | 400  | proxy_providers.invalid  | The provider does not offer residential proxies

  | 400  | bad_request  | The provider API returned an error, try again later

**Response 200 — Get Residential Regions**

```json
{
  "data": [
    {
      "code": "BY",
      "name": "Bavaria"
    },
    {
      "code": "BE",
      "name": "Berlin"
    }
  ],
  "msg": "",
  "success": true
}
```

#### GET Get Residential Cities

`GET https://app.octobrowser.net/api/v2/automation/proxy_providers/:provider_uuid/residential/countries/:country_code/regions/:region_code/cities`

Returns cities where the provider offers residential proxies in the region.

Use code as city in Create Provider Proxies.

  | Status  | Code  | When

  | 400  | proxy_providers.not_exists  | The provider is not available

  | 400  | proxy_providers.invalid  | The provider does not offer residential proxies

  | 400  | bad_request  | The provider API returned an error, try again later

**Response 200 — Get Residential Cities**

```json
{
  "data": [
    {
      "code": "munich",
      "name": "Munich"
    },
    {
      "code": "nuremberg",
      "name": "Nuremberg"
    }
  ],
  "msg": "",
  "success": true
}
```

### 📁 Teams

#### GET Get Extensions

`GET https://app.octobrowser.net/api/v2/automation/teams/extensions?start=0&limit=25`

Returns extensions used by a team installed in any profile.

**Response 200 — Get Extensions**

```json
{
  "data": [
    {
      "name": "Google Translate",
      "uuid": "54d6ff5042c545b990349a7a7e653e81@2.0.12",
      "version": "2.0.12"
    }
  ],
  "msg": "",
  "success": true
}
```

#### DELETE Delete Extensions

`DELETE https://app.octobrowser.net/api/v2/automation/teams/extensions`

Required permission: Delete extensions.

Deletes extensions of a team using UUIDs. The maximum UUID batch length is 100.

IMPORTANT: If any profile is running during this request, the deleted extensions will continue to be available and functioning for this profile. After such a profile stops, these extensions will return to the extensions list. Please make sure that extensions you would like to delete are not in use in any running profile at the time of deletion.

200 does not mean extensions were deleted: unknown ones are ignored.

The request has a JSON body. Make sure your HTTP client sends a body with DELETE requests.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "uuids": [
    "ppdakpfeaodfo@9.0.19"
  ]
}
```

**Response 200 — Delete Extensions**

```json
{
  "data": "",
  "msg": "Extensions deleted successfully",
  "success": true
}
```

#### GET Get subaccounts

`GET https://app.octobrowser.net/api/v2/automation/teams/subaccounts`

Required permission: Manage team.

**Response 200 — Get subaccounts**

```json
{
  "data": [
    {
      "created_at": "2023-11-27 13:07:28",
      "email": "test@octo.com",
      "master": false,
      "permissions": {
        "edit_folders": true,
        "edit_tags": false,
        "extensions": {
          "delete": false
        },
        "manage_action_log": false,
        "manage_team": false,
        "paid_proxies": {
          "create": false
        },
        "profiles": {
          "clone": false,
          "create": false,
          "delete": false,
          "edit": false,
          "passwords": false,
          "transfer": false
        },
        "proxies": {
          "create": false,
          "delete": false,
          "edit": false
        },
        "tasks": {
          "manage": false,
          "view": false
        },
        "templates": {
          "create": false,
          "delete": false,
          "edit": false
        },
        "view_all_folders": true,
        "view_all_tags": false,
        "view_profiles_wo_folders": true,
        "visible_folders": [],
        "visible_tags": [
          "tag_name"
        ]
      },
      "uuid": "54d6ff5042c545b990349a7a7e653e81"
    }
  ],
  "msg": "",
  "success": true,
  "total_count": 1
}
```

#### GET Get invites

`GET https://app.octobrowser.net/api/v2/automation/teams/invites`

Required permission: Manage team.

**Response 200 — Get invites**

```json
{
  "data": [
    {
      "created_at": "2023-11-27 13:07:28",
      "receiver": "test_receiver@octo.net"
    }
  ],
  "msg": "",
  "success": true,
  "total_count": 1
}
```

#### DELETE Delete invite

`DELETE https://app.octobrowser.net/api/v2/automation/teams/invites`

Required permission: Manage team.

The request has a JSON body. Make sure your HTTP client sends a body with DELETE requests.

**Body**

```json
{
  "receiver": "test@octo.net"
}
```

**Response 200 — Delete invite**

```json
{
  "data": "",
  "msg": "Invite deleted",
  "success": true
}
```

#### POST Invite subaccount

`POST https://app.octobrowser.net/api/v2/automation/teams/subaccounts`

Required permission: Manage team.

IMPORTANT: If a permission is not specified, it will be set as false.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "email": "test@octo.net",
    "permissions": {
        "manage_team": false, // [optional]
        "edit_tags": false, // [optional]
        "view_all_tags": false, // [optional]
        "edit_folders": false, // [optional]
        "view_all_folders": true, // [optional]
        "manage_action_log": false, // [optional]
        "proxies": { // [optional]
            "create": false,
            "edit": false,
            "delete": false
        },
        "paid_proxies": { // [optional]
            "create": false
        },
        "profiles": { // [optional]
            "transfer": false,
            "clone": false,
            "create": false,
            "edit": false,
            "delete": false,
            "passwords": false
        },
        "templates": { // [optional]
            "create": false,
            "edit": false,
            "delete": false
        },
        "extensions": { // [optional]
            "delete": false
        },
        "tasks": { // [optional]
            "view": false,
            "manage": false
        },
        "visible_tags": ["tag_name"], // [optional]
        "visible_folders": [], // [optional]
        "view_profiles_wo_folders": true // [optional]
    }
}
```

**Response 200 — Invite subaccount**

```json
{
  "data": "",
  "msg": "Invite sent",
  "success": true
}
```

#### PATCH Update subaccount

`PATCH https://app.octobrowser.net/api/v2/automation/teams/subaccounts`

Required permission: Manage team.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "email": "test@octo.net",
    "permissions": {
        "manage_team": false, // [optional]
        "edit_tags": false, // [optional]
        "view_all_tags": false, // [optional]
        "manage_action_log": false, // [optional]
        "proxies": { // [optional]
            "create": false,
            "edit": false,
            "delete": false
        },
        "paid_proxies": { // [optional]
            "create": false
        },
        "profiles": { // [optional]
            "transfer": false,
            "clone": false,
            "create": false,
            "edit": false,
            "delete": false,
            "passwords": false
        },
        "templates": { // [optional]
            "create": false,
            "edit": false,
            "delete": false
        },
        "extensions": { // [optional]
            "delete": false
        },
        "tasks": { // [optional]
            "view": false,
            "manage": false
        },
        "visible_tags": ["tag_name"] // [optional]
    }
}
```

**Response 200 — Update subaccount**

_request:_
```json
{
    "email": "test@octo.net",
    "permissions": {
        "manage_team": false, // [optional]
        "edit_tags": false, // [optional]
        "view_all_tags": false, // [optional]
        "edit_folders": false, // [optional]
        "view_all_folders": true, // [optional]
        "manage_action_log": false, // [optional]
        "proxies": { // [optional]
            "create": false,
            "edit": false,
            "delete": false
        },
        "paid_proxies": { // [optional]
            "create": false
        },
        "profiles": { // [optional]
            "transfer": false,
            "clone": false,
            "create": false,
            "edit": false,
            "delete": false,
            "passwords": false
        },
        "templates": { // [optional]
            "create": false,
            "edit": false,
            "delete": false
        },
        "extensions": { // [optional]
            "delete": false
        },
        "tasks": { // [optional]
            "view": false,
            "manage": false
        },
        "visible_tags": ["tag_name"], // [optional]
        "visible_folders": [], // [optional]
        "view_profiles_wo_folders": true // [optional]
    }
}
```

```json
{
  "data": {
    "uuid": "d2874db6b3344506946c1bb91bd17bf8"
  },
  "msg": "Team member updated",
  "success": true
}
```

#### DELETE Delete subaccount

`DELETE https://app.octobrowser.net/api/v2/automation/teams/subaccounts`

Required permission: Manage team.

The request has a JSON body. Make sure your HTTP client sends a body with DELETE requests.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "email": "test@octo.net"
}
```

**Response 200 — Delete subaccount**

```json
{
  "data": "",
  "msg": "Team member deleted",
  "success": true
}
```

#### GET Get Subscription

`GET https://app.octobrowser.net/api/v2/automation/teams/subscription`

Returns the team subscription, balance, usage of the plan limits and the current API rate limits.

-
plan — plan name;

-
expiration — subscription end date;

-
balance — team balance in tokens;

-
profiles, team_members, api_tokens — used and limit of the plan (team_members does not count the account owner);

-
rate_limits.rpm, rate_limits.rph — requests per minute and per hour: limit, remaining (this request included) and reset_at (UTC), the time when a request slot becomes free again.

**Response 200 — Get Subscription**

```json
{
  "data": {
    "api_tokens": {
      "limit": 3,
      "used": 2
    },
    "auto_renew": true,
    "balance": "125.5",
    "expiration": "2026-11-27T00:00:00",
    "plan": "team",
    "profiles": {
      "limit": 500,
      "used": 120
    },
    "rate_limits": {
      "rph": {
        "limit": 1500,
        "remaining": 1460,
        "reset_at": "2026-10-27T12:35:00"
      },
      "rpm": {
        "limit": 100,
        "remaining": 98,
        "reset_at": "2026-10-27T12:01:00"
      }
    },
    "team_members": {
      "limit": 5,
      "used": 2
    }
  },
  "msg": "",
  "success": true
}
```

### 📁 Fingerprint

#### GET Get Renderers

`GET https://app.octobrowser.net/api/v2/automation/fingerprint/renderers?page_len=100&page=0&os=win&os_arch=x86`

**Response 200 — Get Renderers**

```json
{
  "data": [
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "ATI Radeon HD 3200 Graphics (Microsoft Corporation WDDM 1.1)"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "ATI Radeon 3100 Graphics (Microsoft Corporation WDDM 1.1)"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "NVIDIA GeForce GTX 660"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "ATI Radeon HD 3400 Series"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "NVIDIA GeForce 210"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "AMD Radeon HD 6800 Series"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "lin",
      "value": "NVIDIA Tegra K1 (nvgpu)/integrated"
    },
    {
      "archs": [
        "arm"
      ],
      "platform": "mac",
      "value": "Apple M2 Pro"
    }
  ],
  "msg": "",
  "page": 0,
  "success": true,
  "total_count": 250
}
```

#### GET Get Screens

`GET https://app.octobrowser.net/api/v2/automation/fingerprint/screens?os=win&os_arch=x86`

**Response 200 — Get Screens**

```json
{
  "data": [
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "1440x900"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "1536x864"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "1536x960"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "1600x900"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "1680x1050"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "1920x1080"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "1920x1200"
    },
    {
      "archs": [
        "x86"
      ],
      "platform": "win",
      "value": "2560x1440 (2K)"
    }
  ],
  "msg": "",
  "success": true
}
```

#### GET Get Mobile Device Models

`GET https://app.octobrowser.net/api/v2/automation/fingerprint/device_models?device_type=phone`

**Response 200 — Get Mobile Device Models**

```json
{
  "data": [
    {
      "archs": [
        "arm"
      ],
      "device_type": "phone",
      "os": "android",
      "os_versions": [
        "12"
      ],
      "value": "M2102J20SG"
    },
    {
      "archs": [
        "arm"
      ],
      "device_type": "tablet",
      "os": "android",
      "os_versions": [
        "13"
      ],
      "value": "21051182G"
    },
    {
      "archs": [
        "arm"
      ],
      "device_type": "tablet",
      "os": "android",
      "os_versions": [
        "13"
      ],
      "value": "SM-T970"
    },
    {
      "archs": [
        "arm"
      ],
      "device_type": "phone",
      "os": "android",
      "os_versions": [
        "12"
      ],
      "value": "M2007J20CG"
    },
    {
      "archs": [
        "arm"
      ],
      "device_type": "phone",
      "os": "android",
      "os_versions": [
        "13"
      ],
      "value": "SM-M526B"
    },
    {
      "archs": [
        "arm"
      ],
      "device_type": "phone",
      "os": "android",
      "os_versions": [
        "13"
      ],
      "value": "moto g32"
    }
  ],
  "msg": "",
  "success": true
}
```

#### GET Get Platforms

`GET https://app.octobrowser.net/api/v2/automation/fingerprint/platforms`

Returns supported operating systems, their architectures and OS versions. Use these values for os, os_arch and os_version in the profile fingerprint.

**Response 200 — Get Platforms**

```json
{
  "code": null,
  "data": [
    {
      "archs": [
        {
          "arch": "x86",
          "os_versions": [
            "10",
            "11"
          ]
        }
      ],
      "os": "win"
    },
    {
      "archs": [
        {
          "arch": "x86",
          "os_versions": [
            "13",
            "14",
            "15",
            "26"
          ]
        },
        {
          "arch": "arm",
          "os_versions": [
            "13",
            "14",
            "15",
            "26"
          ]
        }
      ],
      "os": "mac"
    },
    {
      "archs": [
        {
          "arch": "arm",
          "os_versions": [
            "12",
            "13",
            "14",
            "15"
          ]
        }
      ],
      "os": "android"
    }
  ],
  "msg": "",
  "success": true
}
```

### 📁 Action Log

Action log stream

Endpoint

-
Type: WebSocket

-
URL: wss://app.octobrowser.net//api/v2/automation/ws/action_log

-
Authentication: Auto API Token (header X-Octo-Api-Token)

-
Required permission: Action log. Without it, the connection is rejected with 403 (no_permission).

Response Format

Each WebSocket message contains a StreamPage:

{
"items": [
    {
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "action": "profiles.started",
    "time": 1707053400,
    "user_email": "user@example.com",
    "object_type": "profile",
    "object_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "object_title": "Octo Browser Profile",
    "data": {
        "connection_data": {
            "ip": "203.0.113.42",
            "countryCode": "FR",
            "countryName": "France",
            "subdivisions": [
                "Île-de-France",
                "Paris"
            ],
            "postalCode": "75008",
            "cityName": "Paris",
            "timezone": "Europe/Paris",
            "lat": 48.8566,
            "lon": 2.3522,
            "languages": [
                "fr",
                "en-US",
                "en"
            ],
            "isp": "Example Networks Ltd",
            "connectionType": "Cable/DSL"
        }
    }
    }
  ],
  "watermark": {
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "time": 1707053400
  }
}

Actions made with API tokens

For actions made with an API token, user_email is (API), for example Scraper (API). Actions made with the token from earlier versions show API token (API).

Earlier versions showed the email of the account owner instead.

Examples

Initial Connection

wss://app.octobrowser.net/api/v2/automation/ws/action_log

Reconnect After Disconnect

Use the watermark UUID to resume:

wss://app.octobrowser.net/api/v2/automation/ws/action_log?after_uuid=abc-123

Start From Specific Time

wss://app.octobrowser.net/api/v2/automation/ws/action_log?from_timestamp=1707053400

Event Types (Actions)

-
profiles.started - Profile browser was started

-
profiles.stopped - Profile browser was stopped

-
profiles.force_stopped - Profile browser was force stopped

-
profiles.transferred - Profile was transferred

-
profiles.trashed- Profile was moved to trash bin

-
profiles.created - Profile was created

-
profiles.updated - Profile was updated

-
profiles.deleted - Profile was deleted

-
profiles.proxy_assigned - Proxy was assigned to profile

-
profiles.proxy_unassigned - Proxy was unassigned from profile

-
profiles.proxy_changed - Profile's proxy was changed to another one

Query Parameters

-
after_uuid (string, UUID, optional) - UUID of the last received audit entry. Use this to resume streaming from a specific point.

-
from_timestamp (integer, Unix timestamp, optional) - Start streaming from this timestamp. Events are only available for 24 hours.

How It Works

-
Connect to the WebSocket endpoint

-
Receive pages of events as JSON messages

-
Use the watermark from each response to track your position in the stream and use these values ​​in case of reconnection

Watermark Mechanics

The watermark acts as a cursor for pagination:

-
Contains uuid and time of the last record

-
Ensures stable pagination even when multiple records share the same timestamp

-
Use after_uuid parameter on reconnect to resume from where you left off

-
Use the from_time parameter when reconnecting to continue from a specific time

Constraints

-
Event retention: 24 hours

-
Batch size: Up to 100 records per page

-
Requirements: Team must have API option in subscription

## 📁 Local client API

This is a local client API to run profiles.

The default server port is 58888.

The API URL is http://localhost:58888.

### GET List Active Profiles

`GET http://localhost:58888/api/profiles/active`

Shows the list of profiles launched on your device. webSocketDebuggerUrl will be shown only for profiles that are launched in the headless mode.

**Response 200 — List Active Profiles**

```json
[
  {
    "browser_pid": 26616,
    "debug_port": "55834",
    "headless": true,
    "one_time": false,
    "start_time": 1724173918,
    "state": "STARTED",
    "uuid": "2bbfd1dbaf3349cf979787f15a9e413d",
    "ws_endpoint": "ws://127.0.0.1:55834/devtools/browser/a26c9612-6479-43f1-87ef-34590321a99a"
  }
]
```

### POST Start Profile

`POST http://localhost:58888/api/profiles/start`

debug_port=true enables the automation port. A random free port will be selected.

debug_port=20000 launches the browser on a specific port. Allowed values: 1024-65534.

timeout - seconds overrides the default start timeout value. This is usually required if you are using slow proxies.

flags - list[string] allows you to add additional Chromium flags. Note: we recommend against adding any flags and we don't guarantee correct browser work if you decide to do so. Use this only if you are certain that you absolutely need this and you know precisely what you are doing.

profile_data - mapping allows to override some profile fields during start (images_load_limit: null, size in bytes)

--disk-cache-dir allows you to change the default cache folder. If you want to save your cached data (images, scripts, etc.), you can add this flag and add a path to the desired folder. The path should be outside the profile folder. By default the cache is cleared every time you close the profile.

example: flags:["--disk-cache-dir=C:/Cache"]

--disable-backgrounding-occluded-windows can be useful if you automate many profiles at the same time and your scripts do not work correctly in windows that are out of focus (running in the background).

To listen to, e.g., 0.0.0.0 interface you can add "flags": ["--remote-debugging-address=0.0.0.0"]

chromedrivers allows you to download official chromedrivers.

START_ERROR_CODES = {
    ComponentNotFoundException: 1,
    ProfileAlreadyRunningException: 2,
    ProfileStartFailedException: 3,
    GetProxyDataFailedException: 4,
    InvalidProxyDataException: 5,
    ProfileNotFoundException: 6,
    NoSubscriptionException: 7,
    OutdatedVersionException: 8,
    ProfileVersionConsistencyError: 9,
}

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "uuid": "",
    "headless": false,
    "debug_port": true,
    "only_local": true,
    "flags": [],
    "timeout": 120,
    "password": "password" // [optional]
}
```

**Response 200 — Start Profile GUI**

_request:_
```json
{
  "debug_port": true,
  "flags": [],
  "headless": false,
  "only_local": true,
  "password": "password",
  "timeout": 120,
  "uuid": ""
}
```

```json
{
  "browser_pid": 8776,
  "connection_data": {
    "country": "Germany",
    "ip": "188.188.188.88"
  },
  "debug_port": "54500",
  "headless": false,
  "one_time": false,
  "start_time": 1724172687,
  "state": "STARTED",
  "uuid": "2bbfd1dbaf3349cf979787f15a9e413d",
  "ws_endpoint": "ws://127.0.0.1:54500/devtools/browser/35dc7ef1-04a9-4d9b-ad38-02dc629093e5"
}
```

**Response 200 — Start Profile Headless**

_request:_
```json
{
  "debug_port": true,
  "flags": [],
  "headless": true,
  "only_local": true,
  "password": "password",
  "timeout": 120,
  "uuid": ""
}
```

```json
{
  "browser_pid": 10108,
  "connection_data": {
    "country": "Germany",
    "ip": "188.188.188.88"
  },
  "debug_port": "54739",
  "headless": true,
  "one_time": false,
  "start_time": 1724172886,
  "state": "STARTED",
  "uuid": "2bbfd1dbaf3349cf979787f15a9e413d",
  "ws_endpoint": "ws://127.0.0.1:54739/devtools/browser/4d05ab38-20bf-45e6-b463-6bc643028107"
}
```

**Response 400 — Start Profile Already Running On Different Machine**

_request:_
```json
{
  "debug_port": true,
  "flags": [],
  "headless": false,
  "only_local": true,
  "password": "password",
  "timeout": 120,
  "uuid": ""
}
```

```json
{
  "code": "profiles.already_started",
  "error": "Profile is already started",
  "error_code": 2
}
```

**Response 400 — Start Profile Proxy Error**

_request:_
```json
{
  "debug_port": true,
  "flags": [],
  "headless": false,
  "only_local": true,
  "password": "password",
  "timeout": 120,
  "uuid": ""
}
```

```json
{
  "code": "profiles.proxy_error",
  "error": "Failed to get proxy data",
  "error_code": 4
}
```

### POST Stop Profile

`POST http://localhost:58888/api/profiles/stop`

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "uuid": ""
}
```

**Response 200 — Stop Profile**

```json
{
  "msg": "Profile stopped"
}
```

### POST Force Stop Profile

`POST http://localhost:58888/api/profiles/force_stop`

Requires Octo Browser 1.7 or later

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "uuid": ""
}
```

**Response 200 — Force Stop Profile**

```json
{
  "msg": "Profile stopped successfully"
}
```

### POST Login

`POST http://localhost:58888/api/auth/login`

Requires Octo Browser 1.8.0 or later

If the client was started with OCTO_API_TOKEN, login and logout are disabled and the request returns 400 with the code auth.managed_by_api_token.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "email": "useremail@domain.net",
  "password": "userpassword"
}
```

**Response 200 — Login**

_request:_
```json
{
    "email": "useremail@domain.net",
    "password": "userpassword",
    "api_token": "api_token" // [optional]
}
```

```json
{
  "msg": "Logged in successfully"
}
```

### POST Logout

`POST http://localhost:58888/api/auth/logout`

Requires Octo Browser 1.8.0 or later

If the client was started with OCTO_API_TOKEN, login and logout are disabled and the request returns 400 with the code auth.managed_by_api_token.

**Response 200 — Logout**

```json
{
  "msg": "Logged out successfully"
}
```

### GET Get Client Version

`GET http://localhost:58888/api/update`

Shows the current and latest available browser versions. Update_required field indicates a critical update availability. A critical update means that the current browser version is no longer supported and an update is strongly recommended.

**Response 200 — Critical update available**

```json
{
  "current": "1.7.6",
  "latest": "1.8.3",
  "update_required": true
}
```

**Response 200 — Update**

```json
{
  "current": "1.8.2",
  "latest": "1.8.3",
  "update_required": false
}
```

### POST Update Client

`POST http://localhost:58888/api/update`

Triggers an update to the latest available version. If the browser is up to date this will return an error.

**Response 200 — Update**

```json
{
  "msg": "update to 1.8.3 triggerred successfully"
}
```

**Response 409 — Update No Available Version Error**

```json
{
  "code": "client.update_failed",
  "error": "Update is not triggered. No available version"
}
```

### GET Username

`GET http://localhost:58888/api/username`

Returns the current user username.

**Response 200 — Username**

```json
{
  "username": "user@example.com"
}
```

### POST One-time profile

`POST http://localhost:58888/api/profiles/one_time/start`

Note: if you don't specify a given parameter, we will generate the best values for it on our servers. Change only the parameters you need to customize.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
    "profile_data": {
        "fingerprint": {
            "os": "win",
            "os_version": "11", // [optional]
            "os_arch": "x86", // [optional]
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36", // [optional]
            "screen": "1920x1080", // [optional]
            "languages": { // [optional]
                "type": "ip"
            },
            "timezone": { // [optional]
                "type": "ip"
            },
            "geolocation": { // [optional]
                "type": "ip"
            },
            "cpu": 4, // [optional]
            "ram": 8, // [optional]
            "noise": { // [optional]
                "webgl": true,
                "canvas": false,
                "audio": true,
                "client_rects": false
            },
            "webrtc": { // [optional]
                "type": "ip"
            },
            "dns": "1.1.1.1", // [optional]
            "media_devices": { // [optional]
                "video_in": 1,
                "audio_in": 1,
                "audio_out": 1
            }
        },
        "extensions": [ // [optional]
            "ewbjmajocgfcbeboaewbfgobmjsjcoja@1.0"
        ],
        "start_pages": [ // [optional]
            "https://fb.com"
        ],
        "proxy": { // [optional]
            "type": "socks5",
            "host": "1.1.1.1",
            "port": 5555,
            "login": "",
            "password": ""
        },
        "local_cache": true, // [optional]
        "cookies": [ // [optional]
            {
                "domain": ".google.com",
                "expirationDate": 1639134293.313654,
                "hostOnly": false,
                "httpOnly": false,
                "name": "1P_JAR",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": true,
                "value": "2021-11-10-11"
            }
        ]
    },
    "headless": false, // [optional]
    "debug_port": true, // [optional]
    "flags": [], // [optional]
    "timeout": 60 // [optional]
}
```

**Response 200 — Start One-time Profile**

```json
{
  "browser_pid": 4684,
  "connection_data": {
    "country": "Germany",
    "ip": "188.188.188.88"
  },
  "debug_port": "63269",
  "headless": false,
  "one_time": true,
  "start_time": 1702904780,
  "state": "STARTED",
  "uuid": "9a906e7d45124e6fb37388633277c22f",
  "ws_endpoint": "ws://127.0.0.1:63269/devtools/browser/f7aa4e97-c300-404f-b9c7-2633db0c1515"
}
```

### POST Set profile password

`POST http://localhost:58888/api/profiles/password`

Sets password of profile

Minimal length - at least 4 characters

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "password": "password",
  "uuid": "9585dc0cdc1e497896afe81ba1fbcdb6"
}
```

**Response 200 — Set profile password**

```json
{
  "msg": "Profile password has been set"
}
```

**Response 503 — Set profile password error**

```json
{
  "code": "profiles.password_change_failed",
  "error": "Failed to change profile password",
  "error_code": 1
}
```

### DELETE Delete profile password

`DELETE http://localhost:58888/api/profiles/password`

Unsets password of profile

The request has a JSON body. Make sure your HTTP client sends a body with DELETE requests.

**Headers**

- `Content-Type`: `application/json`

**Body**

```json
{
  "password": "password",
  "uuid": "9585dc0cdc1e497896afe81ba1fbcdb6"
}
```

**Response 200 — Delete profile password**

```json
{
  "msg": "Profile password has been cleared"
}
```

**Response 400 — Another operation in progress**

```json
{
  "error": "Another profile's operation in progress",
  "error_code": 3
}
```

**Response 400 — Delete password error**

```json
{
  "error": "Failed to clear profile password",
  "error_code": 1
}
```

**Response 400 — Incorrect password**

```json
{
  "code": "profiles.invalid_password",
  "error": "Profile password incorrect",
  "error_code": 1
}
```

### POST Check Proxy

`POST http://localhost:58888/api/proxies/check`

The body is one of:

-
a saved proxy: uuid from Get Proxies;

-
proxy data: type (socks5, http, https or ssh), host, port, login, password;

-
a VPN config, in the same format as in Create Proxy: type = vpn, conf — the WireGuard/AmneziaWG config file encoded in base64, vpn_protocol — wireguard.

  | Status  | Code  | When

  | 400  | proxies.proxy_connection_error  | The proxy is unreachable or rejected the connection. error contains the reason

  | 401  | auth.unauthenticated  | The client is not logged in

**Body**

```json
{
  "host": "188.188.188.88",
  "login": "user",
  "password": "pass",
  "port": 1080,
  "type": "socks5"
}
```

**Response 200 — Check Proxy**

```json
{
  "data": {
    "city_name": "Frankfurt am Main",
    "connection_type": "Corporate",
    "country": "DE",
    "country_full_name": "Germany",
    "isp": "Example ISP",
    "mtu": 1500,
    "os": "Linux",
    "postal_code": "60313",
    "real_ip": "188.188.188.88",
    "subdivisions": [
      "Hesse"
    ],
    "supports_udp": true,
    "timezone": "Europe/Berlin"
  }
}
```

**Response 200 — Check Saved Proxy**

_request:_
```json
{
  "uuid": "a1b2c3d4e5f64789a0b1c2d3e4f5a6b7"
}
```

```json
{
  "data": {
    "city_name": "Frankfurt am Main",
    "connection_type": "Corporate",
    "country": "DE",
    "country_full_name": "Germany",
    "isp": "Example ISP",
    "mtu": 1500,
    "os": "Linux",
    "postal_code": "60313",
    "real_ip": "188.188.188.88",
    "subdivisions": [
      "Hesse"
    ],
    "supports_udp": true,
    "timezone": "Europe/Berlin"
  }
}
```

**Response 200 — Check VPN**

_request:_
```json
{
  "conf": "W0ludGVyZmFjZV0KUHJpdmF0ZUtleSA9IC4uLgo=",
  "type": "vpn",
  "vpn_protocol": "wireguard"
}
```

```json
{
  "data": {
    "city_name": "Frankfurt am Main",
    "connection_type": "Corporate",
    "country": "DE",
    "country_full_name": "Germany",
    "isp": "Example ISP",
    "mtu": 1500,
    "os": "Linux",
    "postal_code": "60313",
    "real_ip": "188.188.188.88",
    "subdivisions": [
      "Hesse"
    ],
    "supports_udp": true,
    "timezone": "Europe/Berlin"
  }
}
```

**Response 400 — Check Proxy Connection Error**

```json
{
  "code": "proxies.proxy_connection_error",
  "error": "Connection refused",
  "error_code": -1
}
```

## 📁 Automation Libraries

Examples of connecting automation libraries to a running profile, in different programming languages.

### 📁 Puppeteer/Pyppeteer

Connecting Puppeteer

const puppeteer = require('puppeteer');
const axios = require('axios');
const OCTO_REMOTE_API = axios.create({
    baseURL: 'https://app.octobrowser.net/api/v2/automation/',
    timeout: 2000,
    headers: {
        'X-Octo-Api-Token': 'Token' //Put your Token here
    }
});
const OCTO_LOCAL_API = axios.create({
    baseURL: 'http://127.0.0.1:58888/api/profiles/',
    timeout: 100000
})
async function createProfile() {
    return OCTO_REMOTE_API.post(`/profiles`, {
        title: 'API Test profile',
        fingerprint: {
            os: "win"
        }
    }).then((response) => response.data).catch((error) => error.response ? error.response.data : null)
}
async function startProfile(uuid) {
    return OCTO_LOCAL_API.post('/start', {
        uuid: uuid,
        headless: true,
        debug_port: true
    }).then((response) => response.data).catch((error) => error.response ? error.response.data : null)
}
(async () => {
    const response = await createProfile();
    const profile_uuid = response.data.uuid;
    const start_response = await startProfile(profile_uuid);
    const ws_endpoint = start_response.ws_endpoint;
    const browser = await puppeteer.connect({
        browserWSEndpoint: ws_endpoint,
        defaultViewport: null
    });
    const page = await browser.newPage();
    await page.goto('https://google.com/');
})();

Pyppeteer (python version)

import asyncio
import logging
import os
import httpx
import pyppeteer
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
log = logging.getLogger('octo')
OCTO_TOKEN = os.getenv('OCTO_TOKEN', 'PUT_TOKEN_HERE')
OCTO_API = 'https://app.octobrowser.net/api/v2/automation/profiles'
LOCAL_API = 'http://localhost:58888/api/profiles/start'
HEADERS = {'X-Octo-Api-Token': OCTO_TOKEN}
async def get_profile(cli):
    profiles = (await cli.get(OCTO_API, headers=HEADERS)).json()
    log.info(f'Profiles: {profiles}')
    return profiles['data'][0]['uuid']
async def get_cdp(cli):
    uuid = await get_profile(cli)
    resp = (await cli.post(LOCAL_API, json={'uuid': uuid, 'debug_port': True})).json()
    log.info(f'Start profile resp: {resp}')
    return resp['ws_endpoint']
async def main():
    async with httpx.AsyncClient() as cli:
        ws_url = await get_cdp(cli)
    browser = await pyppeteer.launcher.connect(browserWSEndpoint=ws_url)
    try:
        page = await browser.newPage()
        url = 'https://duckduckgo.com/'
        await page.goto(url)
        values = await page.querySelector('p.badge-link__social')
        it = await values.getProperty('innerText')
        text_value = await it.jsonValue()
        log.info(f'Element text: {text_value}')
    finally:
        await browser.close()
if __name__ == '__main__':
    asyncio.run(main())

### 📁 Playwright

Connecting Playwright

const axios = require('axios');
const pw = require('playwright');
const OCTO_REMOTE_API = axios.create({
  baseURL: 'https://app.octobrowser.net/api/v2/automation/',
  timeout: 2000,
  headers: {
    'X-Octo-Api-Token': 'Token' //Put Your Token Here
  }
});
const OCTO_LOCAL_API = axios.create({
  baseURL: 'http://127.0.0.1:58888/api/profiles/',
  timeout: 100000
})
async function createProfile() {
  return OCTO_REMOTE_API.post(`/profiles`, {
    title: 'API Test profile',
    fingerprint: {
      os: "win"
    }
  }).then((response) => response.data).catch((error) => error.response ? error.response.data : null)
}
async function startProfile(uuid) {
  return OCTO_LOCAL_API.post('/start', {
    uuid: uuid,
    headless: false, //should be false if you want to see actions
    debug_port: true
  }).then((response) => response.data).catch((error) => error.response ? error.response.data : null)
}
(async () => {
  const response = await createProfile();
  const profile_uuid = response.data.uuid;
  const start_response = await startProfile(profile_uuid);
  const ws_endpoint = start_response.ws_endpoint;
  const browser = await pw.chromium.connectOverCDP(ws_endpoint);
  const context = browser.contexts()[0];
  const page = context.pages()[0];
  await page.goto('https://google.com');
})();

Playwright Sync Python

import httpx
from playwright.sync_api import sync_playwright
PROFILE_UUID = "UUID_OF_YOUR_PROFILE"
def main():
    with sync_playwright() as p:
        start_response = httpx.post(
            'http://127.0.0.1:58888/api/profiles/start',
            json={
                'uuid': PROFILE_UUID,
                'headless': False,
                'debug_port': True
            }
        )
        if not start_response.is_success:
            print(f'Start response is not success: {start_response.json()}')
            return
        ws_endpoint = start_response.json().get('ws_endpoint')
        browser = p.chromium.connect_over_cdp(ws_endpoint)
        page = browser.contexts[0].pages[0]
        page.goto('https://google.com')
        browser.close()
if __name__ == '__main__':
    main()

Playwright Async Python

import httpx
import asyncio
from playwright.async_api import async_playwright
PROFILE_UUID = "UUID_OF_YOUR_PROFILE"
async def main():
    async with async_playwright() as p:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'http://127.0.0.1:58888/api/profiles/start',
                json={
                    'uuid': PROFILE_UUID,
                    'headless': False,
                    'debug_port': True
                }
            )
            if not response.is_success:
                print(f'Start response is not successful: {response.json()}')
                return
            start_response = response.json()
            ws_endpoint = start_response.get('ws_endpoint')
        browser = await p.chromium.connect_over_cdp(ws_endpoint)
        page = browser.contexts[0].pages[0]
        await page.goto('https://google.com')
        await browser.close()
if __name__ == '__main__':
    asyncio.run(main())

### 📁 Selenium

Connecting Selenium

NB: By default Selenium is exposed in the browser and can be detected by some sites. It should work fine for most cases; however, if it doesn't, you need to use another automation library (puppeteer, chrome dev protocol).

Alternatively, consider changing default Selenium to undetected-chromedriver.

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
PROFILE_ID = 'PROFILE_UUID'
WEBDRIVERPATH = Service(
    executable_path=r'./chromedriver/chromedriver-win64/chromedriver.exe')
LOCAL_API = 'http://localhost:58888/api/profiles'
def get_webdriver(port):
    chrome_options = Options()
    chrome_options.add_experimental_option(
        'debuggerAddress', f'127.0.0.1:{port}')
    # Change chrome driver path accordingly
    driver = webdriver.Chrome(service=WEBDRIVERPATH, options=chrome_options)
    return driver
def get_debug_port(profile_id):
    data = requests.post(
        f'{LOCAL_API}/start', json={'uuid': profile_id, 'headless': False, 'debug_port': True}
    ).json()
    return data['debug_port']
def main():
    port = get_debug_port(PROFILE_ID)
    driver = get_webdriver(port)
    driver.get('http://amazon.com')
if __name__ == '__main__':
    main()

import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
public class Main {
    private static final String PROFILE_ID = "PROFILE_UUID"; //Profile UUID
    private static final String CHROME_DRIVER = "./path/to/chromedriver.exe"; //Change this Path to your chromedriver.exe
    private static final String LOCAL_API = "http://127.0.0.1:58888/api/profiles";
    public static void main(String[] args) throws Exception {
        int port = getDebugPort(PROFILE_ID);
        WebDriver driver = getWebDriver(port);
        driver.get("http://google.com");
    }
    public static WebDriver getWebDriver(int port) {
        ChromeOptions chromeOptions = new ChromeOptions();
        chromeOptions.setExperimentalOption("debuggerAddress", "127.0.0.1:" + port);
        System.setProperty("webdriver.chrome.driver", CHROME_DRIVER);
        return new ChromeDriver(chromeOptions);
    }
    public static int getDebugPort(String profileId) throws Exception {
        int debugPort;
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpPost httpPost = new HttpPost(LOCAL_API + "/start");
            JSONObject json = new JSONObject();
            json.put("uuid", profileId);
            json.put("headless", false);
            json.put("debug_port", true);
            StringEntity entity = new StringEntity(json.toString());
            httpPost.setEntity(entity);
            httpPost.setHeader("Accept", "application/json");
            httpPost.setHeader("Content-type", "application/json");
            try (CloseableHttpResponse response = httpClient.execute(httpPost)) {
                String responseString = EntityUtils.toString(response.getEntity());
                JSONObject responseJson = new JSONObject(responseString);
                debugPort = responseJson.getInt("debug_port");
            }
        }
        return debugPort;
    }
}

Visual Basic .NET Example

Imports System
Imports System.Net.Http
Imports System.Text
Imports Newtonsoft.Json.Linq
Imports OpenQA.Selenium
Imports OpenQA.Selenium.Chrome
Module Program
Public Class Main
    Private Shared ReadOnly PROFILE_ID As String = "PROFILE_UUID_SHOULD_BE_HERE" 'Profile UUID
    Private Shared ReadOnly CHROME_DRIVER As String = "./chromedriver-win64/chromedriver.exe" 'Change this Path to your chromedriver.exe
    Private Shared ReadOnly LOCAL_API As String = "http://127.0.0.1:58888/api/profiles"
    Public Shared Sub Main(args As String())
        Dim port As Integer = GetDebugPort(PROFILE_ID)
        Dim driver As IWebDriver = GetWebDriver(port)
        driver.Navigate().GoToUrl("http://google.com")
    End Sub
    Public Shared Function GetWebDriver(port As Integer) As IWebDriver
        Dim chromeOptions As New ChromeOptions()
        chromeOptions.DebuggerAddress = "127.0.0.1:" & port
        Environment.SetEnvironmentVariable("webdriver.chrome.driver", CHROME_DRIVER)
        Return New ChromeDriver(chromeOptions)
    End Function
    Public Shared Function GetDebugPort(profileId As String) As Integer
        Dim debugPort As Integer
        Using httpClient As New HttpClient()
            Dim httpPost As New HttpRequestMessage(HttpMethod.Post, LOCAL_API & "/start")
            Dim json As New JObject()
            json("uuid") = profileId
            json("headless") = False
            json("debug_port") = True
            httpPost.Content = New StringContent(json.ToString(), Encoding.UTF8, "application/json")
            httpPost.Headers.Accept.ParseAdd("application/json")
            Using response = httpClient.SendAsync(httpPost).Result
                Dim responseString As String = response.Content.ReadAsStringAsync().Result
                Dim responseJson As JObject = JObject.Parse(responseString)
                debugPort = responseJson("debug_port")
            End Using
        End Using
        Return debugPort
    End Function
End Class
End Module

## 📁 Docker

You can use examples below to run Octo Browser in docker containers.

Method 1: components folder on the host device

This method is suitable if your project architecture includes a static host device for building and running containers. Mount the components folder using the docker run command:

-v '/srv/docker_octo/cache:/home/octo/.Octo Browser/' \

Or use volumes in docker-compose.yaml:

volumes:
     - /srv/docker_octo/cache:/home/octo/.Octo Browser/

Method 2: snapshot inside the image

This method is suitable if there is no static host device: the image can be distributed to any number of devices, and containers will start with the components already in place. Authentication is performed by passing an API token as a variable. The rest of this guide covers this method.

Note: you may encounter operational limitations if you run more than 5 containers simultaneously and:

-
All containers share the same IP address.

-
You log into the same Octo account.

What you'll need

-
Docker, Bash, and jq on the build device (Git Bash or WSL2 on Windows).

-
An Octo Browser API token.

-
About 6 GB of free disk space: octo:base ~2.3 GB, octo:ready ~4.9 GB (shared layers with the base image are not duplicated), snapshot ~700 MB.

-
15–40 minutes for the first full build, depending on network speed. Most of the time is spent installing packages in the base image and downloading ~1.8–2.2 GB of components.

Place all five files below in a single folder and run the build from that folder.

Step 1: creds.json

Create a file named creds.json, paste the text {"octo_api_token":"your_token_here"}, and replace "your_token_here" with your API token.

Step 2: dockerfile — base image

Create a file named dockerfile

FROM ubuntu:22.04
ARG TZ=America/Los_Angeles
ARG DEBIAN_FRONTEND=noninteractive
ENV LANG="C.UTF-8" HOME=/home/octo \
    APPIMAGE_EXTRACT_AND_RUN=1 \
    OCTO_DATA="/home/octo/.Octo Browser"
RUN apt-get update && apt-get install -y \
    apt-transport-https ca-certificates curl gnupg unzip jq \
    libgles2 libegl1 xvfb x11vnc --no-install-recommends \
 && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update && apt-get install -y \
    fontconfig fonts-ipafont-gothic fonts-kacst fonts-noto fonts-symbola \
    fonts-thai-tlwg fonts-wqy-zenhei fonts-freefont-ttf \
    connect-proxy dnsutils iproute2 iptables iputils-ping net-tools \
    openvpn procps socat ssh sshpass sudo tcpdump telnet traceroute \
    tzdata vim-nox libgl1 libglib2.0-0 zip \
 && rm -rf /var/lib/apt/lists/*
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /tmp/chrome.deb \
 && apt-get update && apt-get install -y /tmp/chrome.deb && rm -f /tmp/chrome.deb \
 && rm -rf /var/lib/apt/lists/*
RUN groupadd -r octo \
 && useradd -r -g octo -s /bin/bash -m -G audio,video,sudo \
        -p "$(echo 1 | openssl passwd -1 -stdin)" octo \
 && mkdir -p /home/octo/browser && chown -R octo:octo /home/octo \
 && mkdir -p /etc/sudoers.d \
 && echo 'octo ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/octo && chmod 0440 /etc/sudoers.d/octo
USER octo
RUN curl -o /home/octo/browser/octo-browser.tar.gz \
        https://binaries.octobrowser.net/releases/installer/OctoBrowser.linux.tar.gz \
 && tar -xzf /home/octo/browser/octo-browser.tar.gz -C /home/octo/browser \
 && rm -f /home/octo/browser/octo-browser.tar.gz
CMD ["/bin/bash"]

Build the base image:

docker build -t octo:base -f dockerfile .

Step 3: entrypoint.sh — launching the browser in the container

The entrypoint.sh file starts a virtual display and launches Octo Browser in headless mode every time the container starts:

#!/usr/bin/env bash
# entrypoint.sh — boot headless OctoBrowser inside octo:ready.
set -u
export DISPLAY=:1
OCTO_DATA="${OCTO_DATA:-/home/octo/.Octo Browser}"
rm -f /tmp/.X1-lock "$OCTO_DATA/local_port"
rm -rf /tmp/.X11-unix
Xvfb :1 -ac -screen 0 1920x1080x24 >/tmp/x.log 2>&1 &
for _ in $(seq 1 10); do
    sleep 1
    [ -S /tmp/.X11-unix/X1 ] && break
done
# Keep OctoBrowser as our own child so signals reach it and the container
# lives exactly as long as the browser does.
OCTO_HEADLESS=1 /home/octo/browser/OctoBrowser.AppImage >/tmp/octo.log 2>&1 &
OCTO_PID=$!
term() { kill -TERM "$OCTO_PID" 2>/dev/null || true; }
trap term TERM INT
wait "$OCTO_PID"

Step 4: dockerfile.final — image with the snapshot

Create a file named dockerfile.final

# dockerfile.final — build octo:ready from octo:base + the golden snapshot.
# Build: docker build -t octo:ready -f ./dockerfile.final .
FROM octo:base
# --chown so the unprivileged Octo user can extract the snapshot and own the result.
COPY --chown=octo:octo logged-in-state.tar.gz /tmp/logged-in-state.tar.gz
USER octo
RUN mkdir -p "$OCTO_DATA" \
 && tar -xzf /tmp/logged-in-state.tar.gz -C "$OCTO_DATA" \
 && rm -f /tmp/logged-in-state.tar.gz
COPY --chown=octo:octo entrypoint.sh /home/octo/entrypoint.sh
RUN chmod +x /home/octo/entrypoint.sh
ENTRYPOINT ["/home/octo/entrypoint.sh"]

You don't need to build it manually, as the script in the next step will do this for you.

Step 5: build-golden.sh — creating the snapshot

Create a file named build-golden.sh

#!/usr/bin/env bash
# build-golden.sh — capture a golden snapshot and build octo:ready.
# Requires: octo:base already built, creds.json with an API token, docker, jq.
# Run: bash build-golden.sh
set -euo pipefail
cd "$(dirname "$0")"
step()    { printf '\n\033[36m=== %s ===\033[0m\n' "$1"; }
err()     { printf '\033[31m%s\033[0m\n' "$*" >&2; }
ok()      { printf '\033[32m%s\033[0m\n' "$*"; }
warn()    { printf '\033[33m%s\033[0m\n' "$*"; }
filesize(){ stat -c%s "$1" 2>/dev/null || stat -f%z "$1" 2>/dev/null || echo 0; }
TOKEN=$(jq -r '.octo_api_token // empty' creds.json 2>/dev/null || true)
if [ -z "$TOKEN" ] || printf '%s' "$TOKEN" | grep -qE '^(PASTE|<|TOKEN)'; then
    err 'creds.json does not contain octo_api_token. Format: {"octo_api_token":"..."}'
    exit 1
fi
printf 'Token: %s... (length %d)\n' "${TOKEN:0:8}" "${#TOKEN}"
step "Starting golden container"
docker rm -f octo-golden 2>/dev/null || true
docker run -d --name octo-golden --security-opt seccomp:unconfined \
    -e "OCTO_API_TOKEN=$TOKEN" \
    --entrypoint bash octo:base -lc "sleep 3600"
step "Start Xvfb + OctoBrowser (auth via OCTO_API_TOKEN)"
docker exec octo-golden bash -lc '
  rm -f /tmp/.X1-lock "$HOME/.Octo Browser/local_port"; rm -rf /tmp/.X11-unix
  setsid bash -c "Xvfb :1 -ac -screen 0 1920x1080x24 >/tmp/x.log 2>&1" &
  for i in $(seq 1 10); do sleep 1; [ -S /tmp/.X11-unix/X1 ] && break; done
  DISPLAY=:1 setsid bash -c "OCTO_HEADLESS=1 /home/octo/browser/OctoBrowser.AppImage >/tmp/octo.log 2>&1" &
'
step "Waiting for local_port to appear (up to 90 sec)"
PORT=""
for i in $(seq 1 18); do
    sleep 5
    PORT=$(docker exec octo-golden bash -lc 'cat "$HOME/.Octo Browser/local_port" 2>/dev/null' 2>/dev/null || true)
    if [ -n "$PORT" ]; then printf '  port: %s\n' "$PORT"; break; fi
    printf '  ...not yet (%ds)\n' "$((i*5))"
done
if [ -z "$PORT" ]; then
    err "OctoBrowser did not come up. docker exec octo-golden cat /tmp/octo.log"
    exit 1
fi
step "Checking authorization (OCTO_API_TOKEN)"
AUTHED=false
for i in $(seq 1 12); do
    RESP=$(docker exec octo-golden bash -lc '
      P=$(cat "$HOME/.Octo Browser/local_port" 2>/dev/null)
      [ -n "$P" ] && curl -s http://127.0.0.1:$P/api/username 2>/dev/null
    ' 2>/dev/null || true)
    printf '  [attempt %d] %s\n' "$i" "$RESP"
    if printf '%s' "$RESP" | grep -q '"username"'; then AUTHED=true; break; fi
    if [ $((i % 4)) -eq 0 ] && [ "$i" -lt 12 ]; then
        warn "  restarting the application..."
        docker exec octo-golden bash -lc '
          pkill -f OctoBrowser.AppImage; sleep 3
          rm -f "$HOME/.Octo Browser/local_port"
          DISPLAY=:1 setsid bash -c "OCTO_HEADLESS=1 /home/octo/browser/OctoBrowser.AppImage >>/tmp/octo.log 2>&1" &
        ' >/dev/null 2>&1 || true
        sleep 20
    fi
    sleep 5
done
if [ "$AUTHED" != "true" ]; then
    err "Authorization not confirmed. Check the token / docker exec octo-golden cat /tmp/octo.log"
    exit 1
fi
step "Waiting for components to download (up to 20 min)"
docker exec octo-golden bash -lc '
  B="$HOME/.Octo Browser/bin"
  stable=0; prev=0
  for i in $(seq 1 120); do
    cur=$(du -sm "$B" 2>/dev/null | cut -f1); cur=${cur:-0}
    missing=""
    # Ui is the GUI frontend and is not downloaded in headless mode.
    for c in Octium Tentacle Profile_Parser Tentacle_Ssh userdata; do
      sz=$(du -sm "$B/$c" 2>/dev/null | cut -f1); sz=${sz:-0}
      [ "$sz" -ge 10 ] || missing="$missing $c"
    done
    if [ -z "$missing" ] && [ "$cur" = "$prev" ]; then stable=$((stable+1)); else stable=0; fi
    [ "$stable" -ge 6 ] && { echo "stable ${cur}MB, all components present"; break; }
    prev=$cur; sleep 10
  done
  [ -n "$missing" ] && echo "WARNING: did not wait for:$missing"
  du -sm "$B"/* 2>/dev/null | sort -rn
'
step "Starting profile (warm-up + component-cache stabilization)"
docker exec octo-golden bash -lc '
  COMP="$HOME/.Octo Browser/tmp/components"
  P=$(cat "$HOME/.Octo Browser/local_port")
  RESP=$(curl -s -X POST http://127.0.0.1:$P/api/profiles/one_time/start \
    -H "Content-Type: application/json" \
    -d "{\"profile_data\":{\"fingerprint\":{\"os\":\"win\"}},\"headless\":true,\"timeout\":120,\"flags\":[\"--no-sandbox\",\"--disable-dev-shm-usage\"]}")
  UUID=$(echo "$RESP" | jq -r ".uuid // empty")
  echo "UUID=$UUID resp=$RESP"
  stable=0; prev=-1
  for i in $(seq 1 60); do
    cur=$(du -sm "$COMP" 2>/dev/null | cut -f1); cur=${cur:-0}
    if [ "$cur" = "$prev" ] && [ "$cur" -gt 0 ]; then stable=$((stable+1)); else stable=0; fi
    echo "  components: ${cur}MB (stable=$stable)"
    [ "$stable" -ge 3 ] && { echo "stable ${cur}MB"; break; }
    prev=$cur; sleep 5
  done
  [ "${cur:-0}" -eq 0 ] && echo "WARN: component cache stayed empty (non-fatal)"
  [ -n "$UUID" ] && curl -s -X POST http://127.0.0.1:$P/api/profiles/stop \
    -H "Content-Type: application/json" -d "{\"uuid\":\"$UUID\"}" >/dev/null \
    && echo "profile stopped" || echo "WARN: stop failed (non-fatal)"
'
step "Capturing snapshot logged-in-state.tar.gz"
docker exec octo-golden bash -lc '
  sleep 2
  cd "$HOME/.Octo Browser"
  # localpersist.data holds the machine HID: baking it in makes every container
  # look like the same machine, and a second container steals the first session.
  # The --warning/--ignore-failed-read flags keep the still-running daemon from
  # turning a changed file into a fatal tar error.
  tar --warning=no-file-changed --warning=no-file-removed --ignore-failed-read \
      --exclude=bcache --exclude=logs --exclude=local_port --exclude=localpersist.data \
      --exclude=updates \
      -czf /tmp/logged-in-state.tar.gz . || [ "$?" -eq 1 ]
'
docker cp octo-golden:/tmp/logged-in-state.tar.gz ./logged-in-state.tar.gz
docker rm -f octo-golden
SZ=$(filesize logged-in-state.tar.gz)
printf 'Snapshot: %d MB\n' "$((SZ / 1024 / 1024))"
step "Building octo:ready"
docker build -t octo:ready -f ./dockerfile.final .
step "Checking octo:ready"
docker rm -f octo-check 2>/dev/null || true
docker run -d --init --name octo-check --security-opt seccomp:unconfined \
    -e "OCTO_API_TOKEN=$TOKEN" octo:ready
OK=false
DEAD=false
for i in $(seq 1 18); do
    sleep 5
    if [ "$(docker inspect -f '{{.State.Running}}' octo-check 2>/dev/null || true)" != "true" ]; then
        DEAD=true; break
    fi
    RESP=$(docker exec octo-check bash -lc '
      P=$(cat "$HOME/.Octo Browser/local_port" 2>/dev/null)
      [ -n "$P" ] && curl -s http://127.0.0.1:$P/api/username 2>/dev/null
    ' 2>/dev/null || true)
    if printf '%s' "$RESP" | grep -q '"username"'; then
        ok "  OK: $RESP"; OK=true; break
    fi
    printf '  ...%ds: %s\n' "$((i*5))" "$RESP"
done
if [ "$OK" != "true" ]; then
    # Collect the logs before removing the container, or the evidence is gone.
    err "Check failed."
    if [ "$DEAD" = "true" ]; then
        CODE=$(docker inspect -f '{{.State.ExitCode}}' octo-check 2>/dev/null || true)
        err "  container is not running (exit code: ${CODE:-unknown})"
    fi
    printf '\n[docker logs octo-check]\n'
    docker logs octo-check 2>&1 | tail -n 40 || true
    printf '\n[/tmp/octo.log]\n'
    docker exec octo-check bash -lc 'tail -n 40 /tmp/octo.log' 2>&1 \
        || echo "(unavailable — container not running)"
    printf '\n[/tmp/x.log]\n'
    docker exec octo-check bash -lc 'tail -n 20 /tmp/x.log' 2>&1 \
        || echo "(unavailable — container not running)"
fi
docker rm -f octo-check >/dev/null
if [ "$OK" = "true" ]; then
    ok "DONE: octo:ready built, authorization works."
else
    exit 1
fi

Run the script:

bash build-golden.sh

The script sequentially starts a container from octo:base, authenticates using the token, waits for the components to download, primes them by launching a one-time profile, packages ~/.Octo Browser into logged-in-state.tar.gz, builds octo:ready from it, and verifies that a fresh container starts already authenticated.

A successful completion looks like this:

=== Checking octo:ready ===

OK: {"username":"your@email"}

DONE: octo:ready built, authorization works.

Step 6: running the finished image

docker run -d --init --name octo-1 --security-opt seccomp:unconfined \
    -e "OCTO_API_TOKEN=your_token_here" octo:ready

-
-e OCTO_API_TOKEN is required for authentication.

-
--security-opt seccomp:unconfined is required for the Chrome sandbox.

Updating the snapshot

The snapshot also locks in the component versions, so it will become outdated over time. To rebuild it, delete logged-in-state.tar.gz and run bash build-golden.sh again. If you also need to update the browser itself, rebuild the base image without the cache:

docker build --no-cache -t octo:base -f dockerfile .

## 📁 Kubernetes

If you would like to run the browser inside a kubernetes pod, make sure to properly configure shared memory limits and capabilities

apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: cloud-instance
          image: {{ .Values.octoImage }}:{{ .Values.tag }}
          securityContext:
            capabilities:
              add:
                - NET_ADMIN
                - SYS_ADMIN
          volumeMounts:
            - name: dshm
              mountPath: /dev/shm
      volumes:
        - name: default-data
          emptyDir:
            medium: Memory
            sizeLimit: 1Gi
        - name: dshm
          emptyDir:
            medium: Memory
            sizeLimit: 4Gi

## 📁 Snippets

### 📁 Node.js

Examples of useful scripts for Node.js

#### 📁 Creating Profiles in Bulk

Creating Profiles in Bulk

const axios = require('axios');
// This is the configuration. Insert your API token and specify the desired number of profiles
const config = {
    octo_token: "OCTO_API_TOKEN", // Specify your API token here
    quantity_of_profiles: 10,     // Specify the desired number of profiles
    octo_api_base_url: "https://app.octobrowser.net/api/v2/automation/"
};
const OCTO_REMOTE_API = axios.create({
    baseURL: config.octo_api_base_url,
    timeout: 10000,
    headers: {
        'X-Octo-Api-Token': config.octo_token,
        'Content-Type': "application/json"
    }
});
async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function check_limits(response) {
    function parse_int_safe(value) {
        const parsed = parseInt(value, 10);
        return isNaN(parsed) ? 0 : parsed;
    }
    const ratelimit_header = response.headers.ratelimit;
    if (!ratelimit_header) {
        console.warn('No ratelimit header found!');
        return;
    }
    const limit_entries = ratelimit_header.split(',').map(entry => entry.trim());
    for (const entry of limit_entries) {
        const name_match = entry.match(/^([^;]+)/);
        const r_match = entry.match(/;r=(\d+)/);
        const t_match = entry.match(/;t=(\d+)/);
        if (!r_match || !t_match) {
            console.warn(`Invalid ratelimit format: ${entry}`);
            continue;
        }
        const limit_name = name_match ? name_match[1] : 'unknown_limit';
        const remaining_quantity = parse_int_safe(r_match[1]);
        const window_seconds = parse_int_safe(t_match[1]);
        if (remaining_quantity < 5) {
            const wait_time = window_seconds + 1;
            console.log(`Waiting ${wait_time} seconds due to ${limit_name} limit`);
            await sleep(wait_time);
        }
    }
}
async function create_profile(quantity) {
    for (let i = 0; i < quantity; i++) {
        const data = {
            "title": `Profile ${i}`,
            "fingerprint": {
                "os": "win"
            }
        };
        try {
            const response = await OCTO_REMOTE_API.post('profiles', data);
            await check_limits(response);
            console.log(`Profile ${data.title} created successfully:`, response.data);
        } catch (error) {
            console.error(`Error creating profile ${i}:`, error.response ? error.response.data : error.message);
        }
    }
}
(async () => {
    await create_profile(config.quantity_of_profiles);
})();

#### 📁 Adding Extensions/Start Pages/Bookmarks to Profiles

How to get the extension UUID using API:

-
Add the desired extension to any profile (read How to connect extensions to profiles to learn more).

-
Get the profile with the desired extension using a GET request.

-
The server response will contain all data about the profile, including UUIDs of connected extensions.

-
You can remove unnecessary server response fields to show only the extensions:

const axios = require('axios');
const uuid = 'UUID'; // Specify the profile UUID here
const api_token = 'OCTO_API_TOKEN' // Specify your API token here
const config = {
  method: 'get',
  maxBodyLength: Infinity,
  url: `https://app.octobrowser.net/api/v2/automation/profiles/${uuid}`,
  headers: {
    'X-Octo-Api-Token': api_token
  }
};
axios(config)
.then(function (response) {
    console.dir(response.data.data.extensions);
})
.catch(function (error) {
  console.log(error);
});

Adding Extensions/Start Pages/Bookmarks to Multiple Profiles

const axios = require('axios');
// This is the configuration. Specify your Octo API Token here; you can modify this for your personal needs
const config = {
    octo_token: "OCTO_API_TOKEN", // Specify your API token here
    octo_api_base_url: "https://app.octobrowser.net/api/v2/automation/",
    profiles_to_update: [
        "UUID_1",
        "UUID_2"
        // Add UUIDs of profiles
    ],
    data: {
        extensions: ["nkbihfbeogaeaoehlefnkodbefgpgknn@12.17.2"],
        bookmarks: [
            { name: "google", url: "https://google.com" },
            { name: "facebook", url: "https://facebook.com" }
        ],
        start_pages: ["https://google.com", "https://facebook.com"]
    }
};
const OCTO_REMOTE_API = axios.create({
    baseURL: config.octo_api_base_url,
    timeout: 10000,
    headers: {
        'X-Octo-Api-Token': config.octo_token,
        'Content-Type': "application/json"
    }
});
async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function check_limits(response) {
    function parse_int_safe(value) {
        const parsed = parseInt(value, 10);
        return isNaN(parsed) ? 0 : parsed;
    }
    const ratelimit_header = response.headers.ratelimit;
    if (!ratelimit_header) {
        console.warn('No ratelimit header found!');
        return;
    }
    const limit_entries = ratelimit_header.split(',').map(entry => entry.trim());
    for (const entry of limit_entries) {
        const name_match = entry.match(/^([^;]+)/);
        const r_match = entry.match(/;r=(\d+)/);
        const t_match = entry.match(/;t=(\d+)/);
        if (!r_match || !t_match) {
            console.warn(`Invalid ratelimit format: ${entry}`);
            continue;
        }
        const limit_name = name_match ? name_match[1] : 'unknown_limit';
        const remaining_quantity = parse_int_safe(r_match[1]);
        const window_seconds = parse_int_safe(t_match[1]);
        if (remaining_quantity < 5) {
            const wait_time = window_seconds + 1;
            console.log(`Waiting ${wait_time} seconds due to ${limit_name} limit`);
            await sleep(wait_time);
        }
    }
}
async function update_profile(uuid) {
    try {
        const response = await OCTO_REMOTE_API.patch(`/profiles/${uuid}`, config.data);
        await check_limits(response);
        console.log(`Profile ${uuid} updated successfully`);
    } catch (error) {
        console.error(`Error updating profile ${uuid}:`, error.response?.data || error.message);
    }
}
(async () => {
    for (const uuid of config.profiles_to_update) {
        await update_profile(uuid);
    }
})();

Adding Extensions/Start Pages/Bookmarks to all Profiles on your Account

const axios = require('axios');
// This is the configuration. Specify your Octo API Token here; you can modify this for your personal needs
const config = {
    octo_token: "OCTO_API_TOKEN", // Specify your API token here
    octo_api_base_url: "https://app.octobrowser.net/api/v2/automation/",
    data: {
        "extensions": ["aapfglkgnhmiaabhiijkjpfmhllaodgp@4.2.3"],
        "bookmarks": [
            { "name": "google", "url": "https://google.com" },
            { "name": "facebook", "url": "https://facebook.com" }
        ],
        "start_pages": ["https://google.com", "https://facebook.com"]
    }
}
const OCTO_REMOTE_API = axios.create({
    baseURL: config.octo_api_base_url,
    timeout: 10000,
    headers: {
        'X-Octo-Api-Token': config.octo_token,
        'Content-Type': "application/json"
    }
});
//functions
async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms * 1000));
}
async function check_limits(response) {
    function parse_int_safe(value) {
        const parsed = parseInt(value, 10);
        return isNaN(parsed) ? 0 : parsed;
    }
    const ratelimit_header = response.headers.ratelimit;
    if (!ratelimit_header) {
        console.warn('No ratelimit header found!');
        return;
    }
    const limit_entries = ratelimit_header.split(',').map(entry => entry.trim());
    for (const entry of limit_entries) {
        const name_match = entry.match(/^([^;]+)/);
        const r_match = entry.match(/;r=(\d+)/);
        const t_match = entry.match(/;t=(\d+)/);
        if (!r_match || !t_match) {
            console.warn(`Invalid ratelimit format: ${entry}`);
            continue;
        }
        const limit_name = name_match ? name_match[1] : 'unknown_limit';
        const remaining_quantity = parse_int_safe(r_match[1]);
        const window_seconds = parse_int_safe(t_match[1]);
        if (remaining_quantity < 5) {
            const wait_time = window_seconds + 1;
            console.log(`Waiting ${wait_time} seconds due to ${limit_name} limit`);
            await sleep(wait_time);
        }
    }
}
async function get_total_profiles() {
    const response = await OCTO_REMOTE_API.get('/profiles?page=0&page_len=10');
    const total_profiles = response.data.total_count;
    const total_pages = Math.ceil(response.data.total_count / 100);
    console.log(`Total Profiles: ${total_profiles}\nTotal Pages: ${total_pages}`);
    await check_limits(response);
    return total_pages;
}
async function get_all_profiles_uuids(total_pages) {
    let profiles = [];
    for (let i = 0; i < total_pages; i++) {
        let response = await OCTO_REMOTE_API.get(`/profiles?page=${i}&page_len=100`);
        await check_limits(response);
        profiles.push(...response.data.data);
    }
    return profiles;
}
async function patch_all_profiles(profiles) {
    let updated = [];
    let not_updated = [];
    for (let profile of profiles) {
        try {
            const response = await OCTO_REMOTE_API.patch(`/profiles/${profile.uuid}`, config.data);
            await check_limits(response);
            updated.push(profile);
            console.log(`Successfully updated ${profile.uuid}`);
        } catch (error) {
            not_updated.push(profile);
            console.error(`ERROR: Can't patch profile ${profile.uuid}`);
        }
    }
    return [updated, not_updated];
}
(async () => {
    const total = await get_total_profiles();
    const profiles = await get_all_profiles_uuids(total);
    const [updated, not_updated] = await patch_all_profiles(profiles);
    console.log(`Finished process:\nUpdated: ${updated.length}\nNot updated: ${not_updated.length}`);
})();

Adding Extensions/Start Pages/Bookmarks to Profiles with Certain Tags

Note: You will get all profiles with the specified tag. This means that if a profile has other tags, it will still be included, so keep that in mind. If you specify two tags, you will only get profiles containing both tags.

const axios = require('axios');
//This is the configuration. Specify your Octo API Token here; you can modify this for your personal needs
const config = {
    octo_token: "OCTO_API_TOKEN", // Specify your API token here
    octo_api_base_url: "https://app.octobrowser.net/api/v2/automation/",
    tags: ['tag1', 'tag2'], // Specify the required tags
    page_len: 100,
    extensions: ['nkbihfbeogaeaoehlefnkodbefgpgknn@12.17.2'],
    start_pages: ["https://google.com", "https://facebook.com", "https://amazon.com"],
    bookmarks: [
        { name: "google", url: "https://google.com" },
        { name: "facebook", url: "https://facebook.com" }
    ]
};
const OCTO_REMOTE_API = axios.create({
    baseURL: config.octo_api_base_url,
    timeout: 10000,
    headers: {
        'X-Octo-Api-Token': config.octo_token,
        'Content-Type': "application/json"
    }
});
async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function check_limits(response) {
    function parse_int_safe(value) {
        const parsed = parseInt(value, 10);
        return isNaN(parsed) ? 0 : parsed;
    }
    const ratelimit_header = response.headers.ratelimit;
    if (!ratelimit_header) {
        console.warn('No ratelimit header found!');
        return;
    }
    const limit_entries = ratelimit_header.split(',').map(entry => entry.trim());
    for (const entry of limit_entries) {
        const name_match = entry.match(/^([^;]+)/);
        const r_match = entry.match(/;r=(\d+)/);
        const t_match = entry.match(/;t=(\d+)/);
        if (!r_match || !t_match) {
            console.warn(`Invalid ratelimit format: ${entry}`);
            continue;
        }
        const limit_name = name_match ? name_match[1] : 'unknown_limit';
        const remaining_quantity = parse_int_safe(r_match[1]);
        const window_seconds = parse_int_safe(t_match[1]);
        if (remaining_quantity < 5) {
            const wait_time = window_seconds + 1;
            console.log(`Waiting ${wait_time} seconds due to ${limit_name} limit`);
            await sleep(wait_time);
        }
    }
}
async function get_total_pages() {
    const search_tags = config.tags.join(',');
    const response = await OCTO_REMOTE_API.get(`/profiles?page=0&page_len=${config.page_len}&search_tags=${search_tags}`);
    await check_limits(response);
    const total_count = response.data.total_count;
    return Math.ceil(total_count / config.page_len);
}
async function get_profiles_by_tags(page) {
    const search_tags = config.tags.join(',');
    const response = await OCTO_REMOTE_API.get(`/profiles?page=${page}&page_len=${config.page_len}&search_tags=${search_tags}`);
    await check_limits(response);
    return response.data.data;
}
async function update_profile(uuid) {
    const data = {
        extensions: config.extensions,
        bookmarks: config.bookmarks,
        start_pages: config.start_pages
    };
    try {
        const response = await OCTO_REMOTE_API.patch(`/profiles/${uuid}`, data);
        await check_limits(response);
        console.log(`Profile ${uuid} updated successfully`);
    } catch (error) {
        console.error(`Error updating profile ${uuid}:`, error.response?.data || error.message);
    }
}
(async () => {
    const total_pages = await get_total_pages();
    console.log(`Total pages to process: ${total_pages}`);
    for (let page = 0; page < total_pages; page++) {
        const profiles = await get_profiles_by_tags(page);
        if (profiles.length === 0) {
            console.log(`No profiles found on page ${page} with tags ${config.tags.join(', ')}`);
            continue;
        }
        for (const profile of profiles) {
            await update_profile(profile.uuid);
        }
    }
})();

#### 📁 Creating Saved Proxies in Bulk from a .TXT file and Creating Profiles with Them

To use the following code, you need to have a .TXT file with the proxy data in the following format:

protocol;host;port;login;password;title;change_ip_url

The "change_ip_url" parameter is optional.

The proxy data must be provided strictly in the specified order.

Use only the following protocols: socks5, http, ssh.

An example file:
 [img: https://content.pstmn.io/bc2a08dd-3188-447e-9541-c831429c9186/U25pcHBldC5wbmc=]
const axios = require('axios');
const fs = require('fs').promises;
const config = {
  octo_token: "OCTO_API_TOKEN", // Specify your API token here
  proxies_file: "proxies.txt", // Specify the proxy file name
  octo_api_base_url: "https://app.octobrowser.net/api/v2/automation/"
};
const octo_remote_api = axios.create({
  baseURL: config.octo_api_base_url,
  timeout: 10000,
  headers: {
    'X-Octo-Api-Token': config.octo_token,
    'Content-Type': "application/json"
  }
});
async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
async function check_limits(response) {
    function parse_int_safe(value) {
        const parsed = parseInt(value, 10);
        return isNaN(parsed) ? 0 : parsed;
    }
    const ratelimit_header = response.headers.ratelimit;
    if (!ratelimit_header) {
        console.warn('No ratelimit header found!');
        return;
    }
    const limit_entries = ratelimit_header.split(',').map(entry => entry.trim());
    for (const entry of limit_entries) {
        const name_match = entry.match(/^([^;]+)/);
        const r_match = entry.match(/;r=(\d+)/);
        const t_match = entry.match(/;t=(\d+)/);
        if (!r_match || !t_match) {
            console.warn(`Invalid ratelimit format: ${entry}`);
            continue;
        }
        const limit_name = name_match ? name_match[1] : 'unknown_limit';
        const remaining_quantity = parse_int_safe(r_match[1]);
        const window_seconds = parse_int_safe(t_match[1]);
        if (remaining_quantity < 5) {
            const wait_time = window_seconds + 1;
            console.log(`Waiting ${wait_time} seconds due to ${limit_name} limit`);
            await sleep(wait_time);
        }
    }
}
async function create_proxy(proxy_data) {
  try {
    const response = await octo_remote_api.post('proxies', proxy_data);
    await check_limits(response);
    console.log(`Proxy ${proxy_data.title} created, UUID: ${response.data.data.uuid}`);
    return response.data.data.uuid;
  } catch (error) {
    console.error(`Error creating proxy ${proxy_data.title}:`, error.response ? error.response.data : error.message);
    return null;
  }
}
async function create_profile(profile_number, proxy_uuid, profile_title) {
  const data = {
    title: profile_title || `Profile ${profile_number}`,
    proxy: { uuid: proxy_uuid },
    fingerprint: { os: "win" }
  };
  try {
    const response = await octo_remote_api.post('profiles', data);
    await check_limits(response);
    console.log(`Profile ${data.title} created successfully`);
  } catch (error) {
    console.error(`Error creating profile ${profile_number}:`, error.response ? error.response.data : error.message);
  }
}
async function main() {
  try {
    const data = await fs.readFile(config.proxies_file, 'utf-8');
    const lines = data.split(/\r?\n/).filter(line => line.trim().length > 0);
    for (let i = 0; i < lines.length; i++) {
      const splitted = lines[i].split(';');
      let proxy_data;
      if (splitted.length === 7) {
        let [type, host, port, login, password, title, change_ip_url] = splitted;
        proxy_data = {
          type,
          host,
          port: parseInt(port),
          login,
          password,
          title,
          change_ip_url
        };
      } else if (splitted.length === 6) {
        let [type, host, port, login, password, title] = splitted;
        proxy_data = {
          type,
          host,
          port: parseInt(port),
          login,
          password,
          title
        };
      } else {
        console.log(`Skipping invalid proxy data on line ${i + 1}`);
        continue;
      }
      const proxy_uuid = await create_proxy(proxy_data);
      if (proxy_uuid) {
        await create_profile(i + 1, proxy_uuid, proxy_data.title);
      }
    }
  } catch (err) {
    console.error("Error reading proxies file:", err);
  }
}
main();

#### 📁 Adding a Saved Proxy to a Profile

How to get the UUID of a saved proxy using API:

Getting the favorite proxy's UUID from the profile data:

-
Connect the desired proxy to any profile.

-
Get the profile with the desired proxy using a GET request.

-
The server response will contain all data about the profile, including the UUID of the saved proxy.

-
You can remove unnecessary server response fields and display only the UUID of the saved proxy.

console.dir(response.data.data.proxy.uuid);
// We don't have to output the whole response to the console, only the proxy's UUID.
// Example of a server response:
'f9092a2f33384823be70554442311cc6'

Getting the saved proxy's UUID from the Proxy Manager list:

-
Use a Get Proxies request (you can find it in the documentation). You will get the data for all proxies saved in the Proxy Manager of your Octo Browser account; copy the UUID of the proxy that you need.

-
Example of a server response:

{
      uuid: 'cbc173cc120747c7b57d4f6ea2496141',
      type: 'socks5',
      port: 5003,
      host: '127.0.0.1',
      login: 'admin',
      password: 'admin',
      change_ip_url: null,
      external_id: null,
      profiles_count: 0,
      title: 'USA #2'
},

Adding a Proxy to a Profile

const axios = require('axios');
const config = {
  octo_token: "OCTO_API_TOKEN", // Specify your API token here
  octo_api_base_url: "https://app.octobrowser.net/api/v2/automation/",
  profile_uuid: "PROFILE_UUID",      // UUID of the profile to be updated
  proxy_uuid: "PROXY_UUID"      // UUID of the proxy to be assigned to the profile
};
const OCTO_REMOTE_API = axios.create({
  baseURL: config.octo_api_base_url,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'X-Octo-Api-Token': config.octo_token
  }
});
const patch_data = {
  proxy: {
    uuid: config.proxy_uuid
  }
};
const patch_config = {
  method: 'patch',
  url: `/profiles/${config.profile_uuid}`,
  data: patch_data
};
OCTO_REMOTE_API(patch_config)
  .then(response => {
    console.log('Profile updated successfully:', response.data);
  })
  .catch(error => {
    console.error('Error updating profile:', error.response ? error.response.data : error.message);
  });

#### 📁 Exporting all Profiles on the Export List to Files

This example collects profile data from the Export List and, based on that data, creates files with the .octo extension to be imported later.

Use an already existing folder for the "path_to_folder" parameter.

const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');
const octo_api_token = "OCTO_API_TOKEN"; // Specify your API token here
const path_to_folder = "C:\\PATH\\TO\\YOUR\\FOLDER"; // Specify the path to an existing folder
const octo_remote_api = axios.create({
  baseURL: 'https://app.octobrowser.net/api/v2/automation/',
  headers: {
    'X-Octo-Api-Token': octo_api_token,
    'Content-Type': 'application/json'
  }
});
let export_profiles_data = [];
async function get_total_profiles() {
  try {
    const response = await octo_remote_api.get('profiles/export?page=0');
    return response.data.data.total || 0;
  } catch (error) {
    console.error('Error fetching total profiles:', error.message);
    return 0;
  }
}
async function get_profiles(total_profiles) {
  const total_pages = Math.ceil(total_profiles / 100);
  console.log(`Total pages: ${total_pages}`);
  for (let page = 0; page < total_pages; page++) {
    try {
      const response = await octo_remote_api.get(`profiles/export?page=${page}&page_len=100`);
      export_profiles_data.push(...response.data.data.data);
    } catch (error) {
      console.error(`Error fetching page ${page}:`, error.message);
    }
  }
}
async function ensure_dir_exists(dir) {
  try {
    await fs.access(dir);
  } catch {
    await fs.mkdir(dir, { recursive: true });
  }
}
async function write_to_files() {
  await ensure_dir_exists(path_to_folder);
  const used_file_names = {};
  for (const item of export_profiles_data) {
    const inner_json_string = JSON.stringify(item);
    const outer_object = { data: inner_json_string };
    const json_to_write = JSON.stringify(outer_object);
    let filename = item.title.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    if (used_file_names[filename] !== undefined) {
      used_file_names[filename]++;
      filename += `_${used_file_names[filename]}`;
    } else {
      used_file_names[filename] = 0;
    }
    const file_path = path.join(path_to_folder, `${filename}.octo`);
    try {
      await fs.writeFile(file_path, json_to_write);
    } catch (error) {
      console.error(`Error writing file ${filename}:`, error.message);
    }
  }
}
(async () => {
  const total_profiles = await get_total_profiles();
  console.log(`Total profiles in export list: ${total_profiles}`);
  if (total_profiles === 0) {
    console.log('No profiles found or error fetching total.');
    return;
  }
  await get_profiles(total_profiles);
  console.log(`Quantity of profiles fetched: ${export_profiles_data.length}`);
  await write_to_files();
  console.log('Profiles saved successfully.');
})();

#### 📁 Getting All Profile Titles

This script retrieves all profile titles and saves them into a text file named profiles_titles.txt.

The output file is created in the current working directory.

const fs = require('fs').promises;
const axios = require('axios');
//This is the configuration. Specify your Octo API Token here
const config = {
    octo_token: "OCTO_API_TOKEN", // Specify your API token here
    octo_api_base_url: "https://app.octobrowser.net/api/v2/automation/",
}
const OCTO_REMOTE_API = axios.create({
    baseURL: config.octo_api_base_url,
    timeout: 10000,
    headers: {
        'X-Octo-Api-Token': config.octo_token,
        'Content-Type': "application/json"
    }
});
async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms * 1000));
}
async function check_limits(response) {
    function parse_int_safe(value) {
        const parsed = parseInt(value, 10);
        return isNaN(parsed) ? 0 : parsed;
    }
    const ratelimit_header = response.headers.ratelimit;
    if (!ratelimit_header) {
        console.warn('No ratelimit header found!');
        return;
    }
    const limit_entries = ratelimit_header.split(',').map(entry => entry.trim());
    for (const entry of limit_entries) {
        const name_match = entry.match(/^([^;]+)/);
        const r_match = entry.match(/;r=(\d+)/);
        const t_match = entry.match(/;t=(\d+)/);
        if (!r_match || !t_match) {
            console.warn(`Invalid ratelimit format: ${entry}`);
            continue;
        }
        const limit_name = name_match ? name_match[1] : 'unknown_limit';
        const remaining_quantity = parse_int_safe(r_match[1]);
        const window_seconds = parse_int_safe(t_match[1]);
        if (remaining_quantity < 5) {
            const wait_time = window_seconds + 1;
            console.log(`Waiting ${wait_time} seconds due to ${limit_name} limit`);
            await sleep(wait_time);
        }
    }
}
async function get_total_pages() {
    const response = await OCTO_REMOTE_API.get('/profiles?page=0&page_len=10');
    const total_profiles = response.data.total_count;
    const total_pages = Math.ceil(response.data.total_count / 100);
    console.log(`Total Profiles: ${total_profiles}\nTotal Pages: ${total_pages}`);
    await check_limits(response);
    return total_pages;
}
async function get_all_profiles_titles(total_pages) {
    let profiles = [];
    for (let i = 0; i < total_pages; i++) {
        let response = await OCTO_REMOTE_API.get(`/profiles?page=${i}&page_len=100&fields=title`);
        await check_limits(response);
        profiles.push(...response.data.data);
    }
    return profiles;
}
async function write_file(profiles) {
    const titles = profiles.map(item => item.title).filter(Boolean);
    try {
        await fs.writeFile('./profiles_titles.txt', titles.join('\n'), 'utf-8');
    } catch (error) {
        console.error(`ERROR: While trying writing the file some error occured:\n${error}`);
    }
}
(async () => {
    const total_pages = await get_total_pages();
    const profiles = await get_all_profiles_titles(total_pages);
    await write_file(profiles);
    console.log('Finished. Check profiles_titles.txt file...');
})()

### 📁 Python

Examples of useful scripts for Python

#### 📁 Create Profiles in Bulk

Creating Profiles in Bulk

import requests
import time
# Configuration is here. Insert your API token and specify the desired number of profiles
config = {
    "octo_token": "OCTO_API_TOKEN",  # Place your API token here
    "quantity_of_profiles": 10,      # Specify the desired number of profiles
    "octo_api_base_url": "https://app.octobrowser.net/api/v2/automation/"
}
session = requests.Session()
session.headers.update({
    "X-Octo-Api-Token": config["octo_token"],
    "Content-Type": "application/json"
})
session.timeout = 10
def sleep(ms):
    time.sleep(ms)
def parse_int_safe(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
def check_limits(response):
    ratelimit_header = response.headers.get('ratelimit')
    if not ratelimit_header:
        print('No ratelimit header found!')
        return
    limit_entries = [entry.strip() for entry in ratelimit_header.split(',')]
    for entry in limit_entries:
        parts = entry.split(';')
        limit_name = parts[0] if parts else 'unknown_limit'
        remaining_quantity = 0
        window_seconds = 0
        for part in parts[1:]:
            if part.startswith('r='):
                remaining_quantity = parse_int_safe(part[2:])
            elif part.startswith('t='):
                window_seconds = parse_int_safe(part[2:])
        print(f'{limit_name}: remaining={remaining_quantity}, window={window_seconds}s')
        if remaining_quantity < 5:
            wait_time = window_seconds + 1
            print(f'Waiting {wait_time} seconds due to {limit_name} limit')
            sleep(wait_time)
def create_profiles(quantity):
    for i in range(quantity):
        data = {
            "title": f"Profile {i}",
            "fingerprint": {
                "os": "win"
            }
        }
        try:
            response = session.post(f"{config['octo_api_base_url']}profiles", json=data)
            response.raise_for_status()
            check_limits(response)
            print(f"Profile {data['title']} created successfully:", response.json())
        except requests.RequestException as e:
            error_msg = e.response.json() if e.response else str(e)
            print(f"Error creating profile {i}:", error_msg)
if __name__ == "__main__":
    create_profiles(config["quantity_of_profiles"])

#### 📁 Adding Extensions/Start Pages/Bookmarks to Profiles

How to get the extension UUID using API:

-
Add the desired extension to any profile (read How to connect extensions to profiles to learn more).

-
Get the profile with the desired extension using a GET request.

-
The server response will contain all data about the profile, including UUIDs of connected extensions.

-
You can remove unnecessary server response fields to show only the extensions:

import requests
uuid = 'UUID'  # Specify the profile UUID here
api_token = 'OCTO_API_TOKEN'  # Specify your API token here
url = f"https://app.octobrowser.net/api/v2/automation/profiles/{uuid}"
payload = {}
headers = {
    'X-Octo-Api-Token': api_token
}
response = requests.request("GET", url, headers=headers, data=payload)
data = response.json()
extensions = data['data']['extensions']
print(extensions)

Adding Extensions/Start Pages/Bookmarks to Multiple Profiles

import requests
import time
# This is the configuration. Specify your Octo API Token here; you can modify this for your personal needs
config = {
    "octo_token": "OCTO_API_TOKEN",  # Specify your API token here
    "octo_api_base_url": "https://app.octobrowser.net/api/v2/automation/",
    "profiles_to_update": [
        "UUID_1",
        "UUID_2" # Add UUIDs of profiles
    ],
    "data": {
        "extensions": ["nkbihfbeogaeaoehlefnkodbefgpgknn@12.17.2"],
        "bookmarks": [
            {"name": "google", "url": "https://google.com"},
            {"name": "facebook", "url": "https://facebook.com"}
        ],
        "start_pages": ["https://google.com", "https://facebook.com"]
    }
}
session = requests.Session()
session.headers.update({
    "X-Octo-Api-Token": config["octo_token"],
    "Content-Type": "application/json"
})
session.timeout = 10
def sleep(seconds):
    time.sleep(seconds)
def parse_int_safe(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
def check_limits(response):
    ratelimit_header = response.headers.get('ratelimit')
    if not ratelimit_header:
        print('No ratelimit header found!')
        return
    limit_entries = [entry.strip() for entry in ratelimit_header.split(',')]
    for entry in limit_entries:
        parts = entry.split(';')
        limit_name = parts[0] if parts else 'unknown_limit'
        remaining_quantity = 0
        window_seconds = 0
        for part in parts[1:]:
            if part.startswith('r='):
                remaining_quantity = parse_int_safe(part[2:])
            elif part.startswith('t='):
                window_seconds = parse_int_safe(part[2:])
        print(f'{limit_name}: remaining={remaining_quantity}, window={window_seconds}s')
        if remaining_quantity < 5:
            wait_time = window_seconds + 1
            print(f'Waiting {wait_time} seconds due to {limit_name} limit')
            sleep(wait_time)
def update_profile(uuid):
    try:
        response = session.patch(
            f"{config['octo_api_base_url']}profiles/{uuid}",
            json=config["data"]
        )
        response.raise_for_status()
        check_limits(response)
        print(f"Profile {uuid} updated successfully")
    except Exception as e:
        print(f"Error updating profile {uuid}: {str(e)}")
if __name__ == "__main__":
    for uuid in config["profiles_to_update"]:
        update_profile(uuid)

Adding Extensions/Start Pages/Bookmarks to all Profiles on your Account

import requests
import math
import time
# This is the configuration. Specify your Octo API Token here; you can modify this for your personal needs
config = {
    "octo_token": "OCTO_API_TOKEN", # Specify your API token here
    "octo_api_base_url": "https://app.octobrowser.net/api/v2/automation/",
    "data": {
        "extensions": ["aapfglkgnhmiaabhiijkjpfmhllaodgp@4.2.3"],
        "bookmarks": [
            {"name": "google", "url": "https://google.com"},
            {"name": "facebook", "url": "https://facebook.com"}
        ],
        "start_pages": ["https://google.com", "https://facebook.com"]
    }
}
session = requests.Session()
session.headers.update({
    "X-Octo-Api-Token": config["octo_token"],
    "Content-Type": "application/json"
})
session.timeout = 10
def sleep(seconds):
    time.sleep(seconds)
def parse_int_safe(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
def check_limits(response):
    ratelimit_header = response.headers.get('ratelimit')
    if not ratelimit_header:
        print('No ratelimit header found!')
        return
    limit_entries = [entry.strip() for entry in ratelimit_header.split(',')]
    for entry in limit_entries:
        parts = entry.split(';')
        limit_name = parts[0] if parts else 'unknown_limit'
        remaining_quantity = 0
        window_seconds = 0
        for part in parts[1:]:
            if part.startswith('r='):
                remaining_quantity = parse_int_safe(part[2:])
            elif part.startswith('t='):
                window_seconds = parse_int_safe(part[2:])
        print(f'{limit_name}: remaining={remaining_quantity}, window={window_seconds}s')
        if remaining_quantity < 5:
            wait_time = window_seconds + 1
            print(f'Waiting {wait_time} seconds due to {limit_name} limit')
            sleep(wait_time)
def get_total_profiles():
    response = session.get(f"{config['octo_api_base_url']}profiles?page=0&page_len=10")
    response.raise_for_status()
    total_profiles = response.json()["total_count"]
    total_pages = math.ceil(total_profiles / 100)
    print(f"Total Profiles: {total_profiles}\nTotal Pages: {total_pages}")
    check_limits(response)
    return total_pages
def get_all_profiles_uuids(total_pages):
    profiles = []
    for i in range(total_pages):
        response = session.get(f"{config['octo_api_base_url']}profiles?page={i}&page_len=100")
        response.raise_for_status()
        check_limits(response)
        profiles.extend(response.json()["data"])
    return profiles
def patch_all_profiles(profiles):
    updated = []
    not_updated = []
    for profile in profiles:
        try:
            response = session.patch(
                f"{config['octo_api_base_url']}profiles/{profile['uuid']}",
                json=config["data"]
            )
            response.raise_for_status()
            check_limits(response)
            updated.append(profile)
            print(f"Successfully updated {profile['uuid']}")
        except Exception as e:
            not_updated.append(profile)
            print(f"ERROR: Can't patch profile {profile['uuid']} - {str(e)}")
    return updated, not_updated
if __name__ == "__main__":
    try:
        total = get_total_profiles()
        profiles = get_all_profiles_uuids(total)
        updated, not_updated = patch_all_profiles(profiles)
        print(f"Finished process:\nUpdated: {len(updated)}\nNot updated: {len(not_updated)}")
    except Exception as e:
        print(f"Fatal error: {str(e)}")

Adding Extensions/Start Pages/Bookmarks to Profiles with Certain Tags

Note: You will get all profiles with the specified tag. This means that if a profile has other tags, it will still be included, so keep that in mind. If you specify two tags, you will only get profiles containing both tags.

import requests
import math
import time
# here is config. Paste your Octo API Token here and you can modify this for your personal needs
config = {
    "octo_token": "OCTO_API_TOKEN",  # Place your API token here
    "octo_api_base_url": "https://app.octobrowser.net/api/v2/automation/",
    "tags": ['tag1', 'tag2'], # Specify the required tags
    "page_len": 100,
    "extensions": ['nkbihfbeogaeaoehlefnkodbefgpgknn@12.17.2'],
    "start_pages": ["https://google.com", "https://facebook.com", "https://amazon.com"],
    "bookmarks": [
        {"name": "google", "url": "https://google.com"},
        {"name": "facebook", "url": "https://facebook.com"}
    ]
}
session = requests.Session()
session.headers.update({
    "X-Octo-Api-Token": config["octo_token"],
    "Content-Type": "application/json"
})
session.timeout = 10
def sleep(seconds):
    time.sleep(seconds)
def parse_int_safe(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
def check_limits(response):
    ratelimit_header = response.headers.get('ratelimit')
    if not ratelimit_header:
        print('No ratelimit header found!')
        return
    limit_entries = [entry.strip() for entry in ratelimit_header.split(',')]
    for entry in limit_entries:
        parts = entry.split(';')
        limit_name = parts[0] if parts else 'unknown_limit'
        remaining_quantity = 0
        window_seconds = 0
        for part in parts[1:]:
            if part.startswith('r='):
                remaining_quantity = parse_int_safe(part[2:])
            elif part.startswith('t='):
                window_seconds = parse_int_safe(part[2:])
        print(f'{limit_name}: remaining={remaining_quantity}, window={window_seconds}s')
        if remaining_quantity < 5:
            wait_time = window_seconds + 1
            print(f'Waiting {wait_time} seconds due to {limit_name} limit')
            sleep(wait_time)
def get_total_pages():
    search_tags = ",".join(config["tags"])
    url = f"{config['octo_api_base_url']}profiles?page=0&page_len={config['page_len']}&search_tags={search_tags}"
    response = session.get(url)
    response.raise_for_status()
    check_limits(response)
    total_count = response.json().get("total_count", 0)
    return math.ceil(total_count / config["page_len"])
def get_profiles_by_tags(page):
    search_tags = ",".join(config["tags"])
    url = f"{config['octo_api_base_url']}profiles?page={page}&page_len={config['page_len']}&search_tags={search_tags}"
    response = session.get(url)
    response.raise_for_status()
    check_limits(response)
    return response.json().get("data", [])
def update_profile(uuid):
    data = {
        "extensions": config["extensions"],
        "bookmarks": config["bookmarks"],
        "start_pages": config["start_pages"]
    }
    try:
        url = f"{config['octo_api_base_url']}profiles/{uuid}"
        response = session.patch(url, json=data)
        response.raise_for_status()
        check_limits(response)
        print(f"Profile {uuid} updated successfully")
    except requests.RequestException as e:
        error_info = e.response.json() if e.response else str(e)
        print(f"Error updating profile {uuid}: {error_info}")
def main():
    total_pages = get_total_pages()
    print(f"Total pages to process: {total_pages}")
    for page in range(total_pages):
        profiles = get_profiles_by_tags(page)
        if not profiles:
            print(f"No profiles found on page {page} with tags {', '.join(config['tags'])}")
            continue
        for profile in profiles:
            update_profile(profile.get("uuid"))
if __name__ == "__main__":
    main()

#### 📁 Creating Saved Proxies in Bulk from a .TXT file and Creating Profiles with Them

To work with this example of code, you should have a .TXT file with proxy data in the following format:

protocol;host;port;login;password;title;change_ip_url

change ip URL is optional.

The proxy data must be provided strictly in the specified order.

Use only the following protocols:

socks5, http, ssh

An example file:
 [img: https://content.pstmn.io/bc2a08dd-3188-447e-9541-c831429c9186/U25pcHBldC5wbmc=]
import requests
import time
config = {
    "octo_token": "OCTO_API_TOKEN", # Your API Token
    "proxies_file": "proxies.txt", # File with proxies
    "octo_api_base_url": "https://app.octobrowser.net/api/v2/automation/"
}
session = requests.Session()
session.headers.update({
    'X-Octo-Api-Token': config["octo_token"],
    'Content-Type': "application/json"
})
def sleep(ms):
    time.sleep(ms)
def parse_int_safe(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
def check_limits(response):
    ratelimit_header = response.headers.get('ratelimit')
    if not ratelimit_header:
        print('No ratelimit header found!')
        return
    limit_entries = [entry.strip() for entry in ratelimit_header.split(',')]
    for entry in limit_entries:
        parts = entry.split(';')
        limit_name = parts[0] if parts else 'unknown_limit'
        remaining_quantity = 0
        window_seconds = 0
        for part in parts[1:]:
            if part.startswith('r='):
                remaining_quantity = parse_int_safe(part[2:])
            elif part.startswith('t='):
                window_seconds = parse_int_safe(part[2:])
        print(f'{limit_name}: remaining={remaining_quantity}, window={window_seconds}s')
        if remaining_quantity < 5:
            wait_time = window_seconds + 1
            print(f'Waiting {wait_time} seconds due to {limit_name} limit')
            sleep(wait_time)
def create_proxy(proxy_data):
    try:
        response = session.post(f"{config['octo_api_base_url']}proxies", json=proxy_data, timeout=10)
        response.raise_for_status()
        check_limits(response)
        uuid = response.json().get('data', {}).get('uuid')
        print(f"Proxy {proxy_data.get('title')} created, UUID: {uuid}")
        return uuid
    except Exception as e:
        print(f"Error creating proxy {proxy_data.get('title')}: {e}")
        return None
def create_profile(profile_number, proxy_uuid, profile_title):
    data = {
        "title": profile_title or f"Profile {profile_number}",
        "proxy": {"uuid": proxy_uuid},
        "fingerprint": {"os": "win"}
    }
    try:
        response = session.post(f"{config['octo_api_base_url']}profiles", json=data, timeout=10)
        response.raise_for_status()
        check_limits(response)
        print(f"Profile {data['title']} created successfully")
    except Exception as e:
        print(f"Error creating profile {profile_number}: {e}")
def main():
    try:
        with open(config["proxies_file"], "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading proxies file: {e}")
        return
    for i, line in enumerate(lines):
        splitted = line.split(';')
        if len(splitted) == 7:
            type_, host, port, login, password, title, change_ip_url = splitted
            proxy_data = {
                "type": type_,
                "host": host,
                "port": int(port),
                "login": login,
                "password": password,
                "title": title,
                "change_ip_url": change_ip_url
            }
        elif len(splitted) == 6:
            type_, host, port, login, password, title = splitted
            proxy_data = {
                "type": type_,
                "host": host,
                "port": int(port),
                "login": login,
                "password": password,
                "title": title
            }
        else:
            print(f"Skipping invalid proxy data on line {i + 1}")
            continue
        proxy_uuid = create_proxy(proxy_data)
        if proxy_uuid:
            create_profile(i + 1, proxy_uuid, proxy_data.get("title"))
if __name__ == "__main__":
    main()

#### 📁 Adding a Saved Proxy to a Profile

How to get the UUID of a saved proxy using API:

Getting the favorite proxy's UUID from the profile data:

-
Connect the desired proxy to any profile.

-
Get the profile with the desired proxy using a GET request.

-
The server response will contain all data about the profile, including the UUID of the saved proxy.

-
You can remove unnecessary server response fields and display only the UUID of the saved proxy.

import requests
uuid = 'UUID'  # Place the profile UUID here
api_token = 'OCTO_API_TOKEN'  # Place your API token here
url = f'https://app.octobrowser.net/api/v2/automation/profiles/{uuid}'
headers = {
    'X-Octo-Api-Token': api_token
}
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    proxy_uuid = data['data']['proxy']['uuid']
    print(proxy_uuid)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

Getting the saved proxy's UUID from the Proxy Manager list:

-
Use a Get Proxies request (you can find it in the documentation). You will get the data for all proxies saved in the Proxy Manager of your Octo Browser account; copy the UUID of the proxy that you need.

-
Example of a server response:

{
      uuid: 'cbc173cc120747c7b57d4f6ea2496141',
      type: 'socks5',
      port: 5003,
      host: '127.0.0.1',
      login: 'admin',
      password: 'admin',
      change_ip_url: None,
      external_id: None,
      title: 'USA #2',
      profiles_count: 0
}

Adding a Proxy to a Profile

import requests
config = {
    "octo_token": "OCTO_API_TOKEN",           # Your API token
    "octo_api_base_url": "https://app.octobrowser.net/api/v2/automation/",
    "profile_uuid": "PROFILE_UUID",            # UUID of the profile to update
    "proxy_uuid": "PROXY_UUID"                 # UUID of the proxy to assign to the profile
}
headers = {
    "Content-Type": "application/json",
    "X-Octo-Api-Token": config["octo_token"]
}
patch_data = {
    "proxy": {
        "uuid": config["proxy_uuid"]
    }
}
try:
    url = f"{config['octo_api_base_url']}profiles/{config['profile_uuid']}"
    response = requests.patch(url, json=patch_data, headers=headers, timeout=10)
    response.raise_for_status()
    print("Profile updated successfully:", response.json())
except requests.RequestException as e:
    if e.response is not None:
        print("Error updating profile:", e.response.json())
    else:
        print("Error updating profile:", str(e))

#### 📁 Exporting all Profiles on the Export List to Files

This example collects profile data from the Export List and, based on that data, creates files with the .octo extension to be imported later.

Use an already existing folder for the "PATH_TO_FOLDER" parameter.

import asyncio
import httpx
import json
from pathlib import Path
from typing import List, Dict, Any
# Configuration
OCTO_API_TOKEN = "OCTO_API_TOKEN"  # Place your API token here
PATH_TO_FOLDER = "C:\\PATH\\TO\\YOUR\\FOLDER"  # Specify the path to an existing folder
# HTTP client setup
headers = {
    'X-Octo-Api-Token': OCTO_API_TOKEN,
    'Content-Type': 'application/json'
}
client = httpx.AsyncClient(
    base_url='https://app.octobrowser.net/api/v2/automation/',
    headers=headers
)
export_profiles_data: List[Dict[str, Any]] = []
async def get_total_profiles() -> int:
    """Get total number of profiles"""
    try:
        response = await client.get('profiles/export?page=0')
        data = response.json()
        return data.get('data', {}).get('total', 0)
    except Exception as e:
        print(f'Error fetching total profiles: {e}')
        return 0
async def get_profiles(total_profiles: int) -> None:
    total_pages = (total_profiles + 99) // 100
    print(f'Total pages: {total_pages}')
    for page in range(total_pages):
        try:
            response = await client.get(f'profiles/export?page={page}&page_len=100')
            data = response.json()
            export_profiles_data.extend(data.get('data', {}).get('data', []))
        except Exception as e:
            print(f'Error fetching page {page}: {e}')
async def ensure_dir_exists(directory: str) -> None:
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
async def write_to_files() -> None:
    await ensure_dir_exists(PATH_TO_FOLDER)
    used_file_names: Dict[str, int] = {}
    for item in export_profiles_data:
        inner_json_string = json.dumps(item)
        outer_object = {'data': inner_json_string}
        json_to_write = json.dumps(outer_object)
        filename = ''.join(c if c.isalnum() else '_' for c in item.get('title', '')).lower()
        if filename in used_file_names:
            used_file_names[filename] += 1
            filename += f'_{used_file_names[filename]}'
        else:
            used_file_names[filename] = 0
        file_path = Path(PATH_TO_FOLDER) / f'{filename}.octo'
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_to_write)
        except Exception as e:
            print(f'Error writing file {filename}: {e}')
async def main():
    total_profiles = await get_total_profiles()
    print(f'Total profiles in export list: {total_profiles}')
    if total_profiles == 0:
        print('No profiles found or error fetching total.')
        return
    await get_profiles(total_profiles)
    print(f'Quantity of profiles fetched: {len(export_profiles_data)}')
    await write_to_files()
    print('Profiles saved successfully.')
    await client.aclose()
if __name__ == "__main__":
    asyncio.run(main())

#### 📁 Getting All Profile Titles

This script retrieves all profile titles and saves them into a text file named profiles_titles.txt.

The output file is created in the current working directory.

import httpx
import asyncio
from pathlib import Path
#config. Paste your API Token here
config = {
    "octo_token": "OCTO_API_TOKEN",
    "octo_api_base_url": "https://app.octobrowser.net/api/v2/automation/",
}
headers = {
    "X-Octo-Api-Token": config["octo_token"],
    "Content-Type": "application/json",
}
async def sleep(seconds):
    await asyncio.sleep(seconds)
def parse_int_safe(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
async def check_limits(response):
    ratelimit_header = response.headers.get('ratelimit')
    if not ratelimit_header:
        print('No ratelimit header found!')
        return
    limit_entries = [entry.strip() for entry in ratelimit_header.split(',')]
    for entry in limit_entries:
        parts = entry.split(';')
        limit_name = parts[0] if parts else 'unknown_limit'
        remaining_quantity = 0
        window_seconds = 0
        for part in parts[1:]:
            if part.startswith('r='):
                remaining_quantity = parse_int_safe(part[2:])
            elif part.startswith('t='):
                window_seconds = parse_int_safe(part[2:])
        print(f'{limit_name}: remaining={remaining_quantity}, window={window_seconds}s')
        if remaining_quantity < 5:
            wait_time = window_seconds + 1
            print(f'Waiting {wait_time} seconds due to {limit_name} limit')
            await sleep(wait_time)
async def get_total_pages(client):
    response = await client.get("profiles?page=0&page_len=10")
    data = response.json()
    total_profiles = data["total_count"]
    total_pages = (total_profiles + 99) // 100
    print(f"Total Profiles: {total_profiles}\nTotal Pages: {total_pages}")
    await check_limits(response)
    return total_pages
async def get_all_profiles_titles(client, total_pages):
    profiles = []
    for page in range(total_pages):
        response = await client.get(
            f"profiles?page={page}&page_len=100&fields=title"
        )
        data = response.json()
        await check_limits(response)
        profiles.extend(data["data"])
    return profiles
async def write_file(profiles):
    titles = [item["title"] for item in profiles if item.get("title")]
    try:
        Path("profiles_titles.txt").write_text("\n".join(titles), encoding="utf-8")
    except Exception as e:
        print(f"ERROR: While trying writing the file some error occurred:\n{e}")
async def main():
    async with httpx.AsyncClient(
        base_url=config["octo_api_base_url"],
        headers=headers
    ) as client:
        total_pages = await get_total_pages(client)
        profiles = await get_all_profiles_titles(client, total_pages)
        await write_file(profiles)
        print("Finished. Check profiles_titles.txt file...")
if __name__ == "__main__":
    asyncio.run(main())
