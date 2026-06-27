import io

import requests
from langchain_core.documents import Document
from pypdf import PdfReader

from .base_loader import BaseLoader


class PDFLoader(BaseLoader):
    """
    Loads a PDF document from a URL and converts it into
    LangChain Document(s).
    """

    def load(self, url: str) -> list[Document]:
        """
        Download a PDF and convert each page into a LangChain Document.

        Args:
            url: URL of the PDF.

        Returns:
            A list of LangChain Documents, one per page.
        """

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        pdf = PdfReader(io.BytesIO(response.content))

        documents: list[Document] = []

        for page_number, page in enumerate(pdf.pages, start=1):

            text = page.extract_text() or ""

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": url,
                        "page": page_number,
                        "content_type": "application/pdf",
                    },
                )
            )

        return documents