# Test Generator

## Overview

Automatically generate comprehensive test suites for existing code. Creates unit tests, integration tests, and edge case coverage.

## Usage

Type `/test-generator` followed by target code.

## Parameters

- `target`: File or function to test (required)
- `test_type`: Type of tests (unit, integration, e2e, all) (default: all)
- `coverage_goal`: Target coverage percentage (default: 80)
- `include_edge_cases`: Generate edge case tests (default: true)
- `mock_external`: Auto-mock external dependencies (default: true)

## Example Usage

### Generate Tests for File

```
/test-generator
Target: app/services/auth.py
Test Type: all
Coverage Goal: 90
```

### Unit Tests Only

```
/test-generator
Target: app/utils/validation.py
Test Type: unit
Include Edge Cases: true
```

### Integration Tests

```
/test-generator
Target: app/api/endpoints/users.py
Test Type: integration
Mock External: false
```

### Specific Function

```
/test-generator
Target: app/services/payment.py::process_payment
Test Type: all
Coverage Goal: 100
```

## Workflow

1. **Code Analysis**:
   - Parse target code structure
   - Identify functions, classes, methods
   - Extract dependencies and imports
   - Analyze control flow and branches

2. **Test Planning**:
   - Determine test scenarios
   - Identify edge cases
   - Plan mocking strategy
   - Calculate coverage requirements

3. **Test Generation**:
   - Generate unit tests (fast, isolated)
   - Generate integration tests (with dependencies)
   - Generate edge case tests (boundary conditions)
   - Add fixtures and mocks

4. **Validation**:
   - Run generated tests
   - Measure actual coverage
   - Fix failing tests
   - Report coverage gaps

## Test Types

### Unit Tests
- Fast, isolated tests
- Mock all external dependencies
- Test single functions/methods
- Focus on logic and edge cases

### Integration Tests
- Test component interactions
- Use real dependencies (DB, APIs)
- Verify data flow
- Test error propagation

### E2E Tests
- Full workflow testing
- Real environment
- User scenario simulation
- Performance validation

## Generated Test Structure

```python
import pytest
from unittest.mock import Mock, patch

class TestAuthService:
    """Tests for AuthService"""

    @pytest.fixture
    def auth_service(self):
        """Fixture for AuthService instance"""
        return AuthService()

    def test_login_success(self, auth_service):
        """Test successful login"""
        # Arrange
        # Act
        # Assert
        pass

    def test_login_invalid_credentials(self, auth_service):
        """Test login with invalid credentials"""
        pass

    @pytest.mark.integration
    def test_login_with_database(self, auth_service, db_session):
        """Integration test with real database"""
        pass
```

## Best Practices

- Generate tests alongside new code
- Aim for 80%+ coverage
- Include edge cases and error paths
- Use appropriate markers (@pytest.mark.*)
- Mock external services
- Test both success and failure scenarios
- Add descriptive test names

## Coverage Analysis

After generation, reports:
- Line coverage percentage
- Branch coverage percentage
- Uncovered lines
- Missing edge cases
- Suggested additional tests

## Related Commands

- `/generate-code-batch` - Generate code with tests
- `/qa-critic` - Review test quality
- `/refactor-batch` - Add tests to legacy code
