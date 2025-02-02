import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

class SummaryStorage:
    """Tool for storing and retrieving WhatsApp group summaries."""
    
    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.summaries_dir = self.base_dir / "summaries"
        self.current_dir = self.summaries_dir / "current"
        self.archive_dir = self.summaries_dir / "archive"
        
        # Ensure directories exist
        self.current_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def store_summary(self, group_id: str, summary_data: Dict, date: Optional[str] = None) -> Dict[str, str]:
        """Store summary in both JSON and Markdown formats."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        day_dir = self.current_dir / date
        day_dir.mkdir(exist_ok=True)
        
        # Add metadata to summary
        summary_data["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        # Store JSON format
        json_filename = f"{group_id}_summary.json"
        json_path = day_dir / json_filename
        with open(json_path, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        # Store Markdown format
        md_filename = f"{group_id}_summary.md"
        md_path = day_dir / md_filename
        markdown_content = self._generate_markdown(summary_data)
        with open(md_path, 'w') as f:
            f.write(markdown_content)
        
        return {
            "json": str(json_path),
            "markdown": str(md_path)
        }
    
    def get_summary(self, group_id: str, date: Optional[str] = None, format: str = "json") -> Optional[Dict]:
        """Retrieve summary for a specific date."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        day_dir = self.current_dir / date
        if not day_dir.exists():
            return None
        
        if format == "json":
            filepath = day_dir / f"{group_id}_summary.json"
            if filepath.exists():
                with open(filepath) as f:
                    return json.load(f)
        else:
            filepath = day_dir / f"{group_id}_summary.md"
            if filepath.exists():
                with open(filepath) as f:
                    return f.read()
        
        return None
    
    def archive_old_summaries(self, days_threshold: int = 30) -> Dict[str, list]:
        """Move summaries older than threshold to archive."""
        cutoff_date = datetime.now().date()
        archived_files = {"json": [], "markdown": []}
        
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
                    
                    # Move JSON files
                    for file in day_dir.glob("*_summary.json"):
                        archive_path = month_dir / file.name
                        file.rename(archive_path)
                        archived_files["json"].append(str(archive_path))
                    
                    # Move Markdown files
                    for file in day_dir.glob("*_summary.md"):
                        archive_path = month_dir / file.name
                        file.rename(archive_path)
                        archived_files["markdown"].append(str(archive_path))
                    
                    # Remove empty directory
                    if not any(day_dir.iterdir()):
                        day_dir.rmdir()
            except ValueError:
                continue  # Skip if directory name is not a date
        
        return archived_files
    
    def _generate_markdown(self, summary_data: Dict) -> str:
        """Generate markdown format from summary data."""
        date = summary_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        group_name = summary_data.get("group_id", "Group")
        
        # Build markdown content
        md = [
            f"# Daily Group Summary - {date}\n",
            "## 🔑 Key Discussions"
        ]
        
        # Add key discussions
        for discussion in summary_data["summary"]["key_discussions"]:
            md.append(f"- **{discussion['topic']}**: {discussion['content']}")
        
        # Add activity overview
        activity = summary_data["summary"]["activity"]
        md.extend([
            "\n## 📊 Activity Overview",
            f"- Total Messages: {activity['total_messages']}",
            f"- Active Participants: {activity['active_participants']}",
            f"- Peak Activity Time: {activity['peak_time']}"
        ])
        
        # Add action items
        md.append("\n## 🎯 Action Items")
        for item in summary_data["summary"]["action_items"]:
            due = f" (Due: {item['due_date']})" if item.get('due_date') else ""
            assigned = f" [@{', @'.join(item['assigned_to'])}]" if item.get('assigned_to') else ""
            md.append(f"- {item['description']}{assigned}{due}")
        
        # Add notable interactions
        md.append("\n## 👥 Notable Interactions")
        for interaction in summary_data["summary"]["notable_interactions"]:
            participants = f" [@{', @'.join(interaction['participants'])}]"
            md.append(f"- {interaction['description']}{participants}")
        
        # Add resources
        md.append("\n## 📌 Important Links & Resources")
        for resource in summary_data["summary"]["resources"]:
            md.append(f"- [{resource['description']}]({resource['url']})")
        
        # Add footer
        md.extend([
            f"\n#DailySummary #{group_name}",
            f"\n_Generated at {summary_data['metadata']['generated_at']}_"
        ])
        
        return "\n".join(md) 