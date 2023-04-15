import os
import shutil
import zipfile

import pytest
from src.sandbox import SandBox
from src.tasks.apk_mirror.utils import reduce_list_of_urls
from src.utils import parse_7z_file_to_pattern


def test_utils_parse_7z_file_to_pattern_exception():
    with SandBox() as box:
        file_path = box.temp_file_path('test_1.txt')
        with open(file_path, 'w') as f:
            f.write("test message")

        with pytest.raises(zipfile.BadZipFile):
            parse_7z_file_to_pattern(file_path)


def test_utils_parse_7z_file_to_pattern():
    test_directory = 'test'
    with SandBox() as box:
        created_dir = f'{box.temp_folder_path}/{test_directory}'
        os.makedirs(created_dir)
        with open(f'{created_dir}/test_1.txt', 'w') as f:
            f.write("test message")

        file_name = shutil.make_archive(created_dir, 'zip', created_dir)
        files_in_pattern = parse_7z_file_to_pattern(file_name)
        assert files_in_pattern == ['test-test_1-.txt-12']


@pytest.mark.parametrize(
    "input, expected", [
        ([{'1', '2'}, {'3'}, {'4'}, {'56'}], {'1', '2', '3', '4', '56'}),
        ([{'1', '2'}, {'-5'}, {'0'}, {'1'}], {'-5', '0', '1', '2'}),
        ([], set()),
    ]
)
def test_utils_reduce_list_of_urls(input, expected):
    assert reduce_list_of_urls(input) == expected
