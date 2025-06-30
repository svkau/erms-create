"""
ERMS SVK Ärendehandlingar
========================

Svenska kyrkans anpassning av ERMS för ärendehandlingar.
Bygger på core och lägger till SVK-specifika element och validering.

Usage:
    from erms_create.svk_arende import SVKErms, SVKCase, SVKRecord

    erms = SVKErms()
    case = erms.add_case(
        case_number="F 2019-0032",
        title="Mitt ärende",
        archive_creator="Sunne pastorat",
        org_number="1234567890"
    )

    document = case.add_document(
        title="Min handling",
        direction="incoming",
        sender="Försäkringskassan"
    )
"""

from .svk_erms import SVKErms
from .svk_case import SVKCase
from .svk_record import SVKRecord
from .svk_extensions import SVKExtensions
from . import value_lists
from . import validation

__version__ = "1.0.0"
__author__ = "Henrik Vitalis"

__all__ = [
    'SVKErms',
    'SVKCase',
    'SVKRecord',
    'SVKExtensions',
    'value_lists',
    'validation'
]