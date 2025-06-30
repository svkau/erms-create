"""
SVK Record (Handling)
====================

Utökad version av ERMS Record med SVK-specifika funktioner.
"""

from lxml import etree
from ..core.record import Record              # Ändrat från erms_core till core
from ..core.utils import add_in_element       # Ändrat från erms_core till core
from ..core import namespaces as ns          # Ändrat från erms_core till core
from .svk_extensions import SVKExtensions
from .validation import SVKValidator
from . import value_lists


class SVKRecord(Record):
    """
    Svenska kyrkans utökade handling.
    Bygger på standard ERMS Record och lägger till SVK-funktionalitet.
    """

    def __init__(self, record_type: str = "ärendedokument", physical_or_digital: str = "digital"):
        # Validera SVK-specifika värden
        if record_type and record_type not in value_lists.RECORD_TYPE_SVK:
            raise ValueError(f"Invalid SVK record type: {record_type}")

        # Initiera som standard ERMS Record
        super().__init__(record_type, physical_or_digital)

        # SVK-specifik validering
        self.validator = SVKValidator()

        # SVK-tillägg (placeras i additionalXMLData)
        self.svk_extensions = None

        # SVK-specifika element
        self.direction = None

    def set_document_number(self, document_number: str):
        """
        Sätt dokumentnummer med SVK-validering.
        Format: [ärendenummer]:[löpnummer]
        """
        if not self.validator.validate_document_number(document_number):
            raise ValueError(f"Ogiltigt dokumentnummer: {document_number}")

        self.set_object_id(document_number)

    def set_status_svk(self, status: str):
        """Sätt status med SVK-validering (endast closed/obliterated)"""
        if not self.validator.validate_case_status(status):
            raise ValueError(f"Ogiltig status för SVK: {status}")

        self.set_status(status)

    def set_direction(self, direction: str, other_direction: str = None):
        """
        Sätt riktning för handlingen.

        Args:
            direction: "incoming", "outgoing", eller "other"
            other_direction: Krävs om direction är "other" (ska vara "internal")
        """
        if not self.validator.validate_direction(direction, other_direction):
            raise ValueError(f"Ogiltig riktning: {direction}")

        attributes = {"directionDefinition": direction}
        if other_direction:
            attributes["otherDirectionDefinition"] = other_direction

        self.direction = etree.Element(ns.ERMS + "direction", attributes, nsmap=ns.ERMS_NSMAP)
        add_in_element(self.element, self.direction)

    def add_required_dates(self, created_date: str, originated_date: str,
                          received_date: str = None, expedited_date: str = None):
        """
        Lägg till obligatoriska datum enligt SVK-krav.

        Args:
            created_date: När handlingen skapades i systemet
            originated_date: När handlingen registrerades (diariefördes)
            received_date: Ankomstdatum (för inkommande)
            expedited_date: Expedieringsdatum (för utgående)
        """
        self.add_date(created_date, "created")
        self.add_date(originated_date, "originated")

        if received_date:
            self.add_date(received_date, "received")
        if expedited_date:
            self.add_date(expedited_date, "expedited")

    def add_document_agents(self, creator: str = None, responsible_person: str = None,
                          sender: str = None, receiver: str = None):
        """
        Lägg till aktörer för handlingen enligt SVK-mönster.

        Args:
            creator: Den som skapade handlingen
            responsible_person: Ansvarig för handlingen
            sender: Avsändare (för inkommande handlingar)
            receiver: Mottagare (för utgående handlingar)
        """
        if creator:
            self.add_agent("creator", creator)

        if responsible_person:
            self.add_agent("responsible_person", responsible_person)

        if sender:
            self.add_agent("sender", sender)

        if receiver:
            self.add_agent("receiver", receiver)

    def get_svk_extensions(self) -> SVKExtensions:
        """Hämta eller skapa SVK-tillägg för handlingen"""
        if self.svk_extensions is None:
            self.svk_extensions = SVKExtensions("record")

            # Skapa additionalInformation om det inte finns
            if not hasattr(self, 'additional_information') or self.additional_information is None:
                self.additional_information = etree.Element(ns.ERMS + "additionalInformation", nsmap=ns.ERMS_NSMAP)
                add_in_element(self.element, self.additional_information)

            # Skapa additionalXMLData
            additional_xml = etree.SubElement(self.additional_information, ns.ERMS + "additionalXMLData", nsmap=ns.ERMS_NSMAP)
            additional_xml.append(self.svk_extensions.root_element)

        return self.svk_extensions

    def add_svk_note(self, note_type: str, note_text: str, creator_name: str,
                     created_date: str, creator_org: str = None):
        """Lägg till SVK-anteckning"""
        extensions = self.get_svk_extensions()
        svk_notes = extensions.get_svk_notes()
        svk_notes.add_note(note_type, note_text, creator_name, created_date, creator_org)

    def add_contract_info(self, agreement_type: str, external_ref: str = None,
                         call_off_value: int = None, contract_value: int = None,
                         start_date: str = None, end_date: str = None):
        """Lägg till avtalsinformation (för avtalsdokument)"""
        extensions = self.get_svk_extensions()
        contract_info = extensions.get_contract_info()

        contract_info.set_agreement_type(agreement_type)

        if external_ref:
            contract_info.set_external_reference(external_ref)
        if call_off_value:
            contract_info.set_call_off_value(call_off_value)
        if contract_value:
            contract_info.set_contract_value(contract_value)
        if start_date:
            contract_info.add_date(start_date, "start")
        if end_date:
            contract_info.add_date(end_date, "end")

    def add_svk_appendix(self, name: str, path: str, file_format: str,
                        description: str = None, version_number: int = None,
                        variant: str = "preservation"):
        """
        Lägg till bifogad fil enligt SVK-struktur.

        Args:
            name: Filnamn
            path: Relativ sökväg i arkivpaketet
            file_format: Filformat (utan punkt)
            description: Beskrivning av filen
            version_number: Versionsnummer
            variant: Variant (preservation, production, etc.)
        """
        extensions = self.get_svk_extensions()

        # Skapa SVK appendix struktur
        # Detta är förenklat - den riktiga implementationen skulle vara mer komplex
        appendix_elm = etree.SubElement(extensions.element, "svkAppendix")

        # Grundläggande appendix-info
        appendix_attrs = {
            "name": name,
            "path": path,
            "fileFormat": file_format
        }
        if description:
            appendix_attrs["description"] = description

        appendix = etree.SubElement(appendix_elm, "appendix", appendix_attrs)

        # Filinformation
        if version_number or variant:
            file_info = etree.SubElement(appendix_elm, "fileInfo")
            if version_number:
                version_elm = etree.SubElement(file_info, "versionNumber")
                version_elm.text = str(version_number)
            if variant:
                variant_elm = etree.SubElement(file_info, "variant")
                variant_elm.text = variant

    def validate(self) -> dict:
        """
        Validera handlingen enligt SVK-regler.

        Returns:
            Dict med valideringsresultat
        """
        # Samla data för validering
        record_data = {
            'document_number': self.object_id.text if self.object_id is not None else None,
            'record_type': self.element.get('recordType'),
            'status': self.status.get('value') if self.status is not None else None,
            'direction': self.direction.get('directionDefinition') if self.direction is not None else None,
            # TODO: Lägg till fler fält för validering
        }

        self.validator.validate_record_data(record_data)
        return self.validator.get_validation_report()