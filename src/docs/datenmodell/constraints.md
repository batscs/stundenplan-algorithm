# Datenmodell

## Constraints

#### EmployeeFreeTimeslots

Employee darf keine Events zu den timeslots haben

```json
{
  "id": "string",
  "type": "EmployeeFreeTimeslots",
  "owner": "string",
  "inverted": boolean // ignored
  "fields": {
    "timeslots": [
      {"day":  integer, "timeslot":  integer}
    ]
  }
}
```

#### EmployeeSubsequentTimeslots

Employee darf nicht mehr als *limit* Veranstaltungen hintereinander haben

```json
{
  "id": "string",
  "type": "EmployeeSubsequentTimeslots",
  "owner": "string",
  "inverted": boolean // ignored
  "fields": {
    "limit": integer
  }
}
```

#### EventDistributeWeeklyBlocks

Inverted: False -> Alle Events mit dem übergebenen Namen/Id müssen an verschiedenen Tagen stattfinden  
Inverted: True -> Alle Events mit dem übergebenen Namen/Id müssen am gleichen Tag stattfinden

```json
{
  "id": "string",
  "type": "EmployeeSubsequentTimeslots",
  "owner": "string",
  "inverted": boolean
  "fields": {
    "event": "string"
  }
}
```