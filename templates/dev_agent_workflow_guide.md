# 🔧 **HISH AGENT WORKFLOW GUIDE**

## 🎯 Purpose
Comprehensive procedures for advanced Hish framework operations, cross-project intelligence storage, and complex workflow patterns removed from the initialization prompt for progressive disclosure.

---

## 🧠 **Cross-Project Intelligence Storage**

### **UUID Generation for Intelligence Collection**
The `cross_project_intelligence` collection requires unique identifiers for distributed storage:

```bash
# Generate UUID before storing cross-project observations
python3 -c "import uuid; print(uuid.uuid4())"
# Example output: a870346e-03c7-4622-b113-60a7efc0f9ac

# Use generated UUID in storage command
qdrant-store "Cross-project observation content..." cross_project_intelligence a870346e-03c7-4622-b113-60a7efc0f9ac
```

### **Evidence-Based Pattern Documentation**
Document specific observed connections with measurable validation:

**Pattern Observation Template:**
```
Pattern: [Name] - [Description]
Context: [When/where observed]
Evidence: [Specific data/outcomes]
Cross-Project Applicability: [List of relevant contexts]
Validation Status: [How pattern was confirmed]
Implementation Files: [Relevant code locations]
```

**Relationship Mapping Template:**
```
Relationship: [Project A Pattern] → [Project B Application]
Evidence: [Specific connection observed]
Bidirectional Learning: [How both projects benefit]
Transfer Opportunity: [Actionable next steps]
```

---

## 📊 **Advanced Collection Management**

### **Multi-Collection Search Strategy**
Always search multiple collections for comprehensive knowledge discovery:

```bash
# Framework guidance (established patterns)
qdrant-find "authentication patterns" hish_framework

# Project documentation (working examples, context)
qdrant-find "authentication patterns" project_name_docs_mpnet

# Cross-project intelligence (observed relationships)
qdrant-find "authentication patterns" cross_project_intelligence
```

### **Collection Usage Guidelines**

**`hish_framework` Collection:**
- Framework documentation and guides
- Established project contexts
- Official templates and patterns
- Current framework status

**`{project}_docs_mpnet` Collections:**
- Project documentation and context
- Architectural patterns and decisions
- Configuration and deployment patterns
- Technical documentation

**`cross_project_intelligence` Collection:**
- Pattern observations across projects
- Effectiveness metrics and validation
- Relationship mappings between contexts
- Emerging patterns requiring validation

---

## 🔄 **Session Intelligence Extraction Protocol**

### **Active Pattern Recognition During Every Session**

#### **Observation Collection:**
1. **Notice** patterns that might apply across projects
2. **Identify** connections between current work and other contexts
3. **Spot** emerging themes that could become universal patterns
4. **Recognize** when solutions could benefit other projects
5. **Detect** knowledge gaps for cross-project learning

#### **Documentation Requirements:**
```bash
# Document specific observed connections
qdrant-store "Pattern X in Project A relates to Challenge Y in Project B - [specific evidence]" cross_project_intelligence [UUID]

# Note potential universal applicability
qdrant-store "This approach might apply to [list specific contexts] - [validation approach]" cross_project_intelligence [UUID]

# Capture bidirectional learning opportunities
qdrant-store "Project A's solution could help Project B: [specific benefits] AND Project B's constraint handling could improve Project A: [specific improvements]" cross_project_intelligence [UUID]
```

---

## 🏗️ **Context Update Procedures**

### **Timestamp Verification Protocol**
All context updates require verified timestamps to maintain historical accuracy:

```bash
# Generate verified UTC timestamp
date -u
# OR
curl -s http://worldtimeapi.org/api/timezone/UTC

# Use exact timestamp in context updates
# NEVER use hallucinated or approximate timestamps
```

### **Context Update Format Requirements**

**Achievement Documentation:**
```
achievement_YYYY_MM_DD_HH_MM_SS_description {
  verified_datetime: [actual_system_output];
  scope: [specific_area];
  achievement: [concrete_outcome];
  impact: [measurable_effect];
  files: [modified_files];
  cross_project_applicability: [ecosystem_benefits]
}
```

**Issue Documentation:**
```
issue_YYYY_MM_DD_HH_MM_SS_description {
  verified_datetime: [timestamp];
  issue: [specific_problem];
  impact: [system_effect];
  status: [current_state];
  location: [relevant_files];
  priority: CRITICAL|HIGH|MEDIUM|LOW
}
```

---

## 🎯 **Knowledge-First Development Workflow**

### **Phase 1: Discovery & Context Building**
```bash
# Research existing solutions across all collections
qdrant-find "[feature] implementation patterns" hish_framework_mpnet
qdrant-find "[feature] implementation patterns" {project}_docs_mpnet
qdrant-find "[feature] implementation patterns" cross_project_intelligence_mpnet

# Check for anti-patterns and known issues
qdrant-find "known pitfalls with [approach]" hish_framework
qdrant-find "common [technology] mistakes" cross_project_intelligence

# Cross-repository pattern discovery
qdrant-find "similar features in other projects" cross_project_intelligence
qdrant-find "testing strategies for [component type]" hish_framework
```

### **Phase 2: Implementation with Knowledge Validation**
```bash
# Validate approach against existing patterns
qdrant-find "successful implementations of [similar feature]" {project}_docs_mpnet

# Check for architectural consistency
qdrant-find "design decisions for [component type]" hish_framework

# Review error handling patterns
qdrant-find "error handling patterns for [service type]" cross_project_intelligence
```

### **Phase 3: Knowledge Capture & Ecosystem Enhancement**

**Present to user for review before storage:**
```
Proposed Knowledge Storage:

IMPLEMENTATION PATTERN:
• Solution: [Pattern Name] - [Technical description]
• Context: [Use case and applicability]
• Performance: [Measured outcomes]
• Files: [Implementation locations]
• Cross-Project Value: [How this benefits other contexts]

VALIDATION EVIDENCE:
• Testing: [Coverage and validation approach]
• Outcomes: [Specific measurable results]
• Anti-Patterns Avoided: [Known issues prevented]

Please review for technical accuracy and scope appropriateness.
```

---

## 🔍 **Advanced Workflow Patterns**

### **Error Resolution with Historical Context**
```bash
# Query for similar error patterns
qdrant-find "[error type] resolution patterns" cross_project_intelligence
qdrant-find "[component] debugging approaches" hish_framework

# Find documented solutions
qdrant-find "fixes for [specific issue]" {project}_docs_mpnet
qdrant-find "[error] recovery strategies" cross_project_intelligence_mpnet

# Store successful resolution
qdrant-store "Error Resolution: [Issue] - Root cause: [analysis]. Solution: [implementation]. Validation: [proof]. Context: [applicability]" cross_project_intelligence [UUID]
```

### **Architecture Decision Documentation**
```bash
# Research existing architectural decisions
qdrant-find "[component] architecture decisions" hish_framework
qdrant-find "[pattern] design decisions" cross_project_intelligence

# Validate consistency with existing patterns
qdrant-find "similar architectural choices and outcomes" cross_project_intelligence

# Store architectural decision with full context
qdrant-store "Architecture Decision: [Choice] - [Technical rationale]. Context: [use case]. Trade-offs: [analysis]. Validation: [evidence]" cross_project_intelligence [UUID]
```

---

## 📋 **Quality Assurance Protocols**

### **Knowledge Storage Quality Standards**
- **Pattern Validation**: Solutions must work across multiple project contexts
- **Anti-Pattern Documentation**: Failed approaches documented to prevent repetition
- **Cross-Reference**: Link solutions between framework guidance and implementations
- **Continuous Refinement**: Update patterns based on new learnings and outcomes

### **Cross-Project Validation Workflow**
1. **Apply to Real Projects**: Use patterns on actual development tasks
2. **Measure Real Outcomes**: Track success rates and performance in practice
3. **Identify Evolution Opportunities**: Document areas for improvement
4. **Evolve Patterns**: Refine based on real-world learnings
5. **Store Evolution**: Document improved versions for future use

---

**Following these workflows enables institutional learning and creates compounding value across your entire engineering ecosystem.**
