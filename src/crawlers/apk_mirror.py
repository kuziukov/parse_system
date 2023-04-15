import re
from typing import Set

from src.client import ClientRequest
from src.crawlers.apk_mirror_page import ApkMirrorPage
from src.tasks.apk_mirror.utils import reduce_list_of_urls


class ApkMirror:
    def __init__(self, client: ClientRequest):
        self._client = client

    @staticmethod
    def is_release_url(url: str) -> bool:
        return bool(re.search(r'.apk.(.*)-release\/$', url))

    def filter_release_urls(self, urls: Set[str]) -> Set[str]:
        return {url for url in urls if self.is_release_url(url)}

    @staticmethod
    def is_download_url(url: str) -> bool:
        return bool(re.search(r'.apk.(.*)-download\/$', url))

    def filter_download_urls(self, urls: Set[str]) -> Set[str]:
        return {url for url in urls if self.is_download_url(url)}

    @staticmethod
    def is_download_key_url(url: str) -> bool:
        return bool(re.search(r'.apk.(.*)-download\/download\/.*$', url))

    def filter_download_key_urls(self, urls: Set[str]) -> Set[str]:
        return {url for url in urls if self.is_download_key_url(url)}

    @staticmethod
    def is_download_link_url(url: str) -> bool:
        return bool(re.search(r'.wp-content.(.*).download\.php.*$', url))

    def filter_download_link_urls(self, urls: Set[str]) -> Set[str]:
        return {url for url in urls if self.is_download_link_url(url)}

    @staticmethod
    def is_page_link_url(url: str) -> bool:
        return bool(re.search(r'.uploads.page.(.*).$', url))

    def filter_page_link_urls(self, urls: Set[str]) -> Set[str]:
        return {url for url in urls if self.is_page_link_url(url)}

    @staticmethod
    def get_page_link_num(url: str) -> int:
        m = re.match(r'.uploads.page.(.*).$', url)
        return int(m.group(1)) if m else 0

    def request_page_links(self, path: str) -> Set[str]:
        """
        Метод request_page_links
        Получает список страниц, доступных для перехода

        Пример: {'/uploads/page/2/', '/uploads/page/3/', '/uploads/page/4/'}
        :param path: str - путь по которому получаем список страниц
        :return: set[str] - список доступных страниц
        """
        if not (content := self._client.do_request(path)):
            return set()

        page = ApkMirrorPage(content=content)
        urls = page.find_urls()
        return self.filter_page_link_urls(urls)

    def request_page(self, path: str, recursive: bool = True) -> Set[str]:
        """
        Метод request_page - рекурсивный поиск ссылок на скачивание .apk файла

        Полная схема обхода:
            filter_release_urls -> filter_download_urls -> filter_download_key_urls -> filter_download_link_urls

        Пример: '/' or '/uploads/page/2/'
        :param path: str - путь с которого начинаем поиск
        :param recursive: bool - можно отключить рекурсивный поиск, будет искать только на текущем слое
        :return: set[str] - список ссылок для дальнейшего поиска
        """
        if not (content := self._client.do_request(path)):
            return set()

        page = ApkMirrorPage(content=content)
        urls = page.find_urls()

        if self.is_release_url(path):
            urls = self.filter_download_urls(urls)

        elif self.is_download_url(path):
            urls = self.filter_download_key_urls(urls)

        elif self.is_download_key_url(path):
            return self.filter_download_link_urls(urls)

        else:
            urls = self.filter_release_urls(urls)

        return reduce_list_of_urls([self.request_page(url, recursive) for url in urls]) if recursive else urls
