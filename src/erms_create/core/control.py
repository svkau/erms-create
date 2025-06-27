"""
ERMS Control Element
===================

Handles the control section of ERMS documents which contains metadata
about the document itself.
"""

from lxml import etree
from .elements import Dates, Agent
from .utils import add_in_element, validate_value_list
from . import namespaces as ns
from . import value_lists


class MaintenanceEvent:
    """A single maintenance event"""
    
    def __init__(self, event_type: str, date_time: str, agent_name: str, 
                 agent_type: str, **agent_kwargs):
        """
        Create a maintenance event.
        
        Args:
            event_type: Type of event from value_lists.EVENT_TYPE
            date_time: When the event occurred (ISO format)
            agent_name: Name of person/system performing the event
            agent_type: Type of agent from value_lists.AGENT_TYPE
            **agent_kwargs: Additional agent parameters
        """
        validate_value_list(event_type, value_lists.EVENT_TYPE, "event type")
        
        self.element = etree.Element(ns.ERMS + "maintenanceEvent", nsmap=ns.ERMS_NSMAP)
        
        # Add event type
        event_elm = etree.SubElement(self.element, ns.ERMS + "eventType", 
                                   value=event_type, nsmap=ns.ERMS_NSMAP)
        
        # Add date/time
        date_elm = etree.SubElement(self.element, ns.ERMS + "eventDateTime", nsmap=ns.ERMS_NSMAP)
        date_elm.text = date_time
        
        # Add agent
        agent = Agent(agent_type, agent_name, **agent_kwargs)
        self.element.append(agent.element)


class MaintenanceHistory:
    """Container for maintenance events"""
    
    def __init__(self):
        self.element = etree.Element(ns.ERMS + "maintenanceHistory", nsmap=ns.ERMS_NSMAP)
        self.maintenance_events = []

    def add_maintenance_event(self, event_type: str, date_time: str, 
                            agent_name: str, agent_type: str, **agent_kwargs) -> MaintenanceEvent:
        """Add a maintenance event"""
        event = MaintenanceEvent(event_type, date_time, agent_name, agent_type, **agent_kwargs)
        self.maintenance_events.append(event)
        self.element.append(event.element)
        return event


class MaintenanceAgency:
    """Information about the agency maintaining the document"""
    
    def __init__(self):
        self.element = etree.Element(ns.ERMS + "maintenanceAgency", nsmap=ns.ERMS_NSMAP)
        self.agency_code = etree.SubElement(self.element, ns.ERMS + "agencyCode", nsmap=ns.ERMS_NSMAP)
        self.other_agency_codes = []
        self.agency_names = []

    def set_agency_code(self, agency_code: str, code_type: str):
        """Set the primary agency code"""
        self.agency_code.text = agency_code
        self.agency_code.set("type", code_type)

    def add_other_agency_code(self, agency_code: str, code_type: str = None):
        """Add an alternative agency code"""
        elm = etree.Element(ns.ERMS + "otherAgencyCode", nsmap=ns.ERMS_NSMAP)
        elm.text = agency_code
        if code_type:
            elm.set("type", code_type)
        self.other_agency_codes.append(elm)
        # Insert after agency_code but before agency_names
        self.agency_code.addnext(elm)

    def add_agency_name(self, agency_name: str):
        """Add an agency name"""
        elm = etree.Element(ns.ERMS + "agencyName", nsmap=ns.ERMS_NSMAP)
        elm.text = agency_name
        self.agency_names.append(elm)
        self.element.append(elm)


class MaintenanceInformation:
    """Container for all maintenance information"""
    
    def __init__(self):
        self.element = etree.Element(ns.ERMS + "maintenanceInformation", nsmap=ns.ERMS_NSMAP)
        
        # Add required sub-elements
        self.maintenance_status = etree.SubElement(
            self.element, ns.ERMS + "maintenanceStatus", nsmap=ns.ERMS_NSMAP)
        
        self.maintenance_agency = MaintenanceAgency()
        self.element.append(self.maintenance_agency.element)
        
        self.maintenance_history = MaintenanceHistory()
        self.element.append(self.maintenance_history.element)

    def set_maintenance_status(self, value: str):
        """Set maintenance status"""
        validate_value_list(value, value_lists.MAINTENANCE_STATUS, "maintenance status")
        self.maintenance_status.set("value", value)


class Control:
    """
    ERMS Control element - contains metadata about the document itself
    """

    def __init__(self):
        self.element = etree.Element(ns.ERMS + "control", nsmap=ns.ERMS_NSMAP)
        
        # Initialize collections
        self.identifications = []
        self.information_class = None
        self.security_class = None
        self.dates = None
        
        # Create required sub-elements
        self.classification_schema = etree.SubElement(
            self.element, ns.ERMS + "classificationSchema", nsmap=ns.ERMS_NSMAP)
        
        self.maintenance_information = MaintenanceInformation()
        add_in_element(self.element, self.maintenance_information.element)
        
        self.system_information = None

    def add_identification(self, value: str, identification_type: str):
        """Add an identification element"""
        elm = etree.Element(ns.ERMS + "identification", 
                          identificationType=identification_type, nsmap=ns.ERMS_NSMAP)
        elm.text = value
        self.identifications.append(elm)
        add_in_element(self.element, elm)
        return elm

    def set_information_class(self, value: str):
        """Set information class"""
        if self.information_class is None:
            self.information_class = etree.Element(ns.ERMS + "informationClass", nsmap=ns.ERMS_NSMAP)
            self.information_class.text = value
            add_in_element(self.element, self.information_class)

    def set_classification_schema(self, schema: str):
        """Set the classification schema description"""
        text_elm = etree.SubElement(
            self.classification_schema, 
            ns.ERMS + "textualDescriptionOfClassificationSchema", 
            nsmap=ns.ERMS_NSMAP)
        p_elm = etree.SubElement(text_elm, ns.ERMS + "p", nsmap=ns.ERMS_NSMAP)
        p_elm.text = schema

    def set_security_class(self, security_class: str):
        """Set security class"""
        if self.security_class is None:
            self.security_class = etree.Element(ns.ERMS + "securityClass", nsmap=ns.ERMS_NSMAP)
            self.security_class.text = security_class
            add_in_element(self.element, self.security_class)

    def add_date(self, date: str, date_type: str, other_date_type: str = None):
        """Add a date element"""
        if self.dates is None:
            self.dates = Dates()
            add_in_element(self.element, self.dates.element)
        self.dates.add_date(date, date_type, other_date_type)

    def set_system_information(self):
        """Set system information (TODO: Implement)"""
        # TODO: Implement system information element
        pass
