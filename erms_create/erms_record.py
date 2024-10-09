from lxml import etree
from uuid import uuid4
from erms_create.funcs import add_in_element
from erms_create import ns


class Record:

	def __init__(self, type_of_record=None, physical_or_digital=None):

		attributes = dict()
		attributes["systemIdentifier"] = str(uuid4())
		if type_of_record is not None:
			attributes["recordType"] = type_of_record
		if physical_or_digital is not None:
			attributes["recordPhysicalOrDigital"] = physical_or_digital

		self.element = etree.Element(ns.ERMS + "record", attributes, nsmap=ns.ERMS_NSMAP)
		self.object_id = None
		self.extra_id = []
		self.information_class = None
		self.security_class = None
		self.identification = []
		self.classification = []
		self.parent_aggregation_id = None
		self.level_name = None
		self.keywords = None
		self.title = None
		self.other_title = []
		self.subject = []
		self.status = None
		self.running_number = None
		self.relation = []


	def set_object_id(self, object_id: str):
		elm = etree.Element(ns.ERMS + "objectId", nsmap=ns.ERMS_NSMAP)
		elm.text = object_id
		self.object_id = elm
		add_in_element(self.element, elm)

	def add_extra_id(self, type_of_id, value):
		elm = etree.Element(ns.ERMS + "extraId", extraIdType=type_of_id, nsmap=ns.ERMS_NSMAP)
		elm.text = value
		self.extra_id.append(elm)
		add_in_element(self.element, elm)

	def add_information_class(self, value):
		if self.information_class is None:
			self.information_class = etree.Element(ns.ERMS + "informationClass", nsmap=ns.ERMS_NSMAP)
			self.information_class.text = value
			add_in_element(self.element, self.information_class)

	def add_security_class(self, value):
		if self.security_class is None:
			self.security_class = etree.Element(ns.ERMS + "securityClass", nsmap=ns.ERMS_NSMAP)
			self.security_class.text = value
			add_in_element(self.element, self.security_class)

	def add_identification(self, type_of_identification, value):
		elm = etree.Element(ns.ERMS + "identification", identificationType=type_of_identification, nsmap=ns.ERMS_NSMAP)
		elm.text = value
		self.identification.append(elm)
		add_in_element(self.element, elm)

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
			attributes["newFullyQualifiedClassificationCode"]: new_fully_qual_class_code

		elm = etree.Element(ns.ERMS + "classification", attributes, nsmap=ns.ERMS_NSMAP)
		elm.text = value
		self.classification.append(elm)
		add_in_element(self.element, elm)

	def add_parent_aggregation_id(self, value):
		if self.parent_aggregation_id is None:
			self.parent_aggregation_id = etree.Element(ns.ERMS + "parentAggregationId", nsmap=ns.ERMS_NSMAP)
			self.parent_aggregation_id.text = value
			add_in_element(self.element, self.parent_aggregation_id)

	def add_level_name(self, value):
		if self.level_name is None:
			self.level_name = etree.Element(ns.ERMS + "levelName", nsmap=ns.ERMS_NSMAP)
			self.level_name.text = value
			add_in_element(self.element, self.level_name)

	def add_keyword(self, value):
		if self.keywords is None:
			self.keywords = etree.Element(ns.ERMS + "keywords", nsmap=ns.ERMS_NSMAP)
			add_in_element(self.element, self.keywords)

		elm = etree.Element(ns.ERMS + "keyword", nsmap=ns.ERMS_NSMAP)
		elm.text = value
		self.keywords.append(elm)

	def set_title(self, value):
		if self.title is None:
			self.title = etree.Element(ns.ERMS + "title", nsmap=ns.ERMS_NSMAP)
			self.title.text = value
			add_in_element(self.element, self.title)

	def add_other_title(self, value, type_of_title):
		elm = etree.Element(ns.ERMS + "otherTitle", titleType=type_of_title, nsmap=ns.ERMS_NSMAP)
		elm.text = value
		self.other_title.append(elm)
		add_in_element(self.element, elm)

	def add_subject(self, value):
		elm = etree.Element(ns.ERMS + "subject", nsmap=ns.ERMS_NSMAP)
		elm.text = value
		self.subject.append(elm)
		add_in_element(self.element, elm)

	def set_status(self, value):
		if self.status is None:
			self.status = etree.Element(ns.ERMS + "status", value=value, nsmap=ns.ERMS_NSMAP)
			add_in_element(self.element, self.status)

	def set_running_number(self, value):
		if self.running_number is None:
			self.running_number = etree.Element(ns.ERMS + "runningNumber", nsmap=ns.ERMS_NSMAP)
			self.running_number.text = value
			add_in_element(self.element, self.running_number)

	def add_relation(self, value, type_of_relation, other_type=None):
		attributes = dict()
		attributes["relationType"] = type_of_relation
		if other_type:
			attributes["otherRelationType"] = other_type

		elm = etree.Element(ns.ERMS + "relation", attributes, nsmap=ns.ERMS_NSMAP)
		elm.text = value
		self.relation.append(elm)
		add_in_element(self.element, elm)
