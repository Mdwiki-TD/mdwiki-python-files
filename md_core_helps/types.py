"""
Type definitions for the MDWiki Python Bot codebase.

This module provides type aliases, protocols, and generic types used throughout
the codebase to ensure type safety and improve IDE support.

Usage:
    from md_core_helps.types import (
        JSONDict,
        SQLParams,
        WikiPage,
        APIResponse,
        TemplateData,
    )
"""

from __future__ import annotations

from collections.abc import Callable, Generator, Iterable, Mapping, Sequence
from pathlib import Path
from typing import (
    Any,
    Dict,
    Final,
    List,
    Optional,
    Protocol,
    Tuple,
    TypeAlias,
    TypeVar,
    Union,
    runtime_checkable,
)

# =============================================================================
# BASIC TYPE ALIASES
# =============================================================================

#: A JSON-compatible dictionary structure
JSONDict: TypeAlias = Dict[str, Any]

#: A JSON-compatible list structure
JSONList: TypeAlias = List[Any]

#: Any JSON-compatible value
JSONValue: TypeAlias = Union[None, bool, int, float, str, JSONList, JSONDict]

#: SQL query parameters - can be a tuple, list, or dict
SQLParams: TypeAlias = Union[Tuple[Any, ...], List[Any], Dict[str, Any]]

#: SQL query result row
SQLRow: TypeAlias = Dict[str, Any]

#: SQL query result set
SQLResultSet: TypeAlias = List[SQLRow]

# =============================================================================
# WIKI-SPECIFIC TYPES
# =============================================================================

#: Wiki page title
WikiTitle: TypeAlias = str

#: Wiki page content (wikitext)
WikiText: TypeAlias = str

#: Wiki language code (e.g., "en", "ar", "zh")
LanguageCode: TypeAlias = str

#: Wiki site code (e.g., "enwiki", "www")
SiteCode: TypeAlias = str

#: Wiki family (e.g., "wikipedia", "mdwiki")
WikiFamily: TypeAlias = str

#: Wikidata item ID (e.g., "Q123")
QID: TypeAlias = str

#: Wikidata property ID (e.g., "P31")
PID: TypeAlias = str

#: Wiki revision ID
RevisionID: TypeAlias = int

#: Wiki namespace number
Namespace: TypeAlias = int


class WikiPage(Protocol):
    """Protocol defining the interface for a Wiki page object.

    This protocol describes the expected interface for wiki page objects
    returned by the API wrappers.
    """

    title: WikiTitle
    """The page title."""

    text: WikiText
    """The page content in wikitext format."""

    exists: Callable[[], bool]
    """Check if the page exists."""

    save: Callable[[str, str], bool]
    """Save new content to the page."""


class APIResponse(Protocol):
    """Protocol defining the structure of API responses."""

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the response."""
        ...

    def items(self) -> Iterable[Tuple[str, Any]]:
        """Iterate over response items."""
        ...


# =============================================================================
# TEMPLATE TYPES
# =============================================================================

#: Template parameter value
ParamValue: TypeAlias = Union[str, int, float, None]

#: Template parameters dictionary
TemplateParams: TypeAlias = Dict[str, ParamValue]


class TemplateData(Protocol):
    """Protocol for parsed template data."""

    name: str
    """Template name."""

    params: TemplateParams
    """Template parameters."""

    string: str
    """Raw template string."""


class ParsedTemplate(Protocol):
    """Protocol for template parsing results."""

    templates: Sequence[TemplateData]
    """List of parsed templates."""


# =============================================================================
# DATABASE TYPES
# =============================================================================

#: Database connection parameters
DBConnectionParams: TypeAlias = Dict[str, Union[str, int, None]]

#: Database credentials
DBCredentials: TypeAlias = Dict[str, str]


class DatabaseConnection(Protocol):
    """Protocol for database connection interface."""

    def execute(
        self,
        query: str,
        params: Optional[SQLParams] = None,
    ) -> SQLResultSet:
        """Execute a query and return results."""
        ...

    def close(self) -> None:
        """Close the connection."""
        ...


# =============================================================================
# EXCEPTION TYPES
# =============================================================================


class MDWikiError(Exception):
    """Base exception for MDWiki bot errors."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the exception.

        Args:
            message: Error description.
            context: Additional context about the error.
        """
        super().__init__(message)
        self.message = message
        self.context = context or {}


class AuthenticationError(MDWikiError):
    """Raised when authentication fails."""

    pass


class APIError(MDWikiError):
    """Raised when an API call fails."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[JSONDict] = None,
    ) -> None:
        """Initialize the API error.

        Args:
            message: Error description.
            status_code: HTTP status code if available.
            response: Full API response if available.
        """
        super().__init__(message, {"status_code": status_code, "response": response})
        self.status_code = status_code
        self.response = response


class DatabaseError(MDWikiError):
    """Raised when a database operation fails."""

    def __init__(
        self,
        message: str,
        query: Optional[str] = None,
        params: Optional[SQLParams] = None,
    ) -> None:
        """Initialize the database error.

        Args:
            message: Error description.
            query: The SQL query that failed.
            params: The parameters used with the query.
        """
        super().__init__(message, {"query": query, "params": params})
        self.query = query
        self.params = params


class TemplateError(MDWikiError):
    """Raised when template processing fails."""

    pass


class ValidationError(MDWikiError):
    """Raised when input validation fails."""

    pass


# =============================================================================
# GENERIC TYPES
# =============================================================================

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class Processor(Protocol[T_co]):
    """Protocol for data processors."""

    def process(self, data: Any) -> T_co:
        """Process input data and return result."""
        ...


@runtime_checkable
class Validator(Protocol[T_contra]):
    """Protocol for data validators."""

    def validate(self, data: T_contra) -> bool:
        """Validate input data.

        Returns:
            True if valid, False otherwise.

        Raises:
            ValidationError: If validation fails with details.
        """
        ...


# =============================================================================
# CALLABLE TYPES
# =============================================================================

#: Callback function type for page processing
PageProcessorCallback: TypeAlias = Callable[[WikiTitle, WikiText], WikiText]

#: Callback function type for filtering
FilterCallback: TypeAlias = Callable[[Any], bool]

#: Callback function type for transformation
TransformCallback: TypeAlias = Callable[[T], T]

#: Exception handler callback
ExceptionHandler: TypeAlias = Callable[[Exception], None]

# =============================================================================
# CONFIGURATION TYPES
# =============================================================================

#: Bot configuration dictionary
BotConfig: TypeAlias = Dict[str, Union[str, int, bool, None]]

#: API configuration
APIConfig: TypeAlias = Dict[str, Union[str, int, bool, Dict[str, str]]]


class ConfigProvider(Protocol):
    """Protocol for configuration providers."""

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        ...

    def get_required(self, key: str) -> Any:
        """Get a required configuration value.

        Raises:
            ValidationError: If the key is not found.
        """
        ...


# =============================================================================
# CONSTANTS
# =============================================================================

#: Default timeout for HTTP requests in seconds
DEFAULT_HTTP_TIMEOUT: Final[int] = 30

#: Maximum retries for failed API calls
MAX_API_RETRIES: Final[int] = 3

#: Maximum page size to process (in bytes)
MAX_PAGE_SIZE: Final[int] = 10 * 1024 * 1024  # 10 MB

#: Supported wiki namespaces
NAMESPACES: Final[Dict[str, int]] = {
    "main": 0,
    "talk": 1,
    "user": 2,
    "user_talk": 3,
    "project": 4,
    "project_talk": 5,
    "file": 6,
    "file_talk": 7,
    "mediawiki": 8,
    "mediawiki_talk": 9,
    "template": 10,
    "template_talk": 11,
    "help": 12,
    "help_talk": 13,
    "category": 14,
    "category_talk": 15,
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def is_valid_qid(value: str) -> bool:
    """Check if a string is a valid Wikidata item ID.

    Args:
        value: The string to check.

    Returns:
        True if the value matches the QID pattern (Q followed by digits).

    Examples:
        >>> is_valid_qid("Q123")
        True
        >>> is_valid_qid("q123")
        False
        >>> is_valid_qid("P123")
        False
    """
    return value.startswith("Q") and value[1:].isdigit()


def is_valid_pid(value: str) -> bool:
    """Check if a string is a valid Wikidata property ID.

    Args:
        value: The string to check.

    Returns:
        True if the value matches the PID pattern (P followed by digits).
    """
    return value.startswith("P") and value[1:].isdigit()


def normalize_title(title: str) -> str:
    """Normalize a wiki page title.

    Replaces underscores with spaces and strips whitespace.

    Args:
        title: The page title to normalize.

    Returns:
        The normalized title.

    Examples:
        >>> normalize_title("Hello_World")
        'Hello World'
        >>> normalize_title("  Test  ")
        'Test'
    """
    return title.replace("_", " ").strip()


def title_to_filename(title: str) -> str:
    """Convert a wiki title to a safe filename.

    Args:
        title: The page title.

    Returns:
        A filename-safe version of the title.
    """
    return (
        title.replace(" ", "_")
        .replace("'", "_")
        .replace(":", "_")
        .replace("/", "_")
        .replace('"', "_")
    )
