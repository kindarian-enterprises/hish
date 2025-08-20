#!/bin/bash
# Kindarian Cursor Context - New Project Context Setup
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

# Check if we're in the kindarian-cursor-context directory
if [[ ! -f "templates/persona/dev_agent_persona_template.md" ]]; then
    print_error "This script must be run from the kindarian-cursor-context directory"
    exit 1
fi

# Ensure contexts directory exists
mkdir -p contexts

echo "🚀 Kindarian Cursor Context - New Project Context Setup"
echo "========================================================="
echo "This creates a new project context within the framework."
echo "Your code repositories remain separate from this context management system."
echo

# Get project information
read -p "Enter project name (e.g., 'awesome-web-app'): " PROJECT_NAME
read -p "Enter project description: " PROJECT_DESC
read -p "Enter primary technology stack (e.g., 'React/Node.js/PostgreSQL'): " TECH_STACK
read -p "Enter agent role (e.g., 'senior full-stack engineer'): " AGENT_ROLE
read -p "Enter project type (web_app/mobile_app/api_service/desktop_app/other): " PROJECT_TYPE

# Set defaults if empty
PROJECT_NAME=${PROJECT_NAME:-"new-project"}
PROJECT_DESC=${PROJECT_DESC:-"A modern software project"}
TECH_STACK=${TECH_STACK:-"Modern Development Stack"}
AGENT_ROLE=${AGENT_ROLE:-"senior software engineer"}
PROJECT_TYPE=${PROJECT_TYPE:-"web_app"}

# Sanitize project name for directory
PROJECT_DIR_NAME=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONTEXT_DIR="contexts/$PROJECT_DIR_NAME"

echo
print_status "Setting up project context:"
echo "  Project Name: $PROJECT_NAME"
echo "  Description: $PROJECT_DESC"
echo "  Tech Stack: $TECH_STACK"
echo "  Agent Role: $AGENT_ROLE"
echo "  Project Type: $PROJECT_TYPE"
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

# Copy and customize templates
print_status "Creating project context from templates..."

# Copy persona template
cp "templates/persona/dev_agent_persona_template.md" "$CONTEXT_DIR/dev_agent_persona.md"

# Copy context template  
cp "templates/context/dev_agent_context_template.md" "$CONTEXT_DIR/dev_agent_context.md"

# Copy init prompt template
cp "templates/prompts/dev_agent_init_prompt_template.md" "$CONTEXT_DIR/dev_agent_init_prompt.md"

# Copy session end prompt template
cp "templates/prompts/dev_agent_session_end_prompt_template.md" "$CONTEXT_DIR/dev_agent_session_end_prompt.md"

print_success "Templates copied to context directory"

# Customize templates with project information
print_status "Customizing templates with project information..."

# Update persona file
sed -i.bak "s/\[PROJECT NAME\]/$PROJECT_NAME/g" "$CONTEXT_DIR/dev_agent_persona.md"
sed -i.bak "s/\[Your Project Name\]/$PROJECT_NAME/g" "$CONTEXT_DIR/dev_agent_persona.md"
sed -i.bak "s/\[senior software engineer \/ specialist role\]/$AGENT_ROLE/g" "$CONTEXT_DIR/dev_agent_persona.md"
sed -i.bak "s/\[Technology Stack\]/$TECH_STACK/g" "$CONTEXT_DIR/dev_agent_persona.md"
sed -i.bak "s/\[brief project description with key value propositions\]/$PROJECT_DESC/g" "$CONTEXT_DIR/dev_agent_persona.md"

# Update context file
sed -i.bak "s/\[PROJECT NAME\]/$PROJECT_NAME/g" "$CONTEXT_DIR/dev_agent_context.md"
sed -i.bak "s/\[your-project-id\]/$PROJECT_DIR_NAME/g" "$CONTEXT_DIR/dev_agent_context.md"

# Update init prompt
sed -i.bak "s/\[PROJECT NAME\]/$PROJECT_NAME/g" "$CONTEXT_DIR/dev_agent_init_prompt.md"
sed -i.bak "s/\[Project Name\]/$PROJECT_NAME/g" "$CONTEXT_DIR/dev_agent_init_prompt.md"

# Update session end prompt
sed -i.bak "s/\[PROJECT NAME\]/$PROJECT_NAME/g" "$CONTEXT_DIR/dev_agent_session_end_prompt.md"

# Remove backup files
rm -f "$CONTEXT_DIR"/*.bak

print_success "Templates customized with project information"

# Create project configuration file
print_status "Creating project configuration..."

cat > "$CONTEXT_DIR/project_config.yml" << EOF
# $PROJECT_NAME Project Configuration
# This file defines the relationship between this context and external code repositories

project:
  name: "$PROJECT_NAME"
  description: "$PROJECT_DESC"
  type: "$PROJECT_TYPE"
  
# Code repositories (stored separately from this context framework)
repositories:
  primary:
    name: "${PROJECT_DIR_NAME}-main"
    path: "/path/to/${PROJECT_DIR_NAME}"  # Update with actual path to your code repo
    type: "primary"
    framework: "update_me"
    language: "update_me"
    
  # Add additional repositories as needed
  # secondary:
  #   name: "${PROJECT_DIR_NAME}-api"
  #   path: "/path/to/${PROJECT_DIR_NAME}-api"
  #   type: "backend"
  #   framework: "update_me"
  #   language: "update_me"

# RAG Knowledge Collections  
knowledge:
  collections:
    - "${PROJECT_DIR_NAME}_code"        # Main code patterns
    - "${PROJECT_DIR_NAME}_docs"        # Documentation patterns
    - "shared_${PROJECT_TYPE}_patterns" # Cross-project patterns for this type
    
  # What this project contributes to shared knowledge
  contributes:
    - "$TECH_STACK patterns"
    - "$PROJECT_TYPE architecture"
    - "Project-specific solutions"
    
  # What this project learns from other projects
  learns_from:
    - "Authentication patterns from all projects"
    - "Testing strategies from similar project types"
    - "Performance optimization patterns"
    - "Error handling approaches"

# Development Environment
environment:
  # Update these based on your tech stack
  primary_language: "update_me"
  framework: "update_me"
  database: "update_me"
  
# Integration with CI/CD (optional)
deployment:
  platform: "update_me"  # aws, gcp, azure, docker, kubernetes
  containerization: "update_me"  # docker, none
  ci_cd: "update_me"  # github_actions, gitlab_ci, jenkins

# Cross-project knowledge sharing tags
tags:
  - "$PROJECT_TYPE"
  - "$(echo $TECH_STACK | tr '[:upper:]' '[:lower:]' | tr '/' '-')"
  # Add more relevant tags for knowledge discovery
EOF

print_success "Project configuration created: $CONTEXT_DIR/project_config.yml"

# Create context README
print_status "Creating context documentation..."

cat > "$CONTEXT_DIR/README.md" << EOF
# $PROJECT_NAME - Development Context

This directory contains the development agent context for **$PROJECT_NAME** within the Kindarian Cursor Context framework.

## 📁 **Context Structure**

- \`dev_agent_persona.md\` - Agent identity, coding standards, and tech stack configuration
- \`dev_agent_context.md\` - Project state, achievements, issues, and historical tracking
- \`dev_agent_init_prompt.md\` - Agent initialization protocol for this project
- \`dev_agent_session_end_prompt.md\` - Session continuity and knowledge capture protocol
- \`project_config.yml\` - Configuration linking this context to external code repositories
- \`README.md\` - This documentation

## 🚀 **Usage in Cursor**

1. **Open the framework**: Open the \`kindarian-cursor-context\` directory in Cursor
2. **Initialize agent**: Reference the init prompt for this project:
   \`\`\`
   @contexts/$PROJECT_DIR_NAME/dev_agent_init_prompt.md
   \`\`\`
3. **Cross-project queries**: Use RAG to discover patterns from other projects:
   \`\`\`
   qdrant-find "authentication patterns"
   qdrant-find "testing strategies for $PROJECT_TYPE"
   \`\`\`

## 📊 **Project Information**

- **Name**: $PROJECT_NAME
- **Type**: $PROJECT_TYPE  
- **Tech Stack**: $TECH_STACK
- **Agent Role**: $AGENT_ROLE
- **Description**: $PROJECT_DESC
- **Created**: $(date)

## 🔗 **Code Repository Setup**

1. **Index your code** for RAG knowledge discovery:
   \`\`\`bash
   cd rag/indexer
   python app.py index /path/to/your/code --collection ${PROJECT_DIR_NAME}_code
   \`\`\`

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

## 📚 **Framework Documentation**

For more information about the Kindarian Cursor Context framework:
- [Main README](../../README.md)
- [RAG Setup Guide](../../docs/integration/rag-mcp-setup-guide.md)
- [Cross-Project Patterns](../shared/cross_project_patterns.md)
- [Workflow Examples](../../workflows-and-processes/examples/)

---

*This project context is part of the Kindarian Cursor Context framework enabling cross-project knowledge sharing and institutional learning.*
EOF

print_success "Context documentation created: $CONTEXT_DIR/README.md"

# Ask about code repository indexing
echo
read -p "Do you want to index an existing code repository now? (y/N): " INDEX_CODE

if [[ "$INDEX_CODE" =~ ^[Yy]$ ]]; then
    read -p "Enter the path to your code repository: " CODE_PATH
    
    if [[ -d "$CODE_PATH" ]]; then
        print_status "Indexing code repository..."
        
        cd rag/indexer
        
        if [[ -f "app.py" ]]; then
            python app.py index "$CODE_PATH" --collection "${PROJECT_DIR_NAME}_code"
            print_success "Code repository indexed successfully"
        else
            print_warning "RAG indexer not found. Make sure to run 'docker-compose -f compose.rag.yml up -d' first"
        fi
        
        cd - > /dev/null
    else
        print_warning "Code path '$CODE_PATH' not found. You can index it later."
    fi
fi

echo
print_success "🎉 Project context '$PROJECT_NAME' created successfully!"
echo
print_status "Context Location: $CONTEXT_DIR"
echo
print_status "Next Steps:"
echo "  1. Customize $CONTEXT_DIR/dev_agent_persona.md for your specific tech stack and standards"
echo "  2. Update $CONTEXT_DIR/dev_agent_context.md with current project state"
echo "  3. In Cursor (with kindarian-cursor-context open): @contexts/$PROJECT_DIR_NAME/dev_agent_init_prompt.md"
echo "  4. Start using cross-project knowledge queries:"
echo "     - qdrant-find \"patterns for $PROJECT_TYPE development\""
echo "     - qdrant-find \"$TECH_STACK best practices\""
echo
print_status "Your project will now benefit from and contribute to the shared knowledge ecosystem!"
echo
