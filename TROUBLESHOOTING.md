# Troubleshooting & Diagnostic Guide

> **Fitness Tracker Using Machine Learning (FitAI)**

---

## 1. Common Issues & Remediations

### Issue 1: `ModuleNotFoundError: No module named 'src'`
- **Cause**: Python script executed outside the repository root directory.
- **Remediation**: Run scripts from repository root: `python -m unittest tests/unit/test_inference.py`.

### Issue 2: `FileNotFoundError: xgb_calorie_v1.pkl`
- **Cause**: Serialized machine learning model artifact missing from disk.
- **Remediation**: Execute model generator script: `python scripts/train_model.py`.

### Issue 3: Port `8000` or `3000` Already in Use
- **Cause**: Local backend or frontend development server instances already running.
- **Remediation (Windows PowerShell)**: `Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process`

---

## 2. Diagnostic Commands

```bash
# Verify Python Environment & Dependencies
python --version
pip list

# Run Full Test Suite
python -m unittest tests/unit/test_inference.py tests/integration/test_api.py tests/ml_validation/test_ml_validation.py

# Check API Health Endpoint
curl http://localhost:8000/health
```
