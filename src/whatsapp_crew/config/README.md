# Configuration Directory

This directory contains configuration files that define the behavior of the WhatsApp Group Activity Summary system. The configuration is split into multiple files for better organization and maintainability.

## Configuration Files

### WhatsApp Configuration (`whatsapp_config.yaml`)
Defines WhatsApp Business API settings.
```yaml
whatsapp:
  api_version: "v17.0"
  phone_number_id: "your_phone_number_id"
  access_token: "your_access_token"
  group_id: "your_group_id"
  summary_time: "08:00"
  timezone: "UTC"
```

### Agent Configuration (`agents.yaml`)
Defines AI agents and their capabilities.
- **Message Handler**: Manages WhatsApp communication
  - Tools: WhatsAppTool, MessageStorage
  - Responsibilities: Message flow, storage management
- **Summarization Expert**: Analyzes and summarizes content
  - Tools: MessageAnalyzer, SummaryStorage
  - Responsibilities: Content analysis, summary generation

### Task Configuration (`tasks.yaml`)
Defines system tasks and their scheduling.
1. **Message Monitoring**: Continuous message processing
2. **Message Storage**: On-message storage operations
3. **Message Analysis**: Daily content analysis
4. **Summary Generation**: Midnight summary creation
5. **Summary Distribution**: 8 AM summary delivery

## Configuration Guidelines

### Environment Variables
Required environment variables:
```bash
OPENAI_API_KEY=your_openai_api_key
```

### Timezone Settings
- Default: UTC
- Format: IANA timezone names (e.g., "America/New_York")
- Configure in `whatsapp_config.yaml`

### Scheduling
Cron expressions in `tasks.yaml`:
- Summary Generation: `0 0 * * *` (midnight)
- Summary Distribution: `0 8 * * *` (8 AM)

### Templates
Summary templates are defined in:
- JSON format for structured data
- Markdown format for readable output

## Customization

### Adding New Agents
1. Add agent definition to `agents.yaml`
2. Specify:
   - Role and goal
   - Required tools
   - Backstory for context

### Modifying Tasks
1. Update `tasks.yaml`
2. Define:
   - Description
   - Agent assignment
   - Tool requirements
   - Schedule
   - Dependencies

### Security Notes
- Never commit sensitive credentials
- Use environment variables for secrets
- Keep `whatsapp_config.yaml` in `.gitignore`

## Validation

Configuration files are validated on system startup:
- Schema validation
- Dependency checks
- Schedule validation
- Tool availability checks

## Example Configurations

See the `.example` versions of configuration files for:
- Required fields
- Format examples
- Best practices
- Common configurations 