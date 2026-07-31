# Contributing Guidelines

Thank you for your interest in contributing to **Fitness Tracker Using Machine Learning (FitAI)**!

---

## 1. Code of Conduct
All contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to `raviranjansingh.dev@gmail.com`.

---

## 2. How to Contribute

### 2.1 Reporting Bugs
- Search existing GitHub Issues before filing a bug report.
- Include OS version, Python version, steps to reproduce, and exact error log tracebacks.

### 2.2 Submitting Pull Requests
1. Fork the repository and create a feature branch (`git checkout -b feature/amazing-feature`).
2. Ensure Python code adheres to PEP8 (`black` & `flake8`) and TypeScript adheres to ESLint rules.
3. Add unit tests for any new features or bug fixes.
4. Verify all 9 test suites pass: `python -m unittest tests/unit/test_inference.py tests/integration/test_api.py tests/ml_validation/test_ml_validation.py`.
5. Open a Pull Request targeting the `main` branch with a clear summary of changes.

---

## 3. Local Development Setup

```bash
# Clone repository
git clone https://github.com/raviranjansingh/FITNESS-TRACKER-USING-MACHINE-LEARNNING.git
cd FITNESS-TRACKER-USING-MACHINE-LEARNNING

# Setup Python Virtual Environment
python -m venv venv
source venv/bin/activate # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run ML Model Generator
python scripts/train_model.py

# Execute Tests
python -m unittest tests/unit/test_inference.py tests/integration/test_api.py tests/ml_validation/test_ml_validation.py
```

---

## 4. Repository Ownership
- **Repository Maintainer**: **Ravi Ranjan Singh**
- **Contact**: `raviranjansingh.dev@gmail.com`
