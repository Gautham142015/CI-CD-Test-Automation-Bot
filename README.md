Inputs:

A CSV with natural language inputs describing API test cases.

A Postman collection or Swagger/OpenAPI JSON (for API schema).

Process:

Use GPT API to translate natural language test descriptions into API requests.

Execute the requests against the API (using requests or Postman runtime).

Capture the outputs (status code, response body) + errors.

Outputs:

Write results into a CSV with columns like:
Test ID | Input | Endpoint | Method | Request Body | Response Code | Response Body | Error
