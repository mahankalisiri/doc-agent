from pydantic import BaseModel, Field
from typing import List

class CategoryAnalysis(BaseModel):
    score: str = Field(description="Excellent, Good, Fair, Poor")
    issues: List[str]
    suggestions: List[str]

class DocumentationAnalysis(BaseModel):
    readability: CategoryAnalysis
    structure: CategoryAnalysis
    completeness: CategoryAnalysis
    style_guidelines: CategoryAnalysis
