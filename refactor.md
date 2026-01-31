# Refactor Plan for MDWiki Python Project

## Executive Summary

This document outlines a comprehensive refactor plan for the MDWiki Python automation tool. The analysis reveals significant architectural weaknesses, code quality issues, and technical debt that should be addressed systematically.

---

## Critical Weaknesses Identified

### 1. Dependency Management (CRITICAL)

**Issues:**
- No `requirements.txt` or proper dependency specification file
- No `setup.py` or `pyproject.toml` for package configuration
- Heavy reliance (148+ files) on external `newapi` library without proper dependency declaration
- Dependencies managed through implicit imports and PYTHONPATH manipulation

**Impact:**
- Projects cannot be reliably reproduced
- Deployment is difficult and error-prone
- Version conflicts are inevitable
- New developers cannot easily set up the environment

**Recommendation:**
- Create `pyproject.toml` with proper dependency specifications
- Pin all dependency versions
- Remove reliance on implicit `newapi` - either vendor it or declare as proper dependency

---

### 2. Code Organization & Structure

**Issues:**
- `old/` directories containing deprecated code (should be removed or archived)
- Scattered test files across multiple locations
- Inconsistent module structure (`__init__.py` files with only comments)
- Mixed business logic with bot scripts in the same files

**Directory Structure Issues:**
```
md_core/mdpy/old/          # Dead code
md_core_helps/tw/old/      # Dead code
old/                       # Dead code at root
md_core_helps/one_time/    # One-off scripts mixed with reusable code
```

**Recommendation:**
- Remove or archive all `old/` directories to a separate repository
- Consolidate tests into a top-level `tests/` directory mirroring source structure
- Separate bot scripts from reusable libraries
- Establish clear module boundaries with proper `__init__.py` exports

---

### 3. Code Quality & Style

**Issues:**
- Pre-commit config has critical tools commented out (black, isort, flake8)
- Inconsistent string literal usage (mix of single and double quotes)
- No type hints throughout the codebase
- Global state usage (e.g., `ASK_all` in `write_bot.py`)
- Magic numbers and hardcoded values scattered throughout
- Inconsistent naming conventions (snake_case vs camelCase)
- Excessive commented-out code in production files

**Example from `.pre-commit-config.yaml`:**
```yaml
#  - repo: https://github.com/psf/black
#    rev: 22.12.0
#    hooks:
#      - id: black
#  - repo: https://github.com/PyCQA/isort
#    rev: 5.11.3
#    hooks:
#      - id: isort
```

**Recommendation:**
- Enable and configure black, isort, and flake8
- Run them across the entire codebase
- Add mypy with strict mode (already configured but needs enforcement)
- Establish coding standards document

---

### 4. Testing Weaknesses

**Issues:**
- Tests are scattered across multiple `tests/` directories in different modules
- Many "tests" are actually standalone scripts that require manual execution
- No clear test organization strategy
- Test markers are inconsistent (`skip2`, `dump` markers suggest workarounds)
- No evidence of integration or end-to-end tests
- Pytest warnings are being ignored (deprecation warnings)

**Test File Examples:**
```python
# newupdater/tests/test_MedWorkNew.py - script-like test
# wprefs/tests/test_text.py - hardcoded data, not parametrized
```

**Recommendation:**
- Consolidate all tests to `tests/` directory at root
- Convert script-like tests to proper pytest functions
- Add pytest fixtures for common test data
- Enable deprecation warnings to fix underlying issues
- Add coverage reporting (pytest-cov)

---

### 5. Import & Path Management

**Issues:**
- Direct `sys.path` manipulation in multiple files
```python
sys.path.append(str(Path(__file__).parent.parent))
```
- Relative imports that depend on execution context
- No clear package structure enforcement

**Impact:**
- Code only works when run from specific directories
- IDE support is poor
- Testing is fragile

**Recommendation:**
- Make project a proper installable package
- Use absolute imports throughout
- Remove all `sys.path` manipulation

---

### 6. Logging & Output

**Issues:**
- Custom `printe.output()` instead of standard logging
- Custom `printe.showDiff()` for diffs
- Inconsistent output formatting with color codes like `<<green>>`
- No structured logging

**Recommendation:**
- Migrate to Python's standard `logging` module
- Use proper log levels (DEBUG, INFO, WARNING, ERROR)
- Implement structured logging for better observability

---

### 7. Security & Configuration

**Issues:**
- Credentials potentially hardcoded or in environment variables without specification
- No `.env.example` file showing required configuration
- Cookies stored in `apis/sup/cookies/` directory

**Recommendation:**
- Use `python-dotenv` for environment management
- Create `.env.example` template
- Never commit credentials or cookies
- Use secret management for CI/CD

---

### 8. Documentation

**Issues:**
- Minimal docstrings despite good README
- No API documentation
- No examples for common use cases
- Mixed inline documentation styles

**Recommendation:**
- Add comprehensive docstrings (Google or NumPy style)
- Generate API docs with Sphinx
- Add usage examples for each major module

---

## Refactor Priority Matrix

### Phase 1: Foundation (Weeks 1-2)
**Must complete before anything else:**

1. **Create `pyproject.toml`** with all dependencies
2. **Remove all `old/` directories** (archive if needed)
3. **Enable and run formatting tools** (black, isort, flake8)
4. **Consolidate tests** to single `tests/` directory structure

### Phase 2: Architecture (Weeks 3-4)
**Structural improvements:**

1. **Establish proper package structure** with installable setup
2. **Remove `sys.path` manipulation** - use absolute imports
3. **Separate bot scripts from libraries**
4. **Create configuration management** layer

### Phase 3: Code Quality (Weeks 5-6)
**Improve code maintainability:**

1. **Add type hints** throughout codebase
2. **Replace custom logging with standard logging**
3. **Add comprehensive docstrings**
4. **Extract magic numbers/hardcoded values to config**

### Phase 4: Testing (Weeks 7-8)
**Improve test coverage and quality:**

1. **Convert script-tests to proper pytest**
2. **Add test fixtures** for common scenarios
3. **Enable coverage reporting**
4. **Add integration tests** for critical paths

### Phase 5: Security & Hardening (Ongoing)
**Security improvements:**

1. **Environment-based configuration**
2. **Secret management for CI/CD**
3. **Security audit** of all API calls
4. **Input validation** throughout

---

## Proposed New Directory Structure

```
pybot/
├── pyproject.toml          # Package configuration and dependencies
├── .env.example            # Environment variables template
├── README.md
├── refactor.md             # This document
├── src/
│   └── mdwiki_pybot/       # Main package
│       ├── __init__.py
│       ├── core/           # Core functionality
│       │   ├── __init__.py
│       │   ├── api/        # API clients
│       │   ├── database/   # Database operations
│       │   └── models/     # Data models
│       ├── bots/           # Bot implementations
│       │   └── __init__.py
│       ├── utils/          # Utilities
│       │   └── __init__.py
│       └── config/         # Configuration
│           └── __init__.py
├── tests/                  # All tests consolidated
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/                # Standalone scripts
│   └── __init__.py
└── docs/                   # Documentation
```

---

## Success Metrics

After refactoring, the project should:

- [ ] Be installable via `pip install -e .`
- [ ] Pass all tests with `pytest`
- [ ] Have >70% code coverage
- [ ] Pass all pre-commit hooks without warnings
- [ ] Have no `sys.path` manipulation
- [ ] Use standard logging throughout
- [ ] Have type hints on all public functions
- [ ] Have consistent code style (black + isort)
- [ ] Have no `old/` directories
- [ ] Have documented environment variables

---

## Immediate Actions

1. Create `pyproject.toml` with:
   - Project metadata
   - All dependencies (including `newapi`)
   - Development dependencies (pytest, black, isort, mypy, etc.)
   - Tool configurations (black, isort, mypy, pytest)

2. Run initial formatting:
   ```bash
   black .
   isort .
   ```

3. Move all tests to `tests/` directory

4. Create `.env.example` file

---

## Notes

- This refactor should be done incrementally, module by module
- Each phase should be tested before moving to the next
- Consider creating feature branches for each major change
- Document any breaking changes for users
