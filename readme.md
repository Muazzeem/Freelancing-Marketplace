# Freelancing Marketplace API

## Features

- User registration and authentication using JWT tokens
- Job CRUD operations with permissions
- Role-based access control (Client, Freelancer, Admin)
- Optimized database queries
- Docker containerization

# Running the Application with Docker Compose

To run this application using Docker Compose, follow these steps:

1. Make sure you have Docker and Docker Compose installed on your machine
   - [Install Docker](https://docs.docker.com/get-docker/)
   - Docker Compose is included with Docker Desktop for Windows and macOS

2. Clone the repository and navigate to the project directory containing the `compose.yaml` file

3. Build and start the containers:
   ```bash
   # Build and start in detached mode
   docker compose up -d
   
   # View logs
   docker compose logs -f
   
   # Stop containers when done
   docker compose down
   ```


## API Endpoints

### Authentication Endpoints

#### Register User
- **URL**: `/api/auth/register/`
- **Method**: `POST`
- **Description**: Register a new user account

Note: Default role is **Client**

Request Body for Client:
```json
{
    "role":"Client",
    "email":"example@example.com",
    "username":"muazzemclient",
    "password":"user123"
}
```
Response:
```json
{
    "id": 1,
    "role": "Client",
    "email": "example@example.com",
    "username": "muazzemclient",
    "password": "user123"
}
```

Request Body for Freelancer:
```json
{
    "role":"Freelancer",
    "email":"example@example.com",
    "username":"muazzemfreelancer",
    "password":"user123"
}
```
Response:
```json
{
    "id": 1,
    "role": "Freelancer",
    "email": "example@example.com",
    "username": "muazzemfreelancer",
    "password": "user123"
}
```

Request Body for Admin:
```json
{
    "role":"Admin",
    "email":"example@example.com",
    "username":"admin",
    "password":"user123"
}
```
Response:
```json
{
    "id": 1,
    "role": "Admin",
    "email": "example@example.com",
    "username": "admin",
    "password": "user123"
}
```

#### Login Endpoint

- **URL**: `/api/auth/login/`
- **Method**: `POST`
- **Description**: Login a user account

Request Body:
```json
{
    "username":"muazzem",
    "password":"user123"
}
```
Response:
  ```json
{
      "token": "eyJhbGciOiJIUzI1...",
      "access": "eyJhbGciOiJIUzI1..."
}
```

### User Role Endpoints:

#### Get User

- **URL**: `/api/users/<int:user_id>`
- **Method**: `GET`
- **Description**: Get user details
- **Authentication**: Only required for Admin

Response:
  ```json
{
    "id": 4,
    "role": "Client",
    "email": "muazzem@mamun.com",
    "username": "muazzemfreelancer"
}
```


#### Update User Details

- **URL**: `/api/users/<int:user_id>`
- **Method**: `PUT`
- **Description**: Update user details
- **Authentication**: Only required for Admin

Note: Only the `role` and `email` field can be updated.

Request Body:

```json
{
    "id": 4,
    "role": "Admin",
    "email": "muazzem@mamun.com",
    "username": "muazzemfreelancer"
}
```

Response:
  ```json
{
    "id": 4,
    "role": "Admin",
    "email": "muazzem@mamun.com",
    "username": "muazzemfreelancer"
}
```


### Job Endpoints

#### List All Jobs
- **URL**: api/jobs
- **Method**: GET
- **Description**: Fetch a list of all available jobs .
- **Authentication**: Not required

Response
```json
[
  {
    "id": 1,
    "title": "Software Engineer",
    "description": "Develop and maintain software systems.",
    "created_at": "2025-01-07T12:15:28.203270+06:00"
  },
  {
    "id": 2,
    "title": "Data Analyst",
    "description": "Analyze and interpret data.",
    "created_at": "2025-01-07T12:15:30.203270+06:00"
  }
]
```

#### Get a Job by ID
- **URL**: api/jobs/<int:job_id>
- **Method**: GET
- **Description**: Fetch a job by ID.
- **Authentication**: Not required

Response
```json
[
  {
    "id": 1,
    "title": "Software Engineer",
    "description": "Develop and maintain software systems.",
    "created_at": "2025-01-07T12:15:28.203270+06:00"
  }
]
```

### Create a New Job
- **URL:** api/jobs
- **Method:** POST
- **Authentication:** Required (JWT)
- **Permission:** Client

Request Body:

```json
{
  "title": "Backend Developer",
  "description": "Develop and maintain APIs."
} 
```
Response:
  ```json
  {
    "id": 3,
    "title": "Backend Developer",
    "description": "Develop and maintain APIs.",
    "created_by": "client123"
  }
  ```

#### Update a Job
- **URL:** api/jobs/<int:job_id>
- **Method:** PUT
- **Authentication:** Required (JWT)
- **Permission:** Client

Request Body:
```json
{
  "id": 3,
  "title": "Senior Backend Developer",
  "description": "Lead the development of APIs."
}
```
Response:
```json
{
  "id": 3,
  "title": "Senior Backend Developer",
  "description": "Lead the development of APIs.",
  "created_by": "client123"
}
```

#### Delete a Job
- **URL:** api/jobs/<int:job_id>
- **Method:** DELETE
- **Authentication:** Required (JWT)
- **Permission:** Client or Admin
- **Response:**
```json
{
  "message": "Job deleted successfully"
}
```
Error:
```json
{
  "error": "You can only delete your own jobs"
}
```
## Notes
- Authentication Headers: For endpoints requiring authentication, include the access token in the Authorization header:

Authorization: Bearer <access_token>

- Roles:
  - Client: Can create, update, and delete their own jobs.
  - Admin and Client: Can delete any job.




