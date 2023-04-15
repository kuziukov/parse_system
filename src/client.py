import logging
from time import sleep
from typing import Generator, Optional
from urllib.parse import urljoin

import requests
from fake_useragent import UserAgent
from retry import retry

log = logging.getLogger(__name__)


class ClientBase:
    def __init__(self, base_url: str) -> None:
        self._base_url: str = base_url

    def url_for(self, path: str) -> str:
        return urljoin(self._base_url, path)


class ClientRequest(ClientBase):
    def __init__(self, base_url: str, timeout: int = 60):
        super().__init__(base_url)
        self._user_agent = UserAgent()
        self._headers = {'User-Agent': self._user_agent.random}
        self._timeout = timeout

    def do_refresh_profile(self):
        self._headers['User-Agent'] = self._user_agent.random

    @retry(tries=6, delay=2, backoff=2, logger=log)
    def do_request(self, path: str) -> Optional[bytes]:
        with requests.Session() as session:
            sleep(10)
            resp = session.get(self.url_for(path), headers=self._headers, timeout=self._timeout)
            if resp.status_code != 200:
                self.do_refresh_profile()
                if seconds := resp.headers.get('Retry-After'):
                    log.info(f'waiting for next request (retry-after: {seconds})')
                    sleep(int(seconds))
            resp.raise_for_status()
            self.do_refresh_profile()
            return resp.content

    def do_download_iter(self, path: str, chunk_size: int = 8192) -> Generator[bytes, None, None]:
        with requests.Session() as session:
            with session.get(self.url_for(path), stream=True, headers=self._headers, timeout=self._timeout) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=chunk_size):
                    yield chunk
