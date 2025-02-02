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

### Agent Roles

#### 1. Message Handling Specialist
- **Purpose**: Manages WhatsApp communication
- **Responsibilities**:
  - API integration management
  - Message reception and processing
  - Summary distribution
- **Tools**: WhatsApp Business API, HTTP clients

#### 2. Summarization Specialist
- **Purpose**: Content analysis and synthesis
- **Responsibilities**:
  - Message analysis
  - Topic identification
  - Summary generation
- **Tools**: NLP models, text analysis tools

### Workflow
1. Message Handler receives group messages
2. Summarization Specialist analyzes content
3. Key topics and trends are identified
4. Daily summary is generated
5. Summary is sent back to the group

## 📝 Example Summary Format

```
📝 Daily Group Summary
Date: 2024-02-01

🔑 Key Discussions:
- Topic 1: Brief overview
- Topic 2: Main points discussed

📊 Activity Overview:
- Total Messages: XX
- Active Participants: XX
- Peak Activity Time: XX:XX

🎯 Action Items:
- Action 1
- Action 2

#DailySummary
```

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
