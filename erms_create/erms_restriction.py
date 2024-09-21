from lxml import etree
from erms_create.funcs import add_in_element


class Restriction:
	def __init__(self, type_of_restriction, regulation):
		restriction_types = ["confidential", "gdpr", "integrity"]
		if type_of_restriction in restriction_types:
			self.restriction = etree.Element("restriction", restrictionType=type_of_restriction)
		else:
			self.restriction = etree.Element("restriction", restrictionType="other_type", otherRestrictionType=type_of_restriction)

		self.explanatory_text = None
		self.regulation = etree.Element("regulation")
		self.regulation.text = regulation
		add_in_element(self.restriction, self.regulation)
		self.information_class = None
		self.security_information = None
		self.dates = None
		self.duration = None

	def add_explanatory_text(self, value):
		if self.explanatory_text is None:
			self.explanatory_text = etree.Element("explanatoryText")
			self.explanatory_text.text = value
			add_in_element(self.restriction, self.explanatory_text)
