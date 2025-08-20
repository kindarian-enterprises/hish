# 🔄 Agent Management Workflows

This guide provides standard workflows for common agent management scenarios in the Kindarian Cursor Context framework.

## 🚀 **Project Initiation Workflows**

### **Starting a New Project with Agent**

**1. Context Preparation**
```bash
# Create project context
make new-context

# Configure project context
# Edit contexts/project-name/dev_agent_persona.md
# Edit contexts/project-name/project_config.yml
```

**2. Agent Initialization**
```
@contexts/project-name/dev_agent_init_prompt.md

We're starting a new [project type] project. Research our existing patterns for [technology stack] across all projects and propose an initial architecture that leverages our proven approaches.
```

**3. Knowledge Foundation**
```
Before implementing anything, research these areas across our ecosystem:
- Authentication and authorization patterns
- Testing strategies for [technology]
- Deployment and CI/CD approaches
- Error handling and logging patterns
- Performance optimization techniques

Create an initial architectural proposal that incorporates our best practices.
```

**4. Index Project Code (when code exists)**
```bash
make index-repo REPO_PATH=/path/to/project COLLECTION_NAME=project_name_code
```

### **Onboarding Agent to Existing Project**

**1. Context Loading**
```
@contexts/existing-project/dev_agent_init_prompt.md

This is an existing project. Research the current codebase patterns and our historical approaches to similar projects. Familiarize yourself with our established practices for this technology stack.
```

**2. Current State Analysis**
```
Analyze the current state of this project:
- Review the codebase for existing patterns and approaches
- Identify areas that could benefit from patterns used in our other projects
- Look for opportunities to apply cross-project optimizations
- Note any anti-patterns that should be addressed
```

**3. Improvement Recommendations**
```
Based on your analysis and our ecosystem patterns, propose specific improvements that would:
- Apply successful patterns from other projects
- Address technical debt using proven approaches
- Enhance quality using our established standards
- Improve performance using techniques from similar projects
```

## 🔧 **Development Workflow Management**

### **Feature Development Workflow**

**1. Research Phase**
```
We need to implement [feature description]. Research how we've built similar features across our projects and propose an approach that:
- Leverages our proven patterns
- Considers cross-project compatibility
- Follows our established quality standards
- Can be reused in future projects
```

**2. Implementation Guidance**
```
Implement [feature] following these guidelines:
- Apply the research patterns you discovered
- Maintain consistency with our established approaches
- Document any new patterns that emerge
- Store solutions that could benefit other projects
```

**3. Knowledge Capture**
```
After implementing [feature], ensure you:
- Store the solution pattern for future use
- Document any new workflows that emerged
- Create documentation if this represents a reusable approach
- Update any existing patterns that were improved
```

### **Debugging and Problem-Solving Workflow**

**1. Problem Analysis**
```
We're experiencing [problem description]. Research how we've solved similar issues across our projects and propose a debugging strategy that applies our proven diagnostic approaches.
```

**2. Solution Research**
```
Based on the problem analysis, research solutions that:
- Apply debugging patterns from similar issues
- Use our established diagnostic tools and techniques
- Consider solutions that worked in other project contexts
- Avoid approaches that have failed in our ecosystem
```

**3. Resolution Documentation**
```
After resolving the issue:
- Document the debugging process if it was novel or complex
- Store the solution pattern for similar future issues
- Create workflow documentation if the process should be standardized
- Update any existing troubleshooting guides
```

## 📚 **Documentation Creation Workflows**

### **Workflow Documentation Creation**

**When to trigger:**
- Agent solves same type of problem multiple times
- Complex process emerges that should be standardized
- Team needs to replicate successful approaches

**Instructions to agent:**
```
You've now [accomplished task] in multiple contexts. Create a standardized workflow document that captures this methodology so we can:
- Apply it consistently across projects
- Train other agents on this approach
- Avoid reinventing solutions to similar problems
- Build on this foundation for related challenges

Include:
- Decision trees for when to apply this approach
- Step-by-step process documentation
- Common pitfalls and how to avoid them
- Examples from the implementations you've completed
```

### **Architectural Decision Documentation**

**When to trigger:**
- Major technology or design choices are made
- Trade-offs between approaches are evaluated
- Patterns emerge that should be standardized

**Instructions to agent:**
```
Document this architectural decision as a formal ADR (Architecture Decision Record). Include:
- Problem context and requirements
- Alternatives that were considered
- Decision rationale and trade-offs
- Implementation guidelines and examples
- Success criteria and monitoring approaches

Store this so future similar decisions can reference this analysis.
```

### **Anti-Pattern Documentation**

**When to trigger:**
- Approaches fail or cause significant problems
- Debugging reveals systemic design issues
- Performance problems are traced to specific patterns

**Instructions to agent:**
```
This [problem/approach] represents an anti-pattern that should be documented to prevent future occurrences. Create documentation that includes:
- Clear description of the anti-pattern
- Why it fails and what problems it causes
- How to recognize the symptoms
- Correct approaches and alternatives
- Examples of proper implementation

Make this discoverable so future similar situations can avoid this pitfall.
```

## 🎯 **Quality Management Workflows**

### **Code Quality Review Workflow**

**1. Quality Assessment**
```
Review this codebase against our established quality standards. Research quality patterns from our highest-performing projects and identify specific improvements that would:
- Apply proven quality practices
- Address technical debt systematically
- Improve maintainability and readability
- Enhance testing coverage and effectiveness
```

**2. Improvement Implementation**
```
Implement quality improvements following these priorities:
1. Apply patterns that have proven successful in similar projects
2. Address issues that have caused problems in our ecosystem
3. Enhance areas that would benefit most from standardization
4. Document any new quality practices that emerge
```

**3. Standards Evolution**
```
After completing quality improvements:
- Update our quality standards if new practices emerged
- Document any new quality patterns for other projects
- Store approaches that delivered measurable improvements
- Create guidelines if the improvements should be standardized
```

### **Performance Optimization Workflow**

**1. Performance Analysis**
```
Analyze performance characteristics and research optimization strategies from our other projects. Focus on:
- Proven optimization techniques from similar contexts
- Performance patterns that have delivered measurable improvements
- Monitoring and measurement approaches we've used successfully
- Common performance pitfalls to avoid
```

**2. Optimization Implementation**
```
Implement performance optimizations using:
- Proven techniques from similar project contexts
- Our established performance monitoring approaches
- Optimization patterns that align with our architecture
- Measurement strategies to validate improvements
```

**3. Performance Knowledge Capture**
```
Document performance improvements including:
- Specific techniques applied and their impact
- Measurement methodologies and results
- Optimization patterns that could apply to other projects
- Performance monitoring approaches for ongoing validation
```

## 🔄 **Maintenance and Evolution Workflows**

### **Framework Update Workflow**

**When framework or tools are updated:**
```
The framework has been updated. Review changes and:
- Update project contexts to leverage new capabilities
- Research new patterns that are now available
- Identify improvements that can be applied to existing implementations
- Document any migration patterns that emerge
```

### **Knowledge Base Maintenance Workflow**

**Regular knowledge maintenance:**
```
Perform knowledge base maintenance:
- Review recent solutions for quality and completeness
- Identify patterns that should be better documented
- Update outdated approaches with current best practices
- Consolidate related patterns for better discoverability
```

### **Cross-Project Pattern Evolution**

**When patterns evolve across projects:**
```
A pattern has evolved across multiple projects. Research the evolution and:
- Document the improved pattern
- Identify projects that could benefit from the enhancement
- Create migration guidance for updating existing implementations
- Store the evolved pattern for future applications
```

## 📊 **Monitoring and Assessment Workflows**

### **Agent Performance Assessment**

**Monthly agent performance review:**
```
Assess agent performance across these dimensions:
- Consistency in applying established patterns
- Quality of knowledge capture and storage
- Effectiveness in discovering cross-project solutions
- Proactive creation of useful documentation
- Success in applying proven approaches vs. reinventing solutions
```

### **Knowledge Quality Assessment**

**Quarterly knowledge quality review:**
```
Review knowledge base quality:
- Identify knowledge gaps in emerging problem areas
- Assess whether stored solutions are being effectively discovered
- Update outdated patterns with current best practices
- Consolidate fragmented knowledge into coherent patterns
```

---

## 🎯 **Quick Reference Commands**

### **Project Initiation**
```
@contexts/project-name/dev_agent_init_prompt.md
Research [technology] patterns across our ecosystem and propose initial architecture.
```

### **Feature Development**
```
Research how we've implemented [feature type] across projects and propose an approach that leverages proven patterns.
```

### **Problem Solving**
```
Research similar issues across our ecosystem and apply proven diagnostic and resolution approaches.
```

### **Documentation Creation**
```
Create [workflow/ADR/anti-pattern] documentation for this [process/decision/issue] so it can be applied consistently.
```

### **Quality Improvement**
```
Research quality patterns from our best projects and apply proven practices to improve this codebase.
```

---

**These workflows ensure consistent, high-quality agent management while building institutional knowledge that compounds across all projects.**
