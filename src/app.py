from celery import Celery
from src.config import get_config
from src.tasks.apk_mirror.page import TaskApkMirrorPage
from src.tasks.apk_mirror.page_download import TaskApkMirrorPageDownload
from src.tasks.apk_mirror.pages import TaskApkMirrorPages


def create_app() -> Celery:
    config = get_config()
    celery = Celery(__name__, broker=config.rabbit_uri)
    celery.register_task(TaskApkMirrorPages())
    celery.register_task(TaskApkMirrorPage())
    celery.register_task(TaskApkMirrorPageDownload())

    celery.add_periodic_task(120.0, TaskApkMirrorPages, name=TaskApkMirrorPages.name)
    return celery
