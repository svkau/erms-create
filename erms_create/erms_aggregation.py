from lxml import etree
from uuid import uuid4
from erms.funcs import add_in_element


class Aggregation:
	def __init__(self, type_of_aggregation):
		self.aggregation = etree.Element("aggregation",
									   systemIdentifier=str(uuid4()), aggregationType=type_of_aggregation)
		self.object_id = etree.SubElement(self.aggregation, "objectId")
		self.extra_id = []
		self.information_class = None
		self.security_class = None
		self.identification = []
		self.classification = []
		self.parent_aggregation_id = None
		self.hierarchical_parent_class_id = None
		self.max_levels_of_aggregation = None
		self.level_name = None
		self.keywords = None
		self.title = None
		self.other_title = []
		self.subject = None
		self.status = None
		self.relation = []
		self.additional_information = None
		self.restriction = None
		self.ipp_information = None
		self.loan = None
		self.disposal = None
		self.agents = None
		self.description = None
		self.dates = None
		self.action = []
		self.archival_history = None
		self.dispatch_mode = None
		self.access = None
		self.physical_locations = None
		self.notes = None
		self.e_signatures = None
		self.sub_aggregation = None
		self.record = []

	def add_extra_id(self, type_of_id, value):
		elm = etree.Element("extraId", extraIdType=type_of_id)
		elm.text = value
		self.extra_id.append(elm)
		add_in_element(self.aggregation, elm)

	def add_information_class(self, value):
		if self.information_class is None:
			self.information_class = etree.Element("informationClass")
			self.information_class.text = value
			add_in_element(self.aggregation, self.information_class)

	def add_security_class(self, value):
		if self.security_class is None:
			self.security_class = etree.Element("securityClass")
			self.security_class.text = value
			add_in_element(self.aggregation, self.security_class)

	def add_identification(self, type_of_identification, value):
		elm = etree.Element("identification", identificationType=type_of_identification)
		elm.text = value
		self.identification.append(elm)
		add_in_element(self.aggregation, elm)

	def add_classification(self, value, class_id=None, class_code=None, fully_qual_class_code=None,
						   new_fully_qual_class_code=None):
		attributes = {}
		if class_id:
			attributes["classificationId"] = class_id
		if class_code:
			attributes["classificationCode"] = class_code
		if fully_qual_class_code:
			attributes["fullyQualifiedClassificationCode"] = fully_qual_class_code
		if new_fully_qual_class_code:
			attribute["newFullyQualifiedClassificationCode"]: new_fully_qual_class_code

		elm = etree.Element("classification", attributes)
		elm.text = value
		self.classification.append(elm)
		add_in_element(self.aggregation, elm)

	def add_parent_aggregation_id(self, value):
		if self.parent_aggregation_id is None:
			self.parent_aggregation_id = etree.Element("parentAggregationId")
			self.parent_aggregation_id.text = value
			add_in_element(self.aggregation, self.parent_aggregation_id)

	def add_hierarchical_parent_class_id(self, value):
		if self.hierarchical_parent_class_id is None:
			self.hierarchical_parent_class_id = etree.Element("hierarchicalParentClassId")
			self.hierarchical_parent_class_id.text = value
			add_in_element(self.aggregation, self.hierarchical_parent_class_id)

	def add_max_levels_of_aggregation(self, value):
		if self.max_levels_of_aggregation is None:
			self.max_levels_of_aggregation = etree.Element("maxLevelsOfAggregation")
			self.max_levels_of_aggregation.text = value
			add_in_element(self.aggregation, self.max_levels_of_aggregation)

	def add_level_name(self, value):
		if self.level_name is None:
			self.level_name = etree.Element("levelName")
			self.level_name.text = value
			add_in_element(self.aggregation, self.level_name)

	def add_keyword(self, value):
		if self.keywords is None:
			self.keywords = etree.Element("keywords")
			add_in_element(self.aggregation, self.keywords)

		elm = etree.Element("keyword")
		elm.text = value
		self.keywords.append(elm)

	def add_title(self, value):
		if self.title is None:
			self.title = etree.Element("title")
			self.title.text = value
			add_in_element(self.aggregation, self.title)

	def add_other_title(self, value, type_of_title):
		elm = etree.Element("otherTitle", titleType=type_of_title)
		elm.text = value
		self.other_title.append(elm)
		add_in_element(self.aggregation, elm)

	def add_subject(self, value):
		if self.subject is None:
			self.subject = etree.Element("subject")
			self.subject.text = value
			add_in_element(self.aggregation, self.subject)

	def add_status(self, value):
		if self.status is None:
			self.status = etree.Element("status", value=value)
			add_in_element(self.aggregation, self.status)

	def add_relation(self, value, type_of_relation, other_type=None):
		attributes = {}
		attributes["relationType"] = type_of_relation
		if other_type:
			attributes["otherRelationType"] = other_type

		elm = etree.Element("relation", attributes)
		elm.text = value
		self.relation.append(elm)
		add_in_element(self.aggregation, elm)

	def add_description(self, value):
		if self.description is None:
			self.description = etree.Element("description")
			self.description.text = value
			add_in_element(self.aggregation, self.description)

	def add_date(self, date, type_of_date):
		if self.dates is None:
			self.dates = Dates()
			add_in_element(self.aggregation, self.dates.dates)
			self.dates.add_date(date, type_of_date)

	def add_history_line(self, value):
		if self.archival_history is None:
			self.archival_history = etree.Element("archivalHistory")
			add_in_element(self.aggregation, self.archival_history)

		elm = etree.Element("historyLine")
		elm.text = value
		self.archival_history.append(elm)

	def add_dispatch_mode(self, value):
		if self.dispatch_mode is None:
			self.dispatch_mode = etree.Element("dispatchMode")
			self.dispatch_mode.text = value
			add_in_element(self.aggregation, self.dispatch_mode)

	def add_access(self, value):
		if self.access is None:
			self.access = etree.Element("access")
			self.access.text = value
			add_in_element(self.aggregation, self.access)

	def add_physical_location(self, current_location=None, home_location=None):
		if self.physical_locations is None:
			self.physical_locations = etree.Element("physicalLocations")
			add_in_element(self.aggregation, self.physical_locations)

		phys_loc = etree.Element("physicalLocation")
		self.physical_locations.append(phys_loc)

		if current_location is not None:
			cur_loc = etree.Element("currentLocation")
			cur_loc.text = current_location
			phys_loc.append(cur_loc)

		if home_location is not None:
			for item in home_location:
				elm = etree.Element("homeLocation")
				elm.text = item
				phys_loc.append(elm)

	def add_note(self, value, note_type=None, note_date=None):
		if self.notes is None:
			self.notes = etree.Element("notes")
			add_in_element(self.aggregation, self.notes)

		attribut = {}
		if note_type is not None:
			attribut["noteType"] = note_type
		if note_date is not None:
			attribut["noteDate"] = note_date

		elm = etree.Element("note", attribut)
		elm.text = value
		self.notes.append(elm)

	def add_sub_aggregation(self, aggregation):
		if len(self.record) == 0:
			if self.sub_aggregation is None:
				self.sub_aggregation = aggregation
				add_in_element(self.aggregation, aggregation)

	def add_record(self, record):
		if self.sub_aggregation is None:
			self.record.append(record)
			add_in_element(self.aggregation, record)
