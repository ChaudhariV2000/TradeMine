class TradeMindException(Exception):
    """Base exception for the project."""


class ValidationError(TradeMindException):
    """Raised when input validation fails."""


class ProviderError(TradeMindException):
    """Raised when a data provider fails."""


class IndicatorError(TradeMindException):
    """Raised when indicator calculation fails."""