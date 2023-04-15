from unittest.mock import MagicMock

import pytest
from src.crawlers.apk_mirror import ApkMirror
from tests.fixture_urls import (
    TEST_URL,
    TEST_URL_FILTERED_DOWNLOAD,
    TEST_URL_FILTERED_DOWNLOAD_KEY,
    TEST_URL_FILTERED_DOWNLOAD_LINK,
    TEST_URL_FILTERED_RELEASE,
)


@pytest.mark.parametrize('url, method, response', [
    ('/', 'is_release_url', False),
    ('/url', 'is_release_url', False),
    (
        '/apk/supertreat-a-playtika-studio/solitaire-grand-harvest/solitaire-grand-harvest-'
        '2-336-1-release/solitaire-grand-harvest-2-336-1-android-apk-download/',
        'is_download_url',
        True
    ),
    (
        '/apk/supertreat-a-playtika-studio/solitaire-grand-harvest/solitaire-grand-harvest-2-336-1-release/',
        'is_release_url',
        True
    ),
    (
        '/apk/mozilla/firefox-fenix/firefox-fenix-114-0a1-release'
        '/firefox-nightly-for-developers-114-0a1-2-android-apk-download'
        '/download/?key=8f35ba1319b5ddc4fa9b77d7d65348fa8aa97205',
        'is_download_key_url',
        True
    ),
    (
        '/wp-content/themes/APKMirror/download.php?id=4676269&'
        'key=d6ede5a49b146b6b50c8ea1479dac2361e1adf84&forcebaseapk=true',
        'is_download_link_url',
        True
    )
])
def test_apk_mirror_is_url_consists(url, method, response):
    apk_mirror = ApkMirror(MagicMock())
    assert getattr(apk_mirror, method)(url) == response


@pytest.mark.parametrize('urls, method, resp', [
    (
        set(),
        'filter_release_urls',
        set()
    ),
    (
        TEST_URL,
        'filter_release_urls',
        TEST_URL_FILTERED_RELEASE
    ),
    (
        TEST_URL,
        'filter_download_urls',
        TEST_URL_FILTERED_DOWNLOAD
    ),
    (
        TEST_URL,
        'filter_download_key_urls',
        TEST_URL_FILTERED_DOWNLOAD_KEY
    ),
    (
        TEST_URL,
        'filter_download_link_urls',
        TEST_URL_FILTERED_DOWNLOAD_LINK
    )
])
def test_apk_mirror_filter(urls, method, resp):
    apk_mirror = ApkMirror(MagicMock())
    print(getattr(apk_mirror, method)(urls))
    assert getattr(apk_mirror, method)(urls) == resp
