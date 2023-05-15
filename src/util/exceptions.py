class ImageCouldNotBeDownloadedError(Exception):
    """Exception raised for errors while downloading the image.

    Attributes:
        url -- input url which could not be downloaded
        message -- explanation of the error
    """

    def __init__(self, url: str, message: str = "Image could not be downloaded"):
        self.url = url
        self.message = f"{message}: {self.url}"
        super().__init__(self.message)