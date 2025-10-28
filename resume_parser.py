# MAIN CODE for RESUME PARSER FRAMEWORK
from parser.file_parser import FileParser

from datamodel.extraction_model import ResumeExtractor


class ResumeParserFramework(FileParser, ResumeExtractor):
    """Resume Parser Framework to parse resume file and extract structured data"""

    def __init__(self):
        pass

    def parse_resume(self, file_path: str):
        """Get raw text from resume file and extract structured candidate data using ResumeExtractor"""
        raw_text = FileParser().parse(file_path)
        structured_data = ResumeExtractor(
            strategy_config="llm", raw_text=raw_text
        ).__extract__()
        return structured_data
