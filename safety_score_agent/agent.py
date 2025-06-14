from google.adk.agents import ParallelAgent, SequentialAgent

safety_score_gatherer = ParallelAgent(
    name="safety_score_gatherer",
    sub_agents=[]
)

root_agent = SequentialAgent(
    name="safety_score_agent",
    sub_agents=[
        safety_score_gatherer,

    ]
)