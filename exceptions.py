class ImkitChatError(Exception):
    pass


class ImkitBackendResponseError(ImkitChatError):
    def __init__(self, message="", json_response_obj=None, metadata=None):
        self.message = message
        self.response_code = None
        self.response_message = None
        self.metadata = metadata

        if json_response_obj is not None:
            self.response_code = json_response_obj.get("RC")
            self.response_message = json_response_obj.get("RM")

    def __str__(self):
        if self.response_code is None and self.response_message is None:
            return self.message

        message = (
            f"{self.message}. Response server data: {self.response_code}|"
            f"{self.response_message}. Request metadata: {self.metadata}"
        )

        return message
