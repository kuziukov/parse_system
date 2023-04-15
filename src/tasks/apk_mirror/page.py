import logging

from celery import Task
from requests import HTTPError
from src.client import ClientRequest
from src.crawlers.apk_mirror import ApkMirror
from src.tasks.apk_mirror.page_download import TaskApkMirrorPageDownload

log = logging.getLogger(__name__)


class TaskApkMirrorPage(Task):
    queue = 'common'
    name = 'tasks.apk_mirror.page'
    autoretry_for = (HTTPError,)
    max_retries = 5
    retry_jitter = False
    retry_backoff = True
    retry_backoff_max = 700

    def run(self, url):
        client = ClientRequest(base_url='https://www.apkmirror.com')
        parser = ApkMirror(client=client)
        for url in parser.request_page(url, recursive=False):
            TaskApkMirrorPageDownload().apply_async([url])
        return

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        log.error('{0!r} failed: {1!r}'.format(task_id, exc))
