# Multi-Project Workflow Example

## Overview

This document demonstrates a complete day-in-the-life example of using the Hish framework for cross-project intelligence and knowledge sharing.

## Scenario: Multi-Project Development Day

You're a senior developer working across multiple projects in your organization. Today you need to:

1. **Fix a performance issue** in a React web app
2. **Implement authentication** in a new mobile app
3. **Optimize an API service** that's experiencing high latency
4. **Review a new project** and apply best practices

## Morning: Performance Issue in Web App

### **1. Initialize Agent for Web App**

```
@dev_agent_init_prompt.md
```

The agent loads:
- Universal persona from `dev_agent_persona.md`
- Project-specific context from `local/awesome-web-app/dev_agent_context.md`
- Cross-project knowledge base access

### 2. Research Performance Patterns

```
We're experiencing slow page loads in our React app. Research performance optimization patterns across our projects and propose specific improvements.
```

**Agent Response:**
```
I'll research performance patterns across your ecosystem. Let me query the knowledge base for relevant solutions.

qdrant-find "React performance optimization patterns"
qdrant-find "page load optimization strategies"
qdrant-find "performance bottlenecks in web applications"
```

**Results Found:**
- **Mobile App**: Image lazy loading implementation with 40% load time improvement
- **API Service**: Bundle splitting strategy that reduced initial load by 60%
- **Admin Dashboard**: Virtual scrolling for large data tables
- **Shared Pattern**: Performance monitoring with Core Web Vitals

### 3. Apply Cross-Project Solutions

The agent proposes combining patterns from multiple projects:

```
Based on our ecosystem patterns, here's a comprehensive performance optimization strategy:

1. **Image Optimization** (from Mobile App): Implement lazy loading with intersection observer
2. **Bundle Splitting** (from API Service): Code splitting by routes and components
3. **Virtual Scrolling** (from Admin Dashboard): For large data tables
4. **Performance Monitoring** (from Shared): Core Web Vitals tracking

Let me implement these optimizations following our established patterns.
```

### 4. Store Enhanced Solution

After implementing:

```
qdrant-store "React Performance Optimization Suite: Combined lazy loading (40% improvement), bundle splitting (60% improvement), virtual scrolling, and Core Web Vitals monitoring. Context: React web applications. Implementation: hooks/useLazyLoading.ts, utils/bundleAnalyzer.ts, components/VirtualTable.tsx. Performance: 50% average improvement across metrics."
```

## Mid-Morning: Authentication for New Mobile App

### **1. Switch to Mobile App Context**

```
@dev_agent_init_prompt.md
```

### 2. Research Authentication Patterns

```
We need to implement user authentication for our new React Native app. Research our existing authentication patterns and propose the best approach.
```

**Agent Response:**
```
I'll research authentication patterns across your ecosystem to find the best approach for React Native.

qdrant-find "authentication implementation patterns"
qdrant-find "JWT token management strategies"
qdrant-find "mobile app security patterns"
```

**Results Found:**
- **Web App**: JWT with refresh token rotation (from earlier session)
- **API Service**: OAuth2 server with role-based access control
- **Admin Dashboard**: Multi-factor authentication implementation
- **Shared Pattern**: Secure token storage and automatic refresh

### 3. Adapt Web App Pattern for Mobile

The agent synthesizes the best approach:

```
Based on our ecosystem patterns, here's the optimal authentication strategy for React Native:

1. **JWT Implementation** (from Web App): Use the proven JWT pattern with refresh tokens
2. **Secure Storage** (from Shared): Implement secure token storage using React Native's Keychain
3. **Role-Based Access** (from API Service): Integrate with our existing OAuth2 server
4. **Multi-Factor** (from Admin Dashboard): Add optional MFA for enhanced security

This combines our most successful patterns while adapting them for mobile constraints.
```

### 4. Implement and Document

After implementation:

```
qdrant-store "React Native Authentication: Adapted web app JWT pattern with secure storage, OAuth2 integration, and optional MFA. Context: React Native mobile apps. Implementation: auth/useAuth.ts, auth/secureStorage.ts, auth/mfa.ts. Security: Keychain storage, automatic token refresh, role-based access control."
```

## Afternoon: API Service Optimization

### **1. Switch to API Service Context**

```
@dev_agent_init_prompt.md
```

### 2. Research Performance Patterns

```
Our analytics API is experiencing high latency. Research caching and optimization strategies from our other projects.
```

**Agent Response:**
```
I'll research performance optimization patterns specifically for API services.

qdrant-find "API performance optimization patterns"
qdrant-find "caching strategies for high-traffic services"
qdrant-find "database query optimization approaches"
```

**Results Found:**
- **Web App**: Redis caching layer with 80% latency reduction
- **Mobile App**: Offline-first data strategy with sync
- **Admin Dashboard**: Database query optimization with connection pooling
- **Shared Pattern**: Rate limiting and circuit breaker patterns

### 3. Implement Multi-Project Solution

The agent combines the best patterns:

```
Based on our ecosystem analysis, here's a comprehensive API optimization strategy:

1. **Redis Caching** (from Web App): Implement write-through cache for 80% latency reduction
2. **Query Optimization** (from Admin Dashboard): Add connection pooling and query analysis
3. **Rate Limiting** (from Shared): Implement adaptive rate limiting with circuit breakers
4. **Offline Strategy** (from Mobile App): Add offline data handling for mobile clients

This addresses both server-side performance and client-side resilience.
```

### 4. Document Performance Improvements

After implementation:

```
qdrant-store "API Performance Optimization: Combined Redis caching (80% latency reduction), query optimization (60% improvement), rate limiting, and offline support. Context: High-traffic API services. Implementation: cache/redis.ts, db/connectionPool.ts, middleware/rateLimit.ts. Performance: 70% average latency reduction, 90% uptime improvement."
```

## Late Afternoon: New Project Review

### **1. Initialize for New Project**

```
@dev_agent_init_prompt.md
```

### 2. Apply Ecosystem Best Practices

```
We're starting a new admin dashboard project. Research our best practices across all projects and propose an initial architecture.
```

**Agent Response:**
```
I'll research our ecosystem's best practices for admin dashboards and similar projects.

qdrant-find "admin dashboard architecture patterns"
qdrant-find "data visualization best practices"
qdrant-find "user management system patterns"
```

**Results Found:**
- **Web App**: Component library and design system patterns
- **Mobile App**: Offline-first data strategy
- **API Service**: Role-based access control and audit logging
- **Shared Pattern**: Performance monitoring and error tracking

### 3. Propose Comprehensive Architecture

The agent synthesizes the best approach:

```
Based on our ecosystem analysis, here's the optimal architecture for the admin dashboard:

1. **Component Library** (from Web App): Reuse proven UI components and design system
2. **Data Strategy** (from Mobile App): Implement offline-first with real-time sync
3. **Security** (from API Service): Role-based access control with comprehensive audit logging
4. **Monitoring** (from Shared): Performance tracking, error monitoring, and user analytics

This architecture leverages our most successful patterns while ensuring consistency across the ecosystem.
```

### 4. Document Architectural Decision

```
qdrant-store "Admin Dashboard Architecture: Combines component library (reusability), offline-first data (resilience), role-based security (compliance), and comprehensive monitoring (observability). Context: Admin dashboard applications. Architecture: Component-driven UI, offline-first data layer, security-first backend, monitoring throughout. Benefits: 80% faster development, consistent UX, enterprise security, full observability."
```

## Evening: Knowledge Synthesis

### 1. Cross-Project Pattern Analysis

```
Analyze our ecosystem for emerging patterns and identify opportunities for standardization.
```

**Agent Response:**
```
I'll analyze our ecosystem for patterns that could benefit from standardization.

qdrant-find "authentication patterns across projects"
qdrant-find "performance optimization approaches"
qdrant-find "testing strategies and coverage patterns"
```

**Analysis Results:**
- **Authentication**: JWT + refresh tokens emerging as standard across 4 projects
- **Performance**: Redis caching showing 70-80% improvement consistently
- **Testing**: Integration test patterns with 90%+ coverage showing best results
- **Monitoring**: Core Web Vitals + custom metrics becoming standard

### 2. Propose Standardization

```
Based on our ecosystem analysis, here are the patterns that should become standards:

1. **Authentication Standard**: JWT with refresh tokens, secure storage, role-based access
2. **Performance Standard**: Redis caching layer, query optimization, rate limiting
3. **Testing Standard**: Integration tests with 90%+ coverage, performance testing
4. **Monitoring Standard**: Core Web Vitals + custom metrics + error tracking

These patterns have proven successful across multiple projects and should be standardized.
```

### 3. Update Shared Knowledge

```
qdrant-store "Ecosystem Standards: Authentication (JWT + refresh + roles), Performance (Redis + optimization + monitoring), Testing (integration + coverage + performance), Monitoring (Core Web Vitals + custom + errors). Context: All projects. Benefits: Consistent quality, faster development, shared learning, reduced technical debt. Implementation: Standard libraries, shared components, common patterns."
```

## Key Benefits Demonstrated

### 1. **Cross-Project Learning**
- Solutions from one project immediately benefit others
- Patterns improve through cross-project validation
- Anti-patterns are avoided across the ecosystem

### 2. **Accelerated Development**
- New projects start with proven patterns
- No need to reinvent solutions
- Consistent quality across all projects

### 3. **Institutional Memory**
- Knowledge persists beyond individual developers
- Patterns evolve based on real-world usage
- Best practices become organizational standards

### 4. **Quality Multiplication**
- Each project makes all projects better
- Solutions improve through cross-project application
- Technical debt is addressed systematically

## Workflow Summary

### Daily Pattern
1. **Initialize** agent with project context
2. **Research** existing patterns across ecosystem
3. **Apply** proven solutions with adaptations
4. **Store** enhanced solutions for future use
5. **Synthesize** emerging patterns for standardization

### Tools Used
- `@dev_agent_init_prompt.md` - Universal initialization protocol
- `qdrant-find "query"` - Pattern discovery across projects
- `qdrant-store "solution"` - Knowledge capture and sharing
- Cross-project pattern analysis and synthesis

### Results Achieved
- **Performance**: 50-80% improvements across projects
- **Development Speed**: 80% faster with proven patterns
- **Quality**: Consistent standards across ecosystem
- **Knowledge**: Continuous learning and improvement

---

**This workflow demonstrates how the Hish framework transforms individual project development into ecosystem-wide intelligence and continuous improvement.**
