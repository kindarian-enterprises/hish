# Knowledge-Driven Development Agent Directives

## 🧠 **MANDATORY DEVELOPMENT APPROACH**

**YOU MUST OPERATE WITH KNOWLEDGE-FIRST METHODOLOGY AT ALL TIMES**

### **CORE DIRECTIVE: Query Before Implement**
```bash
# ALWAYS start with knowledge discovery
qdrant-find "similar implementations of [component]"
qdrant-find "error handling patterns for [context]" 
qdrant-find "testing strategies for [component type]"

# ALWAYS check for anti-patterns
qdrant-find "known issues with [approach]"
qdrant-find "common mistakes in [technology]"
```

**REASONING**: Prevents reinventing solutions and repeating documented failures.

### **KNOWLEDGE ACCUMULATION PRINCIPLE**
```
Every solution you implement → MUST store pattern with qdrant-store
Every mistake discovered → MUST document anti-pattern  
Every decision made → MUST capture architectural reasoning
Every problem solved → MUST create reusable methodology
```

## 🏗️ **MANDATORY ARCHITECTURAL PRACTICES**

### **1. Evidence-Based Decision Making**
- **NEVER** propose solutions without querying existing patterns first
- **ALWAYS** reference historical decisions when making new ones
- **ALWAYS** validate approaches against documented anti-patterns
- **ALWAYS** check cross-project patterns before implementing

### **2. Solution Storage Protocol**
```bash
# REQUIRED after successful implementation
qdrant-store "Solution: [Component] - [Description]. Context: [Use case]. Performance: [Metrics]. Files: [File list]. Validation: [Test results]"

# REQUIRED when discovering failures
qdrant-store "Anti-pattern: [Failed approach] - [Why it failed]. Context: [When tried]. Alternative: [Better approach]. Prevention: [How to avoid]"
```

### **3. Cross-Project Intelligence**
- **ALWAYS** search patterns across ALL project collections
- **ALWAYS** consider how solutions benefit other projects
- **ALWAYS** store solutions with cross-project applicability notes
- **ALWAYS** link new implementations to existing patterns

## 🎯 **IMPLEMENTATION WORKFLOW**

### **Phase 1: Discovery (MANDATORY)**
```bash
# Research existing solutions
qdrant-find "[feature] implementation patterns"
qdrant-find "[technology] best practices" 
qdrant-find "architecture decisions for [component]"

# Check failure modes
qdrant-find "common pitfalls with [approach]"
qdrant-find "[technology] performance issues"
```

### **Phase 2: Design (EVIDENCE-BASED)**
- **COMBINE** discovered patterns into solution
- **VALIDATE** against known anti-patterns
- **DOCUMENT** decision rationale with evidence
- **PLAN** knowledge capture strategy

### **Phase 3: Implementation (TRACKED)**
- **IMPLEMENT** using proven patterns
- **MEASURE** performance and outcomes
- **VALIDATE** against success criteria
- **CAPTURE** any deviations from plan

### **Phase 4: Knowledge Capture (MANDATORY)**
```bash
# Store successful patterns
qdrant-store "Solution: [Pattern] - [Implementation details]. Context: [Use case]. Performance: [Actual metrics]. Lessons: [Key insights]"

# Store discovered improvements
qdrant-store "Enhancement: [Improvement] - [How it works better]. Context: [When applicable]. Impact: [Measurable benefits]"
```

## 🚨 **ANTI-PATTERNS TO AVOID**

### **Knowledge Anti-Patterns**
- ❌ **NEVER** implement without querying existing solutions
- ❌ **NEVER** ignore documented anti-patterns
- ❌ **NEVER** fail to store successful solutions
- ❌ **NEVER** assume patterns from one project don't apply to others

### **Decision Anti-Patterns**  
- ❌ **NEVER** make architectural decisions without historical context
- ❌ **NEVER** choose solutions without evidence
- ❌ **NEVER** ignore performance data from similar implementations
- ❌ **NEVER** skip validation against known failure modes

## 🎯 **SUCCESS METRICS**

### **Track These Indicators**
- **Query Rate**: How often you discover existing patterns before implementing
- **Reuse Rate**: How often you apply existing solutions vs creating new ones
- **Storage Rate**: How consistently you capture new solutions
- **Cross-Project Value**: How often your solutions benefit other projects

### **Quality Indicators**
- **Evidence-Based Decisions**: All choices backed by queried patterns
- **Anti-Pattern Avoidance**: Zero implementation of documented anti-patterns
- **Knowledge Accumulation**: Measurable growth in stored patterns
- **Cross-Project Learning**: Regular application of patterns across contexts

---

**CORE PRINCIPLE**: Every development session must leave the knowledge base more valuable than before. Your role is to continuously accumulate and apply collective intelligence across all projects.
