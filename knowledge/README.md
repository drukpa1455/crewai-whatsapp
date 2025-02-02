# Knowledge Base

This folder contains domain-specific knowledge and rules that guide the AI agents in processing and summarizing WhatsApp group messages.

## Structure

```
knowledge/
├── templates/           # Message summary templates
│   ├── daily.md        # Daily summary format
│   └── weekly.md       # Weekly summary format
├── patterns/           # Message analysis patterns
│   ├── topics.yaml     # Topic classification rules
│   └── priorities.yaml # Message priority rules
├── rules/              # Custom processing rules
│   ├── filters.yaml    # Message filtering rules
│   └── grouping.yaml   # Message grouping rules
└── context/            # Group-specific context
    └── categories.yaml # Group message categories
```

## Usage

1. **Templates**: Define how summaries should be formatted
   - Use placeholders for dynamic content
   - Maintain consistent styling
   - Include all required sections

2. **Patterns**: Define how to analyze messages
   - Topic classification rules
   - Priority determination
   - Key information extraction

3. **Rules**: Customize message processing
   - Filtering criteria
   - Grouping logic
   - Special handling cases

4. **Context**: Group-specific information
   - Common topics
   - Important keywords
   - Member roles

## Customization

You can customize these files to better suit your specific use case:

1. Modify templates to change summary formats
2. Adjust patterns to improve topic detection
3. Update rules to refine message processing
4. Add context for better group understanding

## Examples

### Summary Template
```markdown
# Daily Summary - {date}

## Key Discussions
{key_discussions}

## Action Items
{action_items}

## Participation
{participation_stats}
```

### Topic Pattern
```yaml
topics:
  - name: "Technical Discussion"
    keywords:
      - "bug"
      - "feature"
      - "code"
  - name: "Planning"
    keywords:
      - "meeting"
      - "schedule"
      - "deadline"
```

## Maintenance

Keep these files updated as your needs evolve:
1. Review and update patterns regularly
2. Add new templates as needed
3. Refine rules based on performance
4. Update context with new information 