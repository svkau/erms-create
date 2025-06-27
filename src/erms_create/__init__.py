"""
ERMS Create
===========

Python library for creating ERMS XML documents according to Swedish specifications.

This package provides:
- core: Standard ERMS functionality
- svk_arende: Church of Sweden adaptations for case files

Basic usage:
    >>> from svk_arende import SVKErms
    >>> erms = SVKErms()
    >>> case = erms.create_simple_case(
    ...     case_number="F 2024-0001",
    ...     title="My Case",
    ...     archive_creator="My Organization",
    ...     org_number="1234567890"
    ... )
    >>> erms.save_to_file("my_case.xml")
"""

# Import main classes for convenient access
from .core import Erms, Control, Aggregation, Record
from .svk_arende import SVKErms, SVKCase, SVKRecord

# Version info
__version__ = "1.0.0"
__author__ = "Henrik Vitalis"

# Main API exports
__all__ = [
    # Core ERMS classes
    "Erms",
    "Control",
    "Aggregation",
    "Record",

    # SVK extensions
    "SVKErms",
    "SVKCase",
    "SVKRecord",

    # Version info
    "__version__",
]


# Convenience imports for common use cases
def create_simple_case(case_number: str, title: str, archive_creator: str,
                       org_number: str, **kwargs):
    """
    Convenience function to quickly create a simple case.

    Args:
        case_number: Case number (e.g., "F 2024-0001")
        title: Case title
        archive_creator: Name of archive creator
        org_number: Organization number (10 digits)
        **kwargs: Additional arguments passed to SVKErms.create_simple_case()

    Returns:
        tuple: (erms_document, case) ready for adding records and saving

    Example:
        >>> erms, case = create_simple_case(
        ...     "F 2024-0001", 
        ...     "My Case",
        ...     "My Organization", 
        ...     "1234567890"
        ... )
        >>> erms.save_to_file("my_case.xml")
    """
    erms = SVKErms()
    case = erms.create_simple_case(
        case_number=case_number,
        title=title,
        archive_creator=archive_creator,
        org_number=org_number,
        **kwargs
    )
    return erms, case


# Add convenience function to exports
__all__.append("create_simple_case")