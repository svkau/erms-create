from lxml import etree
from erms_create.erms_control import Control
from erms_create.erms_aggregation import Aggregation
from erms_create.erms_record import Record
import erms_create.ns as ns

class Erms:
	def __init__(self, aggr: bool=True):
		self.element = etree.Element(ns.ERMS + "erms", nsmap=ns.ROOT_NSMAP)
		self.control = Control()
		self.element.append(self.control.element)
		if aggr is not None:
			self.aggregations = etree.Element(ns.ERMS + "aggregations", nsmap=ns.ERMS_NSMAP)
			self.element.append(self.aggregations)
			self.records = None
		else:
			self.records = etree.Element(ns.ERMS + "records", nsmap=ns.ERMS_NSMAP)
			self.element.append(self.aggregations)
			self.aggregations = None

	def add_aggregation(self, type_of_aggregation):
		if self.aggregations is not None:
			aggr = Aggregation(type_of_aggregation=type_of_aggregation)
			self.aggregations.append(aggr.element)
			return aggr

	def add_record(self, type_of_record=None, physical_or_digital=None):
		if self.records is not None:
			rec = Record(type_of_record=type_of_record, physical_or_digital=physical_or_digital)
			self.records.append(rec.element)
			return rec
