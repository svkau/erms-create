from lxml import etree
import erms_create.ns as ns

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
	ns.ERMS + "objectId", ns.ERMS + "extraId",
	ns.ERMS + "informationClass",	ns.ERMS + "securityClass",
	ns.ERMS + "identification", ns.ERMS + "classification",
	ns.ERMS + "parentAggregationId", ns.ERMS + "hierarchicalParentClassId",
	ns.ERMS + "maxLevelsOfAggregation", ns.ERMS + "levelName",
	ns.ERMS + "keywords", ns.ERMS + "title",
	ns.ERMS + "otherTitle", ns.ERMS + "subject",
	ns.ERMS + "status", ns.ERMS + "relation",
	ns.ERMS + "additionalInformation", ns.ERMS + "restriction",
	ns.ERMS + "IPPInformation", ns.ERMS + "loan",
	ns.ERMS + "disposal", ns.ERMS + "agents",
	ns.ERMS + "description", ns.ERMS + "dates",
	ns.ERMS + "action", ns.ERMS + "archivalHistory",
	ns.ERMS + "dispatchMode", ns.ERMS + "access",
	ns.ERMS + "physicalLocations", ns.ERMS + "notes",
	ns.ERMS + "eSignatures", ns.ERMS + "aggregation",
	ns.ERMS + "record",
]

RECORD_SORT_ORDER = [
	ns.ERMS + "objectId", ns.ERMS + "extraId",
	ns.ERMS + "informationClass", ns.ERMS + "securityClass",
	ns.ERMS + "identification", ns.ERMS + "classification",
	ns.ERMS + "parentAggregationId", ns.ERMS + "levelName",
	ns.ERMS + "keywords", ns.ERMS + "title",
	ns.ERMS + "otherTitle", ns.ERMS + "subject",
	ns.ERMS + "status", ns.ERMS + "runningNumber",
	ns.ERMS + "relation", ns.ERMS + "restriction",
	ns.ERMS + "IPPInformation", ns.ERMS + "loan",
	ns.ERMS + "disposal", ns.ERMS + "direction",
	ns.ERMS + "agents", ns.ERMS + "description",
	ns.ERMS + "dates", ns.ERMS + "action",
	ns.ERMS + "archivalHistory", ns.ERMS + "dispatchMode",
	ns.ERMS + "access", ns.ERMS + "physicalLocation",
	ns.ERMS + "notes", ns.ERMS + "eSignatures",
	ns.ERMS + "additionalInformation",
]

RESTRICTION_SORT_ORDER = [ns.ERMS + "explanatoryText", ns.ERMS + "regulation",
						  ns.ERMS + "informationClass", ns.ERMS + "securityClass",
						  ns.ERMS + "dates", ns.ERMS + "duration"]


def add_in_element(element: etree.Element, element_to_add: etree.Element):
	if element.tag == ns.ERMS + "control":
		sort_order = CONTROL_SORT_ORDER
	elif element.tag == ns.ERMS + "aggregation":
		sort_order = AGGREGATION_SORT_ORDER
	elif element.tag == ns.ERMS + "record":
		sort_order = RECORD_SORT_ORDER
	elif element.tag == ns.ERMS + "restriction":
		sort_order = RESTRICTION_SORT_ORDER
	else:
		raise Exception(f"Element '{element.tag}' is not a valid element.")

	if len(element) == 0:
		element.append(element_to_add)

	elif len(element.findall(element_to_add.tag)) > 0:
		element.findall(element_to_add.tag)[-1].addnext(element_to_add)

	else:
		i = sort_order.index(element_to_add.tag)

		if i == 0:
			element[0].addprevious(element_to_add)

		else:
			for item in sort_order[i - 1::-1]:

				if len(element.findall(item)) > 0:
					element.findall(item)[-1].addnext(element_to_add)
					break
