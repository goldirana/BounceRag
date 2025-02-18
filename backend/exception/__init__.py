from backend.logger import logger
import os

class BackendException(Exception):
    """Base exception class for all backend exceptions"""
    pass

class DataIngestionError(BackendException):
    """Exception raised for errors during data ingestion"""
    def __init__(self, failure_message="Error occurred during data ingestion"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class StorageError(BackendException):
    """Exception raised for storage-related operations"""
    def __init__(self, failure_message="Storage operation failed"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class QueryError(BackendException):
    """Exception raised for query-related operations"""
    def __init__(self, failure_message="Query processing failed"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class ModelError(BackendException):
    """Exception raised for model-related operations"""
    def __init__(self, failure_message="Model operation failed"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class ConfigurationError(BackendException):
    """Exception raised for configuration-related issues"""
    def __init__(self, failure_message="Configuration error occurred"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class ValidationError(BackendException):
    """Exception raised for data validation failures"""
    def __init__(self, failure_message="Data validation failed"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class AuthenticationError(BackendException):
    """Exception raised for authentication failures"""
    def __init__(self, failure_message="Authentication failed"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class RateLimitExceededError(BackendException):
    """Exception raised when API rate limits are exceeded"""
    def __init__(self, failure_message="API rate limit exceeded"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class ResourceNotFoundError(BackendException):
    """Exception raised when a requested resource is not found"""
    def __init__(self, failure_message="Requested resource not found"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class DependencyError(BackendException):
    """Exception raised when there are issues with external dependencies"""
    def __init__(self, failure_message="Dependency error occurred"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class SerializationError(BackendException):
    """Exception raised during data serialization/deserialization"""
    def __init__(self, failure_message="Serialization error occurred"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class NetworkError(BackendException):
    """Exception raised for network-related issues"""
    def __init__(self, failure_message="Network error occurred"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class ImageSummarizerError(BackendException):
    """Exception raised for image summarization"""
    def __init__(self, failure_message="Error occured while summarizing image"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

class TextSummarizerError(BackendException):
    """Exception raised for text summarization"""
    def __init__(self, failure_message="Error occured while summarizing text"):
        self.failure_message = failure_message
        super().__init__(self.failure_message)

def log_error(exception, sucess_message=None, failure_message=None):
    """
    A decorator that logs a success message if the decorated function executes without exceptions,
    and logs an error message along with the exception details if an exception is raised.
    Args:
        sucess_message (str, optional): The message to log if the function executes successfully.
        failure_message (str, optional): The message to log if the function raises an exception.
    Returns:
        function: The decorated function with added logging functionality.
    """
    def decorator(func):  # This is the actual decorator
        def wrapper(*args, **kwargs):
            logger.name = os.path.basename(func.__code__.co_filename)
            try:
                result = func(*args, **kwargs)
                if sucess_message is not None:
                    logger.info(sucess_message)
                return result
            except exception as e:
                print(f"ERROR: {failure_message}\nException in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator

