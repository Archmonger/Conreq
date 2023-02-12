By default, API endpoints require a user token (typically fetched from the `api/v1/api/user-token` endpoint) and additionally an API key.

User tokens must be provided via `Authorization` header like such: `Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`

The API key must be provided via the `Authorization` header like such: `Authorization: Api-Key 10Q5p9Lr.0Qp9twA07Ve5U7mZJvDgfOuUItdoPV7O`. They can optionally be URL encoded like this: `api/v1/demo-api?apikey=10Q5p9Lr.0Qp9twA07Ve5U7mZJvDgfOuUItdoPV7O`
