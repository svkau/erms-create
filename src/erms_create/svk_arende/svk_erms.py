"""
SVK ERMS
========

Utökad version av ERMS med SVK-specifika funktioner och convenience-metoder.
"""

from datetime import datetime
from core.erms import Erms
from core.control import Control
from .svk_case import SVKCase
from .validation import SVKValidator, validate_complete_erms_document
from . import value_lists


class SVKErms(Erms):
    """
    Svenska kyrkans utökade ERMS-implementation.
    Lägger till SVK-specifik validering och convenience-metoder.
    """
    
    def __init__(self):
        # Initiera som standard ERMS med aggregations
        super().__init__(aggr=True)
        self.validator = SVKValidator()
        
        # Sätt upp kontroll-element med SVK-defaults
        self._setup_svk_control()
    
    def _setup_svk_control(self):
        """Konfigurera control-elementet med SVK-specifika inställningar"""
        # Sätt maintenance status till "new" för nya dokument
        self.control.maintenance_information.set_maintenance_status("new")
        
        # Lägg till skapande-händelse
        self.control.maintenance_information.maintenance_history.add_maintenance_event(
            event_type="created",
            date_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            agent_name="erms-svk-arende",
            agent_type="deliverer",
            organisation="Svenska kyrkan"
        )
    
    def setup_control_info(self, archive_creator: str, org_number: str = None, 
                          aid: str = None, case_number: str = None,
                          classification_schema: str = "KlaSL2016_1.0"):
        """
        Konfigurera control-information enligt SVK-krav.
        
        Args:
            archive_creator: Arkivbildarens namn
            org_number: Organisationsnummer (10 siffror)
            aid: ArkivbildarID (alternativ till org_number)
            case_number: Ärendenummer
            classification_schema: Klassificeringsstruktur
        """
        # Validera parametrar
        if org_number and not self.validator.validate_org_number(org_number):
            raise ValueError(f"Ogiltigt organisationsnummer: {org_number}")
        
        if not self.validator.validate_classification_schema(classification_schema):
            raise ValueError(f"Ogiltig klassificeringsstruktur: {classification_schema}")
        
        # Lägg till obligatoriska identifikationer
        self.control.add_identification(archive_creator, "arkivbildare")
        
        if org_number:
            self.control.add_identification(org_number, "organisationsnummer")
        elif aid:
            self.control.add_identification(aid, "aid")
        else:
            raise ValueError("Antingen organisationsnummer eller aid måste anges")
        
        if case_number:
            if not self.validator.validate_case_number(case_number):
                raise ValueError(f"Ogiltigt ärendenummer: {case_number}")
            self.control.add_identification(case_number, "ärendenummer")
        
        # Sätt klassificeringsstruktur
        self.control.set_classification_schema(classification_schema)
        
        # Konfigurera maintenance agency
        if org_number:
            self.control.maintenance_information.maintenance_agency.set_agency_code(
                org_number, "organisationsnummer")
        elif aid:
            self.control.maintenance_information.maintenance_agency.set_agency_code(
                aid, "aid")
        
        self.control.maintenance_information.maintenance_agency.add_agency_name(archive_creator)
    
    def add_case(self, case_number: str, title: str, archive_creator: str = None,
                org_number: str = None, aid: str = None, **kwargs) -> SVKCase:
        """
        Lägg till ett ärende med SVK-validering.
        
        Args:
            case_number: Ärendenummer (format: [kod] [år]-[nummer])
            title: Ärendemening
            archive_creator: Arkivbildare (för control om inte redan satt)
            org_number: Organisationsnummer
            aid: ArkivbildarID
            **kwargs: Ytterligare parametrar för ärendet
            
        Returns:
            SVKCase: Det skapade ärendet
        """
        # Konfigurera control om inte redan gjort
        if not self.control.identifications and archive_creator:
            self.setup_control_info(archive_creator, org_number, aid, case_number)
        
        # Skapa ärendet
        case = SVKCase(case_number, title)
        
        # Sätt arkivansvarig info
        if org_number or aid:
            case.set_archive_creator_info(org_number, archive_creator, aid)
        
        # Lägg till i aggregations
        self.aggregations.append(case.element)
        
        return case
    
    def create_simple_case(self, case_number: str, title: str, archive_creator: str,
                          org_number: str, opened_date: str = None, closed_date: str = None,
                          status: str = "closed", creator: str = None,
                          responsible_person: str = None) -> SVKCase:
        """
        Skapa ett enkelt, komplett ärende med minimala uppgifter.
        
        Args:
            case_number: Ärendenummer
            title: Ärendemening
            archive_creator: Arkivbildare
            org_number: Organisationsnummer
            opened_date: Öppningsdatum (default: idag)
            closed_date: Avslutningsdatum (default: idag)
            status: Status (default: "closed")
            creator: Skapare av ärendet
            responsible_person: Ansvarig handläggare
            
        Returns:
            SVKCase: Komplett ärende redo för export
        """
        # Sätt default-datum
        today = datetime.now().strftime("%Y-%m-%dT00:00:00")
        if not opened_date:
            opened_date = today
        if not closed_date:
            closed_date = today
        
        # Skapa ärendet
        case = self.add_case(case_number, title, archive_creator, org_number)
        
        # Sätt grundläggande information
        case.set_status_svk(status)
        case.add_required_dates(opened_date, closed_date, today)
        
        # Lägg till aktörer
        if creator or responsible_person:
            case.add_case_agents(creator=creator, responsible_person=responsible_person)
        
        return case
    
    def validate(self, use_schematron: bool = False, schematron_file: str = None) -> dict:
        """
        Validera hela ERMS-dokumentet.
        
        Args:
            use_schematron: Om Schematron-validering ska användas
            schematron_file: Sökväg till Schematron-fil
            
        Returns:
            Dict med valideringsresultat
        """
        # Generera XML för validering
        xml_content = self.to_xml_string()
        
        # Utför validering
        return validate_complete_erms_document(
            xml_content, use_schematron, schematron_file)
    
    def save_with_validation(self, filename: str, validate_before_save: bool = True,
                           use_schematron: bool = False, schematron_file: str = None):
        """
        Spara ERMS-fil med optional validering.
        
        Args:
            filename: Filnamn att spara till
            validate_before_save: Om validering ska köras innan sparande
            use_schematron: Om Schematron-validering ska användas
            schematron_file: Sökväg till Schematron-fil
            
        Raises:
            ValidationError: Om validering misslyckas
        """
        if validate_before_save:
            validation_result = self.validate(use_schematron, schematron_file)
            if not validation_result['valid']:
                error_msg = f"Validering misslyckades:\n"
                for error in validation_result['errors']:
                    error_msg += f"- {error.get('message', str(error))}\n"
                raise ValueError(error_msg)
        
        # Spara filen
        self.save_to_file(filename)
    
    def get_statistics(self) -> dict:
        """
        Få statistik om ERMS-dokumentet.
        
        Returns:
            Dict med statistik
        """
        stats = {
            'cases': 0,
            'records': 0,
            'agents': 0,
            'dates': 0,
            'svk_extensions': 0
        }
        
        # Räkna genom XML-trädet
        for aggregation in self.element.findall('.//aggregation'):
            stats['cases'] += 1
            
            # Räkna records
            for record in aggregation.findall('.//record'):
                stats['records'] += 1
            
            # Räkna agents
            for agent in aggregation.findall('.//agent'):
                stats['agents'] += 1
            
            # Räkna dates
            for date in aggregation.findall('.//date'):
                stats['dates'] += 1
            
            # Räkna SVK-tillägg
            if aggregation.find('.//additionalXMLData') is not None:
                stats['svk_extensions'] += 1
        
        return stats
