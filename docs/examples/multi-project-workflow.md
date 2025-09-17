# Multi-Project Development Example

## Overview

This demonstrates realistic daily development workflows using Hish's cross-project intelligence.

## Development Day Scenario

Working across multiple projects with shared learnings:

1. **Performance issue** in React web app
2. **Authentication implementation** for mobile app
3. **API optimization** for high latency
4. **Quality analysis** for testing coverage
5. **Security analysis** for vulnerability assessment
6. **New project setup** with proven patterns

## React Performance Issue

### Initialize Agent Context

```
@prompts/dev_agent/dev_agent_init_prompt.md
```

### Research and Apply Solutions

```
You: "We're experiencing slow page loads in our React app. Research performance optimization patterns across our projects and propose specific improvements."

Agent: "I'll analyze performance patterns from your ecosystem. Looking at your projects, I found several proven optimizations:

From your mobile app: Image lazy loading reduced load times 40%
From your API service: Bundle splitting cut initial load 60%
From your admin dashboard: Virtual scrolling for large data sets
From multiple projects: Core Web Vitals monitoring is standard

Should I implement these patterns adapted for your React app?"

You: "Yes, focus on the lazy loading and bundle splitting first."

Agent: "I'll implement these following your established patterns. The mobile app's intersection observer approach works well, and I can adapt the API service's route-based splitting strategy."
```

### Implementation and Testing

```
Agent: "I've implemented the optimizations using your proven patterns:

- Lazy loading with intersection observer (from mobile app patterns)
- Route-based code splitting (adapted from API service)
- Performance monitoring hooks (following your Core Web Vitals setup)

I can also set up performance tests to measure the improvements. Would you like me to create a test harness using your existing testing patterns?"

You: "Yes, set up the performance tests so we can measure the impact."

Agent: "I'll create performance tests using Lighthouse and Web Vitals measurement. Let me set up the test scripts following your mobile app's performance testing approach."

[After running tests]

You: "Great! The tests show 40% improvement in load times and 60% better Largest Contentful Paint. Document this for future projects."

Agent: "Storing this React optimization pattern with the verified performance data for future reference."
```

### End Session

```
@prompts/dev_agent/dev_agent_session_end_prompt.md
```

Agent captures the performance optimization patterns, implementation details, and measured results for future React projects.

## Mobile App Authentication

### Start New Session

**In a new Cursor conversation thread:**

```
@prompts/dev_agent/dev_agent_init_prompt.md
```

### Authentication Research and Implementation

```
You: "We need to implement user authentication for our new React Native app. Research our existing authentication patterns and propose the best approach."

Agent: "I'll analyze authentication patterns from your other projects. Looking at your ecosystem:

Your web app uses JWT with refresh token rotation
Your API service has OAuth2 with role-based access control
Your admin dashboard implements multi-factor authentication
Multiple projects use secure token storage patterns

For React Native, I recommend adapting your web app's JWT approach but with secure Keychain storage and integration with your existing OAuth2 server."

You: "That sounds right. How do we handle the secure storage differently from web?"

Agent: "React Native requires different secure storage than web localStorage. I'll use your mobile security patterns: Keychain on iOS, Keystore on Android, with the same token refresh logic from your web app."

You: "Implement that approach."

Agent: [Implements authentication] "I've created the authentication system using your established JWT patterns adapted for mobile security. The token management follows your web app patterns but with proper mobile secure storage."
```

### End Session

```
@prompts/dev_agent/dev_agent_session_end_prompt.md
```

Agent captures the mobile authentication implementation, security patterns, and integration approach for future mobile projects.

## API Service Optimization

### Start New Session

**In a new Cursor conversation thread:**

```
@prompts/dev_agent/dev_agent_init_prompt.md
```

### Performance Research and Implementation

```
You: "Our analytics API is experiencing high latency. Research caching and optimization strategies from our other projects."

Agent: "Analyzing performance patterns from your ecosystem. I found several proven approaches:

Your web app uses Redis caching with significant latency reduction
Your admin dashboard has optimized database queries with connection pooling
Your mobile app handles offline scenarios well
Multiple projects use rate limiting and circuit breaker patterns

For your analytics API, I recommend combining Redis caching from your web app with the query optimization patterns from your admin dashboard."

You: "What about the mobile app patterns? Are those relevant here?"

Agent: "Good point. Your mobile app's offline-first approach could help here too. I can add graceful degradation for when the cache is unavailable, plus the rate limiting patterns to prevent overload."

You: "Implement those optimizations."

Agent: [Implements optimizations] "I've added Redis caching following your web app patterns, optimized database queries using your admin dashboard approach, and added rate limiting. The combination should significantly improve both performance and reliability."
```

### End Session

```
@prompts/dev_agent/dev_agent_session_end_prompt.md
```

Agent captures the API optimization techniques, caching strategies, and performance improvements for future API projects.

## Quality Analysis

### Initialize QA Agent

```
@prompts/qa/qa_agent_init_prompt.md
```

### Analyze Testing Coverage

```
You: "I need to assess the testing coverage and quality standards across our projects. Generate a comprehensive quality analysis report with recommendations."

QA Agent: "I'll analyze testing patterns and quality standards across your ecosystem. Based on my analysis, I found several enhancement opportunities:

**Testing Coverage Analysis:**
- Project A: 85% unit test coverage, missing integration tests for API endpoints
- Project B: 92% coverage, excellent E2E test coverage
- Project C: 67% coverage, needs performance testing

**Quality Gate Assessment:**
- All projects have pre-deployment checks
- Performance benchmarks need updating
- Security testing could be enhanced

**Recommendations:**
1. Implement integration tests for Project A API endpoints
2. Add performance testing suite to Project C
3. Update performance benchmarks across all projects
4. Enhance security testing with automated vulnerability scanning

I'll generate a detailed report in `hish/local/project-name/qa_reports/` with specific implementation guidance."
```

### End QA Session

```
@prompts/qa/qa_agent_session_end_prompt.md
```

## Security Analysis

### Initialize Red Team Agent

```
@prompts/red_team/red_team_agent_init_prompt.md
```

### Analyze Security Vulnerabilities

```
You: "I need to conduct a comprehensive security analysis across our projects. Identify vulnerabilities, attack vectors, and provide remediation guidance."

Red Team Agent: "I'll analyze security patterns and vulnerability landscapes across your ecosystem. Based on my analysis, I found several security concerns:

**Vulnerability Assessment:**
- Project A: SQL injection risk in user input handling, missing input validation
- Project B: Weak authentication mechanism, no rate limiting on login attempts
- Project C: Exposed API endpoints without proper authorization checks

**Attack Vector Analysis:**
- Authentication bypass potential in Project B
- Data exfiltration risk through Project A SQL injection
- Privilege escalation opportunities in Project C

**Security Recommendations:**
1. Implement parameterized queries and input validation for Project A
2. Add rate limiting and strengthen authentication for Project B
3. Implement proper authorization middleware for Project C
4. Add security headers and implement OWASP security guidelines

I'll generate a detailed security report in `hish/local/project-name/red_team_reports/` with specific remediation steps and security enhancements."
```

### End Red Team Session

```
@prompts/red_team/red_team_agent_session_end_prompt.md
```

## New Project Architecture

### Start New Session

**In a new Cursor conversation thread:**

```
@prompts/dev_agent/dev_agent_init_prompt.md
```

### Architecture Research and Planning

```
You: "We're starting a new admin dashboard project. Research our best practices across all projects and propose an initial architecture."

Agent: "Analyzing patterns from your ecosystem for admin dashboard development:

Your web app has proven component library and design system patterns
Your mobile app's offline-first data strategy could work for resilience
Your API service has solid role-based access control and audit logging
Multiple projects use consistent performance monitoring

For the admin dashboard, I'd recommend combining your web app's component patterns, the security model from your API service, and monitoring from all projects."

You: "What about data handling? Should we use the offline-first approach from mobile?"

Agent: "For an admin dashboard, offline-first makes sense for resilience. Users often work with reports and data that shouldn't disappear during network issues. I can adapt your mobile app's sync patterns for dashboard use cases."

You: "Sounds good. Set up the initial architecture following those patterns."

Agent: "I'll create the foundation using your proven component library structure, implement role-based access following your API patterns, and add offline data handling adapted from your mobile app approach."
```

### End Session

```
@prompts/dev_agent/dev_agent_session_end_prompt.md
```

Agent captures the architectural decisions, component choices, and cross-project pattern applications for future dashboard projects.

## Knowledge Synthesis

### Cross-Project Pattern Analysis

```
You: "Analyze our ecosystem for emerging patterns and identify opportunities for standardization."

Agent: "Looking across today's work and your project ecosystem, I see clear patterns emerging:

Authentication: JWT with refresh tokens consistently successful across 4 projects
Performance: Redis caching showing reliable improvements in multiple contexts
Security: Role-based access control becoming standard
Monitoring: Core Web Vitals plus custom metrics appearing everywhere

These patterns have proven themselves across different project types and should be considered for standardization."

You: "What would you recommend for standardization?"

Agent: "Based on the evidence from your projects:

1. JWT + refresh tokens for authentication (proven across web, mobile, API)
2. Redis caching for performance (consistent results across contexts)
3. Role-based access control for security (working well in API and admin systems)
4. Standardized monitoring with Core Web Vitals + custom metrics

These have demonstrated value across multiple project types."

You: "Good analysis. Document these patterns as ecosystem standards."

Agent: "I'll document these proven patterns as recommended standards for future projects, with the evidence and context from where they've been successfully applied."
```

### End Session

```
@prompts/dev_agent/dev_agent_session_end_prompt.md
```

Agent captures the pattern analysis, standardization recommendations, and cross-project insights for future ecosystem development.

## Key Benefits Demonstrated

### Cross-Project Learning
- Solutions from one project apply to others when relevant
- Patterns get validated across different contexts
- Known failure modes are avoided in new implementations

### Development Efficiency
- New projects can start with proven patterns
- Less time spent researching basic implementations
- More consistent approaches across projects

### Knowledge Persistence
- Patterns and solutions persist beyond individual sessions
- Context about why certain decisions were made is retained
- Best practices can evolve based on real experience

### Quality Consistency
- Successful patterns tend to propagate across projects
- Standards emerge naturally from proven approaches
- Technical debt patterns can be identified and addressed

## Workflow Summary

### Daily Development Pattern
1. **Start fresh** - New Cursor conversation thread for each project
2. **Initialize** agent with project context (`@prompts/dev_agent/dev_agent_init_prompt.md`)
3. **Research** by asking agents to find existing patterns
4. **Apply** proven solutions adapted to current needs
5. **End session** with knowledge capture (`@prompts/dev_agent/dev_agent_session_end_prompt.md`)
6. **Repeat** - Start new thread for next project

### QA Analysis Pattern
1. **Initialize QA agent** (`@prompts/qa/qa_agent_init_prompt.md`)
2. **Analyze** quality standards and testing coverage
3. **Generate reports** with findings and recommendations
4. **End QA session** with analysis capture (`@prompts/qa/qa_agent_session_end_prompt.md`)

### Red Team Analysis Pattern
1. **Initialize red team agent** (`@prompts/red_team/red_team_agent_init_prompt.md`)
2. **Analyze** security vulnerabilities and attack vectors
3. **Generate security reports** with findings and remediation guidance
4. **End red team session** with analysis capture (`@prompts/red_team/red_team_agent_session_end_prompt.md`)

### Interaction Model
- Natural conversation with agents about development needs
- Agents handle knowledge base searches automatically
- Focus on problem-solving rather than tool usage
- **Start each project in a new conversation thread for clean context**
- Continuous knowledge building through agent guidance

### Realistic Outcomes
- Faster development when patterns apply to new contexts
- More consistent quality when following proven approaches
- Better documentation of decisions and rationale
- Gradual improvement in development practices

---

**This workflow shows realistic daily development using cross-project intelligence and agent assistance.**
