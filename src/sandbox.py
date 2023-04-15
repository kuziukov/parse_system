import os
import shutil
import uuid
from typing import Self


class SandBox:
    """
    Класс SandBox - временное окружение для файлов

    Основная задача класса - создать временную папку для работы с файлами и
    гарантировано очистить мусор после работы.
    """
    temp_folder_root: str = 'files/'

    def __enter__(self) -> Self:
        self._folder_name = str(uuid.uuid4())
        self._temp_folder = os.path.join(self.temp_folder_root, self._folder_name)
        os.makedirs(self._temp_folder)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        shutil.rmtree(self._temp_folder)

    @property
    def temp_folder_path(self) -> str:
        return self._temp_folder

    def temp_file_path(self, file_name: str) -> str:
        return os.path.join(self._temp_folder, file_name)
