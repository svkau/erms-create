"""
ERMS Main Class
==============

Main ERMS document class.
"""

from lxml import etree
from .control import Control
from .aggregation import Aggregation
from .record import Record
from . import namespaces as ns


class Erms:
    """Main ERMS document class"""
    
    def __init__(self, aggr: bool = True):
        self.element = etree.Element(ns.ERMS + "erms", nsmap=ns.ROOT_NSMAP)
        
        # Add control element
        self.control = Control()
        self.element.append(self.control.element)
        
        # Add aggregations or records container
        if aggr:
            self.aggregations = etree.Element(ns.ERMS + "aggregations", nsmap=ns.ERMS_NSMAP)
            self.element.append(self.aggregations)
            self.records = None
        else:
            self.records = etree.Element(ns.ERMS + "records", nsmap=ns.ERMS_NSMAP)
            self.element.append(self.records)
            self.aggregations = None

    def add_aggregation(self, type_of_aggregation: str = "caseFile") -> Aggregation:
        """Add an aggregation"""
        if self.aggregations is not None:
            aggr = Aggregation(type_of_aggregation=type_of_aggregation)
            self.aggregations.append(aggr.element)
            return aggr
        else:
            raise ValueError("Cannot add aggregation when Erms was initialized with aggr=False")

    def add_record(self, record_type: str = None, physical_or_digital: str = None) -> Record:
        """Add a record"""
        if self.records is not None:
            rec = Record(record_type=record_type, physical_or_digital=physical_or_digital)
            self.records.append(rec.element)
            return rec
        else:
            raise ValueError("Cannot add record when Erms was initialized with aggr=True")
    
    def to_xml_string(self, pretty_print: bool = True, xml_declaration: bool = True, 
                     encoding: str = "UTF-8") -> str:
        """Generate XML string from ERMS structure"""
        return etree.tostring(
            self.element, 
            pretty_print=pretty_print, 
            xml_declaration=xml_declaration, 
            encoding=encoding
        ).decode(encoding)
    
    def save_to_file(self, filename: str, pretty_print: bool = True, 
                    xml_declaration: bool = True, encoding: str = "UTF-8"):
        """Save ERMS structure to file"""
        xml_string = self.to_xml_string(pretty_print, xml_declaration, encoding)
        with open(filename, 'w', encoding=encoding) as f:
            f.write(xml_string)
