def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from an uploaded image using pytesseract (OCR).
    
    Requirements:
        pip install pytesseract Pillow
        Install Tesseract: https://github.com/tesseract-ocr/tesseract
    """
    try:
        import pytesseract
        from PIL import Image
        import io

        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text.strip() if text.strip() else "No text found in image."
    except ImportError:
        return "[OCR unavailable] Install pytesseract and Pillow: pip install pytesseract Pillow"
    except Exception as e:
        return f"[OCR error]: {str(e)}"