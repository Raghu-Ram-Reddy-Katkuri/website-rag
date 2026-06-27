from pathlib import Path

from .base_loader import BaseLoader
from .html_loader import HTMLLoader
from .pdf_loader import PDFLoader


class LoaderFactory:
    """
    Factory responsible for returning the appropriate loader
    for a given resource URL.
    """

    def __init__(self) -> None:
        self._loaders: dict[str, BaseLoader] = {
            ".html": HTMLLoader(),
            ".htm": HTMLLoader(),
            ".pdf": PDFLoader(),
        }

    def get_loader(self, url: str) -> BaseLoader:
        """
        Return the appropriate loader for the given URL.

        Args:
            url: Resource URL.

        Returns:
            A concrete implementation of BaseLoader.

        Raises:
            ValueError:
                If no loader exists for the given resource type.
        """

        extension = Path(url).suffix.lower()

        loader = self._loaders.get(extension)

        if loader is None:
            raise ValueError(
                f"No loader registered for extension: '{extension}'"
            )

        return loader

    def register_loader(
        self,
        extension: str,
        loader: BaseLoader,
    ) -> None:
        """
        Register a new loader.

        Example:
            factory.register_loader(".docx", DOCXLoader())
        """

        self._loaders[extension.lower()] = loader