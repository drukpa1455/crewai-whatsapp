from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class WhatsappGroupActivitySummaryCrewFormationCrew():
    """WhatsappGroupActivitySummaryCrewFormation crew"""

    @agent
    def message_handler(self) -> Agent:
        return Agent(
            config=self.agents_config['message_handler'],
            tools=[],
        )

    @agent
    def summarization_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['summarization_expert'],
            tools=[],
        )


    @task
    def receive_messages_task(self) -> Task:
        return Task(
            config=self.tasks_config['receive_messages_task'],
            tools=[],
        )

    @task
    def summarize_messages_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_messages_task'],
            tools=[],
        )

    @task
    def send_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['send_summary_task'],
            tools=[],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the WhatsappGroupActivitySummaryCrewFormation crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
