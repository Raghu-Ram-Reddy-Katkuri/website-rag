from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    """
    Base class for all crawlers.

    A crawler is responsible ONLY for discovering resources.
    It does not download or parse them.

    Example output:
    [
        "https://example.com/",
        "https://example.com/about",
        "https://example.com/docs/file.pdf"
    ]
    """

    @abstractmethod
    def crawl(self, start_url: str) -> list[str]:
        """
        Discover all reachable resources starting from the given URL.

        Args:
            start_url (str):
                The URL from which crawling begins.

        Returns:
            list[str]:
                A list of discovered resource URLs.
        """
        pass