# REEF API

## Definitions

Managed Session - A time-limited session generated for a user (customer) with a PIN that allows authentication with the vehicle (starting the vehicle) instead of a key (or other method). When the managed session is ended the corresponding PIN for the session will no longer work.

## Environments

### development (dev)

base_url: https://dev.reef.api.arcimoto.com/v1

### staging (staging)

base_url: https://staging.reef.api.arcimoto.com/v1

### production (prod)

base_url: https://reef.api.arcimoto.com/v1

## Authentication

Authentication is handled via mTLS.

## Endpoints

### Managed Sessions List

Retrieve all managed sessions

#### Route

{base_url}/managed-sessions GET

#### Response

##### Format

```text
{
  "managed_sessions": [
    {
      "id": Integer,
      "vin": String,
      "pin": String,
      "initialization": UTC Timestamp,
      "completion": UTC Timestamp or String: "active",
      "verification_id": String
    },
    ...
  ]
}
```

##### Example

```json
{
  "managed_sessions": [
    {
      "id": 1,
      "vin": "1D4PT4GKXBW600841",
      "pin": "163063",
      "initialization": "2021-06-09 22:03:49.508408",
      "completion": "2021-06-09 22:06:56.232012",
      "verification_id": "fg56thd8f41c945091156ty7"
    },
    {
      "id": 2,
      "vin": "1D4PT4GKXBW600841",
      "pin": "062309",
      "initialization": "2021-06-09 22:07:26.955043",
      "completion": "2021-06-09 22:07:39.099169",
      "verification_id": "c24gt2d8f41c9450911e7890"
    },
    {
      "id": 3,
      "vin": "1D4PT4GKXBW600841",
      "pin": "633911",
      "initialization": "2021-06-09 22:07:39.113810",
      "completion": "active",
      "verification_id": "60c252d8f41c9450911e8926"
    },
    {
      "id": 4,
      "vin": "7F7ATR312KER0400",
      "pin": "086403",
      "initialization": "2021-05-09 22:15:04.907120",
      "completion": "2021-05-12 22:15:04.907120",
      "verification_id": "60c252d8f4324550911e896e"
    }
  ]
}
```

### Managed Session Get by Id

Retrieve managed session data by id

#### Route

{base_url}/managed-sessions/{id} GET

#### Parameters

##### id

Managed Session Id

#### Response

##### Format

```text
{
  "managed_sessions": [
    {
      "id": Integer,
      "vin": String,
      "pin": String,
      "initialization": UTC Timestamp,
      "completion": UTC Timestamp or String: "active",
      "verification_id": String
    },
    ...
  ]
}
```

##### Example

```json
{
  "managed_sessions": [
    {
      "id": 2,
      "vin": "1D4PT4GKXBW600841",
      "pin": "062309",
      "initialization": "2021-06-09 22:07:26.955043",
      "completion": "2021-06-09 22:07:39.099169",
      "verification_id": "c24gt2d8f41c9450911e7890"
    }
  ]
}
```

### Managed Session Get by VIN

Get managed session(s) by VIN

#### Route

{base_url}/managed-sessions/vehicles/{vin} GET

#### Parameters

##### vin

Vehicle VIN

#### Response

##### Format

```text
{
  "managed_sessions": [
    {
      "id": Integer,
      "vin": String,
      "pin": String,
      "initialization": UTC Timestamp,
      "completion": UTC Timestamp or String: "active",
      "verification_id": String
    },
    ...
  ]
}
```

##### Example

```json
{
  "managed_sessions": [
    {
      "id": 1,
      "vin": "1D4PT4GKXBW600841",
      "pin": "163063",
      "initialization": "2021-06-09 22:03:49.508408",
      "completion": "2021-06-09 22:06:56.232012",
      "verification_id": "c24gt2d8f41c9450911fu7897"
    },
    {
      "id": 2,
      "vin": "1D4PT4GKXBW600841",
      "pin": "062309",
      "initialization": "2021-06-09 22:07:26.955043",
      "completion": "2021-06-09 22:07:39.099169",
      "verification_id": "rftght2e8f40c94509dhuh89"
    },
    {
      "id": 3,
      "vin": "1D4PT4GKXBW600841",
      "pin": "633911",
      "initialization": "2021-06-09 22:07:39.113810",
      "completion": "active",
      "verification_id": "fd4gt2f6756905091112559"
    }
  ]
}
```

### Managed Session Telemetry Values Get

Retrieve managed session telemetry by id.

Telemetry points retrieved:

- Battery Management System State of Charge (bms_pack_soc)
- GPS Position
- Odometer
- Speed

#### Route

{base_url}/managed-sessions/{id}/telemetry GET

#### Parameters

##### id

Managed Session Id

#### Response

##### Format

```text
{
  vin: String,
  start: UTC Timestamp,
  end: UTC Timestamp,
  bms_pack_soc: [
    {
      "point": Float,
      "time": UTC Timestamp
    },
    ...
  ],
  gps_position: [
    {
      "latitude": Float,
      "longitude": Float,
      "altitude": Integer,
      "time": UTC Timestamp
    },
    ...
  ]
  odometer: [
    {
      "point": Float,
      "time": UTC Timestamp (initial)
    },
    {
      "point": Float,
      "time": UTC Timestamp (last)
    }
  ],
  speed: [
    {
      "point": Float,
      "time": UTC Timestamp
    },
    ...
  ]
}
```

##### Example

```json
{
  "vin": "7F7ATR319KER00009",
  "start": "2021-05-09 22:15:04.907120",
  "end": "2021-05-12 22:15:04.907120",
  "bms_pack_soc": [
    {
      "point": 80,
      "time": "2021-05-10T02:37:00Z"
    },
    {
      "point": 79.5,
      "time": "2021-05-10T05:54:00Z"
    },
    {
      "point": 79,
      "time": "2021-05-10T07:12:00Z"
    }
  ],
  "gps_position": [
    {
      "latitude": 44.0546,
      "longitude": -123.1118,
      "altitude": 12,
      "time": "2021-05-10T00:00:00Z"
    },
    {
      "latitude": 44.05462,
      "longitude": -123.1118,
      "altitude": 12,
      "time": "2021-05-10T00:01:00Z"
    },
    {
      "latitude": 44.0546,
      "longitude": -123.1118,
      "altitude": 12,
      "time": "2021-05-10T00:02:00Z"
    },
    {
      "latitude": 44.05459,
      "longitude": -123.1118,
      "altitude": 11,
      "time": "2021-05-10T00:03:00Z"
    }
  ],
  "odometer": [
    {
      "point": 8996.559,
      "time": "2021-05-10T15:48:00Z"
    },
    {
      "point": 9030.42,
      "time": "2021-05-12T20:33:00Z"
    }
  ],
  "speed": [
    {
      "point": 1.1,
      "time": "2021-05-10T15:48:00Z"
    },
    {
      "point": 0,
      "time": "2021-05-10T15:49:00Z"
    },
    {
      "point": 26.6,
      "time": "2021-05-10T15:55:00Z"
    },
    {
      "point": 0,
      "time": "2021-05-10T15:56:00Z"
    },
    {
      "point": 38.1,
      "time": "2021-05-10T16:03:00Z"
    },
    {
      "point": 82.3,
      "time": "2021-05-10T16:04:00Z"
    },
    {
      "point": 0,
      "time": "2021-05-10T16:05:00Z"
    }
  ]
}
```

### Managed Session Verify Drivers License

Verify Driver's license information

#### Route

{base_url}/managed-sessions/verify-dl POST

#### Parameters

##### first_name

customer first name

##### last_name

customer last name

##### email

customer email

##### drivers_license_number

customer USA driver's license number

##### state

customer USA driver's license number state

#### Response

##### Format

```text
{
  verified: Boolean,
  verification_id: String
}
```

##### Example

```json
{
  "verifified": true,
  "verification_id": "c24gt2d8f41c945091112566"
}
```

### Managed Session Start

Start managed session(s) for VIN

Note: Also ends any existing open managed sessions before starting the new one.

#### Route

{base_url}/managed-sessions/vehicles/{vin}/start POST

#### Parameters

##### vin

Vehicle VIN

#### Response

##### Format

```text
{
  vin: String,
  verification_id: String,
  id: Integer,
  pin: String
}
```

##### Example

```json
{
  "vin": "1D4PT4GKXBW600841",
  "verification_id": "c24gt2d8f41c945091112566",
  "id": 4,
  "pin": "017543"
}
```

### Managed Session End

End managed session(s) for VIN

#### Route

{base_url}/managed-sessions/vehicles/{vin}/end POST

#### Parameters

##### vin

Vehicle VIN

#### Response

##### Format

```text
{
  vin: String,
  verification_id: String,
  id: Integer,
  pin: String
}
```

##### Example

```json
{
  "vin": "1D4PT4GKXBW600841",
  "verification_id": "c24gt2d8f41c945091112566",
  "id": 4,
  "initialization": "2021-06-09 22:07:39.113810",
  "completion": "2021-06-11 14:05:21.234354"
}
```

### Managed Session Vehicle Synchronized

Check if vehicle is synchronized with latest managed session start/end input.
Allows detection of whether a vehicle is responsive to a PIN during a new active session or unrepsonsive to a PIN when a session is ended. Vehicles should synchronize automatically when in reasonable cell coverage situations and if out of coverage synchronize as soon as coverage is restored.

#### Route

{base_url}/managed-sessions/vehicles/{vin}/synchronized GET

#### Parameters

##### vin

Vehicle VIN

#### Response

##### Format

```text
{
  vehicle_synchronized: Boolean
}
```

##### Example

```json
{
  "vehicle_synchronized": true
}
```
