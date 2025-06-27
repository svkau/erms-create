"""
Validation for SVK Ärendehandlingar
===================================

Validering enligt SvKGS-Ärendehandlingar specifikationen och Schematron-regler.
"""

import re
from typing import List, Dict, Any, Optional
from lxml import etree
from . import value_lists


class ValidationError(Exception):
    """Fel vid validering av ERMS SVK data"""
    pass


class SVKValidator:
    """Validator för Svenska kyrkans ERMS-anpassning"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def reset(self):
        """Nollställ fel- och varningslistor"""
        self.errors = []
        self.warnings = []
    
    def validate_case_number(self, case_number: str) -> bool:
        """
        Validera ärendenummer format: [diariekod] [årtal]-[löpnummer]
        Löpnumret ska bestå av fyra siffror och fyllas vid behov ut med nollor
        """
        if not value_lists.validate_case_number(case_number):
            self.errors.append(
                f"Ärendenummer '{case_number}' har felaktigt format. "
                f"Ska vara: [diariekod] [årtal]-[löpnummer] (t.ex. 'F 2019-0032')"
            )
            return False
        return True
    
    def validate_document_number(self, doc_number: str) -> bool:
        """
        Validera dokumentnummer format: [ärendenummer]:[löpnummer]
        """
        if not value_lists.validate_document_number(doc_number):
            self.errors.append(
                f"Dokumentnummer '{doc_number}' har felaktigt format. "
                f"Ska vara: [ärendenummer]:[löpnummer] (t.ex. 'F 2019-0032:1')"
            )
            return False
        return True
    
    def validate_org_number(self, org_number: str) -> bool:
        """Validera organisationsnummer (10 siffror utan bindestreck)"""
        if not value_lists.validate_org_number(org_number):
            self.errors.append(
                f"Organisationsnummer '{org_number}' måste vara 10 siffror utan bindestreck"
            )
            return False
        return True
    
    def validate_person_number(self, person_number: str) -> bool:
        """Validera personnummer (12 siffror utan bindestreck)"""
        if not value_lists.validate_person_number(person_number):
            self.errors.append(
                f"Personnummer '{person_number}' måste vara 12 siffror utan bindestreck"
            )
            return False
        return True
    
    def validate_identification_types(self, identifications: List[Dict[str, str]]) -> bool:
        """
        Validera att rätt identifikationstyper finns enligt ERMS-SVK:1-2
        Krävs: arkivbildare, ärendenummer, och antingen organisationsnummer eller aid
        """
        found_types = {id_info.get('type', '') for id_info in identifications}
        
        # Kontrollera obligatoriska typer
        required = {'arkivbildare', 'ärendenummer'}
        missing_required = required - found_types
        if missing_required:
            self.errors.append(
                f"Saknade obligatoriska identifikationstyper: {', '.join(missing_required)}"
            )
        
        # Kontrollera att minst en av org.nummer eller aid finns
        if 'organisationsnummer' not in found_types and 'aid' not in found_types:
            self.errors.append(
                "Måste ha antingen 'organisationsnummer' eller 'aid' som identifikationstyp"
            )
        
        # Validera organisationsnummer format om det finns
        for id_info in identifications:
            if id_info.get('type') == 'organisationsnummer':
                self.validate_org_number(id_info.get('value', ''))
        
        return len(self.errors) == 0
    
    def validate_classification_schema(self, schema: str) -> bool:
        """Validera klassificeringsstruktur enligt värdelista 2"""
        if schema not in value_lists.CLASSIFICATION_SCHEMA:
            self.errors.append(
                f"Klassificeringsstruktur '{schema}' är inte giltig. "
                f"Giltiga värden: {', '.join(value_lists.CLASSIFICATION_SCHEMA)}"
            )
            return False
        return True
    
    def validate_case_status(self, status: str) -> bool:
        """Validera ärendestatus enligt SVK-begränsning"""
        if status not in value_lists.STATUS_SVK:
            self.errors.append(
                f"Ärendestatus '{status}' är inte giltig. "
                f"Giltiga värden för SVK: {', '.join(value_lists.STATUS_SVK)}"
            )
            return False
        return True
    
    def validate_record_type(self, record_type: str) -> bool:
        """Validera handlingstyp enligt SVK värdelista"""
        if record_type not in value_lists.RECORD_TYPE_SVK:
            self.errors.append(
                f"Handlingstyp '{record_type}' är inte giltig. "
                f"Giltiga värden: {', '.join(value_lists.RECORD_TYPE_SVK)}"
            )
            return False
        return True
    
    def validate_direction(self, direction: str, other_direction: str = None) -> bool:
        """Validera riktning för handling"""
        if direction == "other":
            if other_direction != "internal":
                self.errors.append(
                    "Om riktning är 'other' måste otherDirectionDefinition vara 'internal'"
                )
                return False
        elif direction not in ['incoming', 'outgoing']:
            self.errors.append(
                f"Riktning '{direction}' är inte giltig. "
                f"Giltiga värden: incoming, outgoing, other"
            )
            return False
        return True
    
    def validate_agents_for_direction(self, direction: str, agents: List[Dict[str, Any]]) -> bool:
        """Validera att rätt aktörer finns för given riktning"""
        agent_types = {agent.get('type', '') for agent in agents}
        
        if direction == "incoming":
            if 'sender' not in agent_types:
                self.errors.append("Inkommande handling måste ha avsändare (sender)")
                return False
        elif direction == "outgoing":
            if 'receiver' not in agent_types:
                self.errors.append("Utgående handling måste ha mottagare (receiver)")
                return False
        
        return True
    
    def validate_dates_for_case(self, dates: List[Dict[str, str]]) -> bool:
        """Validera datum för ärende enligt ERMS-SVK:49-51"""
        date_types = {date.get('type', '') for date in dates}
        
        # Kontrollera obligatoriska datum
        if 'opened' not in date_types:
            self.errors.append("Datum för 'opened' är obligatoriskt för ärenden")
        if 'closed' not in date_types:
            self.errors.append("Datum för 'closed' är obligatoriskt för ärenden")
        
        # Kontrollera att 'created' inte förekommer mer än en gång
        created_count = sum(1 for date in dates if date.get('type') == 'created')
        if created_count > 1:
            self.errors.append("Datum av typen 'created' får bara finnas en gång")
        
        return len(self.errors) == 0
    
    def validate_dates_for_record(self, dates: List[Dict[str, str]]) -> bool:
        """Validera datum för handling enligt ERMS-SVK:110-114"""
        date_types = {date.get('type', '') for date in dates}
        
        # Kontrollera obligatoriska datum
        if 'created' not in date_types:
            self.errors.append("Datum för 'created' är obligatoriskt för handlingar")
        if 'originated' not in date_types:
            self.errors.append("Datum för 'originated' är obligatoriskt för handlingar")
        
        # Kontrollera att varje typ bara förekommer en gång
        for date_type in ['created', 'originated', 'received', 'expedited']:
            count = sum(1 for date in dates if date.get('type') == date_type)
            if count > 1:
                self.errors.append(f"Datum av typen '{date_type}' får bara finnas en gång")
        
        return len(self.errors) == 0
    
    def validate_case_data(self, case_data: Dict[str, Any]) -> bool:
        """Komplett validering av ärendedata"""
        self.reset()
        
        # Validera ärendenummer
        if 'case_number' in case_data:
            self.validate_case_number(case_data['case_number'])
        
        # Validera identifikationer
        if 'identifications' in case_data:
            self.validate_identification_types(case_data['identifications'])
        
        # Validera klassificeringsstruktur
        if 'classification_schema' in case_data:
            self.validate_classification_schema(case_data['classification_schema'])
        
        # Validera status
        if 'status' in case_data:
            self.validate_case_status(case_data['status'])
        
        # Validera datum
        if 'dates' in case_data:
            self.validate_dates_for_case(case_data['dates'])
        
        return len(self.errors) == 0
    
    def validate_record_data(self, record_data: Dict[str, Any]) -> bool:
        """Komplett validering av handlingsdata"""
        self.reset()
        
        # Validera dokumentnummer
        if 'document_number' in record_data:
            self.validate_document_number(record_data['document_number'])
        
        # Validera handlingstyp
        if 'record_type' in record_data:
            self.validate_record_type(record_data['record_type'])
        
        # Validera status
        if 'status' in record_data:
            self.validate_case_status(record_data['status'])  # Samma som för ärenden
        
        # Validera riktning
        direction = record_data.get('direction')
        other_direction = record_data.get('other_direction')
        if direction:
            self.validate_direction(direction, other_direction)
            
            # Validera aktörer för riktningen
            if 'agents' in record_data:
                self.validate_agents_for_direction(direction, record_data['agents'])
        
        # Validera datum
        if 'dates' in record_data:
            self.validate_dates_for_record(record_data['dates'])
        
        return len(self.errors) == 0
    
    def get_validation_report(self) -> Dict[str, Any]:
        """Få en rapport över valideringsresultat"""
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors.copy(),
            'warnings': self.warnings.copy(),
            'error_count': len(self.errors),
            'warning_count': len(self.warnings)
        }


class SchematronValidator:
    """
    Validator som använder Schematron-regler från ERMS-SVK-ARENDE.sch
    För framtida implementation med lxml.isoschematron
    """
    
    def __init__(self, schematron_file: Optional[str] = None):
        self.schematron_file = schematron_file
        self.schematron = None
        
    def load_schematron(self, schematron_file: str):
        """Ladda Schematron-regler från fil"""
        try:
            from lxml import isoschematron
            with open(schematron_file, 'r', encoding='utf-8') as f:
                schematron_doc = etree.parse(f)
            self.schematron = isoschematron.Schematron(schematron_doc)
            return True
        except ImportError:
            raise ValidationError("lxml.isoschematron krävs för Schematron-validering")
        except Exception as e:
            raise ValidationError(f"Kunde inte ladda Schematron-fil: {e}")
    
    def validate_xml(self, xml_content: str) -> Dict[str, Any]:
        """Validera XML mot Schematron-regler"""
        if not self.schematron:
            raise ValidationError("Schematron-regler inte laddade")
        
        try:
            xml_doc = etree.fromstring(xml_content.encode('utf-8'))
            is_valid = self.schematron.validate(xml_doc)
            
            errors = []
            if not is_valid:
                for error in self.schematron.error_log:
                    errors.append({
                        'line': error.line,
                        'message': error.message,
                        'path': error.path
                    })
            
            return {
                'valid': is_valid,
                'errors': errors,
                'error_count': len(errors)
            }
            
        except etree.XMLSyntaxError as e:
            return {
                'valid': False,
                'errors': [{'message': f"XML syntax error: {e}"}],
                'error_count': 1
            }


def validate_complete_erms_document(xml_content: str, 
                                  use_schematron: bool = False,
                                  schematron_file: str = None) -> Dict[str, Any]:
    """
    Komplett validering av ett ERMS-dokument.
    
    Args:
        xml_content: XML-innehållet som sträng
        use_schematron: Om Schematron-validering ska användas
        schematron_file: Sökväg till Schematron-fil
        
    Returns:
        Dict med valideringsresultat
    """
    results = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'schematron_results': None
    }
    
    try:
        # Grundläggande XML-validering
        xml_doc = etree.fromstring(xml_content.encode('utf-8'))
        
        # TODO: Implementera mer detaljerad validering av XML-strukturen
        # Detta skulle kunna inkludera:
        # - XSD-validering mot ERMS_v3.xsd och ERMS-SVK-ARENDE.xsd
        # - Kontroll av namespace-deklarationer
        # - Validering av element-ordning
        
        # Schematron-validering om efterfrågad
        if use_schematron and schematron_file:
            try:
                schematron_validator = SchematronValidator()
                schematron_validator.load_schematron(schematron_file)
                results['schematron_results'] = schematron_validator.validate_xml(xml_content)
                
                if not results['schematron_results']['valid']:
                    results['valid'] = False
                    results['errors'].extend(results['schematron_results']['errors'])
                    
            except Exception as e:
                results['warnings'].append(f"Schematron-validering misslyckades: {e}")
        
    except etree.XMLSyntaxError as e:
        results['valid'] = False
        results['errors'].append({'message': f"XML syntax error: {e}"})
    
    return results