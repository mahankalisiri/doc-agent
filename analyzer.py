import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from models import DocumentationAnalysis  # your Pydantic model
from prompts import analysis_prompt      # your loaded PromptTemplate

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API")  # expects .env with GEMINI_API=...
)

# Output parser to enforce structure
parser = JsonOutputParser(pydantic_object=DocumentationAnalysis)

# Chain: prompt -> LLM -> structured output
chain = analysis_prompt | llm | parser

# ✅ THIS is what app.py expects
def analyze_document(content: str, url: str = "N/A") -> dict:
    """
    Analyze the given documentation content using Gemini LLM.
    
    Args:
        content (str): The raw documentation text.
        url (str): The source URL (optional).
    
    Returns:
        dict: A dictionary with readability, structure, completeness, and style_guidelines.
    """
    return chain.invoke({
        "url": url,
        "content": content,
        "format_instructions": parser.get_format_instructions()
    })
