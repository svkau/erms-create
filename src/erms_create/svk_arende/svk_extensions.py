"""
SVK Extensions for ERMS
=======================

Svenska kyrkans tilläggselement som placeras i additionalXMLData.
Motsvarar elementen definierade i ERMS-SVK-element.xsd
"""

from lxml import etree
from core.elements import Dates, Agents, Agent
from core.utils import validate_value_list
from . import value_lists

# Namespace för SVK-elementen
SVK_NAMESPACE = "https://xml.svenskakyrkan.se/ERMS-SVK-element"
SVK = "{%s}" % SVK_NAMESPACE
SVK_NSMAP = {None: SVK_NAMESPACE}


class RelatedObject:
    """Ett relaterat objekt (projekt, fastighet etc.)"""
    
    def __init__(self, object_type: str, object_name: str, object_id: str, 
                 delivery_system_id: str = None):
        validate_value_list(object_type, value_lists.OBJECT_TYPE, "object type")
        
        self.element = etree.Element(SVK + "relatedObject", 
                                   typeOfObject=object_type, nsmap=SVK_NSMAP)
        
        # Lägg till obligatoriska element
        name_elm = etree.SubElement(self.element, SVK + "objectName", nsmap=SVK_NSMAP)
        name_elm.text = object_name
        
        id_elm = etree.SubElement(self.element, SVK + "objectId", nsmap=SVK_NSMAP)
        id_elm.text = object_id
        
        # Lägg till valfria element
        if delivery_system_id:
            sys_id_elm = etree.SubElement(self.element, SVK + "deliveringSystemId", nsmap=SVK_NSMAP)
            sys_id_elm.text = delivery_system_id


class RelatedObjects:
    """Container för relaterade objekt"""
    
    def __init__(self):
        self.element = etree.Element(SVK + "relatedObjects", nsmap=SVK_NSMAP)
        self.objects = []
    
    def add_object(self, object_type: str, object_name: str, object_id: str,
                   delivery_system_id: str = None) -> RelatedObject:
        """Lägg till ett relaterat objekt"""
        obj = RelatedObject(object_type, object_name, object_id, delivery_system_id)
        self.objects.append(obj)
        self.element.append(obj.element)
        return obj


class SVKNote:
    """En SVK-anteckning"""
    
    def __init__(self, note_type: str, note_text: str, creator_name: str, 
                 created_date: str, creator_org: str = None):
        validate_value_list(note_type, value_lists.NOTE_TYPE, "note type")
        
        self.element = etree.Element(SVK + "svkNote", typeOfNote=note_type, nsmap=SVK_NSMAP)
        
        # Anteckningstext
        text_elm = etree.SubElement(self.element, SVK + "noteText", nsmap=SVK_NSMAP)
        text_elm.text = note_text
        
        # Skapare
        agents = Agents()
        agents.add_agent("creator", creator_name, organisation=creator_org)
        self.element.append(agents.element)
        
        # Datum
        dates = Dates()
        dates.add_date(created_date, "created")
        self.element.append(dates.element)


class SVKNotes:
    """Container för SVK-anteckningar"""
    
    def __init__(self):
        self.element = etree.Element(SVK + "svkNotes", nsmap=SVK_NSMAP)
        self.notes = []
    
    def add_note(self, note_type: str, note_text: str, creator_name: str,
                 created_date: str, creator_org: str = None) -> SVKNote:
        """Lägg till en anteckning"""
        note = SVKNote(note_type, note_text, creator_name, created_date, creator_org)
        self.notes.append(note)
        self.element.append(note.element)
        return note


class AuditLogEvent:
    """En händelse i ändringsloggen"""
    
    def __init__(self, event_time: str, user: str, scope: str, action: str,
                 value_before: str = None, value_after: str = None):
        validate_value_list(scope, value_lists.AUDIT_SCOPE, "audit scope")
        validate_value_list(action, value_lists.AUDIT_ACTION, "audit action")
        
        self.element = etree.Element(SVK + "auditLogEvent", nsmap=SVK_NSMAP)
        
        # Obligatoriska element
        time_elm = etree.SubElement(self.element, SVK + "eventTime", nsmap=SVK_NSMAP)
        time_elm.text = event_time
        
        user_elm = etree.SubElement(self.element, SVK + "user", nsmap=SVK_NSMAP)
        user_elm.text = user
        
        scope_elm = etree.SubElement(self.element, SVK + "scope", nsmap=SVK_NSMAP)
        scope_elm.text = scope
        
        action_elm = etree.SubElement(self.element, SVK + "action", nsmap=SVK_NSMAP)
        action_elm.text = action
        
        # Valfria element
        if value_before:
            before_elm = etree.SubElement(self.element, SVK + "valueBeforeChange", nsmap=SVK_NSMAP)
            before_elm.text = value_before
            
        if value_after:
            after_elm = etree.SubElement(self.element, SVK + "valueAfterChange", nsmap=SVK_NSMAP)
            after_elm.text = value_after


class AuditLogEvents:
    """Container för ändringslogg"""
    
    def __init__(self):
        self.element = etree.Element(SVK + "auditLogEvents", nsmap=SVK_NSMAP)
        self.events = []
    
    def add_event(self, event_time: str, user: str, scope: str, action: str,
                  value_before: str = None, value_after: str = None) -> AuditLogEvent:
        """Lägg till en händelse i ändringsloggen"""
        event = AuditLogEvent(event_time, user, scope, action, value_before, value_after)
        self.events.append(event)
        self.element.append(event.element)
        return event


class ContractInfo:
    """Information om avtal"""
    
    def __init__(self):
        self.element = etree.Element(SVK + "contractInfo", nsmap=SVK_NSMAP)
        self.dates = None
    
    def set_external_reference(self, reference: str):
        """Sätt avsändares referens"""
        ref_elm = etree.SubElement(self.element, SVK + "externalReference", nsmap=SVK_NSMAP)
        ref_elm.text = reference
    
    def set_call_off_value(self, value: int, currency: str = "SEK"):
        """Sätt avropat värde"""
        val_elm = etree.SubElement(self.element, SVK + "callOffValue", 
                                 currency=currency, nsmap=SVK_NSMAP)
        val_elm.text = str(value)
    
    def set_contract_value(self, value: int, currency: str = "SEK"):
        """Sätt kontraktsvärde"""
        val_elm = etree.SubElement(self.element, SVK + "contractValue",
                                 currency=currency, nsmap=SVK_NSMAP)
        val_elm.text = str(value)
    
    def set_agreement_type(self, agreement_type: str):
        """Sätt avtalstyp"""
        validate_value_list(agreement_type, value_lists.AGREEMENT_TYPE, "agreement type")
        type_elm = etree.SubElement(self.element, SVK + "typeOfAgreement", nsmap=SVK_NSMAP)
        type_elm.text = agreement_type
    
    def add_date(self, date: str, date_type: str):
        """Lägg till datum (start/end)"""
        if self.dates is None:
            self.dates = Dates()
            self.element.append(self.dates.element)
        self.dates.add_date(date, date_type)


class SVKExtensions:
    """
    Container för alla SVK-tillägg som placeras i additionalXMLData.
    Kan användas för både aggregation och record.
    """
    
    def __init__(self, extension_type: str = "aggregation"):
        """
        Args:
            extension_type: "aggregation" eller "record"
        """
        self.extension_type = extension_type
        
        # Skapa rot-element för SVK-anpassningen
        self.root_element = etree.Element(SVK + "ermsSvkArende", 
                                        schemaVersion="1.0",
                                        ermsSchemaVersion="2.1.2", 
                                        elementSchemaVersion="1.0",
                                        schematronVersion="1.0",
                                        nsmap=SVK_NSMAP)
        
        if extension_type == "aggregation":
            self.element = etree.SubElement(self.root_element, SVK + "ermsSvkAggregation", nsmap=SVK_NSMAP)
        else:
            self.element = etree.SubElement(self.root_element, SVK + "ermsSvkRecord", nsmap=SVK_NSMAP)
        
        # Initiera komponenter
        self.related_objects = None
        self.svk_notes = None
        self.audit_log = None
        self.contract_info = None
        
    def set_initiative(self, initiative: str):
        """Sätt initiativ (endast för aggregation)"""
        if self.extension_type != "aggregation":
            raise ValueError("Initiative can only be set for aggregations")
        validate_value_list(initiative, value_lists.INITIATIVE, "initiative")
        
        init_elm = etree.SubElement(self.element, SVK + "initiative", nsmap=SVK_NSMAP)
        init_elm.text = initiative
    
    def get_related_objects(self) -> RelatedObjects:
        """Hämta eller skapa related objects container"""
        if self.related_objects is None:
            self.related_objects = RelatedObjects()
            self.element.append(self.related_objects.element)
        return self.related_objects
    
    def get_svk_notes(self) -> SVKNotes:
        """Hämta eller skapa SVK notes container"""
        if self.svk_notes is None:
            self.svk_notes = SVKNotes()
            self.element.append(self.svk_notes.element)
        return self.svk_notes
    
    def get_audit_log(self) -> AuditLogEvents:
        """Hämta eller skapa audit log container"""
        if self.audit_log is None:
            self.audit_log = AuditLogEvents()
            self.element.append(self.audit_log.element)
        return self.audit_log
    
    def get_contract_info(self) -> ContractInfo:
        """Hämta eller skapa contract info (endast för record)"""
        if self.extension_type != "record":
            raise ValueError("Contract info can only be set for records")
        if self.contract_info is None:
            self.contract_info = ContractInfo()
            self.element.append(self.contract_info.element)
        return self.contract_info
