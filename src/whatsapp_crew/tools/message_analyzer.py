import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class MessageAnalyzer:
    """Tool for analyzing and processing WhatsApp messages."""
    
    def __init__(self, knowledge_dir: str = "knowledge"):
        self.knowledge_dir = Path(knowledge_dir)
        self.filters = self._load_filters()
        self.topics = self._load_topics()
    
    def _load_filters(self) -> Dict:
        """Load message filtering rules."""
        with open(self.knowledge_dir / "rules/filters.yaml") as f:
            return yaml.safe_load(f)
    
    def _load_topics(self) -> Dict:
        """Load topic classification patterns."""
        with open(self.knowledge_dir / "patterns/topics.yaml") as f:
            return yaml.safe_load(f)
    
    def analyze_messages(self, messages: List[Dict]) -> Dict:
        """Analyze a batch of messages and extract insights."""
        # Filter messages
        filtered_messages = self._filter_messages(messages)
        
        # Analyze content
        topics = self._classify_topics(filtered_messages)
        activity = self._analyze_activity(filtered_messages)
        actions = self._extract_action_items(filtered_messages)
        interactions = self._analyze_interactions(filtered_messages)
        resources = self._extract_resources(filtered_messages)
        
        return {
            "key_discussions": topics,
            "activity": activity,
            "action_items": actions,
            "notable_interactions": interactions,
            "resources": resources
        }
    
    def _filter_messages(self, messages: List[Dict]) -> List[Dict]:
        """Apply filtering rules to messages."""
        filtered = []
        
        for msg in messages:
            text = msg['content']['text']
            
            # Check exclude patterns
            if any(re.match(pattern, text) for pattern in self.filters['exclude_patterns']):
                continue
            
            # Check include patterns
            if any(re.match(pattern, text) for pattern in self.filters['include_patterns']):
                filtered.append(msg)
                continue
            
            # Include messages with substantial content
            if len(text.split()) > 3:  # Messages with more than 3 words
                filtered.append(msg)
        
        return filtered
    
    def _classify_topics(self, messages: List[Dict]) -> List[Dict]:
        """Classify messages into topics."""
        topics = {}
        
        for msg in messages:
            text = msg['content']['text'].lower()
            
            # Check each topic's keywords
            for topic in self.topics['topics']:
                if any(keyword.lower() in text for keyword in topic['keywords']):
                    if topic['name'] not in topics:
                        topics[topic['name']] = {
                            'content': [],
                            'participants': set()
                        }
                    topics[topic['name']]['content'].append(msg['content']['text'])
                    topics[topic['name']]['participants'].add(msg['sender']['name'])
        
        # Format topics for output
        return [
            {
                'topic': topic_name,
                'content': ' | '.join(data['content']),
                'participants': list(data['participants'])
            }
            for topic_name, data in topics.items()
        ]
    
    def _analyze_activity(self, messages: List[Dict]) -> Dict:
        """Analyze message activity patterns."""
        if not messages:
            return {
                'total_messages': 0,
                'active_participants': 0,
                'peak_time': '00:00'
            }
        
        # Count messages by hour
        hour_counts = {}
        participants = set()
        
        for msg in messages:
            timestamp = datetime.fromtimestamp(int(msg['timestamp']))
            hour = timestamp.strftime('%H:00')
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
            participants.add(msg['sender']['name'])
        
        # Find peak hour
        peak_time = max(hour_counts.items(), key=lambda x: x[1])[0]
        
        return {
            'total_messages': len(messages),
            'active_participants': len(participants),
            'peak_time': peak_time
        }
    
    def _extract_action_items(self, messages: List[Dict]) -> List[Dict]:
        """Extract action items from messages."""
        action_items = []
        action_patterns = [
            r'(?i)(?:todo|to-do|to do):?\s*(.+)',
            r'(?i)(?:action item|task):?\s*(.+)',
            r'(?i)(?:please|pls|kindly)\s+(?:do|handle|take care of)\s+(.+)',
            r'(?i)need\s+to\s+(?:do|handle|complete)\s+(.+)'
        ]
        
        for msg in messages:
            text = msg['content']['text']
            
            for pattern in action_patterns:
                match = re.search(pattern, text)
                if match:
                    action = {
                        'description': match.group(1).strip(),
                        'assigned_to': self._extract_mentions(msg),
                    }
                    
                    # Try to extract due date if present
                    due_date = self._extract_due_date(text)
                    if due_date:
                        action['due_date'] = due_date
                    
                    action_items.append(action)
        
        return action_items
    
    def _analyze_interactions(self, messages: List[Dict]) -> List[Dict]:
        """Analyze notable interactions between participants."""
        interactions = []
        
        # Group messages by thread (quoted messages)
        threads = {}
        for msg in messages:
            quoted_id = msg['metadata']['quoted_message_id']
            if quoted_id:
                if quoted_id not in threads:
                    threads[quoted_id] = []
                threads[quoted_id].append(msg)
        
        # Analyze significant threads
        for thread_msgs in threads.values():
            if len(thread_msgs) >= 3:  # Threads with 3+ replies
                participants = {msg['sender']['name'] for msg in thread_msgs}
                if len(participants) >= 2:  # Interactions between 2+ people
                    interactions.append({
                        'description': thread_msgs[0]['content']['text'][:100] + '...',
                        'participants': list(participants)
                    })
        
        return interactions
    
    def _extract_resources(self, messages: List[Dict]) -> List[Dict]:
        """Extract shared resources and links."""
        resources = []
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        
        for msg in messages:
            # Extract URLs
            urls = re.findall(url_pattern, msg['content']['text'])
            for url in urls:
                resources.append({
                    'type': 'link',
                    'url': url,
                    'description': msg['content']['text'][:50] + '...'
                })
            
            # Add media resources
            if msg['content'].get('media_url'):
                resources.append({
                    'type': msg['content']['type'],
                    'url': msg['content']['media_url'],
                    'description': msg['content'].get('caption', 'Shared media')
                })
        
        return resources
    
    def _extract_mentions(self, message: Dict) -> List[str]:
        """Extract mentioned users from a message."""
        return [mention['name'] for mention in message['metadata']['mentions']]
    
    def _extract_due_date(self, text: str) -> Optional[str]:
        """Extract due date from message text."""
        date_patterns = [
            r'(?i)due\s+(?:by|on|before)?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(?i)deadline:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(?i)by\s+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    # Try to parse and standardize the date
                    date_str = match.group(1)
                    date = datetime.strptime(date_str, '%d/%m/%Y')
                    return date.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        
        return None 