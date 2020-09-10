import json
import traceback

from infrastructor.logging.ConsoleLogger import ConsoleLogger


class ErrorHandlers:
    def __init__(self):
        self.separator = '|'
        self.default_content_type = "application/json"
        self.mime_type_string = "mimetype"

    def handle_http_exception(self, exception):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = exception.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "result": "",
            "isSuccess": "false",
            "code": exception.code,
            "name": exception.name,
            "message": exception.description,
        })
        message = "empty"
        if exception is not None and exception.description is not None:
            message = exception.description
        ConsoleLogger().error(f'Ex:{message}')
        response.content_type = self.default_content_type
        return response

    def handle_exception(self, exception):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        exception_traceback = traceback.format_exc()
        output = self.separator.join(exception.args)
        # replace the body with JSON
        response = json.dumps({
            "result": "",
            "isSuccess": "false",
            "message": output,
            "traceback": exception_traceback
        })
        output_message = "empty"
        if output is not None and output != "":
            output_message = output
        ConsoleLogger().error(f"Messsage:{output_message}")
        trace_message = "empty"
        if exception_traceback is not None and exception_traceback != "":
            trace_message = exception_traceback
        ConsoleLogger().error(f'Messsage:{trace_message}')
        # response.content_type = "application/json"
        return response, 500, {self.mime_type_string: self.default_content_type}
