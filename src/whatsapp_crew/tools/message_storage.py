import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class MessageStorage:
    """Tool for storing and retrieving WhatsApp messages."""
    
    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.messages_dir = self.base_dir / "messages"
        self.current_dir = self.messages_dir / "current"
        self.archive_dir = self.messages_dir / "archive"
        
        # Ensure directories exist
        self.current_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def store_messages(self, group_id: str, messages: List[Dict]) -> str:
        """Store messages in the current directory."""
        today = datetime.now().strftime("%Y-%m-%d")
        day_dir = self.current_dir / today
        day_dir.mkdir(exist_ok=True)
        
        # Create filename with timestamp for multiple saves in a day
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{group_id}_{timestamp}.json"
        filepath = day_dir / filename
        
        data = {
            "group_id": group_id,
            "messages": messages
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(filepath)
    
    def get_messages(self, group_id: str, date: Optional[str] = None) -> List[Dict]:
        """Retrieve messages for a specific date."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        day_dir = self.current_dir / date
        if not day_dir.exists():
            return []
        
        messages = []
        for file in day_dir.glob(f"{group_id}_*.json"):
            with open(file) as f:
                data = json.load(f)
                messages.extend(data["messages"])
        
        return messages
    
    def archive_old_messages(self, days_threshold: int = 7) -> List[str]:
        """Move messages older than threshold to archive."""
        cutoff_date = datetime.now().date()
        archived_files = []
        
        # Check each date directory in current
        for day_dir in self.current_dir.iterdir():
            if not day_dir.is_dir():
                continue
                
            try:
                dir_date = datetime.strptime(day_dir.name, "%Y-%m-%d").date()
                days_old = (cutoff_date - dir_date).days
                
                if days_old > days_threshold:
                    # Move to archive
                    month_dir = self.archive_dir / dir_date.strftime("%Y-%m")
                    month_dir.mkdir(exist_ok=True)
                    
                    for file in day_dir.glob("*.json"):
                        archive_path = month_dir / file.name
                        file.rename(archive_path)
                        archived_files.append(str(archive_path))
                    
                    # Remove empty directory
                    if not any(day_dir.iterdir()):
                        day_dir.rmdir()
            except ValueError:
                continue  # Skip if directory name is not a date
        
        return archived_files 