# Environment & Configuration Matrix

> **Fitness Tracker Using Machine Learning (FitAI)**

---

## 1. Environment Variable Matrix

| Variable Name | Required | Development Default | Production Requirement |
| :--- | :---: | :--- | :--- |
| `PROJECT_NAME` | No | `FitAI Machine Learning Engine` | Descriptive title |
| `ENVIRONMENT` | Yes | `development` | Set to `production` |
| `LOG_LEVEL` | No | `INFO` | `INFO` or `WARNING` |
| `SECRET_KEY` | **Yes** | *Dev Key* | Generate via `openssl rand -hex 32` |
| `DATABASE_URL` | Yes | `postgresql+asyncpg://...` | Secure PostgreSQL URI |
| `REDIS_URL` | Yes | `redis://localhost:6379/0` | Secure Redis instance URI |
| `CORS_ORIGINS` | Yes | `http://localhost:3000` | Whitelisted production domain |
| `ML_MODEL_PATH` | Yes | `./src/ml/models/xgb_calorie_v1.pkl` | Path to serialized `.pkl` model |
