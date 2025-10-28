# MAIN CODE for DATA MODEL and EXTRACTION MODEL
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

load_dotenv()


# Validate required environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def validate_env_vars():
    missing_vars = []
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_google_api_key_here":
        missing_vars.append("OPENAI_API_KEY")

    if missing_vars:
        raise ValueError(
            f"Missing or invalid environment variables: {', '.join(missing_vars)}. Please check your .env file."
        )


validate_env_vars()


class FieldExtractor(BaseModel):
    """Structured Extraction Schema for Candidate Information"""

    NameExtractor: str = Field(description="Full name of the candidate")
    EmailExtractor: str = Field(description="Email address of the candidate")
    SkillsExtractor: list[str] = Field(
        description="All programming, data science and machine learning skills of the candidate"
    )


class ResumeData(BaseModel):
    """Candidate Data Schema"""

    CandidateData: FieldExtractor = Field(
        description="Structured candidate information extracted from resume"
    )


class ResumeExtractor:
    """Resume Extraction Framework using LLM"""

    def __init__(self, strategy_config: str, raw_text: str):
        self.StrategyConfig = strategy_config
        self.raw_text = raw_text

    def __extract__(self):
        """Extract structured data from raw resume text using LLM based on strategy config"""
        if self.StrategyConfig == "llm":
            model = init_chat_model(
                "gemini-2.5-flash", model_provider="google_genai", temperature=0
            )

            return model.with_structured_output(ResumeData).invoke(self.raw_text)

        else:
            raise ValueError(
                "Unsupported strategy config, only 'llm' is supported for now."
            )
