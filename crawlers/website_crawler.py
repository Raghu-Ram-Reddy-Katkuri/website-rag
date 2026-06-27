from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from .base_crawler import BaseCrawler


class WebsiteCrawler(BaseCrawler):
    """
    Crawls a website and discovers all internal resource URLs.

    Responsibilities:
        - Start from a given URL.
        - Visit each internal page only once.
        - Discover HTML pages and linked resources (e.g., PDFs).
        - Return a list of discovered URLs.

    Does NOT:
        - Download resources.
        - Extract text.
        - Create LangChain Documents.
    """

    def __init__(self) -> None:
        self._visited: set[str] = set()

    def crawl(self, start_url: str) -> list[str]:
        """
        Crawl the website starting from the given URL.

        Args:
            start_url: The URL from which crawling begins.

        Returns:
            A list of discovered resource URLs.
        """

        discovered_urls: list[str] = []

        queue = deque([start_url])

        domain = urlparse(start_url).netloc

        while queue:
            current_url = queue.popleft()

            if current_url in self._visited:
                continue

            self._visited.add(current_url)
            discovered_urls.append(current_url)

            try:
                response = requests.get(current_url, timeout=10)

                if response.status_code != 200:
                    continue

                content_type = response.headers.get("Content-Type", "")

                if "text/html" not in content_type:
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                anchors: list[Tag] = soup.find_all("a", href=True)  # type: ignore[assignment]

                for anchor in anchors:

                    href = anchor.get("href")

                    if not isinstance(href, str):
                        continue

                    absolute_url = urljoin(current_url, href)

                    parsed_url = urlparse(absolute_url)

                    # Ignore external websites.
                    if parsed_url.netloc != domain:
                        continue

                    # Remove URL fragments (#section).
                    cleaned_url = parsed_url._replace(fragment="").geturl()

                    if (
                        cleaned_url not in self._visited
                        and cleaned_url not in queue
                    ):
                        queue.append(cleaned_url)

            except requests.RequestException:
                continue

        return discovered_urls