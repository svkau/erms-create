from lxml import etree
from erms_elements import Dates, Agent
from erms_create.funcs import add_in_element


class Control:

	def __init__(self):
		self.control = etree.Element("control")
		self.identification = []
		self.information_class = None
		self.classification_schema = None
		self.securityClass = None
		self.dates = None
		self.maintenance_information = etree.Element("maintenanceInformation")
		add_in_element(self.control, self.maintenance_information)
		self.maintenance_status = etree.SubElement(self.maintenance_information, "maintenanceStatus")
		self.maintenance_agency = etree.SubElement(self.maintenance_information, "maintenanceAgency")
		self.maintenance_history = etree.SubElement(self.maintenance_information, "maintenanceHistory")

		self.system_information = None

	def add_identification(self, value, identification_type):
		elm = etree.Element("identification", identificationType=identification_type)
		elm.text = value
		add_in_element(self.control, elm)

	def add_information_class(self, value):
		if self.information_class is None:
			self.information_class = etree.Element("informationClass")
			self.information_class.text = value
			add_in_element(self.control, self.information_class)

	def add_date(self, date, type_of_date):
		if self.dates is None:
			self.dates = Dates()
			add_in_element(self.control, self.dates.dates)
		self.dates.add_date(date, type_of_date)

	def set_maintenance_status(self, maintenance_status: str):
		self.maintenance_status.attrib["value"] = maintenance_status

	def set_maintenance_agency(self, agency_code: str, code_type: str, name: str):
		ag_code = etree.SubElement(self.maintenance_agency, "agencyCode", type=code_type)
		ag_code.text = agency_code
		ag_name = etree.SubElement(self.maintenance_agency, "agencyName")
		ag_name.text = name

	def add_maintenance_event(self, event_type: str, date_time: str, agent_name: str, agent_type: str, **kwargs):
		event= MaintenanceEvent(event_type=event_type, date_time=date_time, agent_name=agent_name, agent_type=agent_type, **kwargs)
		self.maintenance_history.append(event.element)



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
		self.element.append(elm_agent.agent)
