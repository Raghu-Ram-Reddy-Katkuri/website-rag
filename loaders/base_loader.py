from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseLoader(ABC):
    """
    Base class for all resource loaders.

    A loader is responsible for:
        1. Downloading a resource.
        2. Extracting its textual content.
        3. Converting it into one or more LangChain Documents.

    It does NOT:
        - Discover URLs.
        - Generate embeddings.
        - Store vectors.
    """

    @abstractmethod
    def load(self, url: str) -> list[Document]:
        """
        Load a resource from the given URL.

        Args:
            url: URL of the resource.

        Returns:
            A list of LangChain Documents extracted from the resource.
        """
        pass