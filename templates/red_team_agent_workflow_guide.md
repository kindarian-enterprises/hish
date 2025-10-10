# **HISH RED TEAM AGENT WORKFLOW GUIDE**

## **Red Team Analysis Methodology**

### **Systematic Analysis Approach**
1. **Architecture Review** → Identify attack surfaces and improvement opportunities
2. **Code Analysis** → Find vulnerabilities and anti-patterns
3. **Security Testing** → Validate controls and access mechanisms
4. **Performance Testing** → Identify bottlenecks and scalability opportunities
5. **Testing Gap Analysis** → Identify coverage improvement opportunities
6. **Operational Review** → Assess failure modes and recovery procedures

### **Multi-Layer Analysis Strategy**
- **Application Layer**: API security, input validation, authentication
- **Infrastructure Layer**: Network security, container security, secrets management
- **Data Layer**: Data protection, encryption, access controls
- **Integration Layer**: External service security, message validation
- **Operational Layer**: Monitoring, logging, incident response

---

## **Vulnerability Hunting Techniques**

### **Security Analysis**
```bash
# Authentication vulnerabilities
grep -r "password\|token\|secret" --include="*.py" --include="*.js" .
grep -r "auth\|login\|session" --include="*.py" --include="*.js" .

# Input validation gaps
grep -r "input\|user_input\|request" --include="*.py" --include="*.js" .
grep -r "validate\|sanitize\|escape" --include="*.py" --include="*.js" .

# SQL injection patterns
grep -r "execute\|query\|sql" --include="*.py" --include="*.js" .
grep -r "f\".*{.*}.*\"" --include="*.py" --include="*.js" .
```

### **Performance Analysis**
```bash
# Database queries
grep -r "SELECT\|INSERT\|UPDATE\|DELETE" --include="*.py" --include="*.js" .
grep -r "for.*in.*:" --include="*.py" --include="*.js" .

# Memory usage patterns
grep -r "memory\|cache\|buffer" --include="*.py" --include="*.js" .
grep -r "import.*" --include="*.py" --include="*.js" .
```

### **Testing Gap Analysis**
```bash
# Test coverage analysis
find . -name "test_*.py" -o -name "*_test.py" | wc -l
find . -name "*.py" | grep -v test | wc -l

# Missing test patterns
grep -r "def " --include="*.py" | grep -v test
grep -r "class " --include="*.py" | grep -v test
```

---

## 📊 **Red Team Report Structure**

### **Finding Classification**
```markdown
## RED_TEAM_FINDING_[ID]

**Severity**: CRITICAL|HIGH|MEDIUM|LOW
**Category**: SECURITY|PERFORMANCE|ARCHITECTURE|TESTING|OPERATIONAL
**Component**: [Specific component or file]
**Impact**: [Business/technical impact description]

### Evidence
[Reproducible steps or code references]

### Remediation
[Specific fix recommendations with implementation steps]

### Cross-Project Applicability
[Other projects that may be affected by this pattern]
```

### **Report Generation Process**
1. **Identify** specific weakness with clear evidence
2. **Assess** impact and likelihood of exploitation
3. **Prioritize** findings by severity and business impact
4. **Document** detailed remediation steps with external references
5. **Generate** comprehensive report files for immediate action

### **Report Writing Guidelines (MANDATORY)**

#### **Format Requirements**
- **No theatrical language**: Remove emojis, exclamation points, dramatic formatting
- **Technical tone**: Professional, factual, actionable
- **Structured format**: Use consistent markdown formatting
- **External references**: Every remediation must include specific documentation links

#### **Required Content for Each Finding**
```markdown
### **FINDING-ID: [Clear Title]**
**Severity**: [CRITICAL|HIGH|MEDIUM|LOW]
**Component**: [Specific file path and line numbers]
**Impact**: [Technical impact description]

**Evidence**:
```code
# Specific code snippets with line numbers
# Include exact file paths and problematic code
```

**Vulnerability**: [Technical description without drama]

**Remediation**:
1. **Specific action** with external references
   - Reference: [Official documentation URL]
   - Pattern: [GitHub example or implementation pattern]
   - Implementation: [Exact code or configuration]
2. **Additional steps** with tool references
   - Tool: [Specific tool name and version]
   - Command: [Exact command to run]
   - Configuration: [Specific config examples]
```

#### **External Reference Requirements**
Every remediation must include:
- **Documentation links**: Official library/framework docs
- **Code examples**: GitHub repos with working implementations
- **Standards**: RFC numbers, OWASP guidelines
- **Tools**: Specific tools with installation instructions
- **Patterns**: Proven implementation patterns

---

## 🛠️ **Analysis Tools and Techniques**

### **Code Analysis Tools**
```bash
# Static analysis
ruff check . --select=E,W,F
mypy . --strict
bandit -r . -f json

# Security scanning
safety check
pip-audit
```

### **Performance Analysis**
```bash
# Profiling
python -m cProfile script.py
python -m memory_profiler script.py

# Load testing
locust -f load_test.py --host=http://localhost:8000
```

### **Container Security**
```bash
# Image scanning
docker scan image_name
trivy image image_name

# Runtime analysis
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image image_name
```

---

## 🔍 **Cross-Project Pattern Analysis**

### **Pattern Recognition**
- **Security Patterns**: Recurring vulnerabilities across projects
- **Performance Patterns**: Common bottlenecks and optimization opportunities
- **Testing Patterns**: Recurring coverage gaps and testing anti-patterns
- **Architectural Patterns**: Design flaws and improvement opportunities

### **Report File Strategy**
```bash
# Generate security pattern reports in HISH local directory
echo "## SECURITY_PATTERN_SQL_INJECTION" >> /home/nshimokochi/Documents/projects/hish/local/project-a/red_team_report.md
echo "**Evidence**: [specific steps]" >> /home/nshimokochi/Documents/projects/hish/local/project-a/red_team_report.md
echo "**Remediation**: [specific fixes]" >> /home/nshimokochi/Documents/projects/hish/local/project-a/red_team_report.md

# Generate performance pattern reports in HISH local directory
echo "## PERFORMANCE_PATTERN_N_PLUS_1" >> /home/nshimokochi/Documents/projects/hish/local/project-b/red_team_report.md
echo "**Evidence**: [specific steps]" >> /home/nshimokochi/Documents/projects/hish/local/project-b/red_team_report.md
echo "**Remediation**: [specific fixes]" >> /home/nshimokochi/Documents/projects/hish/local/project-b/red_team_report.md

# Generate testing pattern reports in HISH local directory
echo "## TESTING_PATTERN_MISSING_INTEGRATION" >> /home/nshimokochi/Documents/projects/hish/local/project-c/red_team_report.md
echo "**Evidence**: [specific steps]" >> /home/nshimokochi/Documents/projects/hish/local/project-c/red_team_report.md
echo "**Remediation**: [specific fixes]" >> /home/nshimokochi/Documents/projects/hish/local/project-c/red_team_report.md
```

### **CRITICAL: Report File Location Requirements**
**Red team reports MUST be created in the HISH framework local directory structure:**
- **Correct Location**: `hish/local/[project-name]/red_team_report.md`
- **Incorrect Location**: `[project-root]/RED_TEAM_REPORT.md` ❌
- **Purpose**: Maintain project context within HISH framework for cross-project analysis
- **Sharing**: Enable cross-project pattern recognition and knowledge transfer

---

## 🚨 **Critical Analysis Areas**

### **Security Focus Areas**
- **Authentication**: Token management, session handling, password policies
- **Authorization**: Access controls, permission checks, role-based access
- **Input Validation**: SQL injection, XSS, CSRF protection
- **Data Protection**: Encryption, sensitive data handling, PII protection
- **Network Security**: TLS configuration, CORS policies, API security

### **Performance Focus Areas**
- **Database Queries**: N+1 problems, missing indexes, inefficient queries
- **Memory Usage**: Memory leaks, excessive allocations, cache efficiency
- **API Performance**: Response times, rate limiting, caching strategies
- **Resource Utilization**: CPU usage, memory consumption, disk I/O
- **Scalability**: Horizontal scaling, load balancing, state management

### **Testing Focus Areas**
- **Unit Test Coverage**: Missing test cases, inadequate assertions
- **Integration Testing**: Service boundaries, external dependencies
- **Security Testing**: Penetration testing, vulnerability scanning
- **Performance Testing**: Load testing, stress testing, capacity planning
- **E2E Testing**: User workflows, critical path validation

---

## 📋 **Analysis Checklist**

### **Pre-Analysis Preparation**
- [ ] Review project architecture and documentation
- [ ] Identify key components and attack surfaces
- [ ] Set up analysis environment and tools
- [ ] Review previous findings and patterns
- [ ] Plan analysis scope and priorities

### **During Analysis**
- [ ] Systematically probe each component
- [ ] Document findings with evidence
- [ ] Test remediation steps
- [ ] Identify cross-project patterns
- [ ] Prioritize findings by severity

### **Post-Analysis**
- [ ] Generate comprehensive report
- [ ] Validate findings and evidence
- [ ] Propose knowledge storage (with approval)
- [ ] Plan follow-up analysis
- [ ] Update analysis methodology

---

## 🔄 **Continuous Improvement**

### **Analysis Methodology Evolution**
- **New Techniques**: Incorporate new analysis methods and tools
- **Pattern Recognition**: Improve cross-project pattern identification
- **Automation**: Automate repetitive analysis tasks
- **Knowledge Base**: Continuously update with new findings and patterns

### **Quality Metrics**
- **Finding Rate**: Vulnerabilities identified per analysis
- **Evidence Quality**: Percentage of findings with reproducible evidence
- **Remediation Success**: Percentage of recommendations implemented
- **Cross-Project Value**: Patterns identified that benefit multiple projects

---

**🔍 Ready to systematically identify weaknesses and drive quality improvements through rigorous red team analysis.**
