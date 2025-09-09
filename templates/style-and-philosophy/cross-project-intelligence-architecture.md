# 🧠 Cross-Project Intelligence Architecture

## 📋 **Overview**

The Hish framework uses a **dual-layer knowledge architecture** to separate static framework documentation from dynamic cross-project intelligence observations.

## 🏗️ **Architecture Design**

### **📚 Layer 1: Framework Documentation Collection (`hish_framework`)**
**Purpose**: Static framework documentation and context files
**Content Type**: Official documentation, guides, templates, and established patterns

```bash
# What goes in hish_framework collection:
✅ Framework documentation (docs/*)
✅ Project context files (local/*/dev_agent_context.md)
✅ Workflow indexes (local/workflow-indexes/*)
✅ Official templates and guides
✅ Established patterns and protocols
```

### **🧠 Layer 2: Cross-Project Intelligence Collection (`cross_project_intelligence`)**
**Purpose**: Dynamic observations, relationships, and emerging patterns
**Content Type**: Session-based discoveries, evidence-based observations, and pattern evolution

```bash
# What goes in cross_project_intelligence collection:
✅ Pattern observations across projects
✅ Relationship mappings between contexts
✅ Effectiveness metrics and validation status
✅ Knowledge flows and transfer opportunities
✅ Emerging patterns requiring validation
✅ Cross-project solution applicability notes
```

## 🎯 **Clear Separation Guidelines**

### **📖 Framework Context Document (`local/dev_agent_framework_context.md`)**
**Role**: **PROJECT STATUS TRACKER** - Current state of framework development

**Contains:**
- Framework component status and health
- Current development priorities
- Architectural decisions and rationale
- Framework-specific implementation details
- Cross-project relationship summaries (high-level)

**Does NOT contain:**
- Detailed pattern observations (goes to intelligence collection)
- Session-specific discoveries (goes to intelligence collection)
- Evidence-based effectiveness metrics (goes to intelligence collection)

### **🧠 Intelligence Collection (`cross_project_intelligence`)**
**Role**: **PATTERN AND RELATIONSHIP REPOSITORY** - Dynamic knowledge discovery

**Contains:**
- Specific pattern observations with evidence
- Cross-project effectiveness data
- Relationship mappings with validation status
- Session-based discoveries and insights
- Emerging patterns requiring further validation

**Does NOT contain:**
- Framework component status (goes to context document)
- Official documentation (goes to framework collection)
- Established, finalized patterns (goes to framework collection)

## 📊 **Usage Patterns**

### **🔍 When to Search Framework Collection**
```bash
# Looking for established documentation
qdrant-find "How to create a new project context" hish_framework

# Finding official patterns and protocols
qdrant-find "Agent initialization protocol" hish_framework

# Accessing current project status
qdrant-find "project-alpha current status" hish_framework
```

### **🧠 When to Search Intelligence Collection**
```bash
# Finding cross-project patterns
qdrant-find "authentication patterns across projects" cross_project_intelligence

# Looking for effectiveness data
qdrant-find "docker compose patterns performance metrics" cross_project_intelligence

# Discovering relationship insights
qdrant-find "how project-alpha patterns apply to project-beta" cross_project_intelligence
```

### **💾 When to Store in Intelligence Collection**

**⚠️ IMPORTANT: UUID Required for Intelligence Collection Storage**

The `cross_project_intelligence` collection requires valid UUIDs for point identification. This ensures unique identification across distributed storage and prevents ID collisions in cross-project contexts. Always generate a UUID before storing:

```bash
# Step 1: Generate UUID for each storage operation
python3 -c "import uuid; print(uuid.uuid4())"
# Example output: a870346e-03c7-4622-b113-60a7efc0f9ac

# Step 2: Use the generated UUID in storage command
# Pattern observations with evidence
qdrant-store "Observed: JWT refresh pattern from auth-service successfully reduces session timeout issues. Evidence: 50% reduction in authentication errors across 3 test scenarios. Validation needed: Apply to web-application authentication flow." cross_project_intelligence a870346e-03c7-4622-b113-60a7efc0f9ac

# Relationship mappings
qdrant-store "Relationship: api-gateway nginx patterns directly applicable to web-app reverse proxy setup. Common requirements: SSL termination, rate limiting, auth_request. Validation status: Hypothesis - requires testing in web-app context." cross_project_intelligence [UUID]

# Effectiveness metrics
qdrant-store "Effectiveness: Docker compose .env externalization pattern. Context: Applied across multiple projects. Results: 40% faster deployment, 90% reduction in environment configuration errors. Validation: Proven across 2 projects, ready for framework standardization." cross_project_intelligence [UUID]
```

## 🔄 **Information Flow Lifecycle**

### **📊 Discovery → Validation → Integration**

1. **Discovery Phase** (Intelligence Collection)
   - Session observations stored with evidence level: "hypothesis"
   - Cross-project relationships noted with validation requirements
   - Effectiveness data collected with specific context

2. **Validation Phase** (Intelligence Collection)
   - Patterns tested across multiple projects
   - Evidence level upgraded: "testing" → "validated"
   - Relationship effectiveness quantified

3. **Integration Phase** (Framework Collection)
   - Proven patterns documented in official guides
   - Validated relationships become official recommendations
   - Context documents updated with established status

## ⚠️ **Critical Guidelines**

### **🚫 Avoid Double Storage**
- **Never store the same information in both collections**
- **Use intelligence collection for dynamic discoveries**
- **Use framework collection for established knowledge**
- **Regular migration**: Validated intelligence becomes framework documentation

### **📋 Evidence Requirements**
- **All intelligence entries must include evidence level**
- **Specify validation requirements for each observation**
- **Include context constraints and limitations**
- **Note cross-project applicability with confidence levels**

### **🔗 Linking Strategy**
- **Framework context document references intelligence patterns**
- **Intelligence observations cite related framework components**
- **Cross-reference between collections using specific identifiers**
- **Maintain clear traceability from observation to integration**

## 🎯 **Benefits of This Architecture**

### **🔍 Optimized Retrieval**
- **Specialized search patterns** for different knowledge types
- **Clean separation** prevents information dilution
- **Temporal organization** for pattern evolution tracking

### **📈 Intelligence Evolution**
- **Clear pathway** from observation to official documentation
- **Evidence-based validation** before pattern integration
- **Cross-project learning** without premature conclusions

### **🌐 Ecosystem Growth**
- **Systematic knowledge accumulation** across all managed projects
- **Pattern standardization** based on proven effectiveness
- **Framework evolution** driven by real-world observations
