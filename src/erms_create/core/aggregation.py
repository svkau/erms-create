"""
ERMS Aggregation (Standard)
===========================

Standard ERMS Aggregation implementation.
"""

from lxml import etree
from uuid import uuid4
from .utils import add_in_element, validate_value_list
from .elements import Dates, Agents
from . import namespaces as ns
from . import value_lists


class Aggregation:
    """Standard ERMS Aggregation"""

    def __init__(self, type_of_aggregation: str = "caseFile"):
        # Validate aggregation type
        validate_value_list(type_of_aggregation, value_lists.AGGREGATION_TYPE, "aggregation type")

        self.element = etree.Element(
            ns.ERMS + "aggregation", 
            systemIdentifier=str(uuid4()),
            aggregationType=type_of_aggregation, 
            nsmap=ns.ERMS_NSMAP
        )
        
        # Initialize components
        self.object_id = None
        self.extra_id = []
        self.information_class = None
        self.security_class = None
        self.identification = []
        self.classification = []
        self.keywords = None
        self.title = None
        self.other_title = []
        self.subject = []
        self.status = None
        self.relation = []
        self.agents = None
        self.description = None
        self.dates = None
        self.additional_information = None

    def set_object_id(self, object_id: str):
        """Set the object ID"""
        if self.object_id is None:
            self.object_id = etree.Element(ns.ERMS + "objectId", nsmap=ns.ERMS_NSMAP)
            self.object_id.text = object_id
            add_in_element(self.element, self.object_id)

    def add_extra_id(self, type_of_id: str, value: str):
        """Add an extra ID"""
        elm = etree.Element(ns.ERMS + "extraId", extraIdType=type_of_id, nsmap=ns.ERMS_NSMAP)
        elm.text = value
        self.extra_id.append(elm)
        add_in_element(self.element, elm)

    def add_classification(self, value: str, class_code: str = None):
        """Add classification"""
        attributes = {}
        if class_code:
            attributes["classificationCode"] = class_code

        elm = etree.Element(ns.ERMS + "classification", attributes, nsmap=ns.ERMS_NSMAP)
        elm.text = value
        self.classification.append(elm)
        add_in_element(self.element, elm)

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
