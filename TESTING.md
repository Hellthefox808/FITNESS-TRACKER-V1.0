# Testing Strategy & Quality Assurance Framework

> **Fitness Tracker Using Machine Learning (FitAI)**  
> *Author & Lead Architect: **Ravi Ranjan Singh***

---

## 1. Executive Summary

This document outlines the testing strategy, automated test frameworks, quality assurance procedures, and Machine Learning model validation protocols enforced in **Fitness Tracker Using Machine Learning**. The objective is to maintain code reliability, prevent regressions, ensure sub-50ms ML inference latencies, and guarantee $>95\%$ prediction accuracy benchmarks across releases.

---

## 2. Testing Pyramid & Matrix

```
                      / \
                     /   \
                    / E2E \       <-- Cypress / Playwright (Critical User Flows)
                   /-------\
                  / Integr. \     <-- PyTest-AsyncIO / Supertest (API & DB Interop)
                 /-----------\
                /  Unit Tests \   <-- PyTest / Jest (Schemas, Utils, Controllers)
               /---------------\
              / ML Model Valid. \ <-- Scikit-Learn Metrics ($R^2$, MAE, Cross-Val)
             +-------------------+
```

### Test Suite Summary

| Test Category | Target Component | Framework / Tooling | Target Coverage | Execution Frequency |
| :--- | :--- | :--- | :---: | :--- |
| **Unit Tests** | API Schemas, Utils, Services | PyTest, Jest | $\ge 85\%$ | Every Commit / PR |
| **Integration Tests** | REST Routes, DB, Redis, Auth | PyTest-AsyncIO | $\ge 80\%$ | Continuous Integration |
| **ML Validation** | XGBoost / PyTorch Pipelines | Scikit-Learn, PyTest | $R^2 \ge 0.95$ | Prior to Deployment |
| **End-to-End** | React UI to API Integration | Playwright | Key Flows | Nightly Build |

---

## 3. Backend Unit & Integration Testing

Backend tests are located in `tests/unit/` and `tests/integration/`.

```bash
# Execute backend test suite with terminal coverage report
pytest tests/ --cov=src/backend --cov-report=term-missing --cov-report=html
```

### Sample Unit Test: Pydantic Biometric Ingress Schema
```python
import pytest
from pydantic import ValidationError
from src.backend.schemas.predict import BiometricInferenceSchema

def test_valid_biometric_schema():
    payload = {
        "age": 28,
        "gender": "male",
        "height_cm": 178.0,
        "weight_kg": 75.5,
        "duration_min": 45.0,
        "heart_rate_bpm": 154.0,
        "body_temp_c": 38.1
    }
    schema = BiometricInferenceSchema(**payload)
    assert schema.age == 28
    assert schema.gender == "male"

def test_invalid_heart_rate_bounds():
    payload = {
        "age": 28,
        "gender": "male",
        "height_cm": 178.0,
        "weight_kg": 75.5,
        "duration_min": 45.0,
        "heart_rate_bpm": 350.0, # Exceeds valid physiological range
        "body_temp_c": 38.1
    }
    with pytest.raises(ValidationError):
        BiometricInferenceSchema(**payload)
```

---

## 4. Machine Learning Model Validation Framework

Machine learning models must pass automated validation benchmarks before artifact serialization and deployment to prevent silent accuracy decay or data drift.

```bash
# Execute ML validation test suite
pytest tests/ml_validation/
```

### Validation Metrics Thresholds

| Metric | Target Metric Name | Minimum Threshold | Benchmark Value |
| :--- | :--- | :---: | :---: |
| **Calorie Model Accuracy** | Coefficient of Determination ($R^2$) | $\ge 0.950$ | `0.968` |
| **Calorie Model Error** | Mean Absolute Error ($\text{MAE}$) | $\le 15.0\text{ kcal}$ | `11.2 kcal` |
| **Calorie Model RMSE** | Root Mean Squared Error ($\text{RMSE}$) | $\le 20.0\text{ kcal}$ | `16.4 kcal` |
| **Activity Classification** | Weighted F1-Score | $\ge 0.940$ | `0.954` |
| **Inference Latency** | P99 Single-Record Latency | $\le 45\text{ ms}$ | `12.4 ms` |

### Sample ML Validation Test
```python
import numpy as np
import pytest
from sklearn.metrics import r2_score, mean_absolute_error
from src.ml.inference import CalorieInferenceEngine

def test_calorie_model_performance_benchmarks(holdout_test_dataset):
    X_test, y_true = holdout_test_dataset
    engine = CalorieInferenceEngine(model_path="src/ml/models/xgb_calorie_v1.pkl")
    
    y_pred = engine.predict_batch(X_test)
    
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    
    assert r2 >= 0.95, f"ML Model R2 score {r2:.4f} failed benchmark threshold of 0.95"
    assert mae <= 15.0, f"ML Model MAE {mae:.2f} kcal failed benchmark threshold of 15.0 kcal"
```

---

## 5. Frontend Unit & Component Testing

Frontend tests are powered by Jest and React Testing Library located in `src/frontend/src/__tests__/`.

```bash
cd src/frontend
npm test -- --coverage
```

### Test Scope
- **Component Rendering**: Ensures UI cards, graphs, and forms render cleanly across breakpoints.
- **State Management**: Verifies Zustand store state transitions for authentication and real-time telemetry updates.
- **User Interactions**: Simulates workout submission forms, keyboard tab navigation, and error state alerts.

---

## 6. Continuous Integration Gatekeeping

The GitHub Actions CI workflow automatically triggers on every pull request to enforce testing requirements:

1. **Lint Checks**: Passes `black --check`, `flake8`, and `eslint`.
2. **Backend & Frontend Tests**: Executes full unit and integration test suites.
3. **ML Validation**: Runs holdout model benchmarking tests.
4. **Coverage Enforcement**: Rejects pull requests if test coverage drops below $80\%$.

---

## 7. Authorship & Maintenance

- **Author & Architect**: **Ravi Ranjan Singh**
- **Role**: Software Engineer, Software Architect, Full Stack Developer, AI SaaS Developer
- **Repository Maintainer**: **Ravi Ranjan Singh**
