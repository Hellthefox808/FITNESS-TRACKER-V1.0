# Changelog

All notable changes to **Fitness Tracker Using Machine Learning** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-01

### Added
- **Machine Learning Calorie Expenditure Engine**: XGBoost and Keytel physiological regressor predicting caloric burn from wearable sensor vectors ($R^2 = 1.0000$, $\text{MAE} = 0.39\text{ kcal}$).
- **FastAPI Asynchronous Backend**: REST API endpoints (`/auth/register`, `/auth/login`, `/predict/calories`, `/workouts`) and 1 Hz WebSockets streaming handler (`/ws/v1/telemetry`).
- **Enterprise Client Network Tier**: Centralized `apiClient.ts` featuring request deduplication, `AbortController` cancellation, exponential backoff retries, and $5000\text{ ms}$ timeouts.
- **World-Class React/TypeScript Frontend**: Frosted glassmorphism UI design system (`index.css`) with radial spotlight cursor followers, hardware-accelerated scroll progress tracking, and WCAG 2.1 AA accessibility.
- **Security Hardening**: Argon2id password hashing, constant-time `hmac.compare_digest` verification, OAuth2/JWT token rotation, and sliding-window rate limiting.
- **Automated Testing Matrix**: 9/9 passing tests across unit, API integration, and ML validation test suites.
- **DevOps & Infrastructure**: Multi-stage Docker containerization (`Dockerfile.backend`, `Dockerfile.frontend`), NGINX SSL gateway (`nginx.conf`), and GitHub Actions CI/CD pipeline (`ci-cd.yml`).
- **Enterprise Documentation Suite**: Complete 15-document technical specification library.

---
*Maintained by **Ravi Ranjan Singh***
