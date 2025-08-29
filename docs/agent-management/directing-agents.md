# Directing Agents

## Overview

Working effectively with AI agents is a skill. This guide covers the nuanced art of agent management - when to guide, when to correct, when to step back, and how to get the best results from Cursor + Hish.

**Important**: Files in `local/` are managed by agents. Manual editing can disrupt framework behavior and break context tracking. Use agent workflows and prompts to manage project state.

## The Art of Agent Management

### Understanding Agent Behavior

**Agents are powerful but need guidance**. They can access your entire codebase knowledge but still need human judgment about priorities, context, and trade-offs.

**Key insight**: You're not just asking for code - you're directing an intelligent assistant that can learn from your entire development history.

### The Compound Learning Effect

**Important ROI insight**: Good agent guidance compounds over time. Hish's semantic memory stores your corrections and preferences, making agents progressively smarter and more aligned with each session.

**How it works**:
- **Better guidance this session** → More accurate solutions stored → Better research in future sessions
- **Correcting agent mistakes** → Improved decision patterns → Fewer mistakes over time  
- **Teaching agent preferences** → Stored context about your priorities → More aligned suggestions

**Real example**: Spend 10 minutes teaching an agent your security patterns today, save hours of security reviews for months.

## Essential Agent Management Skills

### 1. Setting Clear Context

**Bad**: "Fix the auth bug"
**Good**: "The login endpoint returns 401 for valid tokens after 15 minutes. This started yesterday after the Redis config change. Check if it's related to token expiration handling."

**Why this works**: Specific context helps the agent focus its knowledge search and avoid irrelevant solutions.

### 2. Knowing When to Guide vs. Let Go

**Guide when**:
- Agent goes down wrong path
- Solution doesn't fit your architecture  
- Agent misses critical requirements

**Let go when**:
- Agent is researching patterns effectively
- Implementation is proceeding correctly
- Agent is storing knowledge appropriately

**Example of good guidance**:
```
Agent: "I found JWT implementations using localStorage..."
You: "Stop - we avoid localStorage for security reasons. Check our secure token storage patterns instead."
```

### 3. Correcting Agent Mistakes

**Immediate correction**:
```
You: "That approach won't work - we're using microservices, not a monolith. Research our service-to-service auth patterns instead."
```

**Context adjustment**:
```
You: "You're on the right track with JWT, but this is for mobile app, not web. Check our React Native secure storage implementations."
```

## Strategic Debugging (Critical Cost-Saving Skill)

**Debugging together**:
```
You: "That should work in theory, but I'm getting CORS errors. Let me check the actual network requests... [investigates] ...okay, the issue is the OPTIONS request. Research our CORS patterns for this case."
```

**Why this matters**: Without concrete debugging data, agents will speculate and rabbit-hole through multiple theories. This wastes time, burns through API calls, and costs money.

**The economics**:
- **Agent speculation**: Multiple rounds of theoretical exploration
- **Manual debugging + targeted agent query**: Direct investigation with focused follow-up
- **Result**: Dramatically more efficient use of both time and API calls

**When to step in and debug manually**:
- **Agent shows circular reasoning**: Keeps returning to same theories despite evidence
- **Agent makes broad assumptions**: Suggests multiple possible causes without focusing
- **Agent requests repetitive information**: Asks for the same debugging steps multiple times  
- **Agent proposes theoretical solutions**: Offers fixes without understanding the actual problem



**Effective manual debugging workflow**:
```
1. You: "Hold on, let me investigate this error directly"
2. [Inspect network tab, check logs, run database queries, etc.]
3. You: "Found it! The real issue is [specific technical finding]. Here's the evidence: [concrete data]. Now research our patterns for handling [specific case]."
4. Agent: [Provides targeted, relevant solutions based on accurate diagnosis]
```

**Examples of when to redirect agent focus**:
```
// Agent suggests overly complex solution
Agent: "We could implement a message queue with Redis and background workers..."
You: "Stop. This is a simple user notification. What's the simplest approach that fits our current architecture?"

// Agent goes off-architecture  
Agent: "Let's add GraphQL to handle this data fetching..."
You: "We're a REST shop with established patterns. Research our existing API patterns for this use case instead."

// Agent proposes new dependencies
Agent: "We should use this new validation library..."
You: "Before adding dependencies, research how we've handled similar validation in other services. Let's stay consistent."
```

**The skill**: Recognize when agents are spinning in unproductive patterns, then provide focused direction to get back on track.

### 4. Effective Direction Patterns

**Start broad, get specific**:
```
1. "Research authentication approaches for this project"
2. "Focus on the JWT + Redis pattern you found"  
3. "Adapt that for our requirements"
```

**Set constraints upfront**:
```
"Implement user registration, but no email verification (no SMTP), needs social login, must work with existing JWT."
```

**Challenge overconfidence**:
```
You: "You seem certain about this. What could go wrong?"
Agent: "Actually, looking at past experiences..."
You: "Good. Research failure modes before we proceed."
```

**Leverage memory**:
```
"Remember the payment service race conditions? Apply those same locking patterns here."
```

## Session Management

### Starting Sessions Right

**Always initialize properly**:
```
@dev_agent_init_prompt.md
```

**Set session expectations**:
```
"I'm working on the payment service today. We need to implement refund processing. This connects to the existing billing system and needs to handle edge cases like partial refunds and failed webhook deliveries."
```

### Maintaining Context During Long Sessions

**Remind agents of progress**:
```
"So far we've implemented the refund calculation logic and basic validation. Now we need to handle the webhook delivery failure scenarios."
```

**Reference earlier decisions**:
```
"Earlier you suggested using the retry pattern from the notification service. Let's implement that approach."
```

### Ending Sessions Effectively

**Capture learnings**:
```
"Before we end, please capture what we learned about refund processing edge cases and store the patterns we developed for handling webhook failures."
```

**Use the session end prompt**:
```
@dev_agent_session_end_prompt.md
```

## When Things Go Wrong

**Agent stuck in loops**: "Let's reset. Here's the situation: [fresh context]. Research from a different angle."

**Agent misses the point**: "Stop. You're solving a different problem. The core issue is [restate clearly]."

**Agent overcomplicates**: "That might work, but our team knows [simpler approach]. Research our existing patterns instead."

**Context gets muddled**: Start fresh with `@dev_agent_init_prompt.md`

## Building Agent Intelligence

**Set priorities explicitly**: "We prioritize maintainability over performance. Focus on readable solutions."

**Use for code review**: "Review against our patterns. Check for security gaps and consistency."

**Share investigation results**: "I found the connection pool is exhausted. Research our connection patterns."

**Set clear boundaries**: "Only modify authentication. Don't touch database layer."

**Leverage memory**: "Remember the payment service patterns? Apply those here."

---

## Why This Matters

**The compound effect**: Good guidance creates progressively smarter agents. Week 1 requires corrections and teaching. Month 6 gets you agents that know your patterns and avoid known pitfalls.

**ROI breakdown**: 
- **Investment**: 5-10 minutes per session teaching patterns
- **Returns**: Cleaner code, better architecture decisions, faster debugging, institutional memory

**Think of it as training a senior engineer** who remembers every pattern, every mistake, and every solution across your entire codebase.

**Key principles**:
1. Be specific, not clever
2. Guide when needed, step back when not
3. Trust but verify
4. Start sessions clean, end with captured learnings

Working with agents is a skill. Start small, build trust, then tackle complex work. The investment in proper guidance pays exponential dividends.
