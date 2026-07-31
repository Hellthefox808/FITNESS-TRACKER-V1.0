# API Reference Specification

> **Fitness Tracker Using Machine Learning (FitAI)**  
> *Author & Lead Architect: **Ravi Ranjan Singh***

---

## 1. Overview & Protocol Specification

The **Fitness Tracker Using Machine Learning** application provides a production-ready RESTful API and bi-directional WebSockets API for user management, exercise session logging, real-time machine learning predictions, and analytics retrieval.

- **Base URL (Local)**: `http://localhost:8000/api/v1`
- **WebSocket URL (Local)**: `ws://localhost:8000/ws/v1`
- **Protocol**: HTTPS / WSS
- **Content Type**: `application/json`
- **Specification**: OpenAPI 3.0 (Interactive Swagger UI available at `/docs`)

---

## 2. Authentication Protocol

All protected API endpoints require an HTTP `Authorization` header containing a valid Bearer JSON Web Token (JWT):

```http
Authorization: Bearer <YOUR_JWT_ACCESS_TOKEN>
```

### Authentication Error Responses
If a request lacks a valid token or uses an expired token, the API returns:

```json
{
  "status_code": 401,
  "error_code": "UNAUTHORIZED",
  "message": "Could not validate credentials or token expired.",
  "timestamp": "2026-08-01T01:20:30Z"
}
```

---

## 3. Endpoints Matrix

### 3.1 Authentication Routes

#### `POST /auth/register`
Register a new user account with initial physiological parameters.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "Jane Doe",
  "age": 28,
  "gender": "female",
  "height_cm": 168.0,
  "weight_kg": 62.5
}
```

**Response (201 Created)**:
```json
{
  "status": "success",
  "message": "User account created successfully.",
  "data": {
    "user_id": "usr_98a72f1b-4c01-4b11-9a7e-123456789abc",
    "email": "user@example.com",
    "full_name": "Jane Doe",
    "created_at": "2026-08-01T01:20:30Z"
  }
}
```

---

#### `POST /auth/login`
Authenticate user credentials and return access + refresh tokens.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "d98a72f1b4c014b119a7e123456789abc...",
  "token_type": "bearer",
  "expires_in": 900
}
```

---

### 3.2 Machine Learning Inference Routes

#### `POST /predict/calories`
Execute high-precision ML calorie burn prediction for a given workout parameter vector.

**Headers**: `Authorization: Bearer <TOKEN>`

**Request Body**:
```json
{
  "age": 28,
  "gender": "male",
  "height_cm": 178.0,
  "weight_kg": 75.5,
  "duration_min": 45.0,
  "heart_rate_bpm": 154.0,
  "body_temp_c": 38.1
}
```

**Response (200 OK)**:
```json
{
  "status": "success",
  "data": {
    "predicted_calories_burned": 482.65,
    "unit": "kcal",
    "confidence_interval_95": {
      "lower": 465.10,
      "upper": 500.20
    },
    "derived_metrics": {
      "bmi": 23.83,
      "heart_rate_ratio": 0.802,
      "intensity_zone": "Anaerobic (Zone 4)"
    },
    "model_metadata": {
      "model_name": "XGBoost_Calorie_Regressor",
      "model_version": "v1.0.0",
      "inference_time_ms": 11.4
    }
  },
  "timestamp": "2026-08-01T01:20:30Z"
}
```

---

#### `POST /predict/activity`
Classify physical activity category from raw sensor timeseries data.

**Request Body**:
```json
{
  "sensor_readings": [
    {"accel_x": 0.12, "accel_y": 0.85, "accel_z": 9.78, "gyro_x": 0.01, "gyro_y": 0.05, "gyro_z": -0.02},
    {"accel_x": 0.45, "accel_y": 1.20, "accel_z": 10.12, "gyro_x": 0.04, "gyro_y": 0.08, "gyro_z": 0.01}
  ]
}
```

**Response (200 OK)**:
```json
{
  "status": "success",
  "data": {
    "predicted_activity": "Running",
    "confidence_score": 0.964,
    "class_probabilities": {
      "Running": 0.964,
      "Walking": 0.021,
      "Cycling": 0.010,
      "HIIT": 0.005
    }
  }
}
```

---

### 3.3 Workout Session Routes

#### `POST /workouts`
Log a completed workout session with detailed telemetry.

**Request Body**:
```json
{
  "activity_type": "Running",
  "duration_min": 45.0,
  "avg_heart_rate_bpm": 154.0,
  "max_heart_rate_bpm": 172.0,
  "calories_burned": 482.65,
  "notes": "Morning outdoor run in the park."
}
```

**Response (201 Created)**:
```json
{
  "status": "success",
  "data": {
    "workout_id": "wrk_12345678-aaaa-bbbb-cccc-123456789def",
    "logged_at": "2026-08-01T01:20:30Z"
  }
}
```

---

#### `GET /workouts`
Retrieve paginated workout history for the authenticated user.

**Query Parameters**:
- `page` (optional, default: `1`)
- `limit` (optional, default: `20`)

**Response (200 OK)**:
```json
{
  "status": "success",
  "pagination": {
    "total_records": 42,
    "page": 1,
    "limit": 20,
    "total_pages": 3
  },
  "data": [
    {
      "workout_id": "wrk_12345678-aaaa-bbbb-cccc-123456789def",
      "activity_type": "Running",
      "duration_min": 45.0,
      "calories_burned": 482.65,
      "logged_at": "2026-08-01T01:20:30Z"
    }
  ]
}
```

---

### 3.4 Real-Time WebSockets Telemetry Endpoint

#### `WS /ws/v1/telemetry`
Establish bi-directional WSS streaming connection for live sensor streaming.

**Connection Protocol**:
1. Client connects to `ws://localhost:8000/ws/v1/telemetry?token=<JWT_ACCESS_TOKEN>`.
2. Server validates token and sends connection acknowledgment:
   ```json
   {"event": "CONNECTED", "session_id": "wss_991823719823"}
   ```
3. Client streams 1 Hz biometric frames:
   ```json
   {"event": "TELEMETRY_FRAME", "heart_rate_bpm": 155.0, "body_temp_c": 38.1}
   ```
4. Server responds instantly with calculated burn velocity:
   ```json
   {"event": "BURN_VELOCITY_UPDATE", "current_burn_rate_kcal_per_min": 10.72, "cumulative_calories": 482.65}
   ```

---

## 4. HTTP Status Codes & Error Handling Matrix

| HTTP Code | Error Code | Description | Solution |
| :--- | :--- | :--- | :--- |
| `400` | `BAD_REQUEST` | Payload failed Pydantic validation checks | Correct parameter types or boundaries |
| `401` | `UNAUTHORIZED` | Missing, invalid, or expired JWT token | Re-authenticate via `/auth/login` |
| `403` | `FORBIDDEN` | Insufficient RBAC permissions | Access restricted resource with admin role |
| `404` | `NOT_FOUND` | Requested workout, user, or route not found | Verify resource ID or URL |
| `429` | `RATE_LIMIT_EXCEEDED` | Exceeded 100 requests per minute limit | Pause requests; respect `Retry-After` header |
| `500` | `INTERNAL_SERVER_ERROR` | Unhandled backend exception | Check server logs (`structlog`) |

---

## 5. Rate Limiting Strategy
- **Standard Limits**: 100 requests per minute per IP address for public/authenticated REST endpoints.
- **Inference Limits**: 60 requests per minute per user for `/predict/calories`.
- **Implementation**: Sliding window counter enforced via Redis key `ratelimit:<ip>:<endpoint>`.

---

## 6. Authorship & Maintenance

- **Author & Architect**: **Ravi Ranjan Singh**
- **Role**: Software Engineer, Software Architect, Full Stack Developer, AI SaaS Developer
- **Repository Maintainer**: **Ravi Ranjan Singh**
