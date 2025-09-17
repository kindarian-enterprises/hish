# 🔍 **HISH QA AGENT TODO CHECKLIST**

## 🎯 **MANDATORY QA ANALYSIS WORKFLOW**

**CRITICAL**: This checklist ensures comprehensive quality analysis. Complete ALL items before declaring analysis complete.

**⚠️ WHAT COUNTS AS REAL WORK**:
- ✅ Analyzing actual test files and implementation code
- ✅ Comparing test implementations to actual code being tested
- ✅ Identifying specific quality gaps with evidence
- ✅ Generating concrete findings with recommendations
- ❌ Loading files, running queries, or copying templates (preparation only)

### **📋 PRE-ANALYSIS SETUP**

#### **1. Context Loading**
- [ ] **Load QA Agent Persona**: Read `local/qa_agent_persona.md` or `templates/qa_agent_persona.md`
- [ ] **Load Framework Context**: Read `local/dev_agent_framework_context.md`
- [ ] **Load Project Context**: Read `local/[project-name]/dev_agent_context.md` (if analyzing specific project)
- [ ] **Verify Knowledge Access**: Confirm `qdrant-find` and `qdrant-store` tools available

#### **2. Knowledge Discovery (MANDATORY QUERIES)**
- [ ] **Query 1**: `qdrant-find "testing strategies and quality assurance patterns" hish_framework_mpnet`
- [ ] **Query 2**: `qdrant-find "test coverage and validation methodologies" hish_framework_mpnet`
- [ ] **Query 3**: `qdrant-find "production readiness and deployment validation" hish_framework_mpnet`
- [ ] **Query 4**: `qdrant-find "quality gates and testing workflows" hish_framework_mpnet`
- [ ] **Review Results**: Analyze all query results for relevant patterns and insights

### **🔍 CORE ANALYSIS TASKS**

#### **3. Test-Code Alignment Analysis (CRITICAL)**
- [ ] **Load Test Files**: Read all test files for the functionality being analyzed
- [ ] **Load Implementation Files**: Read corresponding implementation files
- [ ] **Map Test Cases**: Identify each test case and its target function/method
- [ ] **Verify Function Signatures**: Check if test parameters match implementation signatures
- [ ] **Check Parameter Validation**: Verify tests validate all input parameters
- [ ] **Validate Return Values**: Ensure tests check expected return types and values
- [ ] **Analyze Edge Cases**: Verify tests cover boundary conditions and error paths
- [ ] **Check Side Effects**: Validate tests cover state changes and side effects
- [ ] **Identify Gaps**: Document missing test cases for uncovered code paths
- [ ] **Document Misalignments**: Record specific test-code mismatches found

#### **4. Test Structure Introspection**
- [ ] **Architecture Patterns**: Analyze test organization, hierarchy, and modularity
- [ ] **Test Isolation**: Assess test independence, mocking strategies, and coupling
- [ ] **Test Maintainability**: Review refactoring resistance, readability, and documentation
- [ ] **Execution Efficiency**: Analyze performance, resource usage, and parallelization
- [ ] **Assertion Quality**: Evaluate validation completeness and error message clarity
- [ ] **Test Data Strategy**: Assess fixture management, data generation, and cleanup
- [ ] **Naming and Discovery**: Review naming conventions, categorization, and discoverability
- [ ] **Test Validity**: Verify test logic matches requirements and edge cases
- [ ] **Scenario Completeness**: Evaluate test scenario coverage and user journey validation

#### **5. Test Coverage Analysis**
- [ ] **Analyze Unit Test Coverage**: Assess unit test completeness and quality
- [ ] **Analyze Integration Test Coverage**: Evaluate integration test scenarios
- [ ] **Analyze E2E Test Coverage**: Assess end-to-end test coverage
- [ ] **Check Error Handling Coverage**: Verify error conditions are tested
- [ ] **Validate Edge Case Coverage**: Ensure boundary conditions are tested
- [ ] **Assess Performance Test Coverage**: Check if performance requirements are tested
- [ ] **Review Security Test Coverage**: Verify security aspects are tested

#### **6. Quality Gate Analysis**
- [ ] **Review Pre-deployment Checks**: Analyze quality gate criteria
- [ ] **Check Test Coverage Thresholds**: Verify coverage requirements are met
- [ ] **Validate Performance Benchmarks**: Ensure performance criteria are defined
- [ ] **Assess Security Validation**: Check security testing requirements
- [ ] **Review Functional Validation**: Verify functional requirements coverage
- [ ] **Analyze Quality Gate Effectiveness**: Determine if gates prevent issues

### **📊 ANALYSIS REPORTING**

#### **7. Findings Documentation**
- [ ] **Test-Code Alignment Gaps**: Document specific misalignments with line references
- [ ] **Structure Introspection**: Document test architecture, organization, and validity findings
- [ ] **Coverage Gaps**: Identify missing test coverage areas
- [ ] **Quality Gate Issues**: Document ineffective quality gates
- [ ] **Enhancement Opportunities**: List specific improvement recommendations
- [ ] **Cross-Project Patterns**: Identify reusable testing patterns

#### **8. Report Generation**
- [ ] **Create QA Report File**: Generate report in `hish/local/[project]/qa_reports/`
- [ ] **Include Evidence**: Provide reproducible analysis steps
- [ ] **Prioritize Findings**: Categorize by severity (HIGH/MEDIUM/LOW)
- [ ] **Provide Recommendations**: Include specific implementation steps
- [ ] **Document Cross-Project Value**: Explain how findings benefit other projects

### **✅ COMPLETION VERIFICATION**

#### **8. Final Validation**
- [ ] **All Analysis Tasks Complete**: Verify every item above is checked
- [ ] **Test-Code Comparison Done**: Confirm thorough comparison was performed
- [ ] **Coverage Analysis Complete**: Ensure all testing layers analyzed
- [ ] **Quality Gates Assessed**: Verify quality gate analysis finished
- [ ] **Report Generated**: Confirm QA report created with findings
- [ ] **Evidence Documented**: Verify all findings have supporting evidence
- [ ] **Recommendations Provided**: Ensure actionable recommendations included

### **🚨 CRITICAL REMINDERS**

- **NEVER SKIP**: Test-code alignment analysis (most important step)
- **ALWAYS COMPARE**: Test implementations to actual code being tested
- **MANDATORY EVIDENCE**: Every finding must have reproducible analysis steps
- **COMPLETE COVERAGE**: Analyze all testing layers (unit, integration, E2E, performance, security)
- **ACTIONABLE REPORTS**: Provide specific, implementable recommendations
- **REAL ANALYSIS REQUIRED**: Loading files and running queries is preparation, not analysis
- **CONCRETE FINDINGS**: Must identify specific gaps, issues, or opportunities with evidence
- **STRUCTURE INTROSPECTION**: Always analyze test architecture, organization, and validity patterns
- **DEEP VALIDATION**: Evaluate test logic, data quality, and scenario completeness
- **SKEPTICAL ANALYSIS**: Question every quality claim, challenge inadequate practices
- **CRITICAL ASSESSMENT**: Expose quality gaps, demand evidence, criticize insufficient testing
- **DEMANDING EXCELLENCE**: Accept nothing less than production-ready quality standards

### **📈 SUCCESS METRICS**

- **Test-Code Alignment**: 100% of functions have corresponding tests
- **Coverage Analysis**: All testing layers comprehensively assessed
- **Quality Gate Review**: All pre-deployment checks evaluated
- **Evidence-Based Findings**: Every recommendation supported by analysis
- **Cross-Project Value**: Patterns identified for ecosystem benefit

---

**Remember**: This checklist ensures thorough, systematic quality analysis. Complete every item before declaring analysis complete.
