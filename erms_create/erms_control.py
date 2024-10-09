from lxml import etree
from erms_elements import Dates, Agent
from erms_create.funcs import add_in_element
import erms_create.ns as ns



class Control:

	def __init__(self):
		self.element = etree.Element(ns.ERMS + "control", nsmap=ns.ERMS_NSMAP)
		self.identification = []
		self.information_class = None
		self.classification_schema = etree.SubElement(self.element, ns.ERMS + "classificationSchema", nsmap=ns.ERMS_NSMAP)
		self.securityClass = None
		self.dates = None
		self.maintenance_information = MaintenanceInformation()
		add_in_element(self.element, self.maintenance_information.element)
		# self.maintenance_status = etree.SubElement(self.maintenance_information, "maintenanceStatus")
		# self.maintenance_agency = etree.SubElement(self.maintenance_information, "maintenanceAgency")
		# self.maintenance_history = etree.SubElement(self.maintenance_information, "maintenanceHistory")

		self.system_information = None

	def add_identification(self, value, identification_type):
		elm = etree.Element(ns.ERMS + "identification", identificationType=identification_type, nsmap=ns.ERMS_NSMAP)
		elm.text = value
		add_in_element(self.element, elm)

	def set_classification_schema(self, schema):
		text = etree.SubElement(self.classification_schema, ns.ERMS + "textualDescriptionOfClassificationSchema", nsmap=ns.ERMS_NSMAP)
		p = etree.SubElement(text, ns.ERMS + "p", nsmap=ns.ERMS_NSMAP)
		p.text = schema

	def add_information_class(self, value):
		if self.information_class is None:
			self.information_class = etree.Element(ns.ERMS + "informationClass", nsmap=ns.ERMS_NSMAP)
			self.information_class.text = value
			add_in_element(self.element, self.information_class)

	def add_date(self, date, type_of_date):
		if self.dates is None:
			self.dates = Dates()
			add_in_element(self.element, self.dates.element)
		self.dates.add_date(date, type_of_date)



	# def set_maintenance_agency(self, agency_code: str, code_type: str, name: str):
	# 	ag_code = etree.SubElement(self.maintenance_agency, "agencyCode", type=code_type)
	# 	ag_code.text = agency_code
	# 	ag_name = etree.SubElement(self.maintenance_agency, "agencyName")
	# 	ag_name.text = name
	#
	# def add_maintenance_event(self, event_type: str, date_time: str, agent_name: str, agent_type: str, **kwargs):
	# 	event= MaintenanceEvent(event_type=event_type, date_time=date_time, agent_name=agent_name, agent_type=agent_type, **kwargs)
	# 	self.maintenance_history.append(event.element)

class MaintenanceInformation:
	def __init__(self):
		self.element = etree.Element(ns.ERMS + "maintenanceInformation", nsmap=ns.ERMS_NSMAP)
		self.maintenance_status = etree.SubElement(self.element, ns.ERMS + "maintenanceStatus", nsmap=ns.ERMS_NSMAP)
		self.maintenance_agency = MaintenanceAgency()
		self.element.append(self.maintenance_agency.element)
		self.maintenance_history = MaintenanceHistory()
		self.element.append(self.maintenance_history.element)


	def set_maintenance_status(self, value: str):
		self.maintenance_status.set("value", value)

class MaintenanceAgency:
	def __init__(self):
		self.element = etree.Element(ns.ERMS + "maintenanceAgency", nsmap=ns.ERMS_NSMAP)
		self.agency_code = etree.SubElement(self.element, ns.ERMS + "agencyCode", nsmap=ns.ERMS_NSMAP)
		self.other_agency_code = []
		self.agency_name = []

	def  set_agency_code(self, agency_code: str, code_type: str):
		self.agency_code.text = agency_code
		self.agency_code.set("type", code_type)

	def add_other_agency_code(self, agency_code: str, code_type: str=None):
		elm = etree.Element(ns.ERMS + "otherAgencyCode", nsmap=ns.ERMS_NSMAP)
		elm.text = agency_code
		if code_type is not None:
			elm["type"] = code_type
		self.element.insert(1, elm)

	def add_agency_name(self, agency_name: str):
		elm = etree.Element(ns.ERMS + "agencyName", nsmap=ns.ERMS_NSMAP)
		elm.text = agency_name
		self.element.append(elm)

class MaintenanceHistory:
	def __init__(self):
		self.element = etree.Element(ns.ERMS + "maintenanceHistory", nsmap=ns.ERMS_NSMAP)
		self.maintenance_event = []

	def add_maintenance_event(self, event_type: str, date_time: str, agent_name: str, agent_type: str, **kwargs):
		event = MaintenanceEvent(event_type, date_time, agent_name, agent_type, **kwargs)
		self.maintenance_event.append(event)
		self.element.append(event.element)


class MaintenanceEvent:
	event_types = [
		"created", "revised", "deleted",
		"canelled", "derived", "updated",
		"unknown",
	]
	def __init__(self, event_type: str, date_time: str, agent_name: str, agent_type: str, **kwargs):
		self.element = etree.Element("maintenanceEvent")
		etree.SubElement(self.element, "eventTyp", value=event_type)
		elm_date = etree.SubElement(self.element, "eventDateTime")
		elm_date.text = date_time
		elm_agent = Agent(agent_type=agent_type, name=agent_name, **kwargs)
		self.element.append(elm_agent.element)

myc = Control()
myc.add_identification("Sunne pstorat", "arkivbildare")
myc.add_identification("1234567890", "organisationsnummer")
myc.add_identification("P 2023-0034", "ärendenummer")
myc.set_classification_schema("Klassificeringsstruktur för lokal nivå 2018, ver. 1.0")
myc.add_information_class("klass")
myc.maintenance_information.set_maintenance_status("new")
myc.maintenance_information.maintenance_agency.set_agency_code("1234567890", "organisationsnummer")
myc.maintenance_information.maintenance_agency.add_other_agency_code("enannankod")
myc.maintenance_information.maintenance_agency.add_other_agency_code("ytterligareenenannankod")
myc.maintenance_information.maintenance_agency.add_agency_name("Kyrkostyrelsen")
myc.maintenance_information.maintenance_agency.add_agency_name("Kommunen")
myc.maintenance_information.maintenance_history.add_maintenance_event(event_type="created",
																	  date_time="2001-12-17T09:30:47",
																	  agent_name="Henrik Vitalis",
																	  agent_type="deliverer",
																	  organisation="KPML(r)")

result = etree.tostring(myc.element, pretty_print=True, xml_declaration=True, encoding="UTF-8")
print(result.decode("UTF-8"))