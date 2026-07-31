# Project Brief & Executive Overview

> **Fitness Tracker Using Machine Learning (FitAI)**  
> *Author & Lead Architect: **Ravi Ranjan Singh***

---

## 1. Project Vision
The vision of **Fitness Tracker Using Machine Learning** is to democratize high-precision physiological analytics by providing an open, extensible, and production-ready SaaS platform that converts raw wearable biometrics and user activity vectors into personalized, actionable health intelligence. By leveraging state-of-the-art machine learning regression models, computer vision pose tracking, and real-time streaming telemetry, the platform replaces outdated static MET formulas with dynamic physiological modeling tailored to every user's unique body chemistry.

---

## 2. Business Problem
Current mainstream fitness applications face severe limitations in accuracy, personalization, and real-time responsiveness:

1. **Inaccurate Caloric Burn Models**: Most commercial apps calculate calorie expenditure using generic Metabolic Equivalent of Task (MET) averages based purely on body weight and duration. They ignore critical real-time physiological signals such as continuous heart rate, heart rate recovery velocity, ambient/body temperature, and individual metabolic efficiency.
2. **Static Goal Setting**: Conventional platforms set rigid daily step or calorie targets regardless of user fatigue, rest status, or physiological strain.
3. **Siloed Data & Proprietary Locks**: Wearable device manufacturers obscure raw telemetry data within proprietary ecosystems, prohibiting cross-device analysis and continuous machine learning model training.
4. **High Latency Feedback**: Existing cloud platforms batch-process workout sessions after completion, depriving users of live intensity adjustments during active training.

---

## 3. The Solution
**Fitness Tracker Using Machine Learning** addresses these challenges by delivering an end-to-end Machine Learning as a Service (MLaS) telemetry engine:

- **Ensemble ML Calorie Predictor**: Integrates Gradient Boosted Decision Trees (XGBoost) and Random Forest Regressors trained on gold-standard calorimetry datasets, achieving $< 12.5\text{ kcal}$ Mean Absolute Error (MAE).
- **Real-Time WebSocket Pipeline**: Ingests high-frequency heart rate and movement streams to deliver sub-50ms inference updates during live sessions.
- **Adaptive Goal Recommendation**: Employs time-series forecasting models to calculate daily recovery scores and dynamically adjust workout intensity recommendations.
- **Open Enterprise Stack**: Built using open, modern web and machine learning standards (FastAPI, React, PyTorch, Scikit-Learn, PostgreSQL, Redis, Docker), ensuring zero vendor lock-in.

---

## 4. Target Users

| User Persona | Primary Needs & Use Cases | Platform Value Proposition |
| :--- | :--- | :--- |
| **Fitness Enthusiasts** | Accurate calorie tracking, exercise progress logging, real-time heart rate zone alerts | Precise caloric burn telemetry, intuitive visual dashboard, dark mode UI |
| **Athletes & Coaches** | Granular session analysis, target heart rate monitoring, strain vs. recovery scoring | Advanced physiological analytics, CSV/JSON data export, performance heatmaps |
| **Health Researchers** | Access to normalized time-series biometric vectors for wellness research | Standardized REST API, anonymized telemetry pipelines, open data schemas |
| **Software Engineers & Reviewers** | Clean reference architecture showcasing production full-stack ML engineering | Enterprise-grade code structure, complete test suite, strict TypeScript/Python typing |

---

## 5. Core Features

### 1. Machine Learning Calorie Expenditure Engine
- Feature vector inputs: Age, Gender, Height, Weight, Duration, Heart Rate, Body Temperature.
- Algorithms: XGBoost Regressor, Random Forest Regressor, Multilayer Perceptron (MLP).
- Output: Instantaneous and cumulative calorie expenditure with 95% confidence intervals.

### 2. Biometric Activity Classification
- Automatically categorizes activity types (Running, Cycling, Swimming, HIIT, Walking, Calisthenics) from accelerometer/gyroscope time-series streams using PyTorch neural classifiers.

### 3. Real-Time Telemetry & WebSockets
- Bi-directional WSS connection allowing wear devices or web simulators to broadcast 1 Hz biometric signals and receive live burn velocity metrics.

### 4. Interactive Analytics Dashboard
- Responsive React/TypeScript dashboard displaying heart rate zone distribution, caloric velocity, historical volume, and personalized recovery indicators.

---

## 6. Architecture Summary

The application follows a clean 4-tier micro-services compatible architecture:

```
+-------------------------------------------------------------------------------+
|                            PRESENTATION LAYER                                 |
|          Next.js / React 18 SPA  |  Mobile Viewport  |  WebSocket UI          |
+-------------------------------------------------------------------------------+
                                       |
                                       v
+-------------------------------------------------------------------------------+
|                           GATEWAY & SECURITY LAYER                            |
|             NGINX Reverse Proxy  |  Rate Limiter  |  JWT Auth                 |
+-------------------------------------------------------------------------------+
                                       |
                                       v
+-------------------------------------------------------------------------------+
|                            APPLICATION LOGIC LAYER                            |
|          FastAPI Async REST Controllers  |  WebSocket Manager                 |
+-------------------------------------------------------------------------------+
                    |                                   |
                    v                                   v
+---------------------------------------+   +-----------------------------------+
|         ML INFERENCE ENGINE           |   |       DATA & PERSISTENCE          |
|  - Preprocessing Pipelines            |   |  - PostgreSQL (Relational DB)     |
|  - XGBoost & PyTorch Models           |   |  - Redis (In-Memory Cache)        |
+---------------------------------------+   +-----------------------------------+
```

---

## 7. Technology Stack

- **Frontend**: React 18, TypeScript 5, Vanilla CSS Design System, Chart.js, Axios
- **Backend**: Python 3.10+, FastAPI, Pydantic v2, Uvicorn, SQLAlchemy 2.0 AsyncIO
- **Machine Learning**: Scikit-Learn, XGBoost, PyTorch, Pandas, NumPy, ONNX Runtime
- **Database & Cache**: PostgreSQL 15, TimescaleDB extension, Redis 7
- **DevOps & Infra**: Docker, Docker Compose, NGINX, GitHub Actions CI/CD

---

## 8. Development & Engineering Goals

1. **Maintainability**: Maintain clean separation of concerns between backend routing, business domain services, and ML inference algorithms.
2. **Reproducibility**: Ensure 100% reproducible ML model training pipelines using fixed random seeds and serialized pipeline artifacts.
3. **Observability**: Implement structured JSON logging across all backend services and collect detailed inference execution latencies.

---

## 9. Engineering Principles

- **SOLID Architecture**: Enforce single responsibility, open/closed principles, and dependency inversion across all software modules.
- **Fail-Safe Inference**: Fall back to cached standard physiological models if the machine learning pipeline encounters missing or corrupted sensor fields.
- **Strict Data Validation**: Validate all ingress payloads at API boundaries using Pydantic models and TypeScript interfaces before reaching core logic.

---

## 10. Scalability Goals

- **Vertical & Horizontal Scaling**: Dockerized stateless backend instances capable of scaling horizontally behind load balancers.
- **Database Query Optimization**: Indexed time-series tables, connection pooling via AsyncPG, and pre-calculated daily summary rollups.
- **Sub-50ms Inference Guarantee**: Compiled ONNX execution formats to serve predictions with minimal CPU overhead.

---

## 11. Security Goals

- **Zero Plaintext Secrets**: All sensitive keys loaded via environment variables or secret vaults.
- **Strong Encryption**: TLS 1.3 in transit; AES-256-GCM for sensitive database fields.
- **Authentication**: JWT access tokens (15-min expiry) paired with secure HTTP-only refresh tokens.

---

## 12. Performance Goals

- **API Response Latency**: 99th percentile REST response latency $< 100\text{ ms}$.
- **ML Inference Latency**: Median inference latency $< 15\text{ ms}$.
- **Frontend Lighthouse Score**: $\ge 95$ across Performance, Accessibility, Best Practices, and SEO.

---

## 13. Future Roadmap

- **Q3 2026**: Web Bluetooth wearable pairing & computer vision pose correction.
- **Q4 2026**: On-device WASM ML execution for offline tracking.
- **Q1 2027**: Heart rate variability (HRV) recovery scoring and anomaly detection.

---

## 14. Project Authorship

- **Author & Architect**: **Ravi Ranjan Singh**
- **Role**: Software Engineer, Software Architect, Full Stack Developer, AI SaaS Developer
- **Repository Maintainer**: **Ravi Ranjan Singh**
