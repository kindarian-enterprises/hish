# Testing Workflow Template

## 🎯 **PURPOSE**
Template for establishing comprehensive testing workflows that integrate with RAG knowledge discovery and maintain high quality standards.

## 🧪 **TESTING STRATEGY FRAMEWORK**

### **Test Categories**
```
Unit Tests (Fast, Isolated)
├── Pure functions and business logic
├── Individual component behavior
└── Mocked external dependencies

Integration Tests (Real Services)
├── Service boundary interactions
├── Database operations
├── External API integration
└── End-to-end user flows

Performance Tests (Load & Scale)
├── Response time validation
├── Throughput testing
├── Resource utilization
└── Scalability limits
```

## 🔍 **RAG-ENHANCED TEST DEVELOPMENT**

### **Discovery Phase**
```bash
# Find existing test patterns for similar components
qdrant-find "testing strategies for [component type]"
qdrant-find "test fixtures for [framework/library]"
qdrant-find "mocking patterns for [external dependency]"

# Query for test anti-patterns to avoid
qdrant-find "testing anti-patterns and pitfalls"
qdrant-find "flaky test causes and solutions"
qdrant-find "test performance optimization techniques"
```

### **Implementation Phase**
```bash
# Validate approach against successful patterns
qdrant-find "successful test implementations for [feature type]"
qdrant-find "test coverage strategies for [domain]"
qdrant-find "continuous integration testing patterns"
```

### **Knowledge Storage Phase**
```bash
# Store successful test patterns
qdrant-store "Test Pattern: [test type] for [component] - Approach: [methodology]. Setup: [requirements]. Validates: [behaviors]. Execution time: [duration]. Coverage: [percentage]. Edge cases: [list]."

# Store test anti-patterns discovered
qdrant-store "Test Anti-Pattern: [problematic approach] - Problem: [what went wrong]. Symptoms: [how to recognize]. Alternative: [better approach]. Context: [when this applies]."
```

## 📋 **TEST DEVELOPMENT CHECKLIST**

### **Before Writing Tests**
- [ ] Query existing test patterns for similar functionality
- [ ] Understand the component's responsibilities and boundaries
- [ ] Identify external dependencies and integration points
- [ ] Plan test data and fixture requirements
- [ ] Define success criteria and edge cases

### **During Test Implementation**
- [ ] Follow established testing patterns from knowledge base
- [ ] Use descriptive test names that explain the scenario
- [ ] Implement proper setup and teardown procedures
- [ ] Mock external dependencies appropriately
- [ ] Validate both success and failure scenarios

### **After Test Implementation**
- [ ] Verify test passes and fails appropriately
- [ ] Check test execution time and optimize if needed
- [ ] Ensure test is deterministic and not flaky
- [ ] Update test documentation and coverage reports
- [ ] Store successful patterns in knowledge base

## 🛠️ **TEST FRAMEWORK PATTERNS**

### **Test Structure Pattern**
```[language]
# ✅ Arrange-Act-Assert Pattern
def test_[component]_[scenario]_[expected_outcome]():
    # Arrange: Set up test data and conditions
    [setup_code]
    
    # Act: Execute the functionality being tested
    result = [component].[method]([parameters])
    
    # Assert: Verify the expected outcomes
    assert result.[property] == [expected_value]
    assert [additional_assertions]
```

### **Test Fixture Pattern**
```[language]
# ✅ Reusable test fixtures
@pytest.fixture
def [fixture_name]():
    """Provide [description] for tests."""
    [setup_code]
    yield [test_object]
    [cleanup_code]
```

### **Mock Pattern**
```[language]
# ✅ External dependency mocking
@patch('[module].[dependency]')
def test_[functionality]_with_mocked_[dependency](mock_dependency):
    mock_dependency.[method].return_value = [expected_response]
    
    result = [component_under_test].[method]()
    
    assert result == [expected_outcome]
    mock_dependency.[method].assert_called_once_with([expected_args])
```

## 📊 **TEST QUALITY METRICS**

### **Coverage Targets**
```
Unit Test Coverage: [X]% minimum
├── Critical paths: 100%
├── Business logic: 95%
├── Error handling: 90%
└── Utility functions: 85%

Integration Test Coverage
├── API endpoints: 100%
├── Database operations: 95%
├── External integrations: 90%
└── User workflows: 85%
```

### **Performance Targets**
```
Test Execution Speed
├── Unit tests: < [X] seconds total
├── Integration tests: < [Y] minutes total
├── Individual test: < [Z] milliseconds
└── CI pipeline: < [W] minutes total
```

### **Quality Indicators**
```
Test Reliability
├── Flaky test rate: < 1%
├── False positive rate: < 0.5%
├── Test maintenance overhead: < 10% of dev time
└── Bug detection rate: > 90%
```

## 🔄 **CONTINUOUS TESTING WORKFLOW**

### **Development Phase**
1. **Write failing test first** (TDD approach)
2. **Implement minimal code** to make test pass
3. **Refactor** while keeping tests green
4. **Add edge case tests** for comprehensive coverage
5. **Store patterns** in knowledge base

### **Code Review Phase**
1. **Review test quality** and patterns
2. **Verify test coverage** meets standards
3. **Check for test anti-patterns**
4. **Validate test documentation**
5. **Ensure CI integration**

### **CI/CD Integration**
1. **Run tests on every commit**
2. **Generate coverage reports**
3. **Monitor test performance**
4. **Alert on test failures**
5. **Track quality metrics**

## 🚨 **TESTING ANTI-PATTERNS TO AVOID**

### **❌ Common Test Anti-Patterns**
```[language]
# ❌ NEVER write tests that depend on external services
test_api_call_to_production()  // Use mocks instead

# ❌ NEVER write tests with hidden dependencies
test_function_that_requires_specific_global_state()  // Make dependencies explicit

# ❌ NEVER write tests that depend on execution order
test_step_1()  // Each test should be independent
test_step_2()  // Don't rely on test_step_1 results

# ❌ NEVER write overly complex tests
test_everything_in_one_massive_test()  // Break into focused, single-purpose tests
```

### **❌ Test Maintenance Anti-Patterns**
- **Never ignore flaky tests** - Fix or remove them
- **Never skip test updates** when changing functionality
- **Never commit code** without running the test suite
- **Never mock everything** - Test real integrations where appropriate

## 📚 **TEST DOCUMENTATION TEMPLATES**

### **Test Plan Template**
```markdown
# Test Plan: [Feature Name]

## Scope
- **In Scope**: [What will be tested]
- **Out of Scope**: [What won't be tested]

## Test Strategy
- **Unit Tests**: [Approach and coverage]
- **Integration Tests**: [Services and boundaries]
- **Performance Tests**: [Metrics and thresholds]

## Test Environment
- **Dependencies**: [Required services and data]
- **Configuration**: [Settings and environment variables]
- **Test Data**: [Fixtures and sample data requirements]

## Success Criteria
- **Coverage**: [Minimum percentage required]
- **Performance**: [Response time and throughput targets]
- **Reliability**: [Acceptable failure rates]
```

### **Test Case Template**
```markdown
# Test Case: [Scenario Description]

## Objective
[What this test validates]

## Preconditions
[Required setup and state]

## Test Steps
1. [Action 1]
2. [Action 2]
3. [Action 3]

## Expected Results
- [Expected outcome 1]
- [Expected outcome 2]
- [Expected outcome 3]

## Edge Cases
- [Edge case 1 and expected behavior]
- [Edge case 2 and expected behavior]
```

---

## 🎯 **CUSTOMIZATION CHECKLIST**

When adapting this template:
- [ ] Replace `[language]` with your programming language
- [ ] Update `[framework/library]` references to your testing framework
- [ ] Adjust coverage targets to match your project requirements
- [ ] Customize performance targets based on your application needs
- [ ] Add domain-specific testing requirements
- [ ] Include any regulatory or compliance testing needs

This template provides a foundation for building robust, maintainable test suites that leverage knowledge discovery and maintain high quality standards.
