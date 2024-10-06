from lxml import etree
from erms_create.erms_control import Control
from erms_create.erms_aggregation import Aggregation

class Erms:
	def __init__(self):
		self.element = etree.Element("erms")
		self.control = Control()
		self.element.append(self.control.control)
		self.aggregations = etree.Element("aggregations")
		self.element.append(self.aggregations)

	def add_aggregation(self, type_of_aggregation):
		aggr = Aggregation(type_of_aggregation=type_of_aggregation)
		self.aggregations.append(aggr.aggregation)
		return aggr