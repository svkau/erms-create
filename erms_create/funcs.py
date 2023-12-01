from lxml import etree

CONTROL_SORT_ORDER = [
	"identification",
	"informationClass",
	"classificationSchema",
	"securityClass",
	"dates",
	"maintenanceInformation",
	"systemInformation",
]

AGGREGATION_SORT_ORDER = [
	"objectId", "extraId",
	"informationClass",	"securityClass",
	"identification", "classification",
	"parentAggregationId", "hierarchicalParentClassId",
	"maxLevelsOfAggregation", "levelName",
	"keywords", "title",
	"otherTitle", "subject",
	"status", "relation",
	"additionalInformation", "restriction",
	"IPPInformation", "loan",
	"disposal", "agents",
	"description", "dates",
	"action", "archivalHistory",
	"dispatchMode", "access",
	"physicalLocations", "notes",
	"eSignatures", "aggregation",
	"record",
]

RECORD_SORT_ORDER = [
	"objectId", "extraId",
	"informationClass", "securityClass",
	"identification", "classification",
	"parentAggregationId", "levelName",
	"keywords", "title",
	"otherTitle", "subject",
	"status", "runningNumber",
	"relation", "restriction",
	"IPPInformation", "loan",
	"disposal", "direction",
	"agents", "description",
	"dates", "action",
	"archivalHistory", "dispatchMode",
	"access", "physicalLocation",
	"notes", "eSignatures",
	"additionalInformation",
]

RESTRICTION_SORT_ORDER = ["explanatoryText", "regulation", "informationClass", "securityClass", "dates", "duration"]


def add_in_element(element: etree.Element, element_to_add: etree.Element):

	if element.tag == "control":
		sort_order = CONTROL_SORT_ORDER
	elif element.tag == "aggregation":
		sort_order = AGGREGATION_SORT_ORDER
	elif element.tag == "record":
		sort_order = RECORD_SORT_ORDER
	elif element.tag == "restriction":
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
