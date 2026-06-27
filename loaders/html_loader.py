import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

from .base_loader import BaseLoader


class HTMLLoader(BaseLoader):
    """
    Loads an HTML page and converts it into LangChain Document(s).
    """

    def load(self, url: str) -> list[Document]:
        """
        Download an HTML page and convert it into a LangChain Document.

        Args:
            url: URL of the HTML page.

        Returns:
            A list containing a single LangChain Document.
        """

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator="\n", strip=True)

        document = Document(
            page_content=text,
            metadata={
                "source": url,
                "content_type": "text/html",
            },
        )

        return [document]