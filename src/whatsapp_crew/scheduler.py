import schedule
import time
import yaml
import pytz
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, Optional

class Scheduler:
    """Scheduler for managing periodic WhatsApp group summary tasks."""
    
    def __init__(self):
        self.config = self._load_config()
        self.timezone = pytz.timezone(self.config['timezone'])
        self.scheduled_jobs = {}
        
    def _load_config(self) -> Dict:
        """Load WhatsApp configuration."""
        config_path = "whatsapp_config.yaml"
        if not os.path.exists(config_path):
            raise FileNotFoundError("WhatsApp configuration file not found.")
        
        with open(config_path) as f:
            config = yaml.safe_load(f)
            return config['whatsapp']
    
    def schedule_daily_summary(self, task: Callable) -> None:
        """Schedule daily summary generation."""
        summary_time = self.config['summary_time']
        
        # Schedule the task
        job = schedule.every().day.at(summary_time).do(
            self._run_task_with_retry,
            task=task,
            max_retries=3,
            retry_delay=300  # 5 minutes
        )
        
        self.scheduled_jobs['daily_summary'] = job
    
    def schedule_archival(self, task: Callable, interval_days: int = 1) -> None:
        """Schedule periodic data archival."""
        # Run at midnight
        job = schedule.every(interval_days).days.at("00:00").do(
            self._run_task_with_retry,
            task=task,
            max_retries=3,
            retry_delay=600  # 10 minutes
        )
        
        self.scheduled_jobs['archival'] = job
    
    def _run_task_with_retry(
        self,
        task: Callable,
        max_retries: int = 3,
        retry_delay: int = 300,
        **kwargs
    ) -> None:
        """Run a task with retry logic."""
        attempt = 0
        last_error = None
        
        while attempt < max_retries:
            try:
                # Add timezone info to kwargs
                kwargs['current_time'] = datetime.now(self.timezone)
                
                # Run the task
                task(**kwargs)
                return  # Success
            except Exception as e:
                attempt += 1
                last_error = e
                
                if attempt < max_retries:
                    # Wait before retry
                    time.sleep(retry_delay)
                    # Increase delay for next retry
                    retry_delay *= 2
        
        # Log the failure after all retries
        print(f"Task failed after {max_retries} attempts. Last error: {last_error}")
    
    def run(self) -> None:
        """Run the scheduler."""
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("Scheduler stopped by user.")
    
    def stop(self) -> None:
        """Stop all scheduled jobs."""
        for job_name, job in self.scheduled_jobs.items():
            schedule.cancel_job(job)
        self.scheduled_jobs.clear()
    
    def get_next_run(self, job_name: str) -> Optional[datetime]:
        """Get the next scheduled run time for a job."""
        job = self.scheduled_jobs.get(job_name)
        if job:
            return job.next_run
        return None 