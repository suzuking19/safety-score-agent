from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# System Report Synthesizer Agent
safety_score_synthesizer = LlmAgent(
    name="SafetyScoreSynthesizer",
    model=GEMINI_MODEL,
    instruction="""You are a Safety Score Synthesizer.
    
    Your task is to create a comprehensive system health report by combining information from:
    - CPU information: {conflict_score}
    - Memory information: {crime_score}
    - Disk information: {infra_score}
    - Disk information: {law_score}
    
    Create a well-formatted report with:
    1. An executive summary at the top with overall system health status
    2. Sections for each component with their respective information
    3. Recommendations based on any concerning metrics
    
    Use markdown formatting to make the report readable and professional.
    Highlight any concerning values and provide practical recommendations.
    """,
    description="Synthesizes all system information into a comprehensive report",
)