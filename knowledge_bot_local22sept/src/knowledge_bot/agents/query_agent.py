from crewai import Agent

def build_query_agent(config) -> Agent:
    return Agent(
        config=config,
        tools=[],
        verbose=config.get("verbose", True)
    )

