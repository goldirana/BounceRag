class BackendException(Exception):
    """Base exception class for all backend exceptions"""
    pass

class DataIngestionError(BackendException):
    """Exception raised for errors during data ingestion"""
    def __init__(self, message="Error occurred during data ingestion"):
        self.message = message
        super().__init__(self.message)

class StorageError(BackendException):
    """Exception raised for storage-related operations"""
    def __init__(self, message="Storage operation failed"):
        self.message = message
        super().__init__(self.message)

class QueryError(BackendException):
    """Exception raised for query-related operations"""
    def __init__(self, message="Query processing failed"):
        self.message = message
        super().__init__(self.message)

class ModelError(BackendException):
    """Exception raised for model-related operations"""
    def __init__(self, message="Model operation failed"):
        self.message = message
        super().__init__(self.message)

class ConfigurationError(BackendException):
    """Exception raised for configuration-related issues"""
    def __init__(self, message="Configuration error occurred"):
        self.message = message
        super().__init__(self.message)

class ValidationError(BackendException):
    """Exception raised for data validation failures"""
    def __init__(self, message="Data validation failed"):
        self.message = message
        super().__init__(self.message)

class AuthenticationError(BackendException):
    """Exception raised for authentication failures"""
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)

class RateLimitExceededError(BackendException):
    """Exception raised when API rate limits are exceeded"""
    def __init__(self, message="API rate limit exceeded"):
        self.message = message
        super().__init__(self.message)

class ResourceNotFoundError(BackendException):
    """Exception raised when a requested resource is not found"""
    def __init__(self, message="Requested resource not found"):
        self.message = message
        super().__init__(self.message)

class DependencyError(BackendException):
    """Exception raised when there are issues with external dependencies"""
    def __init__(self, message="Dependency error occurred"):
        self.message = message
        super().__init__(self.message)

class SerializationError(BackendException):
    """Exception raised during data serialization/deserialization"""
    def __init__(self, message="Serialization error occurred"):
        self.message = message
        super().__init__(self.message)

class NetworkError(BackendException):
    """Exception raised for network-related issues"""
    def __init__(self, message="Network error occurred"):
        self.message = message
        super().__init__(self.message)
