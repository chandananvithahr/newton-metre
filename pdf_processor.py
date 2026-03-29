"""
PDF processing utilities for extracting pages as images
"""
from pathlib import Path
from typing import List, Optional
from PIL import Image
import io

def extract_pdf_pages(pdf_file, max_pages: Optional[int] = None) -> List[Image.Image]:
    """
    Extract pages from PDF file as PIL Images.
    
    Args:
        pdf_file: PDF file object (from Streamlit uploader) or file path
        max_pages: Maximum number of pages to extract (None for all)
        
    Returns:
        List of PIL Image objects, one per page
    """
    try:
        from pdf2image import convert_from_bytes, convert_from_path
        
        # Handle Streamlit uploaded file
        if hasattr(pdf_file, 'read'):
            pdf_bytes = pdf_file.read()
            pdf_file.seek(0)  # Reset file pointer
            images = convert_from_bytes(pdf_bytes, dpi=200)
        else:
            # Handle file path
            pdf_path = Path(pdf_file)
            if not pdf_path.exists():
                return []
            images = convert_from_path(str(pdf_path), dpi=200)
        
        # Limit pages if specified
        if max_pages:
            images = images[:max_pages]
        
        return images
        
    except ImportError:
        raise ImportError(
            "pdf2image is required for PDF processing. Install with: pip install pdf2image\n"
            "Also install poppler: https://github.com/oschwartz10612/poppler-windows/releases/"
        )
    except Exception as e:
        raise Exception(f"Error extracting PDF pages: {str(e)}")


def get_pdf_page_count(pdf_file) -> int:
    """
    Get the number of pages in a PDF file.
    
    Args:
        pdf_file: PDF file object or file path
        
    Returns:
        Number of pages in PDF
    """
    try:
        import PyPDF2
        
        if hasattr(pdf_file, 'read'):
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_file.seek(0)  # Reset file pointer
            return len(pdf_reader.pages)
        else:
            with open(pdf_file, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                return len(pdf_reader.pages)
                
    except ImportError:
        # Fallback: try to extract and count
        try:
            images = extract_pdf_pages(pdf_file, max_pages=100)
            return len(images)
        except:
            return 0
    except Exception:
        return 0


def is_pdf_supported() -> bool:
    """Check if PDF processing is available."""
    try:
        from pdf2image import convert_from_bytes
        return True
    except ImportError:
        return False
