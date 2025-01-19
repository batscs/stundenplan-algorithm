# Datenmodell

## Datenbasis für zu generierenden Stundenplan

#### Stundenplan

```json
{
  "metadata": metadata,
  "rooms": [room],
  "events": [event],
  "constraints": {
    "hard": [constraint],
    "soft": [constraint]
  }
}
```

#### Room 
```json
{
  "name": "string",
  "capacity": 0,
  "room_type": "string"
}
```

#### Event
```json
{
  "name": "string",
  "employees": ["string"],
  "participants": ["string"],
  "room_type": "string",
  "size": 0,
  "weekly_blocks": 0
}
```

#### Constraint
```json
{
  "id": "string",
  "type": "string",
  "owner": "string",
  "inverted": false,
  "fields": { ... }
}
```

#### Metadata
```json
{
  "days": 0,
  "timeslots": 0
}
```
