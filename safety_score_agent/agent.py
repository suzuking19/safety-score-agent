from google.adk.agents import ParallelAgent, SequentialAgent

# Import all sub-agents
from .sub_agents.conflict_agent.agent import conflict_info_agent
from .sub_agents.crime_agent.agent import crime_agent
from .sub_agents.infra_agent.agent import infra_agent
from .sub_agents.law_agent.agent import law_agent
from .sub_agents.synthesizer_agent.agent import safety_score_synthesizer

# Parallel agent for gathering safety information from all specialized agents
safety_score_gatherer = ParallelAgent(
    name="safety_score_gatherer",
    sub_agents=[
        conflict_info_agent,  # テロ・紛争リスク評価
        crime_agent,          # 犯罪・治安評価
        infra_agent,          # 社会基盤安定度評価
        law_agent,            # 法執行機関信頼性評価
    ]
)

# Main sequential agent that first gathers information, then synthesizes the final report
root_agent = SequentialAgent(
    name="safety_score_agent",
    sub_agents=[
        safety_score_gatherer,    # 4つの専門エージェントから情報収集
        safety_score_synthesizer, # 総合安全スコア算出・レポート生成
    ]
)