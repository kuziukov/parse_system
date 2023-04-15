import logging
from typing import Set

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


class ApkMirrorPage:
    def __init__(self, content):
        self._soup = BeautifulSoup(content, 'html5lib')

    def find_urls(self) -> Set[str]:
        return {tag['href'] for tag in self._soup.find_all('a', href=True)}
