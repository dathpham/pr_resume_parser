import os
from parser.file_parser import FileParser
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from datamodel.extraction_model import ResumeData, ResumeExtractor , FieldExtractor
from resume_parser import ResumeParserFramework

load_dotenv()

# Testing environment variable loading

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def test_env():
    assert (
        GOOGLE_API_KEY is not None and GOOGLE_API_KEY != "your_google_api_key_here"
    ), "GOOGLE_API_KEY is not set properly in .env file."

def test_init_chat_model():
    model = init_chat_model(
                "gemini-2.5-flash", model_provider="google_genai", temperature=0
            )
    response = model.invoke("Hello")
    assert response is not None and len(response.content) > 0, "Chat model initialization failed."

# Testing FileParser, ResumeExtractor, and ResumeParserFramework
def test_file_parser():

    parser = FileParser()
    pdf_content = parser.parse("sample.pdf")
    docx_content = parser.parse("sample.docx")
    assert isinstance(pdf_content, str) and len(pdf_content) > 0, "PDF parsing failed."
    assert (
        isinstance(docx_content, str) and len(docx_content) > 0
    ), "DOCX parsing failed."

def test_field_extractor():
    fe= FieldExtractor(NameExtractor ="John Doe", EmailExtractor="azxc@gmail.com",
                       SkillsExtractor=["Python", "Machine Learning", "Data Science"])

    assert fe.NameExtractor =="John Doe"
    assert fe.EmailExtractor == 'azxc@gmail.com'
    assert fe.SkillsExtractor == ["Python", "Machine Learning", "Data Science"]

def test_resume_data():
    fe= FieldExtractor(NameExtractor ="John Doe", EmailExtractor="azxc@gmail.com",
                       SkillsExtractor=["Python", "Machine Learning", "Data Science"])
    rd = ResumeData(CandidateData=fe)
    assert rd.CandidateData == fe, "ResumeData initialization failed."

def test_resume_extractor():

    sample_text = """Ken Bre
    Email:  abc@gmail.com
    Skills: Machine Learning, Data Science, Python"""
    extractor = ResumeExtractor(strategy_config="llm", raw_text=sample_text)
    structured_data = extractor.__extract__()
    assert (
        structured_data.CandidateData.NameExtractor is not None
    ), "Name extraction failed."
    assert (
        structured_data.CandidateData.EmailExtractor is not None
    ), "Email extraction failed."
    assert (
        len(structured_data.CandidateData.SkillsExtractor) > 0
    ), "Skills extraction failed."


def test_resume_parser_framework():

    parser = ResumeParserFramework()
    structured_data_pdf = parser.parse_resume("sample.pdf")
    structured_data_docx = parser.parse_resume("sample.docx")
    assert isinstance(
        structured_data_pdf, ResumeData
    ), "Resume parsing from PDF did not return ResumeData."
    assert (
        structured_data_pdf.CandidateData.NameExtractor is not None
    ), "Resume parsing from PDF failed."
    assert (
        structured_data_docx.CandidateData.NameExtractor is not None
    ), "Resume parsing from DOCX failed."
    assert (
        structured_data_pdf.CandidateData.EmailExtractor is not None
    ), "Email extraction from PDF failed."
    assert (
        structured_data_docx.CandidateData.EmailExtractor is not None
    ), "Email extraction from DOCX failed."
    assert (
        len(structured_data_pdf.CandidateData.SkillsExtractor) > 0
    ), "Skills extraction from PDF failed."
    assert (
        len(structured_data_docx.CandidateData.SkillsExtractor) > 0
    ), "Skills extraction from DOCX failed."
