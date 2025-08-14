import os
import logging
from typing import Optional, Union
import io
from PIL import Image
import pdfplumber
import PyPDF2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Multi-format document text extraction with fallback mechanisms"""
    
    def __init__(self):
        """Initialize the document processor"""
        self.supported_formats = {
            'pdf': ['.pdf'],
            'image': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'],
            'text': ['.txt', '.csv', '.md'],
            'spreadsheet': ['.xlsx', '.xls', '.ods']
        }
        
        self.max_file_size = 50 * 1024 * 1024  # 50MB limit
        logger.info("Document processor initialized")
    
    def process_document(self, uploaded_file) -> Optional[str]:
        """Main entry point for document processing"""
        try:
            # Validate the uploaded file
            if not self._validate_file(uploaded_file):
                return None
            
            # Determine file type and process accordingly
            file_extension = self._get_file_extension(uploaded_file.name)
            
            if file_extension in self.supported_formats['pdf']:
                return self.extract_text_from_pdf(uploaded_file)
            
            elif file_extension in self.supported_formats['image']:
                return self.extract_text_from_image(uploaded_file)
            
            elif file_extension in self.supported_formats['text']:
                return self.extract_text_from_file(uploaded_file)
            
            elif file_extension in self.supported_formats['spreadsheet']:
                return self.extract_text_from_spreadsheet(uploaded_file)
            
            else:
                logger.warning(f"Unsupported file format: {file_extension}")
                return f"Unsupported file format: {file_extension}. Please upload a PDF, image, or text file."
                
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return f"Error processing document: {str(e)}"
    
    def extract_text_from_pdf(self, uploaded_file) -> Optional[str]:
        """Extract text from PDF using pdfplumber with PyPDF2 fallback"""
        try:
            # Try pdfplumber first (better text extraction)
            try:
                with pdfplumber.open(uploaded_file) as pdf:
                    text_content = []
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_content.append(page_text.strip())
                    
                    if text_content:
                        logger.info("Successfully extracted text using pdfplumber")
                        return "\n\n".join(text_content)
                
            except Exception as e:
                logger.warning(f"pdfplumber failed: {str(e)}, trying PyPDF2 fallback")
            
            # Fallback to PyPDF2
            try:
                uploaded_file.seek(0)  # Reset file pointer
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text_content = []
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text.strip())
                
                if text_content:
                    logger.info("Successfully extracted text using PyPDF2 fallback")
                    return "\n\n".join(text_content)
                else:
                    logger.warning("No text content found in PDF")
                    return "No text content could be extracted from this PDF file."
                    
            except Exception as e:
                logger.error(f"PyPDF2 fallback also failed: {str(e)}")
                return f"Error extracting text from PDF: {str(e)}"
                
        except Exception as e:
            logger.error(f"Unexpected error in PDF processing: {str(e)}")
            return f"Error processing PDF file: {str(e)}"
    
    def extract_text_from_image(self, uploaded_file) -> Optional[str]:
        """Extract text from image (placeholder for future OCR implementation)"""
        try:
            # For now, return a placeholder message
            # Future implementation would use OCR libraries like Tesseract
            logger.info("Image text extraction requested (OCR not yet implemented)")
            return "Image text extraction (OCR) is not yet implemented. Please upload a PDF or text file instead."
            
            # Future OCR implementation would look like:
            # from PIL import Image
            # import pytesseract
            # image = Image.open(uploaded_file)
            # text = pytesseract.image_to_string(image)
            # return text
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return f"Error processing image file: {str(e)}"
    
    def extract_text_from_file(self, uploaded_file) -> Optional[str]:
        """Extract text from text-based files"""
        try:
            # Read the file content
            content = uploaded_file.read()
            
            # Try to decode as UTF-8
            try:
                text_content = content.decode('utf-8')
            except UnicodeDecodeError:
                # Fallback to other encodings
                try:
                    text_content = content.decode('latin-1')
                except UnicodeDecodeError:
                    text_content = content.decode('cp1252', errors='ignore')
            
            if text_content.strip():
                logger.info("Successfully extracted text from file")
                return text_content.strip()
            else:
                logger.warning("Empty text content in file")
                return "The uploaded file appears to be empty."
                
        except Exception as e:
            logger.error(f"Error extracting text from file: {str(e)}")
            return f"Error reading file content: {str(e)}"
    
    def extract_text_from_spreadsheet(self, uploaded_file) -> Optional[str]:
        """Extract text from spreadsheet files (placeholder for future implementation)"""
        try:
            # For now, return a placeholder message
            # Future implementation would use pandas or openpyxl
            logger.info("Spreadsheet text extraction requested (not yet implemented)")
            return "Spreadsheet text extraction is not yet implemented. Please export as CSV or upload a PDF file instead."
            
            # Future implementation would look like:
            # import pandas as pd
            # df = pd.read_excel(uploaded_file)
            # return df.to_string()
            
        except Exception as e:
            logger.error(f"Error processing spreadsheet: {str(e)}")
            return f"Error processing spreadsheet file: {str(e)}"
    
    def _validate_file(self, uploaded_file) -> bool:
        """Validate uploaded file for security and format"""
        try:
            # Check file size
            if uploaded_file.size > self.max_file_size:
                logger.warning(f"File too large: {uploaded_file.size} bytes")
                return False
            
            # Check file name
            if not uploaded_file.name or len(uploaded_file.name) > 255:
                logger.warning("Invalid file name")
                return False
            
            # Check for suspicious file extensions
            suspicious_extensions = ['.exe', '.bat', '.cmd', '.com', '.scr', '.vbs', '.js']
            file_extension = self._get_file_extension(uploaded_file.name)
            if file_extension.lower() in suspicious_extensions:
                logger.warning(f"Suspicious file extension: {file_extension}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating file: {str(e)}")
            return False
    
    def _get_file_extension(self, filename: str) -> str:
        """Get file extension from filename"""
        try:
            return os.path.splitext(filename)[1].lower()
        except Exception:
            return ""
    
    def get_supported_formats(self) -> dict:
        """Get list of supported file formats"""
        return self.supported_formats.copy()
    
    def is_format_supported(self, filename: str) -> bool:
        """Check if a file format is supported"""
        file_extension = self._get_file_extension(filename)
        for format_list in self.supported_formats.values():
            if file_extension in format_list:
                return True
        return False
