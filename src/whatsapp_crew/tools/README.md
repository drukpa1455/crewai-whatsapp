# Tools Directory

This directory contains the core tools used by the WhatsApp Group Activity Summary system. Each tool is implemented as a CrewAI tool class and serves a specific purpose in the message processing and summarization pipeline.

## Tool Overview

### WhatsApp Tool (`whatsapp_tool.py`)
The primary interface for WhatsApp Business API communication.
- **Purpose**: Handles all WhatsApp message operations
- **Key Features**:
  - Message sending and receiving
  - Group chat management
  - Error handling with retries
  - API rate limiting
- **Usage**: Used by the Message Handler agent for all WhatsApp interactions

### Message Analyzer (`message_analyzer.py`)
Processes and analyzes message content for insights.
- **Purpose**: Extract meaningful information from messages
- **Key Features**:
  - Content analysis and classification
  - Topic identification
  - Action item extraction
  - Sentiment analysis
  - Mention and hashtag processing
- **Usage**: Used by the Summarization Specialist for message analysis

### Message Storage (`message_storage.py`)
Manages the persistence of WhatsApp messages.
- **Purpose**: Organized storage of processed messages
- **Key Features**:
  - Message persistence
  - Data organization by date
  - Retention policy implementation
  - Query and retrieval functions
- **Usage**: Used by both agents for message data management

### Summary Storage (`summary_storage.py`)
Handles the storage and retrieval of generated summaries.
- **Purpose**: Manage daily summary documents
- **Key Features**:
  - Summary document management
  - Template handling
  - Archive organization
  - Export functionality
- **Usage**: Used by the Summarization Specialist for summary management

### Custom Tool (`custom_tool.py`)
Template for implementing custom functionality.
- **Purpose**: Base structure for new tool development
- **Key Features**:
  - Input schema definition template
  - Tool description template
  - Execution logic template
- **Usage**: Extend this template to add new functionality

## Implementation Details

### Base Structure
All tools inherit from `crewai.tools.BaseTool` and follow this structure:
```python
class MyTool(BaseTool):
    name: str = "Tool Name"
    description: str = "Tool Description"
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, **kwargs) -> str:
        # Implementation
```

### Error Handling
Tools implement error handling for:
- API failures
- Rate limiting
- Data validation
- Storage issues

### Configuration
Tools read configuration from:
- Environment variables
- YAML configuration files
- Runtime parameters

## Adding New Tools

1. Copy `custom_tool.py` as a template
2. Implement required functionality
3. Add tool to `agents.yaml`
4. Update task configurations in `tasks.yaml`
5. Document the new tool in this README 