import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from models import DocumentationAnalysis 
from prompts import analysis_prompt     

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API")  
)


parser = JsonOutputParser(pydantic_object=DocumentationAnalysis)


chain = analysis_prompt | llm | parser


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
