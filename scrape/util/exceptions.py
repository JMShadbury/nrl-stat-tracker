""" This module is use to define custom exceptions for the project. """


class InvalidURL(Exception):
    """Exception raised for invalid URLs."""

    def __init__(self, url, message="The URL is invalid."):
        self.url = url
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.url} -> {self.message}"


class InvalidPath(Exception):
    """Exception raised for invalid paths."""

    def __init__(self, path, message="The path is invalid."):
        self.path = path
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.path} -> {self.message}"


class InvalidFile(Exception):
    """Exception raised for invalid files."""

    def __init__(self, file, message="The file is invalid."):
        self.file = file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.file} -> {self.message}"


class InvalidData(Exception):
    """Exception raised for invalid data."""

    def __init__(self, data, message="The data is invalid."):
        self.data = data
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.data} -> {self.message}"


class InvalidJSON(Exception):
    """Exception raised for invalid JSON."""

    def __init__(self, json, message="The JSON is invalid."):
        self.json = json
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.json} -> {self.message}"


class InvalidHTML(Exception):
    """Exception raised for invalid HTML."""

    def __init__(self, html, message="The HTML is invalid."):
        self.html = html
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.html} -> {self.message}"


class WebScraperError(Exception):
    """Exception raised for errors in the WebScraper class."""

    def __init__(self, message="An error occurred in the WebScraper class."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
