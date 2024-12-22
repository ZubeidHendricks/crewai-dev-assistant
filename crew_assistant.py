from crewai import Agent, Task, Crew, Process
from github import Github
import os
from datetime import datetime

class DevAssistant:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.setup_agents()

    def setup_agents(self):
        self.project_manager = Agent(
            role='Project Manager',
            goal='Manage and coordinate development tasks',
            backstory='Experienced project manager with agile expertise'
        )

        self.tech_lead = Agent(
            role='Technical Lead',
            goal='Review code and maintain technical standards',
            backstory='Senior developer focused on code quality'
        )

    def create_daily_tasks(self):
        return [
            Task(
                description=f'Review code changes and PRs for {datetime.now().strftime("%Y-%m-%d")}',
                agent=self.tech_lead
            ),
            Task(
                description=f'Update project status and plan next steps for {datetime.now().strftime("%Y-%m-%d")}',
                agent=self.project_manager
            )
        ]

    def run(self):
        crew = Crew(
            agents=[self.project_manager, self.tech_lead],
            tasks=self.create_daily_tasks(),
            process=Process.sequential
        )
        return crew.kickoff()

if __name__ == '__main__':
    assistant = DevAssistant()
    result = assistant.run()
    print(result)