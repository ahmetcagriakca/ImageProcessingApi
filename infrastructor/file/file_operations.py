import base64
import io
import os

from models.configs.ApiConfig import ApiConfig


class FileOperations:
    def __init__(self, api_config: ApiConfig):
        self.api_config: ApiConfig = api_config

    def get_file_path(self, file_name):
        return os.path.join(self.api_config.root_directory, 'images', file_name)

    def check_file(self, file_name, file_order):
        path = os.path.join(self.api_config.root_directory, 'images', file_name)
        if os.path.exists(path):
            if file_order > 0:
                order = os.path.splitext(file_name)[0].split('__')[1]
                new_file_order = file_order + 1

            new_file_name = os.path.splitext(file_name)[0] + f"__{new_file_order}" + os.path.splitext(file_name)[1]
            return self.check_file(new_file_name, new_file_order)
        else:
            return path, file_name

    def write_binary_file_to_server(self, file, file_name):
        path = os.path.join(self.api_config.root_directory, 'images', file_name)
        with open(path, 'wb') as ff:
            ff.write(file)
            ff.close()
        return file_name

    def write_file_to_server(self, file):
        path = os.path.join(self.api_config.root_directory, "images", file.filename)
        file.save(path)
        file.close()

    def read_file_from_server_(self, image_name):
        path = os.path.join(self.api_config.root_directory, "images", image_name)
        f = open(path, 'rb')
        bytes = bytearray(f.read())
        base64_string = base64.b64encode(bytes)
        return base64_string

    def read_file_from_server(self, image_name):
        path = os.path.join(self.api_config.root_directory, "images", image_name)
        file = open(path, 'rb')

        byte_io = io.BytesIO()
        byte_io.write(file.read())
        byte_io.seek(0)

        file.close()
        return byte_io
