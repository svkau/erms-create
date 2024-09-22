from lxml import etree
from erms_dates import Dates
from erms_create.funcs import add_in_element


class Control:

	def __init__(self):
		self.control = etree.Element("control")
		self.identification = []
		self.information_class = None
		self.classification_schema = None
		self.securityClass = None
		self.dates = None
		self.maintenance_information = None
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

	def date(self, date, type_of_date):
		if self.dates is None:
			self.dates = Dates()
			add_in_element(self.control, self.dates.dates)
		self.dates.add_date(date, type_of_date)



class Maintenance:
	status_types = [
		"cancelled", "created", "deleted", "derived",
		"new", "revised", "unknown", "updated",
	]
	status = None
	agency_code = None
	other_agency_code = []
	agency_name = []

