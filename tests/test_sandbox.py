import os

from src.sandbox import SandBox


def test_sand_box_remove_temp_dir():
    sand_box = SandBox()
    with sand_box as box:
        temp_dir = box.temp_folder_path
        assert os.path.isdir(temp_dir)

        file_path = box.temp_file_path('test_1.txt')
        with open(file_path, 'w') as f:
            f.write("test message")

        assert os.listdir(sand_box.temp_folder_path) == ['test_1.txt']
    assert not os.path.isdir(temp_dir)
