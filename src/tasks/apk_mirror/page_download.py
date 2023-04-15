import logging
import uuid

from celery import Task
from requests import HTTPError
from src.client import ClientRequest
from src.crawlers.apk_mirror import ApkMirror
from src.sandbox import SandBox
from src.utils import parse_7z_file_to_pattern

log = logging.getLogger(__name__)


class TaskApkMirrorPageDownload(Task):
    queue = 'common'
    name = 'tasks.apk_mirror.page.download'
    autoretry_for = (HTTPError,)
    max_retries = 5
    retry_backoff = True
    retry_backoff_max = 700
    retry_jitter = False

    def run(self, url):
        client = ClientRequest(base_url='https://www.apkmirror.com')
        parser = ApkMirror(client=client)

        # Загружаем файл во временную папку с chunk_size = 8192
        for url in parser.request_page(path=url):
            with SandBox() as context:
                temp_file_path = context.temp_file_path(file_name=str(uuid.uuid4()))
                with open(temp_file_path, 'wb') as f:
                    for chunk in client.do_download_iter(url, chunk_size=8192):
                        f.write(chunk)

                # Выводим содержимое архива в формате: архив – файл – тип - размер
                files_in_pattern = parse_7z_file_to_pattern(temp_file_path)
                log.info(f'Response: {files_in_pattern[:4]}, Total count: {len(files_in_pattern)}')
        return

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        log.error('{0!r} failed: {1!r}'.format(task_id, exc))
