# Data Storage

This directory contains the persistent storage for WhatsApp messages and generated summaries.

## Structure

```
data/
├── messages/              # Raw message storage
│   ├── current/          # Current day's messages
│   │   └── YYYY-MM-DD/   # Date-based organization
│   └── archive/          # Historical messages
│       └── YYYY-MM/      # Month-based archives
└── summaries/            # Generated summaries
    ├── current/          # Recent summaries
    │   └── YYYY-MM-DD/   # Date-based organization
    └── archive/          # Historical summaries
        └── YYYY-MM/      # Month-based archives
```

## Message Storage Format

Messages are stored in JSON format with the following structure:

```json
{
  "group_id": "string",
  "messages": [
    {
      "message_id": "string",
      "timestamp": "ISO-8601 datetime",
      "sender": {
        "id": "string",
        "name": "string"
      },
      "content": {
        "type": "text|image|video|audio|document",
        "text": "string",
        "media_url": "string (optional)",
        "caption": "string (optional)"
      },
      "metadata": {
        "quoted_message_id": "string (optional)",
        "mentions": ["string"],
        "tags": ["string"]
      }
    }
  ]
}
```

## Summary Storage Format

Summaries are stored in both JSON and Markdown formats:

### JSON Format
```json
{
  "group_id": "string",
  "date": "YYYY-MM-DD",
  "summary": {
    "key_discussions": [
      {
        "topic": "string",
        "content": "string",
        "participants": ["string"]
      }
    ],
    "activity": {
      "total_messages": "number",
      "active_participants": "number",
      "peak_time": "HH:MM"
    },
    "action_items": [
      {
        "description": "string",
        "assigned_to": ["string"],
        "due_date": "YYYY-MM-DD (optional)"
      }
    ],
    "notable_interactions": [
      {
        "description": "string",
        "participants": ["string"]
      }
    ],
    "resources": [
      {
        "type": "link|document|image",
        "url": "string",
        "description": "string"
      }
    ]
  },
  "metadata": {
    "generated_at": "ISO-8601 datetime",
    "version": "string"
  }
}
```

### Markdown Format
The markdown format follows the template defined in `knowledge/templates/daily.md`

## Retention Policy

1. **Current Messages**
   - Stored in `messages/current/` for 7 days
   - Automatically archived after 7 days

2. **Archived Messages**
   - Stored in `messages/archive/` for 90 days
   - Compressed after 90 days
   - Deleted after 1 year (configurable)

3. **Current Summaries**
   - Stored in `summaries/current/` for 30 days
   - Automatically archived after 30 days

4. **Archived Summaries**
   - Stored in `summaries/archive/` indefinitely
   - Compressed after 1 year

## Usage

The data directory is used by:
1. Message Handler Agent - Stores incoming messages
2. Summarization Agent - Reads messages and stores summaries
3. Archival Process - Manages data retention

## Backup

It's recommended to:
1. Regularly backup this directory
2. Use version control for summary templates
3. Implement automated cleanup based on retention policy 