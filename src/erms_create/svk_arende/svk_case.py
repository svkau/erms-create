"""
SVK Case (Ärendeakt)
===================

Utökad version av ERMS Aggregation med SVK-specifika funktioner och validering.
"""

from lxml import etree
from core.aggregation import Aggregation
from core.utils import add_in_element
from core import namespaces as ns
from .svk_extensions import SVKExtensions
from .validation import SVKValidator
from . import value_lists


class SVKCase(Aggregation):
    """
    Svenska kyrkans utökade ärendeakt.
    Bygger på standard ERMS Aggregation och lägger till SVK-funktionalitet.
    """
    
    def __init__(self, case_number: str = None, title: str = None):
        # Initiera som standard ERMS caseFile
        super().__init__(type_of_aggregation="caseFile")
        
        # SVK-specifik validering
        self.validator = SVKValidator()
        
        # SVK-tillägg (placeras i additionalXMLData)
        self.svk_extensions = None
        
        # Sätt grundläggande information
        if case_number:
            self.set_case_number(case_number)
        if title:
            self.set_title(title)
    
    def set_case_number(self, case_number: str):
        """
        Sätt ärendenummer med SVK-validering.
        Format: [diariekod] [årtal]-[löpnummer]
        """
        if not self.validator.validate_case_number(case_number):
            raise ValueError(f"Ogiltigt ärendenummer: {case_number}")
        
        self.set_object_id(case_number)
    
    def set_archive_creator_info(self, org_number: str, name: str = None, aid: str = None):
        """
        Sätt information om arkivansvarig enligt SVK-krav.
        Antingen org_number eller aid måste anges.
        """
        if org_number:
            if not self.validator.validate_org_number(org_number):
                raise ValueError(f"Ogiltigt organisationsnummer: {org_number}")
            self.add_extra_id("organisationsnummer", org_number)
        
        if aid:
            self.add_extra_id("aid", aid)
        
        if not org_number and not aid:
            raise ValueError("Antingen organisationsnummer eller aid måste anges")
    
    def set_status_svk(self, status: str):
        """Sätt status med SVK-validering (endast closed/obliterated)"""
        if not self.validator.validate_case_status(status):
            raise ValueError(f"Ogiltig status för SVK: {status}")
        
        self.set_status(status)
    
    def add_required_dates(self, opened_date: str, closed_date: str, created_date: str = None):
        """
        Lägg till obligatoriska datum enligt SVK-krav.
        
        Args:
            opened_date: När ärendet officiellt öppnades
            closed_date: När ärendet avslutades/makulerades  
            created_date: När ärendet skapades i systemet (optional)
        """
        if created_date:
            self.add_date(created_date, "created")
        self.add_date(opened_date, "opened")
        self.add_date(closed_date, "closed")
    
    def add_case_agents(self, creator: str = None, responsible_person: str = None,
                       counterparts: list = None, closing_person: str = None):
        """
        Lägg till aktörer för ärendet enligt SVK-mönster.
        
        Args:
            creator: Den som skapade ärendet
            responsible_person: Ansvarig handläggare
            counterparts: Lista med externa parter
            closing_person: Den som avslutade ärendet
        """
        if creator:
            self.add_agent("creator", creator)
        
        if responsible_person:
            self.add_agent("responsible_person", responsible_person)
        
        if counterparts:
            for counterpart in counterparts:
                if isinstance(counterpart, str):
                    self.add_agent("counterpart", counterpart)
                else:
                    # Förvänta dict med mer info
                    self.add_agent("counterpart", counterpart.get('name', ''), 
                                 organisation=counterpart.get('organisation'),
                                 id_number=counterpart.get('id_number'),
                                 id_type=counterpart.get('id_type'))
        
        if closing_person:
            self.add_agent("other", closing_person, other_agent_type="closing_person")
    
    def get_svk_extensions(self) -> SVKExtensions:
        """Hämta eller skapa SVK-tillägg för ärendet"""
        if self.svk_extensions is None:
            self.svk_extensions = SVKExtensions("aggregation")
            
            # Skapa additionalInformation om det inte finns
            if not hasattr(self, 'additional_information') or self.additional_information is None:
                self.additional_information = etree.Element("additionalInformation")
                add_in_element(self.element, self.additional_information)
            
            # Skapa additionalXMLData
            additional_xml = etree.SubElement(self.additional_information, "additionalXMLData")
            additional_xml.append(self.svk_extensions.root_element)
        
        return self.svk_extensions
    
    def set_initiative(self, initiative: str):
        """Sätt initiativ (eget/externt)"""
        extensions = self.get_svk_extensions()
        extensions.set_initiative(initiative)
    
    def add_related_project(self, project_name: str, project_id: str, system_id: str = None):
        """Lägg till relaterat projekt"""
        extensions = self.get_svk_extensions()
        related_objects = extensions.get_related_objects()
        related_objects.add_object("project", project_name, project_id, system_id)
    
    def add_related_property(self, property_name: str, property_id: str, system_id: str = None):
        """Lägg till relaterad fastighet"""
        extensions = self.get_svk_extensions()
        related_objects = extensions.get_related_objects()
        related_objects.add_object("realEstate", property_name, property_id, system_id)
    
    def add_svk_note(self, note_type: str, note_text: str, creator_name: str, 
                     created_date: str, creator_org: str = None):
        """Lägg till SVK-anteckning"""
        extensions = self.get_svk_extensions()
        svk_notes = extensions.get_svk_notes()
        svk_notes.add_note(note_type, note_text, creator_name, created_date, creator_org)
    
    def add_audit_event(self, event_time: str, user: str, scope: str, action: str,
                       value_before: str = None, value_after: str = None):
        """Lägg till händelse i ändringsloggen"""
        extensions = self.get_svk_extensions()
        audit_log = extensions.get_audit_log()
        audit_log.add_event(event_time, user, scope, action, value_before, value_after)
    
    def add_record_svk(self, document_number: str = None, title: str = None, 
                      record_type: str = "ärendedokument"):
        """
        Lägg till en SVK-handling till ärendet.
        
        Returns:
            SVKRecord: Den skapade handlingen
        """
        # Importera här för att undvika cirkulär import
        from .svk_record import SVKRecord
        
        record = SVKRecord(record_type=record_type)
        
        if document_number:
            record.set_document_number(document_number)
        if title:
            record.set_title(title)
        
        # Lägg till i aggregation
        add_in_element(self.element, record.element)
        return record
    
    def validate(self) -> dict:
        """
        Validera ärendet enligt SVK-regler.
        
        Returns:
            Dict med valideringsresultat
        """
        # Samla data för validering
        case_data = {
            'case_number': self.object_id.text if self.object_id is not None else None,
            'status': self.status.get('value') if self.status is not None else None,
            # TODO: Lägg till fler fält för validering
        }
        
        self.validator.validate_case_data(case_data)
        return self.validator.get_validation_report()
