from langchain_core.prompts import ChatPromptTemplate

analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert technical writer.
Analyze the given documentation and provide feedback on:
- Readability
- Structure
- Completeness
- Style (clarity, tone, simplification)

Output as: {format_instructions}"""),
    ("human", "URL: {url}\n\nContent:\n{content}")
])

revision_prompt = ChatPromptTemplate.from_messages([
    ("system", "Revise this documentation using the feedback. Keep content accurate."),
    ("human", """
Original Content:
{original_content}

Feedback:
{feedback}
""")
])
