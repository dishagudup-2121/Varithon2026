from pydantic import BaseModel, ConfigDict

class ExplainResponse(BaseModel):
    language: str
    summary: str
    reasoning: str
    confidence_caveat: str
    
    model_config = ConfigDict(from_attributes=True)
