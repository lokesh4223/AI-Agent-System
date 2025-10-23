# MongoDB Schema for AI Agent System

This document describes the MongoDB schema used in the AI Agent System.

## Database: `ai_agent_system`

### Collection: `usertable`

This collection stores user information for the AI Agent System.

#### Document Structure

```javascript
{
  "_id": ObjectId,           // MongoDB auto-generated ID
  "name": String,            // User's full name
  "email": String,           // User's email address (unique)
  "password": String,        // Hashed password
  "code": Number,            // Verification code (used for email verification and password reset)
  "status": String           // Account status ("verified" or "notverified")
}
```

#### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | MongoDB auto-generated unique identifier |
| `name` | String | User's full name |
| `email` | String | User's email address (must be unique) |
| `password` | String | User's hashed password (using Werkzeug) |
| `code` | Number | Verification code used for:
  - Email verification during signup (6-digit random number)
  - Password reset process (6-digit random number)
  - Set to 0 when code is used or expired |
| `status` | String | Account verification status:
  - "notverified" - Account created but email not verified
  - "verified" - Email verified, account fully active |

#### Indexes

```javascript
// Unique index on email field
db.usertable.createIndex({ "email": 1 }, { unique: true })

// Index on code field for faster lookups
db.usertable.createIndex({ "code": 1 })
```

#### Example Document

```javascript
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "pbkdf2:sha256:260000$abc123$def456...",
  "code": 123456,
  "status": "notverified"
}
```

#### Common Queries

1. **Find user by email**:
   ```javascript
   db.usertable.findOne({ "email": "user@example.com" })
   ```

2. **Find user by verification code**:
   ```javascript
   db.usertable.findOne({ "code": 123456 })
   ```

3. **Update user status after email verification**:
   ```javascript
   db.usertable.updateOne(
     { "code": 123456 },
     { $set: { "code": 0, "status": "verified" } }
   )
   ```

4. **Update user password**:
   ```javascript
   db.usertable.updateOne(
     { "email": "user@example.com" },
     { $set: { "code": 0, "password": "new_hashed_password" } }
   )
   ```

5. **Update verification code for password reset**:
   ```javascript
   db.usertable.updateOne(
     { "email": "user@example.com" },
     { $set: { "code": 654321 } }
   )
   ```

### Collection: `course_enrollments`

This collection stores course enrollment information and user schedule preferences.

#### Document Structure

```javascript
{
  "_id": ObjectId,              // MongoDB auto-generated ID
  "user_id": String,            // Reference to user ID from usertable
  "course_id": String,          // Course identifier
  "course_name": String,        // Human-readable course name
  "schedule": Object,           // User's schedule preferences
  "status": String              // Enrollment status ("active", etc.)
}
```

#### Schedule Object Structure

The `schedule` field contains user preferences for their learning schedule:

```javascript
{
  "fullname": String,              // User's full name for certificate
  "whatsapp": String,              // WhatsApp number with country code
  "duration": String,              // Learning duration in days
  "preferred_time": String,        // Preferred time for lessons
  "notification_method": String,   // How to receive notifications ("email", "whatsapp", "both")
  "frequency": String,             // Lesson frequency ("daily", etc.)
  "pace": String                   // Learning pace ("beginner", "intermediate", etc.)
}
```

#### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | MongoDB auto-generated unique identifier |
| `user_id` | String | Reference to the user's ID in the usertable collection |
| `course_id` | String | Identifier for the course (e.g., "python", "java") |
| `course_name` | String | Human-readable name of the course |
| `schedule` | Object | Object containing all user schedule preferences |
| `status` | String | Enrollment status (currently "active") |

#### Example Document

```javascript
{
  "_id": ObjectId("507f1f77bcf86cd799439012"),
  "user_id": "68e5163fef8bfd666eca5332",
  "course_id": "java",
  "course_name": "Java Development",
  "schedule": {
    "fullname": "John Doe",
    "whatsapp": "+1234567890",
    "duration": "30",
    "preferred_time": "10:00 AM",
    "notification_method": "email",
    "frequency": "daily",
    "pace": "intermediate"
  },
  "status": "active"
}
```

#### Common Queries

1. **Find all enrollments for a user**:
   ```javascript
   db.course_enrollments.find({ "user_id": "user_id_here" })
   ```

2. **Find specific course enrollment for a user**:
   ```javascript
   db.course_enrollments.findOne({ "user_id": "user_id_here", "course_id": "java" })
   ```

3. **Update schedule for a course enrollment**:
   ```javascript
   db.course_enrollments.updateOne(
     { "user_id": "user_id_here", "course_id": "java" },
     { $set: { "schedule": { /* new schedule object */ } } }
   )
   ```