import base64
import json
import uuid

from flask import jsonify, request, make_response, send_file
from flask_cors import cross_origin

from domain.imageprocessing.services.ImageProcessingService import ImageProcessingService
from infrastructor.api.ControllerBase import ControllerBase
from infrastructor.data.DatabaseManager import DatabaseManager
from infrastructor.data.MssqlConnector import MssqlDbConnector
from infrastructor.data.OracleConnector import OracleDbConnector
from infrastructor.data.SqlBuilder import DefaultInsertSqlBuilder
from infrastructor.file.file_operations import FileOperations
from infrastructor.logging.ConsoleLogger import ConsoleLogger


class ImageProcessingController(ControllerBase):
    def __init__(self, image_processing_service: ImageProcessingService,
                 file_operations: FileOperations

                 ):
        self.file_operations = file_operations
        self.image_processing_service = image_processing_service

    def endpoints(self) -> []:
        return [
            {
                'endpoint': f'get',
                'endpoint_name': 'GET',
                'handler': self.get,
                'methods': ['GET']
            },
            {
                'endpoint': f'start_operation',
                'endpoint_name': 'start_operation',
                'handler': self.start_operation,
                'methods': ['POST']
            },
            {
                'endpoint': f'upload_file',
                'endpoint_name': 'upload_file',
                'handler': self.upload_file,
                'methods': ['PUT']
            },
            {
                'endpoint': f'get_image',
                'endpoint_name': 'get_image',
                'handler': self.get_image,
                'methods': ['GET']
            }
        ]

    @cross_origin()
    def get(self):
        return jsonify({'sum': 1 + 2})

    def start_operation(self):
        request_json = request.data.decode('utf-8')
        data = json.loads(request_json)
        ConsoleLogger().info('Data Integration is Begin with data:' + request_json)
        image_name = None
        if request_json is not None and len(request_json) > 0:
            image_name = data.get('FileOid')
        self.image_processing_service.start_operation(image_name)
        return jsonify({'ProcessedImageName': 'processed_' + image_name})

    def upload_file(self):
        file = request.data
        file_name = str(uuid.uuid4()) + ".jpg"
        self.file_operations.write_binary_file_to_server(file, file_name)

        return jsonify({'FileOid': file_name})

    def get_image(self):
        args = request.args
        if "ImageName" in args:
            image_name = args["ImageName"]

        byte_io = self.file_operations.read_file_from_server(image_name)
        response = make_response(send_file(byte_io, mimetype='image/jpg'))
        response.headers['Content-Transfer-Encoding'] = 'base64'
        return response
