class ExcelGeneratorError(Exception):
    """Base exception for Excel generation errors"""
    pass

class TemplateValidationError(ExcelGeneratorError):
    """Exception raised when the template is invalid"""
    pass

class SheetNotFoundError(TemplateValidationError):
    """Exception raised when a required sheet is missing"""
    pass

class MappingError(TemplateValidationError):
    """Exception raised when a mapping target is invalid"""
    pass
