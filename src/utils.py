import os
import zipfile
from typing import List


def parse_7z_file_to_pattern(archive_path: str) -> List[str]:
    """
    Функция преобразования 7zip файла в массив строк вида: "архив – файл – тип - размер"
    :param archive_path: str, (example: <folder>/<file>.[apk/7z])
    :return: List[str]
    """
    files_in_pattern = []
    archive_name = os.path.basename(archive_path)
    archive_file_name, _ = os.path.splitext(archive_name)

    with zipfile.ZipFile(archive_path, 'r') as archive:
        for file in archive.filelist:
            filename = os.path.basename(file.filename)
            file_name, file_ext = os.path.splitext(filename)
            files_in_pattern.append('{0}-{1}-{2}-{3}'.format(archive_file_name, file_name, file_ext, file.file_size))
        return files_in_pattern
