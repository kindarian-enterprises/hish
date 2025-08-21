#!/bin/bash
# Kindarian Cursor Context - New Project Setup Script
# This script sets up a new project with customized agent templates

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

# Get project information
echo "🚀 Kindarian Cursor Context - New Project Setup"
echo "================================================"
echo

# Get target directory
read -p "Enter target project directory: " TARGET_DIR

if [[ -z "$TARGET_DIR" ]]; then
    print_error "Target directory cannot be empty"
    exit 1
fi

# Convert to absolute path
TARGET_DIR=$(realpath "$TARGET_DIR" 2>/dev/null || echo "$TARGET_DIR")

# Create target directory if it doesn't exist
if [[ ! -d "$TARGET_DIR" ]]; then
    print_status "Creating target directory: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
fi

# Get project information
read -p "Enter project name (e.g., 'MyAwesome'): " PROJECT_NAME
read -p "Enter project description: " PROJECT_DESC
read -p "Enter primary technology stack (e.g., 'React/Node.js/PostgreSQL'): " TECH_STACK
read -p "Enter agent role (e.g., 'senior full-stack engineer'): " AGENT_ROLE

# Set defaults if empty
PROJECT_NAME=${PROJECT_NAME:-"YourProject"}
PROJECT_DESC=${PROJECT_DESC:-"A modern software project"}
TECH_STACK=${TECH_STACK:-"Modern Web Development"}
AGENT_ROLE=${AGENT_ROLE:-"senior software engineer"}

echo
print_status "Setting up project with:"
echo "  Project Name: $PROJECT_NAME"
echo "  Description: $PROJECT_DESC"
echo "  Tech Stack: $TECH_STACK"
echo "  Agent Role: $AGENT_ROLE"
echo "  Target Directory: $TARGET_DIR"
echo

read -p "Continue? (y/N): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    print_warning "Setup cancelled"
    exit 0
fi

echo

# Copy and customize templates
print_status "Copying and customizing templates..."

# Copy persona template
cp "templates/persona/dev_agent_persona_template.md" "$TARGET_DIR/dev_agent_persona.md"
print_success "Copied persona template"

# Copy context template  
cp "templates/context/dev_agent_context_template.md" "$TARGET_DIR/dev_agent_context.md"
print_success "Copied context template"

# Copy prompt templates
cp "templates/prompts/dev_agent_init_prompt_template.md" "$TARGET_DIR/dev_agent_init_prompt.md"
cp "templates/prompts/dev_agent_session_end_prompt_template.md" "$TARGET_DIR/dev_agent_session_end_prompt.md"
print_success "Copied prompt templates"

# Customize templates with project information
print_status "Customizing templates with project information..."

# Update persona file
sed -i.bak "s/\[PROJECT NAME\]/$PROJECT_NAME/g" "$TARGET_DIR/dev_agent_persona.md"
sed -i.bak "s/\[Your Project Name\]/$PROJECT_NAME/g" "$TARGET_DIR/dev_agent_persona.md"
sed -i.bak "s/\[senior software engineer \/ specialist role\]/$AGENT_ROLE/g" "$TARGET_DIR/dev_agent_persona.md"
sed -i.bak "s/\[Technology Stack\]/$TECH_STACK/g" "$TARGET_DIR/dev_agent_persona.md"
sed -i.bak "s/\[brief project description with key value propositions\]/$PROJECT_DESC/g" "$TARGET_DIR/dev_agent_persona.md"

# Update context file
sed -i.bak "s/\[PROJECT NAME\]/$PROJECT_NAME/g" "$TARGET_DIR/dev_agent_context.md"
sed -i.bak "s/\[your-project-id\]/$(echo $PROJECT_NAME | tr '[:upper:]' '[:lower:]' | tr ' ' '-')/g" "$TARGET_DIR/dev_agent_context.md"

# Update init prompt
sed -i.bak "s/\[PROJECT NAME\]/$PROJECT_NAME/g" "$TARGET_DIR/dev_agent_init_prompt.md"
sed -i.bak "s/\[Project Name\]/$PROJECT_NAME/g" "$TARGET_DIR/dev_agent_init_prompt.md"

# Update session end prompt
sed -i.bak "s/\[PROJECT NAME\]/$PROJECT_NAME/g" "$TARGET_DIR/dev_agent_session_end_prompt.md"

# Remove backup files
rm -f "$TARGET_DIR"/*.bak

print_success "Templates customized with project information"

# Ask about RAG setup
echo
read -p "Set up RAG knowledge system? (y/N): " SETUP_RAG

if [[ "$SETUP_RAG" =~ ^[Yy]$ ]]; then
    print_status "Setting up RAG infrastructure..."
    
    # Copy RAG components
    cp -r rag "$TARGET_DIR/"
    cp -r mcp "$TARGET_DIR/"
    cp compose.rag.yml "$TARGET_DIR/"
    
    print_success "RAG infrastructure copied"
    
    # Ask about starting services
    read -p "Start RAG services now? (requires Docker) (y/N): " START_SERVICES
    
    if [[ "$START_SERVICES" =~ ^[Yy]$ ]]; then
        print_status "Starting RAG services..."
        
        cd "$TARGET_DIR"
        
        if command -v docker-compose &> /dev/null; then
            docker-compose -f compose.rag.yml up -d
            print_success "RAG services started successfully"
            
            print_status "Waiting for Qdrant to be ready..."
            sleep 10
            
            # Test Qdrant connection
            if curl -s http://localhost:6333/health &> /dev/null; then
                print_success "Qdrant is ready at http://localhost:6333"
            else
                print_warning "Qdrant may still be starting up. Check with: curl http://localhost:6333/health"
            fi
        else
            print_error "docker-compose not found. Please install Docker and try again."
        fi
        
        cd - > /dev/null
    fi
fi

# Ask about workflows
echo
read -p "Copy workflow examples? (y/N): " COPY_WORKFLOWS

if [[ "$COPY_WORKFLOWS" =~ ^[Yy]$ ]]; then
    print_status "Copying workflow examples..."
    
    mkdir -p "$TARGET_DIR/workflows-and-processes"
    cp -r workflows-and-processes/* "$TARGET_DIR/workflows-and-processes/"
    
    print_success "Workflow examples copied"
fi

# Create a simple setup summary
print_status "Creating setup summary..."

cat > "$TARGET_DIR/SETUP_SUMMARY.md" << EOF
# $PROJECT_NAME - Cursor Context Setup Summary

This project has been configured with Kindarian Cursor Context.

## Files Created
- \`dev_agent_persona.md\` - Agent identity, coding standards, tech stack
- \`dev_agent_context.md\` - Project state, achievements, issues tracking
- \`dev_agent_init_prompt.md\` - Agent initialization protocol
- \`dev_agent_session_end_prompt.md\` - Session continuity protocol

## Next Steps

### 1. Customize Your Agent
Edit the persona file to match your specific:
- Coding standards and practices
- Architectural decisions
- Technology stack details
- Quality requirements

### 2. Initialize Context
Update the context file with:
- Current project status
- Existing achievements
- Known issues and technical debt
- Development environment details

### 3. Start Using in Cursor
Reference the initialization prompt in Cursor:
\`\`\`
@dev_agent_init_prompt.md
\`\`\`

### 4. RAG Knowledge System
$(if [[ "$SETUP_RAG" =~ ^[Yy]$ ]]; then
echo "✅ RAG infrastructure is set up and ready to use.

Index your codebase:
\`\`\`bash
cd rag/indexer
python3 app.py index /path/to/your/code --collection ${PROJECT_NAME,,}_code
\`\`\`

Use knowledge queries in Cursor:
\`\`\`
qdrant-find \"authentication patterns\"
qdrant-store \"Solution: JWT implementation with refresh tokens\"
\`\`\`"
else
echo "❌ RAG infrastructure not set up. To add later, copy the rag/, mcp/ directories and compose.rag.yml from kindarian-cursor-context."
fi)

## Project Configuration
- **Name**: $PROJECT_NAME
- **Technology Stack**: $TECH_STACK
- **Agent Role**: $AGENT_ROLE
- **Setup Date**: $(date)

For more information, see the documentation in the kindarian-cursor-context repository.
EOF

print_success "Setup summary created: $TARGET_DIR/SETUP_SUMMARY.md"

echo
print_success "🎉 Project setup complete!"
echo
print_status "Next steps:"
echo "  1. cd $TARGET_DIR"
echo "  2. Customize dev_agent_persona.md for your tech stack"
echo "  3. Update dev_agent_context.md with current project state"
echo "  4. In Cursor, reference: @dev_agent_init_prompt.md"
echo
print_status "For detailed guidance, see SETUP_SUMMARY.md in your project directory"
echo
