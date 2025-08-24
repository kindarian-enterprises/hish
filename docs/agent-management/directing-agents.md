# Directing Agents

## Overview

This guide explains how to effectively direct and manage development agents within the Hish framework.

### **Agent Initialization**

To initialize an agent for a specific project:

```
@dev_agent_init_prompt.md
```

The agent will:
- Load the universal persona from `dev_agent_persona.md`
- Load project-specific context from `local/your-project-name/dev_agent_context.md`
- Be ready to operate with both universal intelligence and project-specific knowledge

### Project Context Discovery

Agents automatically discover:
- Project boundaries and relationships
- Technology stacks and patterns
- Current development status
- Historical achievements and issues

## Directing Agent Behavior

### Research and Discovery

```
Research authentication patterns across our projects and propose an approach for this context that leverages our proven solutions.
```

The agent will:
- Query the knowledge base with `qdrant-find`
- Analyze patterns across all indexed projects
- Propose solutions combining best practices
- Store new insights with `qdrant-store`

### Implementation Guidance

```
Implement user authentication following these guidelines:
- Apply the research patterns you discovered
- Maintain consistency with our established approaches
- Document any new patterns that emerge
- Store solutions that could benefit other projects
```

### Quality Assurance

```
Review this implementation against our established quality standards:
- Apply proven quality practices from similar projects
- Address any technical debt using proven approaches
- Ensure consistency with our architectural patterns
- Document any new quality practices that emerge
```

## Knowledge Management

### Storing Solutions

```
qdrant-store "Solution: JWT refresh token rotation - Implemented secure token management with Redis blacklist. Context: Web API authentication. Performance: <50ms response time. Files: auth/middleware.py, auth/models.py"
```

### Finding Patterns

```
qdrant-find "authentication implementation patterns"
qdrant-find "error handling approaches for APIs"
qdrant-find "testing strategies for [project type]"
```

## Cross-Project Intelligence

### Pattern Discovery

Agents can discover patterns from:
- All indexed code repositories
- All project contexts in `local/`
- Framework documentation and examples
- Framework examples in `contexts/`

### Solution Adaptation

When an agent finds a pattern from another project:
1. **Analyze Context**: Understand when and why the pattern was used
2. **Adapt for Current Project**: Modify the pattern for current technology and requirements
3. **Validate Approach**: Ensure the adaptation maintains quality standards
4. **Store Enhanced Solution**: Contribute the improved pattern back to the knowledge base

## Agent Workflows

### Feature Development

```
We need to implement [feature description]. Research how we've built similar features across our projects and propose an approach that:
- Leverages our proven patterns
- Considers cross-project compatibility
- Follows our established quality standards
- Can be reused in future projects
```

### Problem Solving

```
We're experiencing [problem description]. Research how we've solved similar issues across our projects and propose a debugging strategy that applies our proven diagnostic approaches.
```

### Architecture Decisions

```
We need to make an architectural decision about [topic]. Research our historical approaches and the trade-offs we've considered. Propose a solution that:
- Builds on our proven patterns
- Avoids known pitfalls
- Maintains consistency with our ecosystem
- Can be applied to similar future decisions
```

## Quality Management

### Code Review

```
Review this codebase against our established quality standards. Research quality patterns from our highest-performing projects and identify specific improvements that would:
- Apply proven quality practices
- Address technical debt systematically
- Improve maintainability and readability
- Enhance testing coverage and effectiveness
```

### Performance Optimization

```
Analyze performance characteristics and research optimization strategies from our other projects. Focus on:
- Proven optimization techniques from similar contexts
- Performance patterns that have delivered measurable improvements
- Monitoring and measurement approaches we've used successfully
- Common performance pitfalls to avoid
```

## Best Practices

### Effective Direction

1. **Be Specific**: Provide clear context about what you want the agent to accomplish
2. **Leverage Knowledge**: Ask the agent to research existing patterns before implementing
3. **Encourage Storage**: Prompt the agent to store successful solutions for future use
4. **Cross-Project Thinking**: Encourage the agent to look beyond the current project

### Knowledge Capture

1. **Store Solutions**: Always store successful implementations with `qdrant-store`
2. **Document Context**: Include when and why a solution works
3. **Performance Metrics**: Include measurable improvements when possible
4. **File References**: Reference specific files for implementation details

### Quality Standards

1. **Consistency**: Maintain consistency with established patterns across projects
2. **Documentation**: Document new patterns and approaches as they emerge
3. **Validation**: Test solutions against known quality standards
4. **Evolution**: Allow patterns to evolve based on real-world feedback

## Troubleshooting

### Common Issues

**Agent doesn't find relevant patterns:**
- Ensure your code repositories are indexed
- Check that project contexts are properly set up
- Verify the knowledge base contains relevant content

**Agent suggests inappropriate solutions:**
- Provide more context about your specific requirements
- Ask the agent to research similar contexts more thoroughly
- Guide the agent to focus on relevant technology stacks

**Knowledge isn't being stored:**
- Ensure the agent has access to `qdrant-store`
- Check that the MCP integration is working properly
- Verify the agent is following storage protocols

## Advanced Techniques

### Multi-Project Analysis

```
Analyze our entire ecosystem for [topic] and identify:
- Common patterns and their success rates
- Technology-specific approaches
- Performance characteristics across projects
- Opportunities for standardization
```

### Pattern Evolution

```
Research how [pattern] has evolved across our projects and identify:
- Improvements that have been made
- Contexts where the pattern works best
- Limitations and alternatives
- Opportunities for further enhancement
```

### Knowledge Synthesis

```
Combine insights from multiple projects to create a comprehensive approach for [topic]:
- Identify the best elements from each implementation
- Create a unified solution that addresses all contexts
- Document when to use each variation
- Store the synthesized approach for future use
```

## **Workflow and Process Management**

### **Local Workflows Directory Structure**

The framework creates a `local/workflows-and-processes/` directory that contains:
- **Workflow files**: Recorded workflows from actual development work
- **Process documentation**: Best practices and process improvements

**⚠️ IMPORTANT**: Users should NOT manually create or edit workflow files. Instead, agents should manage all workflow documentation.

### **Agent Workflow Management Responsibilities**

#### **1. Workflow Recording**
When a user completes a task successfully, the agent should:

1. **Analyze the accomplishment**: Understand what was achieved and how
2. **Document the workflow**: Create a detailed workflow file in `local/workflows-and-processes/`
3. **Store in knowledge base**: Use `qdrant-store` to make the workflow discoverable
4. **Update workflow index**: Ensure the workflow is properly categorized and searchable

**Example workflow recording prompt**:
```
"Please record this workflow for future reference. We just successfully implemented JWT authentication with refresh tokens, including proper error handling and Redis blacklisting."
```

#### **2. Workflow Updates**
When users discover improvements or new learnings, agents should:

1. **Review existing workflows**: Find relevant workflow files
2. **Incorporate new information**: Update workflows with learnings
3. **Document improvements**: Add new sections or modify existing content
4. **Store enhanced knowledge**: Update the knowledge base with improvements

**Example workflow update prompt**:
```
"Please update the JWT authentication workflow with what we learned about clock skew issues between services."
```

### **Workflow File Structure**

#### **Workflow Format**
```markdown
# [Workflow Name]

## Purpose
Brief description of what this workflow accomplishes

## Prerequisites
- Required tools, dependencies, or setup

## Steps
1. **Step 1**: Detailed description
   - Sub-steps if needed
   - Expected outcomes

2. **Step 2**: Next action
   - Any decision points
   - Alternative approaches

## Validation
- How to verify the workflow succeeded
- Common failure points and solutions

## Context
- When to use this workflow
- Related workflows or patterns
- Cross-project applicability

## Knowledge Integration
- How this workflow contributes to the ecosystem
- Related patterns from other projects
```

### **Workflow Lifecycle Management**

#### **Discovery Phase**
- Agents identify workflow opportunities during development
- Recognize when tasks could benefit from documentation
- Suggest workflow recording when appropriate

#### **Recording Phase**
- Document workflows with full context and rationale
- Include decision points and alternatives considered
- Store in the workflows directory

#### **Refinement Phase**
- Update workflows based on new learnings
- Incorporate feedback from other projects
- Evolve workflows based on usage patterns

#### **Reuse Phase**
- Apply workflows to similar future tasks
- Adapt workflows to new contexts
- Share workflows across projects

#### **Evolution Phase**
- Continuously improve workflows based on outcomes
- Merge similar workflows when appropriate
- Archive outdated workflows

### **Knowledge Base Integration**

#### **Automatic Indexing**
- All workflows are automatically indexed in the RAG system
- Available for cross-project discovery via `qdrant-find`
- Enhanced with learnings from other projects

#### **Cross-Project Learning**
- Workflows from one project can benefit others
- Patterns discovered in one context can be applied elsewhere
- Knowledge evolves through real-world usage

#### **Quality Assurance**
- Agents validate workflows against best practices
- Ensure workflows are complete and actionable
- Maintain consistency across the ecosystem

### **User Interaction Patterns**

#### **Proactive Workflow Management**
Agents should proactively:
- Suggest workflow recording when tasks are completed
- Identify opportunities for workflow improvement
- Maintain workflow quality and relevance

#### **Reactive Workflow Support**
Agents should respond to user requests by:
- Recording workflows as requested
- Updating existing workflows with new information
- Providing workflow guidance and examples

#### **Workflow Discovery**
Agents should help users:
- Find relevant workflows for current tasks
- Understand how workflows can be adapted
- Discover related patterns from other projects
- Learn from workflow evolution and improvements

---

**Key Principle**: Agents are responsible for all workflow documentation. Users focus on development work while agents maintain institutional knowledge through structured workflow management.

**Effective agent direction transforms your development workflow from reactive problem-solving to proactive, knowledge-driven engineering. Use these techniques to maximize the value of your cross-project intelligence.**
