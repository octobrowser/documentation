# Folders API

Folders group browser profiles for organisation and access control. They were introduced in Octo Browser 3.0 (July 2026) and are managed independently, then referenced from profile payloads via the `folder` field.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ..., "code": string | null }`.

## Get Folders

List every folder in the workspace. The response is not paginated.

**Endpoint**: `GET /folders`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/folders" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    {
      "uuid": "4d867ccd37224526ac2f6a65761c8614",
      "name": "clients",
      "assignable_wo_permission": false
    }
  ],
  "code": null
}
```

## Create Folders

Creates one or more folders in a single request.

**Endpoint**: `POST /folders`

Returns HTTP `200 OK` (not `201`, unlike `POST /profiles`, `POST /tags`, and `POST /proxies`).

**Request Body**:
- `folders` (array, required) — 1 to 100 folder objects, each with:
  - `name` (string, required) — folder name, 1–20 characters.
  - `assignable_wo_permission` (bool, optional) — whether profiles can be assigned to this folder without an explicit folder permission. Defaults to `false`.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/folders" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"folders":[{"name":"clients"}]}'
```

### Example Response

`data` is an array of the created folders:

```json
{
  "success": true,
  "msg": "",
  "data": [
    {
      "uuid": "4d867ccd37224526ac2f6a65761c8614",
      "name": "clients",
      "assignable_wo_permission": false
    }
  ],
  "code": null
}
```

## Update Folder

**Endpoint**: `PATCH /folders/{folder}`

The `{folder}` path parameter accepts either the folder UUID or the folder name. Both body fields are optional; supply only what you want to change:
- `name` (string, optional) — new name, 1–20 characters.
- `assignable_wo_permission` (bool, optional).

```bash
curl -X PATCH "https://app.octobrowser.net/api/v2/automation/folders/4d867ccd37224526ac2f6a65761c8614" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"clients-eu","assignable_wo_permission":true}'
```

### Example Response

`data` is the updated folder object:

```json
{
  "success": true,
  "msg": "",
  "data": {
    "uuid": "4d867ccd37224526ac2f6a65761c8614",
    "name": "clients-eu",
    "assignable_wo_permission": true
  },
  "code": null
}
```

## Remove Folder

**Endpoint**: `DELETE /folders/{folder}`

The `{folder}` path parameter accepts either the folder UUID or the folder name.

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/folders/clients-eu" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": null,
  "code": null
}
```

## Using Folders with Profiles

Profile payloads accept an optional `folder` field (string) on `POST /profiles`, `PATCH /profiles/{uuid}`, and `POST /profiles/import` to place the profile into a folder.

## Common Errors

- **400 Bad Request** — validation failure, e.g. a name longer than 20 characters. Note that this payload has no `success`/`msg`/`data`/`code` envelope, only `validation_error`:

  ```json
  {
    "validation_error": {
      "body_params": [
        {
          "type": "string_too_long",
          "loc": ["name"],
          "msg": "String should have at most 20 characters",
          "input": "a-folder-name-that-is-too-long"
        }
      ]
    }
  }
  ```

- **404 Not Found** — folder UUID or name does not exist:

  ```json
  {
    "success": false,
    "msg": "Folder not found",
    "data": "",
    "code": "not_found"
  }
  ```

See [errors.md](errors.md) for the standard error envelope.
