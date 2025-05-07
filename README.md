# HireLink API Documentation

## Authentication
All API endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Education APIs

### List All Education Records
```http
GET /api/educations/
```

**Response (200 OK)**
```json
[
    {
        "id": 1,
        "education_type": "bachelors",
        "school_name": "University of Example",
        "degree": "Bachelor of Science",
        "field_of_study": "Computer Science",
        "start_date": "2018-09-01",
        "end_date": "2022-05-15",
        "grade": "3.8",
        "created_at": "2024-03-06T10:00:00Z",
        "updated_at": "2024-03-06T10:00:00Z"
    },
    {
        "id": 2,
        "education_type": "masters",
        "school_name": "Tech University",
        "degree": "Master of Science",
        "field_of_study": "Software Engineering",
        "start_date": "2022-09-01",
        "end_date": "2024-05-15",
        "grade": "3.9",
        "created_at": "2024-03-06T10:05:00Z",
        "updated_at": "2024-03-06T10:05:00Z"
    }
]
```

### Create Education Record
```http
POST /api/educations/
```

**Request Body**
```json
{
    "education_type": "bachelors",
    "school_name": "University of Example",
    "degree": "Bachelor of Science",
    "field_of_study": "Computer Science",
    "start_date": "2018-09-01",
    "end_date": "2022-05-15",
    "grade": "3.8"
}
```

**Response (201 Created)**
```json
{
    "id": 1,
    "education_type": "bachelors",
    "school_name": "University of Example",
    "degree": "Bachelor of Science",
    "field_of_study": "Computer Science",
    "start_date": "2018-09-01",
    "end_date": "2022-05-15",
    "grade": "3.8",
    "created_at": "2024-03-06T10:00:00Z",
    "updated_at": "2024-03-06T10:00:00Z"
}
```

### Get Specific Education Record
```http
GET /api/educations/{id}/
```

**Response (200 OK)**
```json
{
    "id": 1,
    "education_type": "bachelors",
    "school_name": "University of Example",
    "degree": "Bachelor of Science",
    "field_of_study": "Computer Science",
    "start_date": "2018-09-01",
    "end_date": "2022-05-15",
    "grade": "3.8",
    "created_at": "2024-03-06T10:00:00Z",
    "updated_at": "2024-03-06T10:00:00Z"
}
```

### Update Education Record
```http
PATCH /api/educations/{id}/
```

**Request Body**
```json
{
    "grade": "3.9",
    "end_date": "2022-06-15"
}
```

**Response (200 OK)**
```json
{
    "id": 1,
    "education_type": "bachelors",
    "school_name": "University of Example",
    "degree": "Bachelor of Science",
    "field_of_study": "Computer Science",
    "start_date": "2018-09-01",
    "end_date": "2022-06-15",
    "grade": "3.9",
    "created_at": "2024-03-06T10:00:00Z",
    "updated_at": "2024-03-06T10:30:00Z"
}
```

### Delete Education Record
```http
DELETE /api/educations/{id}/
```

**Response (204 No Content)**

## Experience APIs

### List All Experience Records
```http
GET /api/experiences/
```

**Response (200 OK)**
```json
[
    {
        "id": 1,
        "company_name": "Tech Corp",
        "designation": "Software Engineer",
        "job_type": "Full-time",
        "location": "New York",
        "currently_working": true,
        "job_description": "Developed and maintained web applications",
        "start_date": "2022-06-01",
        "end_date": null,
        "created_at": "2024-03-06T10:00:00Z",
        "updated_at": "2024-03-06T10:00:00Z"
    },
    {
        "id": 2,
        "company_name": "StartUp Inc",
        "designation": "Junior Developer",
        "job_type": "Full-time",
        "location": "San Francisco",
        "currently_working": false,
        "job_description": "Worked on frontend development",
        "start_date": "2021-01-01",
        "end_date": "2022-05-31",
        "created_at": "2024-03-06T10:05:00Z",
        "updated_at": "2024-03-06T10:05:00Z"
    }
]
```

### Create Experience Record
```http
POST /api/experiences/
```

**Request Body**
```json
{
    "company_name": "Tech Corp",
    "designation": "Software Engineer",
    "job_type": "Full-time",
    "location": "New York",
    "currently_working": true,
    "job_description": "Developed and maintained web applications",
    "start_date": "2022-06-01",
    "end_date": null
}
```

**Response (201 Created)**
```json
{
    "id": 1,
    "company_name": "Tech Corp",
    "designation": "Software Engineer",
    "job_type": "Full-time",
    "location": "New York",
    "currently_working": true,
    "job_description": "Developed and maintained web applications",
    "start_date": "2022-06-01",
    "end_date": null,
    "created_at": "2024-03-06T10:00:00Z",
    "updated_at": "2024-03-06T10:00:00Z"
}
```

### Get Specific Experience Record
```http
GET /api/experiences/{id}/
```

**Response (200 OK)**
```json
{
    "id": 1,
    "company_name": "Tech Corp",
    "designation": "Software Engineer",
    "job_type": "Full-time",
    "location": "New York",
    "currently_working": true,
    "job_description": "Developed and maintained web applications",
    "start_date": "2022-06-01",
    "end_date": null,
    "created_at": "2024-03-06T10:00:00Z",
    "updated_at": "2024-03-06T10:00:00Z"
}
```

### Update Experience Record
```http
PATCH /api/experiences/{id}/
```

**Request Body**
```json
{
    "designation": "Senior Software Engineer",
    "job_description": "Lead developer for web applications"
}
```

**Response (200 OK)**
```json
{
    "id": 1,
    "company_name": "Tech Corp",
    "designation": "Senior Software Engineer",
    "job_type": "Full-time",
    "location": "New York",
    "currently_working": true,
    "job_description": "Lead developer for web applications",
    "start_date": "2022-06-01",
    "end_date": null,
    "created_at": "2024-03-06T10:00:00Z",
    "updated_at": "2024-03-06T10:30:00Z"
}
```

### Delete Experience Record
```http
DELETE /api/experiences/{id}/
```

**Response (204 No Content)**

## Field Descriptions

### Education Fields
- `education_type`: One of ['primary', 'secondary', 'higher_secondary', 'bachelors', 'masters', 'phd', 'other']
- `school_name`: Name of the educational institution
- `degree`: Degree or qualification earned
- `field_of_study`: Major or specialization
- `start_date`: Start date of education (YYYY-MM-DD)
- `end_date`: End date of education (YYYY-MM-DD)
- `grade`: Grade or GPA achieved

### Experience Fields
- `company_name`: Name of the company
- `designation`: Job title or position
- `job_type`: Type of employment (e.g., 'Full-time', 'Part-time', 'Contract')
- `location`: Work location
- `currently_working`: Boolean indicating if currently employed
- `job_description`: Description of responsibilities and achievements
- `start_date`: Start date of employment (YYYY-MM-DD)
- `end_date`: End date of employment (YYYY-MM-DD), null if currently working

## Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid data provided"
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Postman Collection

You can import the following collection into Postman:

```json
{
  "info": {
    "name": "HireLink API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Education",
      "item": [
        {
          "name": "List Education",
          "request": {
            "method": "GET",
            "url": "{{base_url}}/api/educations/",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ]
          }
        },
        {
          "name": "Create Education",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/api/educations/",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              },
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n    \"education_type\": \"bachelors\",\n    \"school_name\": \"University of Example\",\n    \"degree\": \"Bachelor of Science\",\n    \"field_of_study\": \"Computer Science\",\n    \"start_date\": \"2018-09-01\",\n    \"end_date\": \"2022-05-15\",\n    \"grade\": \"3.8\"\n}"
            }
          }
        },
        {
          "name": "Get Education",
          "request": {
            "method": "GET",
            "url": "{{base_url}}/api/educations/{{education_id}}/",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ]
          }
        },
        {
          "name": "Update Education",
          "request": {
            "method": "PATCH",
            "url": "{{base_url}}/api/educations/{{education_id}}/",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              },
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n    \"grade\": \"3.9\",\n    \"end_date\": \"2022-06-15\"\n}"
            }
          }
        },
        {
          "name": "Delete Education",
          "request": {
            "method": "DELETE",
            "url": "{{base_url}}/api/educations/{{education_id}}/",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ]
          }
        }
      ]
    },
    {
      "name": "Experience",
      "item": [
        {
          "name": "List Experience",
          "request": {
            "method": "GET",
            "url": "{{base_url}}/api/experiences/",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ]
          }
        },
        {
          "name": "Create Experience",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/api/experiences/",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              },
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n    \"company_name\": \"Tech Corp\",\n    \"designation\": \"Software Engineer\",\n    \"job_type\": \"Full-time\",\n    \"location\": \"New York\",\n    \"currently_working\": true,\n    \"job_description\": \"Developed and maintained web applications\",\n    \"start_date\": \"2022-06-01\",\n    \"end_date\": null\n}"
            }
          }
        },
        {
          "name": "Get Experience",
          "request": {
            "method": "GET",
            "url": "{{base_url}}/api/experiences/{{experience_id}}/",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ]
          }
        },
        {
          "name": "Update Experience",
          "request": {
            "method": "PATCH",
            "url": "{{base_url}}/api/experiences/{{experience_id}}/",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              },
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n    \"designation\": \"Senior Software Engineer\",\n    \"job_description\": \"Lead developer for web applications\"\n}"
            }
          }
        },
        {
          "name": "Delete Experience",
          "request": {
            "method": "DELETE",
            "url": "{{base_url}}/api/experiences/{{experience_id}}/",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ]
          }
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "type": "string"
    },
    {
      "key": "token",
      "value": "your_jwt_token_here",
      "type": "string"
    },
    {
      "key": "education_id",
      "value": "1",
      "type": "string"
    },
    {
      "key": "experience_id",
      "value": "1",
      "type": "string"
    }
  ]
}
```

To use this collection:
1. Import it into Postman
2. Create an environment with variables:
   - `base_url`: Your API base URL (e.g., http://localhost:8000)
   - `token`: Your JWT token
   - `education_id`: ID of an education record (for testing GET/PATCH/DELETE)
   - `experience_id`: ID of an experience record (for testing GET/PATCH/DELETE)
3. Make sure to authenticate first to get a valid token
4. All endpoints now include trailing slashes to avoid Django's APPEND_SLASH issues

Example workflow:
1. Create a new education record using the "Create Education" request
2. Copy the returned ID to the `education_id` environment variable
3. Use the "Get Education" request to verify the creation
4. Use the "Update Education" request to modify the record
5. Use the "Delete Education" request to remove the record

The same workflow applies to experience records.