"""
ERMS Core Library
================

Standard ERMS implementation following DILCIS Board specifications.
This library contains only standard ERMS elements and value lists.

Usage:
    from core import Erms, Control, Aggregation, Record

    erms = Erms()
    aggregation = erms.add_aggregation("caseFile")
    aggregation.set_title("My Case")

    record = aggregation.add_record()
    record.set_title("My Document")
"""

from .erms import Erms
from .control import Control
from .aggregation import Aggregation
from .record import Record
from .elements import Dates, Agents, Agent
from . import namespaces as ns
from . import value_lists

__version__ = "1.0.0"
__author__ = "Henrik Vitalis"

__all__ = [
    'Erms',
    'Control',
    'Aggregation',
    'Record',
    'Dates',
    'Agents',
    'Agent',
    'ns',
    'value_lists'
]