from crewai.tools import BaseTool
from typing import Type, Optional, List
from pydantic import BaseModel, Field
import requests
import yaml
import os
from datetime import datetime
import pytz
from pathlib import Path

class WhatsAppMessage(BaseModel):
    """Schema for WhatsApp messages."""
    text: str = Field(..., description="The message text")
    timestamp: datetime = Field(..., description="Message timestamp")
    sender: str = Field(..., description="Sender information")

class WhatsAppToolInput(BaseModel):
    """Input schema for WhatsApp operations."""
    operation: str = Field(..., description="Operation to perform: 'send' or 'receive'")
    message: Optional[str] = Field(None, description="Message to send (for 'send' operation)")
    time_range: Optional[str] = Field(None, description="Time range for message retrieval (for 'receive' operation)")

class WhatsAppTool(BaseTool):
    name: str = "WhatsApp Communication Tool"
    description: str = (
        "A tool for sending and receiving WhatsApp messages using the WhatsApp Business API. "
        "Can be used to retrieve messages from a group or send messages to a group."
    )
    args_schema: Type[BaseModel] = WhatsAppToolInput

    def __init__(self):
        super().__init__()
        self.config = self._load_config()
        self.base_url = f"https://graph.facebook.com/{self.config['whatsapp']['api_version']}"
        self.headers = {
            "Authorization": f"Bearer {self.config['whatsapp']['access_token']}",
            "Content-Type": "application/json"
        }

    def _load_config(self) -> dict:
        """Load WhatsApp configuration from YAML file."""
        config_path = Path(__file__).parent.parent / "config" / "whatsapp_config.yaml"
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _send_message(self, message: str) -> str:
        """Send a message to the WhatsApp group."""
        endpoint = f"{self.base_url}/{self.config['whatsapp']['phone_number_id']}/messages"
        
        data = {
            "messaging_product": "whatsapp",
            "to": self.config['whatsapp']['group_id'],
            "type": "text",
            "text": {"body": message}
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return f"Message sent successfully: {response.json()}"
        except requests.exceptions.RequestException as e:
            return f"Error sending message: {str(e)}"

    def _receive_messages(self, time_range: Optional[str] = None) -> List[WhatsAppMessage]:
        """Retrieve messages from the WhatsApp group."""
        # Note: The actual implementation would depend on your webhook setup
        # This is a placeholder that would need to be integrated with your webhook handler
        return "Messages would be retrieved here based on your webhook implementation"

    def _run(self, operation: str, message: Optional[str] = None, time_range: Optional[str] = None) -> str:
        """Execute the WhatsApp operation."""
        if operation == "send" and message:
            return self._send_message(message)
        elif operation == "receive":
            return self._receive_messages(time_range)
        else:
            return "Invalid operation or missing parameters" 