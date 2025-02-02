import os
import requests
from datetime import datetime
from typing import Dict, List, Optional
import yaml

class WhatsAppAPI:
    """Tool for interacting with WhatsApp Business API."""
    
    def __init__(self):
        self.config = self._load_config()
        self.base_url = f"https://graph.facebook.com/{self.config['api_version']}"
        self.headers = {
            "Authorization": f"Bearer {self.config['access_token']}",
            "Content-Type": "application/json"
        }
    
    def _load_config(self) -> Dict:
        """Load WhatsApp configuration."""
        config_path = "whatsapp_config.yaml"
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                "WhatsApp configuration file not found. Please copy whatsapp_config.example.yaml "
                "to whatsapp_config.yaml and update with your credentials."
            )
        
        with open(config_path) as f:
            config = yaml.safe_load(f)
            return config['whatsapp']
    
    def receive_messages(self, since: Optional[datetime] = None) -> List[Dict]:
        """Retrieve messages from the WhatsApp group."""
        endpoint = f"{self.base_url}/{self.config['phone_number_id']}/messages"
        
        params = {
            "group_id": self.config['group_id']
        }
        if since:
            params['since'] = since.isoformat()
        
        response = requests.get(endpoint, headers=self.headers, params=params)
        response.raise_for_status()
        
        return self._process_messages(response.json())
    
    def send_message(self, content: str) -> Dict:
        """Send a message to the WhatsApp group."""
        endpoint = f"{self.base_url}/{self.config['phone_number_id']}/messages"
        
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "group",
            "to": self.config['group_id'],
            "type": "text",
            "text": {"body": content}
        }
        
        response = requests.post(endpoint, headers=self.headers, json=data)
        response.raise_for_status()
        
        return response.json()
    
    def _process_messages(self, response_data: Dict) -> List[Dict]:
        """Process and format received messages."""
        messages = []
        
        for msg in response_data.get('data', []):
            processed_msg = {
                "message_id": msg['id'],
                "timestamp": msg['timestamp'],
                "sender": {
                    "id": msg['from'],
                    "name": msg.get('contact', {}).get('name', 'Unknown')
                },
                "content": {
                    "type": msg['type'],
                    "text": msg.get('text', {}).get('body', ''),
                    "media_url": msg.get('image', {}).get('url') or msg.get('video', {}).get('url'),
                    "caption": msg.get('image', {}).get('caption') or msg.get('video', {}).get('caption')
                },
                "metadata": {
                    "quoted_message_id": msg.get('context', {}).get('id'),
                    "mentions": msg.get('mentions', []),
                    "tags": self._extract_tags(msg.get('text', {}).get('body', ''))
                }
            }
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