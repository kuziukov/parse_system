import logging

from celery import Task
from requests import HTTPError
from src.client import ClientRequest
from src.crawlers.apk_mirror import ApkMirror
from src.tasks.apk_mirror.page import TaskApkMirrorPage

log = logging.getLogger(__name__)


class TaskApkMirrorPages(Task):
    queue = 'common'
    name = 'tasks.apk_mirror.pages'
    autoretry_for = (HTTPError,)
    max_retries = 5
    retry_jitter = False
    retry_backoff = True
    retry_backoff_max = 700

    def run(self):
        client = ClientRequest(base_url='https://www.apkmirror.com')
        parser = ApkMirror(client=client)

        urls = parser.request_page_links('/')
        max_page_number = max([parser.get_page_link_num(url) for url in urls])
        # max_page_number = 2
        for num in range(1, max_page_number):
            TaskApkMirrorPage().apply_async([f'/uploads/page/{num}/'])
        return

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        log.error('{0!r} failed: {1!r}'.format(task_id, exc))
