# WhatsApp Group Activity Summary 🤖

[![CrewAI](https://img.shields.io/badge/built%20with-CrewAI-blue.svg)](https://crewai.com)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Transform your WhatsApp group chats into organized, insightful summaries with the power of AI. This intelligent system uses a team of AI agents to monitor group conversations, identify key discussions, and automatically generate comprehensive daily summaries.

### Why This Project?
- 📚 **Information Overload**: Keep up with busy group chats without reading every message
- 🎯 **Key Insights**: Never miss important discussions or decisions
- ⏰ **Time Saving**: Get daily summaries delivered automatically
- 🤝 **Better Collaboration**: Keep everyone informed with minimal effort

Built with [CrewAI](https://crewai.com), this project demonstrates the power of multi-agent AI systems working together. The Message Handler manages WhatsApp communication while the Summarization Specialist analyzes content, creating a seamless automated summary pipeline.

### Perfect For:
- 🏢 Business Teams
- 👥 Community Groups
- 📚 Study Groups
- 🌐 Remote Teams
- 📊 Project Management
- 🤝 Networking Groups

## 🌟 Features

- 🤖 Multi-agent AI system for intelligent message processing
- 📱 WhatsApp Business API integration
- 📊 Daily group activity summaries
- ⏰ Automated scheduling of summaries
- 🔍 Smart message analysis and topic identification
- 🎯 Customizable summary formats and timing

## 🚀 Quick Start

### Prerequisites

- Python >=3.10 <=3.13
- [UV](https://docs.astral.sh/uv/) package manager
- WhatsApp Business Account
- OpenAI API key

### Installation

1. **Install UV Package Manager**:
   ```bash
   pip install uv
   ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/whatsapp-group-summary.git
   cd whatsapp-group-summary
   ```

3. **Install Dependencies**:
   ```bash
   crewai install
   ```

## 🔧 Configuration

### 1. WhatsApp Business Setup

#### Create WhatsApp Business Account
1. Visit [Meta Developer Portal](https://developers.facebook.com/)
2. Create a new app or select existing one
3. Add WhatsApp product to your app
4. Complete business verification if required

#### API Setup
1. Navigate to WhatsApp > API Setup in your app dashboard
2. Collect required credentials:
   - Phone Number ID
   - Access Token
   - API Version (v17.0 recommended)

#### Webhook Configuration
1. Go to WhatsApp > Configuration
2. Set up webhook URL for receiving messages
3. Configure webhook events:
   - `messages` - For receiving group messages
   - `message_status` - For delivery confirmations

### 2. Project Configuration

#### WhatsApp Configuration
Create your configuration file:
```bash
cp src/whatsapp_crew/config/whatsapp_config.example.yaml whatsapp_config.yaml
```

Update with your credentials:
```yaml
whatsapp:
  api_version: "v17.0"
  phone_number_id: "your_phone_number_id"
  access_token: "your_access_token"
  group_id: "your_group_id"
  summary_time: "08:00"
  timezone: "UTC"
```

#### Environment Variables
Create `.env` file in project root:
```bash
echo "OPENAI_API_KEY=your_openai_api_key" > .env
```

## 🎮 Usage

### Running the Project

Start the AI crew:
```bash
crewai run
```

### Customization

Modify agent behaviors and tasks in:
- `config/agents.yaml` - Agent definitions
- `config/tasks.yaml` - Task configurations
- `crew.py` - Core logic and tools
- `main.py` - Input handling and execution flow

## 🤖 Understanding the AI Crew

### Agent Roles and Tools

#### 1. Message Handling Specialist
- **Purpose**: Manages WhatsApp communication and message processing
- **Responsibilities**:
  - Monitors group chat activity using WhatsApp Business API
  - Processes incoming messages and extracts metadata
  - Handles message storage and retrieval
  - Manages message retention and archival
- **Tools**: 
  - `whatsapp_tool.py`: WhatsApp Business API integration
  - `message_storage.py`: Message persistence and retrieval
  - `custom_tool.py`: Custom tool extensions

#### 2. Summarization Specialist
- **Purpose**: Analyzes content and generates insightful summaries
- **Responsibilities**:
  - Performs message analysis and classification
  - Generates and stores daily summaries
  - Maintains summary archives
  - Implements summary templates
- **Tools**: 
  - `message_analyzer.py`: Content analysis and classification
  - `summary_storage.py`: Summary persistence and retrieval

### Tool Implementations

#### WhatsApp Tool (`whatsapp_tool.py`)
- WhatsApp Business API integration
- Message sending and receiving
- Group chat management
- Error handling and retry logic

#### Message Analyzer (`message_analyzer.py`)
- Content analysis and classification
- Topic identification
- Action item extraction
- Sentiment analysis
- Mention and hashtag processing

#### Message Storage (`message_storage.py`)
- Message persistence
- Data organization
- Retention policy implementation
- Query and retrieval functions

#### Summary Storage (`summary_storage.py`)
- Summary document management
- Template handling
- Archive organization
- Export functionality

#### Custom Tool (`custom_tool.py`)
- Template for implementing custom functionality
- Provides base structure for new tools:
  - Input schema definition
  - Tool description
  - Execution logic
- Can be extended for:
  - Custom message filters
  - Special processing rules
  - Integration with additional services
  - Custom analytics
  - Specialized data transformations

### Tasks and Scheduling

The system operates through five main tasks, each with specific responsibilities and scheduling:

#### 1. Message Monitoring
- **Agent**: Message Handling Specialist
- **Tools**: WhatsApp Tool, Message Storage
- **Schedule**: Continuous operation
- **Purpose**: Real-time monitoring and processing of incoming messages

#### 2. Message Storage
- **Agent**: Message Handling Specialist
- **Tools**: Message Storage, Custom Tool
- **Schedule**: Triggered on message receipt
- **Purpose**: Organized storage and management of processed messages
- **Dependencies**: Message Monitoring

#### 3. Message Analysis
- **Agent**: Summarization Specialist
- **Tools**: Message Analyzer
- **Schedule**: Daily execution
- **Purpose**: Content analysis and insight extraction
- **Dependencies**: Message Storage

#### 4. Summary Generation
- **Agent**: Summarization Specialist
- **Tools**: Message Analyzer, Summary Storage
- **Schedule**: Daily at midnight (UTC by default)
- **Purpose**: Creation of comprehensive daily summaries
- **Dependencies**: Message Analysis

#### 5. Summary Distribution
- **Agent**: Message Handling Specialist
- **Tools**: WhatsApp Tool, Summary Storage
- **Schedule**: Daily at 8:00 AM (UTC by default)
- **Purpose**: Delivery of generated summaries to the WhatsApp group
- **Dependencies**: Summary Generation

### System Workflow

The system follows a sequential workflow:

1. **Continuous Monitoring**: The Message Handler continuously monitors the WhatsApp group for new messages using the WhatsApp Tool.

2. **Message Processing**:
   - New messages are immediately processed and stored
   - Messages are organized by date and metadata
   - Custom processing rules can be applied through the Custom Tool

3. **Daily Analysis**:
   - Messages are analyzed for content and context
   - Key topics and trends are identified
   - Action items and important information are extracted

4. **Summary Creation**:
   - Daily summaries are generated at midnight
   - Content is organized by topic and importance
   - Summaries are stored in both JSON and formatted text

5. **Distribution**:
   - Formatted summaries are sent to the WhatsApp group at 8:00 AM
   - Delivery confirmations are tracked
   - Any distribution issues are handled with retry logic

### Customization Options

You can customize the system behavior by modifying:

1. **Scheduling**:
   - Adjust summary generation time in `tasks.yaml`
   - Modify distribution schedule
   - Change timezone settings

2. **Processing Rules**:
   - Implement custom message filters
   - Add new analysis criteria
   - Create custom summary formats

3. **Storage Policies**:
   - Configure retention periods
   - Modify archival rules
   - Adjust storage organization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🆘 Support

### CrewAI Support
- [Documentation](https://docs.crewai.com)
- [GitHub Repository](https://github.com/joaomdmoura/crewai)
- [Discord Community](https://discord.com/invite/X4JWnZnxPb)
- [Documentation Chat](https://chatg.pt/DWjSBZn)

### WhatsApp API Support
- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
- [Meta Developers Support](https://developers.facebook.com/support)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ using [CrewAI](https://crewai.com)
