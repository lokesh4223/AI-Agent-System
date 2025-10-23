# AI Agent System - API Specifications

## Overview

This document describes the RESTful API endpoints for the AI Agent System. All endpoints are served by the Flask application and follow REST conventions.

## Base URL

```
http://localhost:5000/api/v1
```

*Note: Currently, the application does not have a dedicated API prefix. Endpoints are served directly from the root.*

## Authentication

Most endpoints require authentication via session cookies. Users must be logged in to access protected resources.

### Session Management

- Session cookies are automatically managed by the browser
- Sessions expire after a period of inactivity
- Users can log out to invalidate their session

## API Endpoints

### User Authentication

#### Register User
```
POST /signup-user
```

**Request Body:**
```json
{
  "name": "string",
  "email": "string",
  "password": "string",
  "cpassword": "string"
}
```

**Response:**
- 302 Redirect to `/user-otp` on success
- 200 with error messages on failure

**Description:** Registers a new user account and sends verification email.

#### Login User
```
POST /login-user
```

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
- 302 Redirect to `/home` on successful login
- 302 Redirect to `/user-otp` if email verification needed
- 200 with error messages on failure

**Description:** Authenticates a user and creates a session.

#### Logout User
```
GET /logout-user
```

**Response:**
- 302 Redirect to `/`

**Description:** Destroys the user session and logs them out.

#### Verify Email OTP
```
POST /user-otp
```

**Request Body:**
```json
{
  "otp": "string"
}
```

**Response:**
- 302 Redirect to `/home` on success
- 200 with error messages on failure

**Description:** Verifies the email verification code sent during registration.

#### Forgot Password
```
POST /forgot-password
```

**Request Body:**
```json
{
  "email": "string"
}
```

**Response:**
- 302 Redirect to `/reset-code` on success
- 200 with error messages on failure

**Description:** Initiates the password reset process by sending a code to the user's email.

#### Verify Password Reset Code
```
POST /reset-code
```

**Request Body:**
```json
{
  "otp": "string"
}
```

**Response:**
- 302 Redirect to `/new-password` on success
- 200 with error messages on failure

**Description:** Verifies the password reset code sent to the user's email.

#### Set New Password
```
POST /new-password
```

**Request Body:**
```json
{
  "password": "string",
  "cpassword": "string"
}
```

**Response:**
- 302 Redirect to `/password-changed` on success
- 200 with error messages on failure

**Description:** Sets a new password for the user account.

### User Profile

#### Get User Profile
```
GET /profile
```

**Response:**
- 200 with profile page HTML
- 302 Redirect to `/login-user` if not authenticated

**Description:** Displays the authenticated user's profile information.

### Course Management

#### Get Course Agent Page
```
GET /course-agent
```

**Response:**
- 200 with course agent page HTML
- 302 Redirect to `/login-user` if not authenticated

**Description:** Displays the course agent selection page.

#### Get Course Schedule Configuration
```
GET /course-agent/schedule/{course_id}
```

**Path Parameters:**
- `course_id`: Identifier for the course (e.g., "python", "java")

**Response:**
- 200 with schedule configuration page HTML
- 302 Redirect to `/login-user` if not authenticated

**Description:** Displays the schedule configuration form for a specific course.

#### Save Course Schedule
```
POST /course-agent/schedule/save
```

**Request Body:**
```json
{
  "course_id": "string",
  "fullname": "string",
  "whatsapp": "string",
  "duration": "string",
  "preferred_time": "string",
  "notification_method": "string"
}
```

**Response:**
- 302 Redirect to `/course-agent/success` on success
- 302 Redirect to `/course-agent` on failure

**Description:** Saves the user's course schedule preferences.

#### Select Course
```
POST /select-course
```

**Request Body:**
```json
{
  "course_id": "string"
}
```

**Response:**
- 302 Redirect to `/course-agent/schedule/{course_id}`

**Description:** Redirects to the schedule configuration page for the selected course.

#### Course Enrollment Success
```
GET /course-agent/success
```

**Response:**
- 200 with success page HTML
- 302 Redirect to `/login-user` if not authenticated

**Description:** Displays a success message after course enrollment.

### Public Pages

#### Home Page
```
GET /
```

**Response:**
- 200 with landing page HTML

**Description:** Displays the main landing page.

#### Authenticated Home Page
```
GET /home
```

**Response:**
- 200 with dashboard page HTML
- 302 Redirect to `/login-user` if not authenticated

**Description:** Displays the authenticated user's dashboard.

## Error Responses

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 302 | Redirect |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

### Error Format

Errors are typically returned as HTML pages with user-friendly messages. For API endpoints (future enhancement), errors would follow this format:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "string"
  }
}
```

## Request/Response Examples

### User Registration
**Request:**
```http
POST /signup-user HTTP/1.1
Content-Type: application/x-www-form-urlencoded

name=John+Doe&email=john@example.com&password=secret123&cpassword=secret123
```

**Response:**
```http
HTTP/1.1 302 Found
Location: /user-otp
Set-Cookie: session=abc123; Path=/
```

### User Login
**Request:**
```http
POST /login-user HTTP/1.1
Content-Type: application/x-www-form-urlencoded

email=john@example.com&password=secret123
```

**Response:**
```http
HTTP/1.1 302 Found
Location: /home
Set-Cookie: session=def456; Path=/
```

### Course Enrollment
**Request:**
```http
POST /course-agent/schedule/save HTTP/1.1
Content-Type: application/x-www-form-urlencoded

course_id=python&fullname=John+Doe&whatsapp=%2B1234567890&duration=30&preferred_time=10%3A00+AM&notification_method=email
```

**Response:**
```http
HTTP/1.1 302 Found
Location: /course-agent/success
```

## Rate Limiting

Currently, the application does not implement rate limiting. For production deployment, consider implementing:

- Login attempt throttling
- Email sending rate limits
- API request rate limiting

## CORS Policy

The application serves HTML pages directly and does not currently implement a CORS policy. For API endpoints, CORS headers would need to be configured.

## Versioning

The API does not currently implement versioning. Future versions should use URL versioning:

```
/v1/users
/v2/users
```

## Future API Enhancements

### RESTful JSON API
Planned enhancements include a dedicated JSON API:

#### Get User Information
```
GET /api/v1/users/me
```

#### Get Course Enrollments
```
GET /api/v1/users/me/enrollments
```

#### Create Course Enrollment
```
POST /api/v1/users/me/enrollments
```

### Webhook Endpoints
For integration with external services:

#### Course Completion Notification
```
POST /api/v1/webhooks/course-completed
```

#### User Activity Tracking
```
POST /api/v1/webhooks/user-activity
```