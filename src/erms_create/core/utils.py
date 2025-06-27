"""
Utility functions for ERMS Core
"""

from lxml import etree
from . import namespaces as ns

# Element ordering for correct XML structure
CONTROL_SORT_ORDER = [
    ns.ERMS + "identification",
    ns.ERMS + "informationClass", 
    ns.ERMS + "classificationSchema",
    ns.ERMS + "securityClass",
    ns.ERMS + "dates",
    ns.ERMS + "maintenanceInformation",
    ns.ERMS + "systemInformation",
]

AGGREGATION_SORT_ORDER = [
    ns.ERMS + "objectId",
    ns.ERMS + "extraId",
    ns.ERMS + "informationClass",
    ns.ERMS + "securityClass",
    ns.ERMS + "identification",
    ns.ERMS + "classification",
    ns.ERMS + "parentAggregationId",
    ns.ERMS + "hierarchicalParentClassId",
    ns.ERMS + "maxLevelsOfAggregation",
    ns.ERMS + "levelName",
    ns.ERMS + "keywords",
    ns.ERMS + "title",
    ns.ERMS + "otherTitle",
    ns.ERMS + "subject",
    ns.ERMS + "status",
    ns.ERMS + "relation",
    ns.ERMS + "additionalInformation",
    ns.ERMS + "restriction",
    ns.ERMS + "IPPInformation",
    ns.ERMS + "loan",
    ns.ERMS + "disposal",
    ns.ERMS + "agents",
    ns.ERMS + "description",
    ns.ERMS + "dates",
    ns.ERMS + "action",
    ns.ERMS + "archivalHistory",
    ns.ERMS + "dispatchMode",
    ns.ERMS + "access",
    ns.ERMS + "physicalLocations",
    ns.ERMS + "notes",
    ns.ERMS + "eSignatures",
    ns.ERMS + "aggregation",
    ns.ERMS + "record",
]

RECORD_SORT_ORDER = [
    ns.ERMS + "objectId",
    ns.ERMS + "extraId",
    ns.ERMS + "informationClass",
    ns.ERMS + "securityClass",
    ns.ERMS + "identification",
    ns.ERMS + "classification",
    ns.ERMS + "parentAggregationId",
    ns.ERMS + "levelName",
    ns.ERMS + "keywords",
    ns.ERMS + "title",
    ns.ERMS + "otherTitle",
    ns.ERMS + "subject",
    ns.ERMS + "status",
    ns.ERMS + "runningNumber",
    ns.ERMS + "relation",
    ns.ERMS + "restriction",
    ns.ERMS + "IPPInformation",
    ns.ERMS + "loan",
    ns.ERMS + "disposal",
    ns.ERMS + "direction",
    ns.ERMS + "agents",
    ns.ERMS + "description",
    ns.ERMS + "dates",
    ns.ERMS + "action",
    ns.ERMS + "archivalHistory",
    ns.ERMS + "dispatchMode",
    ns.ERMS + "access",
    ns.ERMS + "physicalLocation",
    ns.ERMS + "notes",
    ns.ERMS + "eSignatures",
    ns.ERMS + "additionalInformation",
]

RESTRICTION_SORT_ORDER = [
    ns.ERMS + "explanatoryText",
    ns.ERMS + "regulation",
    ns.ERMS + "informationClass",
    ns.ERMS + "securityClass",
    ns.ERMS + "dates",
    ns.ERMS + "duration"
]


def add_in_element(element: etree.Element, element_to_add: etree.Element):
    """
    Add an element to the correct position according to ERMS element ordering.
    
    Args:
        element: Parent element to add to
        element_to_add: Child element to add
        
    Raises:
        ValueError: If element type is not supported for ordering
    """
    # Determine sort order based on element type
    if element.tag == ns.ERMS + "control":
        sort_order = CONTROL_SORT_ORDER
    elif element.tag == ns.ERMS + "aggregation":
        sort_order = AGGREGATION_SORT_ORDER
    elif element.tag == ns.ERMS + "record":
        sort_order = RECORD_SORT_ORDER
    elif element.tag == ns.ERMS + "restriction":
        sort_order = RESTRICTION_SORT_ORDER
    else:
        # For unknown elements, just append at the end
        element.append(element_to_add)
        return

    # If no existing children, just append
    if len(element) == 0:
        element.append(element_to_add)
        return

    # If element already exists of this type, add after the last one
    existing_elements = element.findall(element_to_add.tag)
    if len(existing_elements) > 0:
        existing_elements[-1].addnext(element_to_add)
        return

    # Find correct position based on sort order
    try:
        target_index = sort_order.index(element_to_add.tag)
    except ValueError:
        # Element not in sort order, append at end
        element.append(element_to_add)
        return

    # If this should be the first element
    if target_index == 0:
        element[0].addprevious(element_to_add)
        return

    # Find the correct position by looking backwards in sort order
    for i in range(target_index - 1, -1, -1):
        existing = element.findall(sort_order[i])
        if existing:
            existing[-1].addnext(element_to_add)
            return

    # If we get here, add at the beginning
    element[0].addprevious(element_to_add)


def validate_value_list(value: str, valid_values: list, context: str = "value") -> None:
    """
    Validate that a value is in a list of valid values.
    
    Args:
        value: Value to validate
        valid_values: List of acceptable values
        context: Description of what is being validated (for error messages)
        
    Raises:
        ValueError: If value is not in valid_values
    """
    if value not in valid_values:
        raise ValueError(f"Invalid {context}: '{value}'. Must be one of: {', '.join(valid_values)}")


def create_element_with_text(tag: str, text: str, nsmap: dict = None, **attributes) -> etree.Element:
    """
    Create an XML element with text content and optional attributes.
    
    Args:
        tag: Element tag name (including namespace)
        text: Text content
        nsmap: Namespace map
        **attributes: Element attributes
        
    Returns:
        etree.Element: Created element
    """
    if nsmap is None:
        nsmap = ns.ERMS_NSMAP
        
    element = etree.Element(tag, attributes, nsmap=nsmap)
    element.text = text
    return element
