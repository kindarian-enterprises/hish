#!/bin/bash
# Hish - New Project Context Setup
# Creates a new project context within the framework (not a separate repository)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Ensure local directory exists (gitignored)
mkdir -p local

# Create local workflows directory structure (first time only, for entire local ecosystem)
if [[ ! -d "local/workflows-and-processes" ]]; then
    mkdir -p "local/workflows-and-processes"

    # Create initial workflows README
    cat > "local/workflows-and-processes/README.md" << EOF
# Local Workflows and Processes

This directory contains workflows and processes specific to your development ecosystem.

## 🚀 **How to Use This Directory**

**⚠️ IMPORTANT: Do NOT manually create or edit workflow files!**

Instead, ask your development agent to:
- Record new workflows as you work
- Update existing workflows based on new learnings
- Document process improvements and best practices

## 📝 **Agent-Controlled Workflow Management**

### **Recording New Workflows**
When you complete a task successfully, ask your agent:
> "Please record this workflow for future reference"

The agent will:
1. Analyze what you accomplished
2. Document the steps taken
3. Store the workflow in this directory
4. Update the workflow index

### **Updating Existing Workflows**
When you discover improvements, ask your agent:
> "Please update the [workflow name] workflow with what we learned"

The agent will:
1. Review the existing workflow
2. Incorporate new learnings
3. Update the workflow file
4. Store the improvement in the knowledge base

## 🔄 **Workflow Lifecycle**

1. **Discovery**: Agent identifies workflow opportunities during development
2. **Recording**: Agent documents the workflow with full context
3. **Refinement**: Agent updates workflows based on new learnings
4. **Reuse**: Agent applies workflows to similar future tasks
5. **Evolution**: Agent continuously improves workflows based on outcomes

## 📚 **Knowledge Integration**

All workflows are automatically:
- Indexed in the RAG knowledge base
- Available for cross-project discovery
- Enhanced with learnings from other projects
- Validated against best practices

---

**Remember: Let your agent do the workflow management - focus on your development work!**
EOF

    print_success "Created local workflows directory structure"
fi

# Initialize workflow indexes (first time only, for entire local ecosystem)
if [[ ! -d "local/workflow-indexes" ]]; then
    mkdir -p "local/workflow-indexes"

    # Copy workflow index templates
    if [[ -d "templates/workflow-indexes" ]]; then
        cp templates/workflow-indexes/* local/workflow-indexes/
        print_success "Initialized workflow indexes from templates"
    else
        print_warning "Workflow index templates not found in templates/workflow-indexes/"
    fi
fi

# Copy style and philosophy directives (first time only, for entire local ecosystem)
if [[ ! -d "local/style-and-philosophy" ]]; then
    mkdir -p "local/style-and-philosophy"

    # Copy agent directive templates
    if [[ -d "templates/style-and-philosophy" ]]; then
        cp templates/style-and-philosophy/* local/style-and-philosophy/
        print_success "Initialized agent style and philosophy directives from templates"
    else
        print_warning "Agent directive templates not found in templates/style-and-philosophy/"
    fi
fi

# Initialize framework context file (first time only, for entire local ecosystem)
if [[ ! -f "local/dev_agent_framework_context.md" ]]; then
    # Copy framework context template
    if [[ -f "templates/context/dev_agent_framework_context_template.md" ]]; then
        cp "templates/context/dev_agent_framework_context_template.md" "local/dev_agent_framework_context.md"
        print_success "Initialized framework context from template"
    else
        print_warning "Framework context template not found in templates/context/"
    fi
fi

# Initialize agent templates (first time only, for entire local ecosystem)
if [[ ! -f "local/dev_agent_persona.md" ]]; then
    if [[ -f "templates/dev_agent_persona.md" ]]; then
        cp "templates/dev_agent_persona.md" "local/dev_agent_persona.md"
        print_success "Copied agent persona from template"
    else
        print_warning "Agent persona template not found in templates/"
    fi
fi

if [[ ! -f "local/dev_agent_workflow_guide.md" ]]; then
    if [[ -f "templates/dev_agent_workflow_guide.md" ]]; then
        cp "templates/dev_agent_workflow_guide.md" "local/dev_agent_workflow_guide.md"
        print_success "Copied workflow guide from template"
    else
        print_warning "Workflow guide template not found in templates/"
    fi
fi

if [[ ! -f "local/dev_agent_troubleshooting.md" ]]; then
    if [[ -f "templates/dev_agent_troubleshooting.md" ]]; then
        cp "templates/dev_agent_troubleshooting.md" "local/dev_agent_troubleshooting.md"
        print_success "Copied troubleshooting guide from template"
    else
        print_warning "Troubleshooting guide template not found in templates/"
    fi
fi

echo "🚀 Hish - New Project Context Setup"
echo "========================================================="
echo "This creates a new project context within the framework."
echo "Your code repositories remain separate from this context management system."
echo "Contexts are created in the 'local/' directory (gitignored for local changes)."
echo

# Get essential project information
read -p "Enter project name (e.g., 'awesome-web-app'): " PROJECT_NAME
read -p "Enter path to code repository: " REPO_PATH

# Set reasonable defaults
PROJECT_DESC="Development context for $PROJECT_NAME"
TECH_STACK="Mixed"
AGENT_ROLE="Full-stack developer"
PROJECT_TYPE="other"

# Set defaults if empty
PROJECT_NAME=${PROJECT_NAME:-"new-project"}
PROJECT_DESC=${PROJECT_DESC:-"A modern software project"}
TECH_STACK=${TECH_STACK:-"Modern Development Stack"}
AGENT_ROLE=${AGENT_ROLE:-"senior software engineer"}
PROJECT_TYPE=${PROJECT_TYPE:-"web_app"}
REPO_PATH=${REPO_PATH:-""}

# Sanitize project name for directory
PROJECT_DIR_NAME=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONTEXT_DIR="local/$PROJECT_DIR_NAME"

echo
print_status "Setting up project context:"
echo "  Project Name: $PROJECT_NAME"
echo "  Code Repository: $REPO_PATH"
echo "  Context Directory: $CONTEXT_DIR"
echo

# Check if context already exists
if [[ -d "$CONTEXT_DIR" ]]; then
    print_warning "Context directory '$CONTEXT_DIR' already exists!"
    read -p "Continue and overwrite? (y/N): " OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
        print_warning "Setup cancelled"
        exit 0
    fi
fi

read -p "Continue? (y/N): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    print_warning "Setup cancelled"
    exit 0
fi

echo

# Create context directory
print_status "Creating project context directory..."
mkdir -p "$CONTEXT_DIR"

# Store repository path for automatic indexing
if [[ -n "$REPO_PATH" ]]; then
    echo "$REPO_PATH" > "$CONTEXT_DIR/repo_path.txt"
    print_success "Repository path stored: $REPO_PATH"
fi

# Check if required templates exist
if [[ ! -f "templates/context/dev_agent_context_template.md" ]]; then
    print_error "Required template not found: templates/context/dev_agent_context_template.md"
    exit 1
fi

# Copy template files
cp "templates/context/dev_agent_context_template.md" "$CONTEXT_DIR/dev_agent_context.md"

# Update context template with project details
sed -i.bak "s/\[PROJECT NAME\]/$PROJECT_NAME/g" "$CONTEXT_DIR/dev_agent_context.md"
sed -i.bak "s/\[Project Name\]/$PROJECT_NAME/g" "$CONTEXT_DIR/dev_agent_context.md"
sed -i.bak "s/\[PROJECT TYPE\]/$PROJECT_TYPE/g" "$CONTEXT_DIR/dev_agent_context.md"
sed -i.bak "s/\[TECH STACK\]/$TECH_STACK/g" "$CONTEXT_DIR/dev_agent_context.md"
sed -i.bak "s/\[AGENT ROLE\]/$AGENT_ROLE/g" "$CONTEXT_DIR/dev_agent_context.md"
sed -i.bak "s/\[PROJECT DESC\]/$PROJECT_DESC/g" "$CONTEXT_DIR/dev_agent_context.md"

# Remove backup files
rm -f "$CONTEXT_DIR"/*.bak

print_success "Templates customized with project information"

# Create context README
print_status "Creating context documentation..."

cat > "$CONTEXT_DIR/README.md" << EOF
# $PROJECT_NAME - Development Context

This directory contains the development agent context for **$PROJECT_NAME** within the Hish framework.

## 📁 **Context Structure**

- **\`dev_agent_context.md\`** - Project state, achievements, issues, and historical tracking
- **\`README.md\`** - This documentation

**Note**: The following files are now universal and shared across all projects:
- **\`dev_agent_persona.md\`** - Universal dev agent persona (top-level)
- **\`dev_agent_init_prompt.md\`** - Universal initialization protocol (top-level)
- **\`dev_agent_session_end_prompt.md\`** - Universal session end protocol (top-level)

## 🚀 **Usage in Cursor**

1. **Open the framework**: Open the \`hish\` directory in Cursor
2. **Initialize agent**: Reference the universal init prompt: \`@dev_agent_init_prompt.md\`
3. **Load project context**: The agent will automatically load project-specific context from \`dev_agent_context.md\`
4. **Cross-project queries**: Use RAG to discover patterns from other projects:
   - \`qdrant-find "authentication patterns"\`
   - \`qdrant-find "testing strategies"\`

## 📊 **Project Information**

- **Name**: $PROJECT_NAME
- **Created**: $(date)

## 🔗 **Code Repository Setup**

1. **Index your code** for RAG knowledge discovery:
   Use: \`make index-repo REPO_PATH=/path/to/your/code COLLECTION_NAME=${PROJECT_DIR_NAME}_code\`

## 🧠 **Cross-Project Learning**

This context benefits from and contributes to the shared knowledge base:

### **Learns From**
- Authentication patterns from all projects
- Testing strategies from similar project types
- Performance optimization techniques
- Architecture patterns from the entire ecosystem

### **Contributes**
- $TECH_STACK implementation patterns
- $PROJECT_TYPE specific solutions
- Testing approaches for this domain
- Performance optimizations discovered

## 📚 **Additional Resources**

- [Framework Documentation](../../README.md) - Complete framework overview
- [Getting Started Guide](../../docs/setup/getting-started.md) - Setup instructions
- [Agent Management](../../docs/agent-management/directing-agents.md) - How to work with agents
- [Framework Examples](../../contexts/) - Example project contexts
- [Local Workflows](../../workflows-and-processes/README.md) - Your project-specific workflows

---

*This project context is part of the Hish framework enabling cross-project knowledge sharing and institutional learning.*
EOF

print_success "Context documentation created: $CONTEXT_DIR/README.md"

# Ask about code repository indexing
echo
read -p "Do you want to index all repositories now? (y/N): " INDEX_CODE

if [[ "$INDEX_CODE" =~ ^[Yy]$ ]]; then
    print_status "Indexing framework docs and all project repositories (host-based)..."
    if make index; then
        print_success "All repositories indexed successfully"
    else
        print_warning "Indexing failed. Make sure you have Python dependencies installed."
        print_warning "See docs/setup/virtual-environment-guide.md for setup instructions."
        print_warning "You can run indexing manually later with: make index"
    fi
fi

echo
print_success "🎉 Project context '$PROJECT_NAME' created successfully!"
echo
print_status "Context Location: $CONTEXT_DIR"
echo
print_status "Next steps:"
echo "  1. Update $CONTEXT_DIR/dev_agent_context.md with current project state"
echo "  2. In Cursor (with hish open): @dev_agent_init_prompt.md"
echo "  3. Start using cross-project knowledge queries:"
echo "     - qdrant-find \"authentication patterns\""
echo "     - qdrant-find \"testing strategies\""
echo "     - qdrant-store \"your solutions for future projects\""
echo
print_status "The universal dev agent persona and protocols are now available:"
echo "  - @dev_agent_persona.md - Universal dev agent persona"
echo "  - @dev_agent_init_prompt.md - Universal initialization protocol"
echo "  - @dev_agent_session_end_prompt.md - Universal session end protocol"
echo
print_status "Your project will now benefit from and contribute to the shared knowledge ecosystem!"
echo
print_status "Note: This context is in the 'local/' directory (gitignored) so you can make local changes"
echo "while still consuming framework updates from the main repository."
echo
