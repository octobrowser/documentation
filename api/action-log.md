# Action Log API

The action log is a real-time audit stream of team events (profile starts, stops, proxy changes, transfers, deletions) delivered over a WebSocket. Unlike the rest of the cloud API, it is not a REST endpoint: you open one long-lived connection and receive JSON pages as events happen.

> **Live check on 2026-08-20:** an HTTP upgrade request to this path returned 404 `not_found`; the endpoint is documented in the official Postman collection and may require the API option to be enabled on the subscription — treat the details below as upstream-documented, not mirror-verified.

## Endpoint

- **Type**: WebSocket
- **URL**: `wss://app.octobrowser.net/api/v2/automation/ws/action_log`
- **Authentication**: API token in the `X-Octo-Api-Token` header, sent with the upgrade request (same token as the REST API, see [authentication.md](authentication.md)).

Example handshake with [`websocat`](https://github.com/vi/websocat):

```bash
websocat -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  "wss://app.octobrowser.net/api/v2/automation/ws/action_log"
```

## Query Parameters

- `after_uuid` (string, UUID, optional) — UUID of the last received entry. Use this to resume streaming from a specific point after a disconnect.
- `from_timestamp` (integer, Unix timestamp, optional) — start streaming from this time. Events are only available for 24 hours.

> Parts of the upstream docs call this parameter `from_time`; `from_timestamp` is the name used in the upstream parameter table and examples, and the one documented here.

```text
wss://app.octobrowser.net/api/v2/automation/ws/action_log
wss://app.octobrowser.net/api/v2/automation/ws/action_log?after_uuid=550e8400-e29b-41d4-a716-446655440000
wss://app.octobrowser.net/api/v2/automation/ws/action_log?from_timestamp=1707053400
```

## Message Format

Each WebSocket message is a **StreamPage**: an `items` array of up to 100 events plus a `watermark` cursor. There is no `{ success, msg, data }` envelope.

**Response**

```json
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
          "subdivisions": ["Île-de-France", "Paris"],
          "postalCode": "75008",
          "cityName": "Paris",
          "timezone": "Europe/Paris",
          "lat": 48.8566,
          "lon": 2.3522,
          "languages": ["fr", "en-US", "en"],
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
```

### Item Fields

- `uuid` (string) — unique id of the log entry; feed it back as `after_uuid` to resume.
- `action` (string) — event type, see [Event Types](#event-types).
- `time` (integer) — Unix timestamp of the event.
- `user_email` (string) — team member who triggered the event.
- `object_type` (string) — type of the affected object, e.g. `profile`.
- `object_id` (string) — UUID of the affected object.
- `object_title` (string) — human-readable title of the affected object.
- `data` (object) — event-specific payload; for profile start events it carries `connection_data`.

### `connection_data` Fields

- `ip` (string) — egress IP address of the profile's connection.
- `countryCode` / `countryName` (string) — geolocation of the IP.
- `subdivisions` (array of string) — region / city hierarchy.
- `postalCode`, `cityName` (string) — postal code and city name.
- `timezone` (string) — IANA timezone, e.g. `Europe/Paris`.
- `lat`, `lon` (number) — approximate coordinates.
- `languages` (array of string) — languages derived from the location.
- `isp` (string) — provider name.
- `connectionType` (string) — e.g. `Cable/DSL`.

### Watermark

The `watermark` object acts as a cursor:

- contains `uuid` and `time` of the last record in the page;
- guarantees stable ordering even when several records share the same timestamp;
- store it after every message and pass `after_uuid` (or `from_timestamp`) on reconnect to continue where you left off.

## Event Types

- `profiles.started` — profile browser was started
- `profiles.stopped` — profile browser was stopped
- `profiles.force_stopped` — profile browser was force stopped
- `profiles.transferred` — profile was transferred
- `profiles.trashed` — profile was moved to the trash bin
- `profiles.updated` — profile was updated
- `profiles.deleted` — profile was deleted
- `profiles.proxy_assigned` — proxy was assigned to a profile
- `profiles.proxy_unassigned` — proxy was unassigned from a profile
- `profiles.proxy_changed` — profile's proxy was changed to another one

## How It Works

1. Connect to the WebSocket endpoint with the token header.
2. Receive pages of events as JSON messages.
3. Persist the `watermark` from each page and use it on reconnect.

## Constraints

- **Event retention**: 24 hours; entries older than 24 h are no longer available.
- **Batch size**: up to 100 records per page.
- **Subscription**: the team must have the API option in its subscription.
- **Permissions**: subaccounts presumably need the `manage_action_log` permission (see [teams.md](teams.md)); this was not verified.

## Common Errors

- **401 Unauthorized** — missing or invalid `X-Octo-Api-Token` header.
- **403 Forbidden** — likely when the API option is not enabled on the subscription or the subaccount lacks `manage_action_log` (not verified).
- **404 Not Found** (`not_found`) — returned to a plain HTTP/upgrade request when the stream is unavailable for the account (observed on 2026-08-20; likely the API option is missing from the subscription).

See [errors.md](errors.md) for the standard error envelope.
