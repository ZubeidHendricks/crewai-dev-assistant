from crewai import Agent, Task, Crew, Process
from langchain.llms import Anthropic
from github import Github
import os
from datetime import datetime

class DevAssistant:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        # Initialize Claude 3.5 Sonnet specifically
        self.llm = Anthropic(
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
            model="claude-3-sonnet-20240229",
            temperature=0.7  # Good balance for creative yet focused responses
        )
        self.setup_agents()

    def setup_agents(self):
        self.project_manager = Agent(
            role='Project Manager',
            goal='Manage and coordinate development tasks',
            backstory='Experienced project manager with agile expertise',
            llm=self.llm,
            max_iterations=3  # Limit iterations for cost efficiency
        )

        self.tech_lead = Agent(
            role='Technical Lead',
            goal='Review code and maintain technical standards',
            backstory='Senior developer focused on code quality',
            llm=self.llm,
            max_iterations=3
        )

        self.qa_specialist = Agent(
            role='QA Specialist',
            goal='Ensure quality and testing standards',
            backstory='Expert in quality assurance and testing automation',
            llm=self.llm,
            max_iterations=3
        )

    def create_daily_tasks(self):
        # Create more focused tasks suited for Sonnet's capabilities
        return [
            Task(
                description=(
                    "Review latest code changes in the POS repositories:\n"
                    "- Check for coding standards compliance\n"
                    "- Identify potential performance issues\n"
                    "- Suggest specific improvements"
                ),
                agent=self.tech_lead
            ),
            Task(
                description=(
                    "Create daily project status report:\n"
                    "- Track progress on current sprint goals\n"
                    "- Identify blockers and risks\n"
                    "- Propose specific next steps"
                ),
                agent=self.project_manager
            ),
            Task(
                description=(
                    "Update testing strategy:\n"
                    "- Review current test coverage\n"
                    "- Identify critical test scenarios\n"
                    "- Propose automation improvements"
                ),
                agent=self.qa_specialist
            )
        ]

    def run(self):
        crew = Crew(
            agents=[self.project_manager, self.tech_lead, self.qa_specialist],
            tasks=self.create_daily_tasks(),
            process=Process.sequential,
            verbose=True  # Enable detailed logging
        )
        
        try:
            result = crew.kickoff()
            # Save results to a daily log file
            with open(f'logs/daily_run_{datetime.now().strftime("%Y%m%d")}.txt', 'w') as f:
                f.write(result)
            return result
        except Exception as e:
            print(f"Error during crew execution: {str(e)}")
            return None

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    assistant = DevAssistant()
    result = assistant.run()
    
    if result:
        print("\nExecution completed successfully!")
        print("\nSummary of actions:")
        print(result)