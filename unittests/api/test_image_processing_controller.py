import base64
import json
import os
# from StringIO import StringIO
from io import BytesIO
from unittest import TestCase

from flask.testing import FlaskClient

from domain.imageprocessing.services.ImageProcessingService import ImageProcessingService
from unittests.test_container import TestIocContainer


class DefaultSqlBuilder(object):
    pass


class TestImageProcessingController(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestImageProcessingController, self).__init__(methodName)
        self.applicationWrapper = TestIocContainer.applicationWrapper()
        self.client: FlaskClient = self.applicationWrapper.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_start_operation(self):
        #  Send reply back to client
        #  In the real world usage, after you finish your work, send your output here

        data = json.dumps(
            {
            }
        )

        response = self.client.post(
            '/api/imageprocessing/start_operation',
            data=data,
            content_type='application/json',
        )

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['isSuccess'] == 'true'
        assert len(response_data['result']) > 0

        import requests

    def test_get_predictions(self):
        url = "http://localhost:9020/api/fasterrcnn/predict/"

        root_directory = TestIocContainer.configurations.api_config.root_directory
        path = os.path.join(root_directory, "images//test_image.jpg")
        f = open(path, 'rb')
        image_bytes = bytearray(f.read())
        image_string = base64.b64encode(image_bytes)
        #
        # f.close()

        files = {'image': open(f'{path}', 'rb')}

        # post_data['uploaded_file'] = f
        # response = self.client.post(url, post_data)

        with open(path) as fp:
            response = self.client.post('/api/imageprocessing/predict',
                                        dict(uploaded_file=f),
                                        content_type='application/x-www-form-urlencoded',
                                        )

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['isSuccess'] == 'true'
        assert len(response_data['result']) > 0

    def test_upload_image(self):
        root_directory = TestIocContainer.configurations.api_config.root_directory
        path = os.path.join(root_directory, "images//test_image.jpg")

        with open(path, 'rb') as img1:
            imgStringIO1 = BytesIO(img1.read())
        data = dict(
            file=(imgStringIO1, "test.jpg"),
        )

        response = self.client.post('/api/imageprocessing/predict', content_type='multipart/form-data',
                                    data=data)
        self.assertEquals(response.status, "200 OK")

    def test_download_and_resize_image(self):
        image_name = 'test_image.jpg'
        root_directory = TestIocContainer.configurations.api_config.root_directory
        path = os.path.join(root_directory, f"images//{image_name}")
        image_processing_service: ImageProcessingService = TestIocContainer.image_processing_service()
        file_path = image_processing_service.download_and_resize_image_from_file(path)

        folder = os.path.dirname(path)
        expect= os.path.join(folder, 'temp_' + image_name)
        assert expect == file_path

    def test_and_resize_image_from_file(self, path):
        image_name = 'test_image.jpg'
        root_directory = TestIocContainer.configurations.api_config.root_directory
        path = os.path.join(root_directory, f"images//{image_name}")
        return path