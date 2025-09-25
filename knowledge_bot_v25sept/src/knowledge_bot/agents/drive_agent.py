from crewai import Agent

def build_drive_agent(config) -> Agent:
    return Agent(
        config=config,
        tools=[],
        verbose=config.get("verbose", True)
    )

