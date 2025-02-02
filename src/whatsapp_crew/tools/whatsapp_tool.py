from crewai.tools import BaseTool
from typing import Type, Optional, List, Dict
from pydantic import BaseModel, Field
import requests
import yaml
import os
from datetime import datetime
import pytz
from pathlib import Path

class WhatsAppMessage(BaseModel):
    """Schema for WhatsApp messages."""
    message_id: str = Field(..., description="Unique message identifier")
    text: str = Field(..., description="The message text")
    timestamp: datetime = Field(..., description="Message timestamp")
    sender: Dict = Field(..., description="Sender information with id and name")
    content_type: str = Field(..., description="Type of content (text, image, video, etc.)")
    media_url: Optional[str] = Field(None, description="URL for media content if any")
    caption: Optional[str] = Field(None, description="Caption for media content")
    quoted_message_id: Optional[str] = Field(None, description="ID of quoted message if any")
    mentions: List[str] = Field(default_factory=list, description="List of mentioned users")
    tags: List[str] = Field(default_factory=list, description="List of hashtags in message")

class WhatsAppToolInput(BaseModel):
    """Input schema for WhatsApp operations."""
    operation: str = Field(..., description="Operation to perform: 'send' or 'receive'")
    message: Optional[str] = Field(None, description="Message to send (for 'send' operation)")
    since: Optional[datetime] = Field(None, description="Retrieve messages since this time (for 'receive' operation)")

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
        if not config_path.exists():
            raise FileNotFoundError(
                "WhatsApp configuration file not found. Please copy whatsapp_config.example.yaml "
                "to whatsapp_config.yaml and update with your credentials."
            )
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _send_message(self, message: str) -> str:
        """Send a message to the WhatsApp group."""
        endpoint = f"{self.base_url}/{self.config['whatsapp']['phone_number_id']}/messages"
        
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "group",
            "to": self.config['whatsapp']['group_id'],
            "type": "text",
            "text": {"body": message}
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return f"Message sent successfully. Message ID: {response.json().get('messages', [{}])[0].get('id')}"
        except requests.exceptions.RequestException as e:
            error_msg = f"Error sending message: {str(e)}"
            if hasattr(e.response, 'json'):
                error_msg += f"\nAPI Error: {e.response.json()}"
            raise RuntimeError(error_msg)

    def _receive_messages(self, since: Optional[datetime] = None) -> List[WhatsAppMessage]:
        """Retrieve messages from the WhatsApp group."""
        endpoint = f"{self.base_url}/{self.config['whatsapp']['phone_number_id']}/messages"
        
        params = {
            "group_id": self.config['whatsapp']['group_id']
        }
        if since:
            params['since'] = since.isoformat()

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return self._process_messages(response.json())
        except requests.exceptions.RequestException as e:
            error_msg = f"Error receiving messages: {str(e)}"
            if hasattr(e.response, 'json'):
                error_msg += f"\nAPI Error: {e.response.json()}"
            raise RuntimeError(error_msg)

    def _process_messages(self, response_data: Dict) -> List[WhatsAppMessage]:
        """Process and format received messages."""
        messages = []
        
        for msg in response_data.get('data', []):
            processed_msg = WhatsAppMessage(
                message_id=msg['id'],
                text=msg.get('text', {}).get('body', ''),
                timestamp=datetime.fromtimestamp(int(msg['timestamp'])),
                sender={
                    'id': msg['from'],
                    'name': msg.get('contact', {}).get('name', 'Unknown')
                },
                content_type=msg['type'],
                media_url=msg.get('image', {}).get('url') or msg.get('video', {}).get('url'),
                caption=msg.get('image', {}).get('caption') or msg.get('video', {}).get('caption'),
                quoted_message_id=msg.get('context', {}).get('id'),
                mentions=[m['name'] for m in msg.get('mentions', [])],
                tags=self._extract_tags(msg.get('text', {}).get('body', ''))
            )
            messages.append(processed_msg)
        
        return messages

    def _extract_tags(self, text: str) -> List[str]:
        """Extract hashtags from message text."""
        if not text:
            return []
        
        return [
            word[1:] for word in text.split()
            if word.startswith('#') and len(word) > 1
        ]

    def _run(self, operation: str, message: Optional[str] = None, since: Optional[datetime] = None) -> str:
        """Execute the WhatsApp operation."""
        try:
            if operation == "send" and message:
                return self._send_message(message)
            elif operation == "receive":
                messages = self._receive_messages(since)
                return f"Retrieved {len(messages)} messages successfully"
            else:
                raise ValueError("Invalid operation or missing parameters")
        except Exception as e:
            return f"Operation failed: {str(e)}" 