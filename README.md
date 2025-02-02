# WhatsappGroupActivitySummaryCrewFormation Crew

Welcome to the WhatsappGroupActivitySummaryCrewFormation Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

## WhatsApp Setup

This project uses the WhatsApp Business API to send and receive messages. Follow these steps to set up WhatsApp integration:

1. **Create a WhatsApp Business Account**:
   - Go to the [Meta Developer Portal](https://developers.facebook.com/)
   - Create a new app or use an existing one
   - Add the WhatsApp product to your app
   - Set up a WhatsApp Business Account

2. **Get API Credentials**:
   - In your app's dashboard, go to WhatsApp > API Setup
   - Note down your:
     - Phone Number ID
     - Access Token
     - API Version (default is v17.0)

3. **Configure Webhook**:
   - In your app's dashboard, go to WhatsApp > Configuration
   - Set up a webhook URL where you'll receive messages
   - Subscribe to the necessary webhook events (messages, message_status)

4. **Update Configuration**:
   - Copy `src/whatsapp_group_activity_summary_crew_formation/config/whatsapp_config.example.yaml` to `whatsapp_config.yaml`
   - Update the configuration with your:
     ```yaml
     whatsapp:
       api_version: "v17.0"
       phone_number_id: "your_phone_number_id"
       access_token: "your_access_token"
       group_id: "your_group_id"
       summary_time: "08:00"
       timezone: "UTC"
     ```

5. **Environment Variables**:
   Create a `.env` file in the root directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/whatsapp_group_activity_summary_crew_formation/config/agents.yaml` to define your agents
- Modify `src/whatsapp_group_activity_summary_crew_formation/config/tasks.yaml` to define your tasks
- Modify `src/whatsapp_group_activity_summary_crew_formation/crew.py` to add your own logic, tools and specific args
- Modify `src/whatsapp_group_activity_summary_crew_formation/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the whatsapp_group_activity_summary_crew_formation Crew, assembling the agents and assigning them tasks as defined in your configuration.

The agents will:
1. Monitor your specified WhatsApp group for messages
2. Analyze and summarize the group's activity
3. Send a daily summary at the configured time

## Understanding Your Crew

The whatsapp_group_activity_summary_crew_formation Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

### Agent Roles

1. **Message Handling Specialist**:
   - Manages WhatsApp API integration
   - Receives and processes group messages
   - Sends summarized content back to the group

2. **Summarization Specialist**:
   - Analyzes group messages
   - Creates concise, meaningful summaries
   - Identifies key topics and trends

## Support

For support, questions, or feedback regarding the WhatsappGroupActivitySummaryCrewFormation Crew or crewAI:
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

For WhatsApp Business API specific questions:
- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
- [Meta for Developers Support](https://developers.facebook.com/support)

Let's create wonders together with the power and simplicity of crewAI.
