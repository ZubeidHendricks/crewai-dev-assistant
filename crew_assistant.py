from crewai import Agent, Task, Crew, Process
from langchain.llms import Anthropic
from github import Github
import os
from datetime import datetime

class DevAssistant:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        # Initialize Claude
        self.llm = Anthropic(
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
            model="claude-3-opus-20240229"
        )
        self.setup_agents()

    def setup_agents(self):
        self.project_manager = Agent(
            role='Project Manager',
            goal='Manage and coordinate development tasks',
            backstory='Experienced project manager with agile expertise',
            llm=self.llm
        )

        self.tech_lead = Agent(
            role='Technical Lead',
            goal='Review code and maintain technical standards',
            backstory='Senior developer focused on code quality',
            llm=self.llm
        )

        self.qa_specialist = Agent(
            role='QA Specialist',
            goal='Ensure quality and testing standards',
            backstory='Expert in quality assurance and testing automation',
            llm=self.llm
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
            ),
            Task(
                description=f'Review and update test cases for {datetime.now().strftime("%Y-%m-%d")}',
                agent=self.qa_specialist
            )
        ]

    def run(self):
        crew = Crew(
            agents=[self.project_manager, self.tech_lead, self.qa_specialist],
            tasks=self.create_daily_tasks(),
            process=Process.sequential
        )
        return crew.kickoff()

if __name__ == '__main__':
    assistant = DevAssistant()
    result = assistant.run()
    print(result)