# 🔧 **HISH AGENT TROUBLESHOOTING GUIDE**

## 🎯 Purpose
Error recovery, problem resolution, and session continuity procedures for Hish framework operations.

---

## 🚀 **Quick Recovery Commands**

### **Framework Service Issues**
```bash
# Check service health
make health

# Check logs for errors
make logs

# Complete service rebuild
make clean
docker compose -f compose.rag.yml up -d
```

### **MCP Connection Issues**
```bash
# Regenerate Cursor MCP configuration
make setup-cursor

# Restart Cursor application after config update
# Check MCP server status
make mcp

# Verify environment configuration
cat env.mcp
```

### **Knowledge Base Issues**
```bash
# List current collections
make collections

# Complete knowledge base rebuild
make clean && make index

# Reindex specific contexts
./reindex context1 context2

# Backup knowledge base
make backup
```

---

## 📊 **Context Recovery Procedures**

### **Lost Session Context**
If agent loses awareness of current project or framework state:

1. **Reload Core Identity**
   ```
   Read: dev_agent_persona.md
   Read: local/dev_agent_framework_context.md
   ```

2. **Identify Current Project**
   ```bash
   # Check available project contexts
   ls local/*/dev_agent_context.md

   # Read specific project context
   Read: local/[project-name]/dev_agent_context.md
   ```

3. **Restore Operational Wisdom**
   ```bash
   qdrant-find "current session patterns" hish_framework
   qdrant-find "recent project work" cross_project_intelligence
   ```

### **Historical Data Recovery**
Protocol for recovering from context corruption or timestamp issues:

1. **Verify Current State**
   ```bash
   # Get verified timestamp
   date -u

   # Check context file integrity
   grep "verified_datetime" local/*/dev_agent_context.md
   ```

2. **Reconstruct Missing Context**
   ```bash
   # Query for recent activities
   qdrant-find "recent achievements" hish_framework
   qdrant-find "recent patterns" cross_project_intelligence

   # Check git history for file changes
   git log --oneline --since="1 week ago" local/
   ```

3. **Update Context with Recovery Note**
   ```
   recovery_YYYY_MM_DD_HH_MM_SS_context_restored {
     verified_datetime: [actual_timestamp];
     recovery_reason: [what_was_lost];
     restoration_method: [how_recovered];
     data_integrity: [confidence_level]
   }
   ```

---

## 🔄 **Knowledge Storage Troubleshooting**

### **qdrant-store Command Failures**

**UUID Requirements for cross_project_intelligence:**
```bash
# Generate UUID for intelligence storage
python3 -c "import uuid; print(uuid.uuid4())"

# Retry storage with proper UUID
qdrant-store "content..." cross_project_intelligence [generated-uuid]
```

**Collection Name Validation:**
```bash
# List available collections
make collections

# Use correct collection names:
# - hish_framework (framework docs)
# - {project-name}_code (project code)
# - cross_project_intelligence (observations)
```

**Content Format Issues:**
```bash
# Ensure content is properly quoted
qdrant-store "Solution: Component authentication - JWT implementation with refresh tokens" hish_framework

# Avoid special characters that break storage
# Use descriptive, searchable content
```

### **qdrant-find Query Issues**

**Empty Results Troubleshooting:**
```bash
# Check collection exists
make collections

# Try broader search terms
qdrant-find "authentication" hish_framework
qdrant-find "JWT" {project}_code

# Check if content was indexed
qdrant-find "recent patterns" cross_project_intelligence
```

**Query Optimization:**
```bash
# Use specific technical terms
qdrant-find "JWT token validation patterns" hish_framework

# Search multiple collections
qdrant-find "error handling" hish_framework
qdrant-find "error handling" {project}_code
qdrant-find "error handling" cross_project_intelligence

# Use domain-specific language
qdrant-find "React component performance optimization" {project}_code
```

---

## 🏗️ **Protocol Violation Recovery**

### **Timestamp Corruption Recovery**
When timestamps are inaccurate or fictional:

1. **Stop Further Updates**
   - Do not add more entries until verified
   - Assess scope of timestamp issues

2. **Generate Verified Timestamp**
   ```bash
   # Get current UTC timestamp
   date -u
   # OR
   curl -s http://worldtimeapi.org/api/timezone/UTC
   ```

3. **Add Recovery Entry**
   ```
   timestamp_recovery_YYYY_MM_DD_HH_MM_SS {
     verified_datetime: [actual_system_output];
     issue: timestamp_accuracy_violation;
     recovery_action: verified_timestamp_implementation;
     forward_compliance: committed_to_accurate_timestamps
   }
   ```

### **Historical Data Preservation Issues**
When data is accidentally removed or overwritten:

1. **Check Git History**
   ```bash
   git log --oneline local/[affected-file]
   git show [commit-hash]:[file-path]
   ```

2. **Restore from Version Control**
   ```bash
   git checkout [commit-hash] -- local/[affected-file]
   # OR recover specific sections manually
   ```

3. **Document Recovery**
   ```
   data_recovery_YYYY_MM_DD_HH_MM_SS {
     verified_datetime: [timestamp];
     recovered_data: [what_was_restored];
     recovery_method: [git_checkout|manual_reconstruction];
     data_integrity: [confidence_assessment]
   }
   ```

---

## 🔍 **Common Error Patterns**

### **Docker/Service Issues**
```bash
# Port conflicts
docker ps  # Check running containers
lsof -i :6333  # Check Qdrant port usage

# Permission issues
ls -la local/  # Check directory permissions
docker logs qdrant  # Check container logs

# Network connectivity
curl http://localhost:6333/collections  # Test Qdrant access
```

### **Python/Indexing Issues**
```bash
# Virtual environment problems
which python3
pip list | grep -E "(llama|qdrant|sentence)"

# Index creation failures
make clean  # Clear existing index
make index  # Rebuild from scratch

# Memory issues during indexing
free -h  # Check available memory
# Consider smaller chunk sizes in indexer config
```

### **MCP Integration Issues**
```bash
# Cursor settings verification
cat ~/.cursor-tabs/settings.json | grep mcp

# MCP server startup
make mcp  # Start server manually
ps aux | grep llamaindex  # Check if server running

# Environment variable issues
cat env.mcp  # Verify configuration
source env.mcp && make mcp  # Test with explicit environment
```

---

## 📋 **Prevention Strategies**

### **Maintain Session Continuity**
- Always verify timestamps before context updates
- Read existing context completely before modifications
- Use exact command patterns from framework indexes
- Store successful patterns immediately after validation

### **Prevent Knowledge Loss**
- Regular `make backup` operations
- Commit context changes to git frequently
- Document decision rationale with evidence
- Store patterns with cross-project applicability notes

### **Quality Assurance**
- Use multi-collection searches for comprehensive coverage
- Validate patterns against known anti-patterns
- Test stored knowledge through actual application
- Update patterns based on real-world outcomes

---

## 🎯 **Emergency Recovery Checklist**

When framework is completely non-functional:

- [ ] Check Docker services: `make health`
- [ ] Restart framework: `make clean && docker compose -f compose.rag.yml up -d`
- [ ] Regenerate MCP config: `make setup-cursor`
- [ ] Restart Cursor application
- [ ] Test basic functionality: `qdrant-find "test" hish_framework`
- [ ] Reload agent context: Read local/dev_agent_persona.md and local/dev_agent_framework_context.md
- [ ] Restore session state through knowledge queries
- [ ] Document recovery process for future reference

**Remember: Following protocols creates resilience. Every recovery strengthens the framework's robustness.**
