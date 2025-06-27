"""
ERMS Record (Standard)
=====================

Standard ERMS Record implementation.
"""

from lxml import etree
from uuid import uuid4
from .utils import add_in_element, validate_value_list
from .elements import Dates, Agents
from . import namespaces as ns
from . import value_lists


class Record:
    """Standard ERMS Record"""

    def __init__(self, record_type: str = None, physical_or_digital: str = None):
        attributes = {"systemIdentifier": str(uuid4())}
        
        if record_type is not None:
            attributes["recordType"] = record_type
        if physical_or_digital is not None:
            validate_value_list(physical_or_digital, value_lists.RECORD_PHYSICAL_OR_DIGITAL, 
                              "record physical or digital")
            attributes["recordPhysicalOrDigital"] = physical_or_digital

        self.element = etree.Element(ns.ERMS + "record", attributes, nsmap=ns.ERMS_NSMAP)
        
        # Initialize components
        self.object_id = None
        self.extra_id = []
        self.title = None
        self.status = None
        self.running_number = None
        self.agents = None
        self.dates = None
        self.additional_information = None

    def set_object_id(self, object_id: str):
        """Set the object ID"""
        if self.object_id is None:
            self.object_id = etree.Element(ns.ERMS + "objectId", nsmap=ns.ERMS_NSMAP)
            self.object_id.text = object_id
            add_in_element(self.element, self.object_id)

    def set_title(self, value: str):
        """Set title"""
        if self.title is None:
            self.title = etree.Element(ns.ERMS + "title", nsmap=ns.ERMS_NSMAP)
            self.title.text = value
            add_in_element(self.element, self.title)

    def set_status(self, value: str):
        """Set status"""
        validate_value_list(value, value_lists.STATUS, "status")
        if self.status is None:
            self.status = etree.Element(ns.ERMS + "status", value=value, nsmap=ns.ERMS_NSMAP)
            add_in_element(self.element, self.status)

    def set_running_number(self, value: int):
        """Set running number"""
        if self.running_number is None:
            self.running_number = etree.Element(ns.ERMS + "runningNumber", nsmap=ns.ERMS_NSMAP)
            self.running_number.text = str(value)
            add_in_element(self.element, self.running_number)

    def add_agent(self, agent_type: str, name: str, **kwargs):
        """Add an agent"""
        if self.agents is None:
            self.agents = Agents()
            add_in_element(self.element, self.agents.element)
        self.agents.add_agent(agent_type, name, **kwargs)

    def add_date(self, date: str, date_type: str, other_date_type: str = None):
        """Add a date"""
        if self.dates is None:
            self.dates = Dates()
            add_in_element(self.element, self.dates.element)
        self.dates.add_date(date, date_type, other_date_type)
