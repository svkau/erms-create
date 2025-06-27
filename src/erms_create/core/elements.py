"""
Common ERMS Elements
===================

Reusable elements that can be used in multiple contexts.
"""

from lxml import etree
from . import namespaces as ns
from . import value_lists
from .utils import validate_value_list


class Dates:
    """Container for date elements"""
    
    def __init__(self):
        self.element = etree.Element(ns.ERMS + "dates", nsmap=ns.ERMS_NSMAP)

    def add_date(self, date: str, date_type: str, other_date_type: str = None):
        """
        Add a date element.
        
        Args:
            date: Date in ISO format (YYYY-MM-DDTHH:MM:SS)
            date_type: Type of date from value_lists.DATE_TYPE
            other_date_type: Required if date_type is "other"
        """
        # Validate date type
        validate_value_list(date_type, value_lists.DATE_TYPE, "date type")
        
        # Check if other_date_type is required
        if date_type == "other" and not other_date_type:
            raise ValueError("other_date_type is required when date_type is 'other'")
        
        # Create element
        attributes = {"dateType": date_type}
        if other_date_type:
            attributes["otherDateType"] = other_date_type
            
        elm = etree.Element(ns.ERMS + "date", attributes, nsmap=ns.ERMS_NSMAP)
        elm.text = date
        self.element.append(elm)
        return elm


class Agent:
    """Individual agent (person or organization)"""
    
    def __init__(self, agent_type: str, name: str, organisation: str = None, 
                 unit_name: str = None, id_number: str = None, id_type: str = None,
                 role: str = None, protected_identity: bool = False, 
                 other_agent_type: str = None):
        """
        Create an agent element.
        
        Args:
            agent_type: Type of agent from value_lists.AGENT_TYPE
            name: Name of person or organization
            organisation: Organization name (if person)
            unit_name: Unit within organization
            id_number: ID number (personnummer, etc.)
            id_type: Type of ID number
            role: Role description
            protected_identity: Whether identity is protected
            other_agent_type: Required if agent_type is "other"
        """
        # Validate agent type
        validate_value_list(agent_type, value_lists.AGENT_TYPE, "agent type")
        
        # Check if other_agent_type is required
        if agent_type == "other" and not other_agent_type:
            raise ValueError("other_agent_type is required when agent_type is 'other'")
        
        # Create main element
        attributes = {"agentType": agent_type}
        if other_agent_type:
            attributes["otherAgentType"] = other_agent_type
            
        self.element = etree.Element(ns.ERMS + "agent", attributes, nsmap=ns.ERMS_NSMAP)
        
        # Add name (required)
        name_elm = etree.SubElement(self.element, ns.ERMS + "name", nsmap=ns.ERMS_NSMAP)
        name_elm.text = name
        
        # Add optional elements
        if organisation:
            org_elm = etree.SubElement(self.element, ns.ERMS + "organisation", nsmap=ns.ERMS_NSMAP)
            org_elm.text = organisation
            
        if unit_name:
            unit_elm = etree.SubElement(self.element, ns.ERMS + "unitName", nsmap=ns.ERMS_NSMAP)
            unit_elm.text = unit_name
            
        if id_number:
            id_attrs = {}
            if id_type:
                id_attrs["idNumberType"] = id_type
            id_elm = etree.SubElement(self.element, ns.ERMS + "idNumber", id_attrs, nsmap=ns.ERMS_NSMAP)
            id_elm.text = id_number
            
        if role:
            role_elm = etree.SubElement(self.element, ns.ERMS + "role", nsmap=ns.ERMS_NSMAP)
            role_elm.text = role
            
        if protected_identity:
            prot_elm = etree.SubElement(self.element, ns.ERMS + "protectedIdentity", nsmap=ns.ERMS_NSMAP)
            prot_elm.text = "true"


class Agents:
    """Container for multiple agents"""
    
    def __init__(self):
        self.element = etree.Element(ns.ERMS + "agents", nsmap=ns.ERMS_NSMAP)
        self.agents = []

    def add_agent(self, agent_type: str, name: str, **kwargs) -> Agent:
        """
        Add an agent to the collection.
        
        Args:
            agent_type: Type of agent
            name: Agent name
            **kwargs: Additional arguments passed to Agent constructor
            
        Returns:
            Agent: Created agent object
        """
        agent = Agent(agent_type, name, **kwargs)
        self.element.append(agent.element)
        self.agents.append(agent)
        return agent
