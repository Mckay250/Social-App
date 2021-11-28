class APIKeyNotFound(Exception):
    """
    Exception raised when api key is not set in the environment.
    """

    def __init__(self, message="Api key not found"):
        self.message = message
        super().__init__(self.message)
