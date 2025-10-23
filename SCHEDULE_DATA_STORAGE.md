# Schedule Form Data Storage in MongoDB

This document explains how the schedule form data is stored in MongoDB for the AI Agent System.

## Overview

When a user submits their learning schedule through the schedule form, the data is stored in the `course_enrollments` collection in MongoDB. Each enrollment document contains the user's schedule preferences along with course and user identification information.

## Data Flow

1. User fills out the schedule form with their preferences
2. Form data is submitted to the `/course-agent/schedule/save` endpoint
3. The [save_schedule()](file:///d:/project%202/A_I-Agent-master/app.py#L273-L313) function in [app.py](file:///d:/project%202/A_I-Agent-master/app.py) processes the form data
4. The data is passed to the [select_course()](file:///d:/project%202/A_I-Agent-master/utils/course_controller.py#L32-L65) function in [course_controller.py](file:///d:/project%202/A_I-Agent-master/utils/course_controller.py)
5. A new document is created in the `course_enrollments` collection

## Form Fields and Storage Mapping

The following table shows how form fields map to database fields:

| Form Field | Database Field | Example Value |
|------------|----------------|---------------|
| `fullname` | `schedule.fullname` | "John Doe" |
| `whatsapp` | `schedule.whatsapp` | "+1234567890" |
| `duration` | `schedule.duration` | "30" |
| `preferred_time` | `schedule.preferred_time` | "10:00 AM" |
| `notification_method` | `schedule.notification_method` | "email" |

Additional system fields are also stored:

| Field | Value | Description |
|-------|-------|-------------|
| `frequency` | "daily" | Default lesson frequency |
| `pace` | "intermediate" | Default learning pace |

## Database Document Structure

Each enrollment document in the `course_enrollments` collection has the following structure:

```javascript
{
  "_id": ObjectId("..."),           // Auto-generated MongoDB ID
  "user_id": "user_id_string",      // Reference to user in usertable
  "course_id": "course_identifier", // Course ID (e.g., "python", "java")
  "course_name": "Course Name",     // Human-readable course name
  "schedule": {
    "fullname": "User Full Name",
    "whatsapp": "+1234567890",
    "duration": "30",
    "preferred_time": "10:00 AM",
    "notification_method": "email",
    "frequency": "daily",
    "pace": "intermediate"
  },
  "status": "active"                // Enrollment status
}
```

## Example Database Document

```javascript
{
  "_id": ObjectId("68e5163fef8bfd666eca5332"),
  "user_id": "68e5163fef8bfd666eca5332",
  "course_id": "java",
  "course_name": "Java Development",
  "schedule": {
    "fullname": "Lokesh Mannuru",
    "whatsapp": "+91 8143761305",
    "duration": "30",
    "preferred_time": "10:00 AM",
    "notification_method": "email",
    "frequency": "daily",
    "pace": "intermediate"
  },
  "status": "active"
}
```

## Verification

The data storage has been verified through testing:

1. All form fields are correctly captured and stored
2. The data structure matches the expected format
3. MongoDB indexes support efficient querying
4. Data integrity is maintained

## Querying Schedule Data

To retrieve a user's schedule data:

```javascript
// Find all enrollments for a specific user
db.course_enrollments.find({ "user_id": "user_id_here" })

// Find a specific course enrollment
db.course_enrollments.findOne({ 
  "user_id": "user_id_here", 
  "course_id": "java" 
})
```

## Data Security

- User identification is done through `user_id` references
- No sensitive data (passwords) is stored in the enrollments collection
- All data is stored in the configured MongoDB database