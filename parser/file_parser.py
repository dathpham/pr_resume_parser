# MAIN CODE for FILE PARSER FRAMEWORK


class PDFParser:
    """Parse PDF file and extract text content"""

    def parse(self, file_path):
        """Using pypdf to parse PDF and extract text from all pages"""
        from pypdf import PdfReader

        try:
            reader = PdfReader(file_path)
            content = "".join([p.extract_text() for p in reader.pages])
        except Exception as e:
            raise ValueError(f"Error parsing PDF file: {e}")
        return content


class WordParser:
    """Parse Word document and extract text content"""

    def parse(self, file_path):
        """using python-docx to parse Word document and extract text from all paragraphs"""
        import docx

        try:
            doc = docx.Document("sample.docx")
            content = "".join([p.text for p in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Error parsing DOCX file: {e}")
        return content


class FileParser(PDFParser, WordParser):
    """File Parser Framework to handle different file types"""

    def parse(self, FilePath: str):
        """Determine file type based on file path and parse accordingly"""
        try:
            FileType = FilePath.split(".")[-1].lower()
        except Exception as e:
            raise ValueError(f"file path has no file: {e}")
        if FileType == "pdf":
            return PDFParser.parse(self, FilePath)
        elif FileType == "docx":
            return WordParser.parse(self, FilePath)
        else:
            raise ValueError("Unsupported file type, only PDF and DOCX are supported.")
