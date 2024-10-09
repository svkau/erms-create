from lxml import etree
from uuid import uuid4

from erms_create.funcs import add_in_element
from erms_create.erms_elements import Dates, Agents
from erms_create.erms_record import Record
import erms_value_lists as value_lists
import erms_create.ns as ns


class Aggregation:
	"""
	Class Aggregation
	"""
	def __init__(self, type_of_aggregation):

		if type_of_aggregation not in value_lists.aggregation_type:
			raise Exception(f"'{type_of_aggregation}' is not a valid type of aggregation.")

		self.aggregation = etree.Element(ns.ERMS + "aggregation", systemIdentifier=str(uuid4()),
										 aggregationType=type_of_aggregation, nsmap=ns.ERMS_NSMAP)
		self.object_id = None
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
		self.subject = []
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

	def set_object_id(self, text: str):

		"""
		Creates element **objectId** (if not previously set) with text,
		and then adds it to the aggregation element.

		The element object is assigned to **Aggregation.object_id**

		:param text: string
			Element's text
		"""

		if self.object_id is None:
			self.object_id = etree.Element(ns.ERMS + "objectId", nsmap=ns.ERMS_NSMAP)
			self.object_id.text = text
			add_in_element(self.aggregation, self.object_id)

	def add_extra_id(self, type_of_id: str, text: str) -> etree.Element:

		"""
		Creates element **extraId** with attribute and text,
		and then adds it to the aggregation element.

		The element object is added to the list **Aggregation.extra_id**

		Returns the created element.

		:param type_of_id: string
			Type of extra id.
		:param text: string
			Element's text
		:return: etree.Element
		"""

		elm = etree.Element(ns.ERMS + "extraId", extraIdType=type_of_id, nsmap=ns.ERMS_NSMAP)
		elm.text = text
		self.extra_id.append(elm)
		add_in_element(self.aggregation, elm)
		return elm

	def set_information_class(self, text: str):

		"""
		Creates element **informationClass** (if not previously set)
		with text value and then adds it to the aggregation element.

		The element object is assigned to **Aggregation.information_class**.

		:param text: string - Element's text
		"""

		if self.information_class is None:
			self.information_class = etree.Element(ns.ERMS + "informationClass", nsmap=ns.ERMS_NSMAP)
			self.information_class.text = text
			add_in_element(self.aggregation, self.information_class)

	def set_security_class(self, text: str):

		"""
		Creates element **securityClass** (if not previously set)
		with text value and then adds it to the aggregation element.

		The element object is assigned to **Aggregation.security_class**.

		:param text: string - Element's text
		"""

		if self.security_class is None:
			self.security_class = etree.Element(ns.ERMS + "securityClass", nsmap=ns.ERMS_NSMAP)
			self.security_class.text = text
			add_in_element(self.aggregation, self.security_class)

	def add_identification(self, type_of_identification: str, text: str) -> etree.Element:

		"""
		Creates element **identification** with attribute and text,
		and then adds it to the aggregation element.

		The element object is added to the list **Aggregation.identification**

		Returns the created element.

		:param type_of_identification: string - Type of identification
		:param text: string - Element's text
		:return: etree.Element
		"""

		elm = etree.Element(ns.ERMS + "identification", identificationType=type_of_identification, nsmap=ns.ERMS_NSMAP)
		elm.text = text
		self.identification.append(elm)
		add_in_element(self.aggregation, elm)
		return elm

	def add_classification(self, text: str, class_id: str = None, class_code: str = None,
						   fully_qual_class_code: str = None, new_fully_qual_class_code: str = None) -> etree.Element:

		"""
		Creates element **classification** with attributesand text,
		and then adds it to the aggregation element.

		The element object is added to the list **Aggregation.classification**

		Returns the created element.

		:param text: string - Element's text
		:param class_id: string - string - (optional)
		:param class_code: string - (optional)
		:param fully_qual_class_code: - (optional)
		:param new_fully_qual_class_code: - (optional)
		:return: etree.Element
		"""

		attributes = {}
		if class_id:
			attributes["classificationId"] = class_id
		if class_code:
			attributes["classificationCode"] = class_code
		if fully_qual_class_code:
			attributes["fullyQualifiedClassificationCode"] = fully_qual_class_code
		if new_fully_qual_class_code:
			attributes["newFullyQualifiedClassificationCode"] = new_fully_qual_class_code

		elm = etree.Element(ns.ERMS + "classification", attributes, nsmap=ns.ERMS_NSMAP)
		elm.text = text
		self.classification.append(elm)
		add_in_element(self.aggregation, elm)
		return elm

	def set_parent_aggregation_id(self, text: str):

		"""
		Creates element **parentAggregationId** (if not previously set)
		with text value and then adds it to the aggregation element.

		The element object is assigned to **Aggregation.parent_aggregation_id**.

		:param text: string - Element's text
		"""

		if self.parent_aggregation_id is None:
			self.parent_aggregation_id = etree.Element(ns.ERMS + "parentAggregationId", nsmap=ns.ERMS_NSMAP)
			self.parent_aggregation_id.text = text
			add_in_element(self.aggregation, self.parent_aggregation_id)

	def set_hierarchical_parent_class_id(self, text: str):

		"""
		Creates element **hierarchicalParentClassId** (if not previously set)
		with text value and then adds it to the aggregation element.

		The element object is assigned to **Aggregation.hierarchical_parent_class_id**.

		:param text: string - Element's text
		"""

		if self.hierarchical_parent_class_id is None:
			self.hierarchical_parent_class_id = etree.Element(ns.ERMS + "hierarchicalParentClassId", nsmap=ns.ERMS_NSMAP)
			self.hierarchical_parent_class_id.text = text
			add_in_element(self.aggregation, self.hierarchical_parent_class_id)

	def set_max_levels_of_aggregation(self, text: str):

		"""
		Creates element **maxLevelsOfAggragation** (if not previously set)
		with text value and then adds it to the aggregation element.

		The element object is assigned to **Aggregation.max_levels_of_aggregation**.

		:param text: string - Element's text
		"""

		if self.max_levels_of_aggregation is None:
			self.max_levels_of_aggregation = etree.Element(ns.ERMS + "maxLevelsOfAggregation", nsmap=ns.ERMS_NSMAP)
			self.max_levels_of_aggregation.text = text
			add_in_element(self.aggregation, self.max_levels_of_aggregation)

	def set_level_name(self, text: str):

		"""
		Creates element **levelName** (if not previously set)
		with text value and then adds it to the aggregation element.

		The element object is assigned to **Aggregation.level_name**.

		:param text: string - Element's text
		"""

		if self.level_name is None:
			self.level_name = etree.Element(ns.ERMS + "levelName", nsmap=ns.ERMS_NSMAP)
			self.level_name.text = text
			add_in_element(self.aggregation, self.level_name)

	def add_keyword(self, text: str) -> etree.Element:

		"""
		Creates element **keywords** (if not previously set)
		which is added to the aggregation element.

		Creates element **keyword** with text value and then
		adds it to the keywords' element.

		Returns the created keyword element.

		:param text: string - Element's text
		:return: etree.Element
		"""

		if self.keywords is None:
			self.keywords = etree.Element(ns.ERMS + "keywords", nsmap=ns.ERMS_NSMAP)
			add_in_element(self.aggregation, self.keywords)

		elm = etree.Element(ns.ERMS + "keyword", nsmap=ns.ERMS_NSMAP)
		elm.text = text
		self.keywords.append(elm)
		return elm

	def set_title(self, text: str):

		"""
		Creates element **title** (if not previously set)
		with text value and then adds it to the aggregation element.

		The element object is assigned to **Aggregation.title**.

		:param text: string - Element's text
		"""

		if self.title is None:
			self.title = etree.Element(ns.ERMS + "title", nsmap=ns.ERMS_NSMAP)
			self.title.text = text
			add_in_element(self.aggregation, self.title)

	def add_other_title(self, text: str, type_of_title: str) -> etree.Element:

		"""
		Creates element **otherTitle** with attribute and text,
		and then adds it to the aggregation element.

		The element object is added to the list **Aggregation.other_title**

		Returns the created element.

		:param type_of_title: string - Type of title
		:param text: string - Element's text
		:return: etree.Element
		"""

		elm = etree.Element(ns.ERMS + "otherTitle", titleType=type_of_title, nsmap=ns.ERMS_NSMAP)
		elm.text = text
		self.other_title.append(elm)
		add_in_element(self.aggregation, elm)
		return elm

	def add_subject(self, text: str) -> etree.Element:

		"""
		Creates element **subject** with text,
		and then adds it to the aggregation element.

		The element object is added to the list **Aggregation.subject**

		Returns the created element.

		:param text: string - Element's text
		:return: etree.Element
		"""

		elm = etree.Element(ns.ERMS + "subject", nsmap=ns.ERMS_NSMAP)
		elm.text = text
		self.subject.append(elm)
		add_in_element(self.aggregation, elm)
		return elm

	def set_status(self, text: str):

		"""
		Creates element **status** (if not previously set)
		with text value and then adds it to the aggregation element.

		The element object is assigned to **Aggregation.status**.

		:param text: string - Element's text
		"""

		if text not in value_lists.status:
			raise Exception(f"'{text}' is not a valid status.")

		if self.status is None:
			self.status = etree.Element(ns.ERMS + "status", value=text, nsmap=ns.ERMS_NSMAP)
			add_in_element(self.aggregation, self.status)

	def add_relation(self, text: str, type_of_relation: str, other_type: str = None):

		"""
			Creates element **relation** with text and attribute,
			and then adds it to the aggregation element.

			The element object is added to the list **Aggregation.relation**

			Returns the created element.

			:param text: string - Element's text
			:param type_of_relation: string - Selected from a list of values.
			:param other_type: string - Obligatory if type_of_relation is "own_relation_definition".
			:return: etree.Element
			"""

		if type_of_relation not in value_lists.relation_type:
			raise Exception(f"'{type_of_relation}' is not a valid type of relation.")

		if type_of_relation == "own_relation_definition" and other_type is None:
			raise Exception(f"Parameter other_type is missing.")

		attributes = dict()
		attributes["relationType"] = type_of_relation
		if other_type:
			attributes["otherRelationType"] = other_type

		elm = etree.Element(ns.ERMS + "relation", attributes, nsmap=ns.ERMS_NSMAP)
		elm.text = text
		self.relation.append(elm)
		add_in_element(self.aggregation, elm)
		return elm

	def set_description(self, text: str):

		"""
		Creates element **description** (if not previously set)
		with text value and then adds it to the aggregation element.

		The element object is assigned to **Aggregation.description**.

		:param text: string - Element's text
		"""

		if self.description is None:
			self.description = etree.Element(ns.ERMS + "description", nsmap=ns.ERMS_NSMAP)
			self.description.text = text
			add_in_element(self.aggregation, self.description)

	def add_agent(self, agent_type, name, **kwargs):
		if self.agents is None:
			self.agents = Agents()
			add_in_element(self.aggregation, self.agents.element)
		self.agents.add_agent(agent_type, name, **kwargs)

	def add_date(self, date, type_of_date):
		if self.dates is None:
			self.dates = Dates()
			add_in_element(self.aggregation, self.dates.element)
		self.dates.add_date(date, type_of_date)

	def history_line(self, value):
		if self.archival_history is None:
			self.archival_history = etree.Element(ns.ERMS + "archivalHistory", nsmap=ns.ERMS_NSMAP)
			add_in_element(self.aggregation, self.archival_history)

		elm = etree.Element("historyLine")
		elm.text = value
		self.archival_history.append(elm)

	def dispatch_mode(self, value):
		if self.dispatch_mode is None:
			self.dispatch_mode = etree.Element(ns.ERMS + "dispatchMode", nsmap=ns.ERMS_NSMAP)
			self.dispatch_mode.text = value
			add_in_element(self.aggregation, self.dispatch_mode)

	def access(self, value):
		if self.access is None:
			self.access = etree.Element(ns.ERMS + "access", nsmap=ns.ERMS_NSMAP)
			self.access.text = value
			add_in_element(self.aggregation, self.access)

	def physical_location(self, current_location=None, home_location=None):
		if self.physical_locations is None:
			self.physical_locations = etree.Element(ns.ERMS + "physicalLocations", nsmap=ns.ERMS_NSMAP)
			add_in_element(self.aggregation, self.physical_locations)

		phys_loc = etree.Element(ns.ERMS + "physicalLocation", nsmap=ns.ERMS_NSMAP)
		self.physical_locations.append(phys_loc)

		if current_location is not None:
			cur_loc = etree.Element(ns.ERMS + "currentLocation", nsmap=ns.ERMS_NSMAP)
			cur_loc.text = current_location
			phys_loc.append(cur_loc)

		if home_location is not None:
			for item in home_location:
				elm = etree.Element(ns.ERMS + "homeLocation", nsmap=ns.ERMS_NSMAP)
				elm.text = item
				phys_loc.append(elm)

	def note(self, value, note_type=None, note_date=None):
		if self.notes is None:
			self.notes = etree.Element(ns.ERMS + "notes", nsmap=ns.ERMS_NSMAP)
			add_in_element(self.aggregation, self.notes)

		attribut = {}
		if note_type is not None:
			attribut["noteType"] = note_type
		if note_date is not None:
			attribut["noteDate"] = note_date

		elm = etree.Element(ns.ERMS + "note", attribut, nsmap=ns.ERMS_NSMAP)
		elm.text = value
		self.notes.append(elm)

	def sub_aggregation(self, aggregation):
		if len(self.record) == 0:
			if self.sub_aggregation is None:
				self.sub_aggregation = aggregation
				add_in_element(self.aggregation, aggregation)

	def add_record(self):
		if self.sub_aggregation is None:
			new_rec = Record()
			self.record.append(new_rec)
			add_in_element(self.aggregation, new_rec.element)
			return new_rec
