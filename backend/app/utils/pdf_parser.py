from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract full text from PDF.

    - Handles multi-page PDFs
    - Skips empty pages safely
    """

    reader = PdfReader(file_path)

    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text_parts.append(page_text)

    # Join all pages
    full_text = "\n".join(text_parts)

    return full_text