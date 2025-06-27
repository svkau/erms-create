"""
SVK Ärendehandlingar Value Lists
===============================

Värdelistor specifika för Svenska kyrkans anpassning av ERMS för ärendehandlingar.
Baserat på ERMS-SVK-ARENDE-vardelistor.md version 1.0
"""

# Värdelista 1 - Typ av identifikator
IDENTIFICATION_TYPE = [
    "aid",  # ArkivbildarID
    "arkivbildare",  # Arkivbildarens namn
    "organisationsnummer",  # Tio siffror utan bindestreck
    "ärendenummer",  # Ärendets beteckning (t.ex. F 2020-0435)
]

# Värdelista 2 - Klassificeringsstruktur  
CLASSIFICATION_SCHEMA = [
    "KlaSL2016_1.0",  # Klassificeringsstruktur för lokal nivå 1.0
    "KlaSN2018_1.0",  # Klassificeringsstruktur för nationell nivå 1.0
    "KlaSS2016_1.0",  # Klassificeringsstruktur för regional nivå 1.0
]

# Värdelista 4 - Typ av ID
ID_TYPE = [
    "aid",  # ArkivbildarID
    "organisationsnummer",  # Tio siffror utan bindestreck
]

# Värdelista 6 - Typ av aktör (utökad från ERMS)
AGENT_TYPE_EXTENSIONS = [
    "closing_person",  # Den som avslutar eller färdigställer något
    "delegator",  # Person i vars ställe något utförs
]

# Värdelista 7 - Ärende- och handlingsstatus (begränsad från ERMS)
STATUS_SVK = [
    "closed",  # Avslutat/registrerad
    "obliterated",  # Makulerad
]

# Värdelista 8 - Typ av idNumber
ID_NUMBER_TYPE = [
    "username",  # Personens användarnamn i ärendehanteringssystemet
    "organisationsnummer",  # Tio siffror utan bindestreck
    "personnummer",  # Tolv siffror utan bindestreck
]

# Värdelista 9 - Initiativ
INITIATIVE = [
    "eget",
    "externt",
]

# Värdelista 10 - Typ av anteckning
NOTE_TYPE = [
    "arkivanteckning",
    "generell anteckning", 
    "intern anteckning",
    "expedieringsanteckning",
    "chattanteckning",
]

# Värdelista 11 - Tillämpningsområde
AUDIT_SCOPE = [
    "ankomstdatum",
    "ansvarig",
    "anteckning",
    "avsändare",
    "beskrivning",
    "beslut",
    "dokumentnummer",
    "dokumentreferens",
    "dokumentstatus",
    "dokumenttitel",
    "expedieringsdatum",
    "fastighet",
    "fil",
    "form",
    "handling",
    "initiativ",
    "klassificering",
    "kommentar",
    "medhandläggare",
    "mottagare",
    "nyckelord",
    "projekt",
    "riktning",
    "sekretess",
    "status",
    "ärende",
    "ärendemening",
    "ärendenummer",
    "ärendepart",
    "ärendereferens",
    "ärendestatus",
]

# Värdelista 12 - Åtgärd
AUDIT_ACTION = [
    "create",
    "read", 
    "update",
    "delete",
]

# Värdelista 13 - Handlingstyp
RECORD_TYPE_SVK = [
    "ärendedokument",
    "avtalsdokument",
    "personalaktsdokument",
    "projektdokument",
    "bild",
    "video",
    "fil",
]

# Värdelista 15 - Riktning (utökad från ERMS)
DIRECTION_SVK = [
    "incoming",  # Inkommen handling
    "outgoing",  # Handling som upprättats genom expediering
    "internal",  # Handling som upprättats på annat sätt
]

# Värdelista 16 - Avtalstyp
AGREEMENT_TYPE = [
    "avtal",
    "kontrakt",
    "licens",
    "uppgörelse",
    "överenskommelse",
]

# Värdelista 17 - Variant
FILE_VARIANT = [
    "display",  # Visningsformat
    "production",  # Produktionsformat
    "preservation",  # Arkivformat
    "public",  # Offentligt format
    "signed",  # Signerat format
]

# Värdelista 18 - Typ av objekt
OBJECT_TYPE = [
    "project",  # projekt
    "realEstate",  # fastighet/byggnad
]

# Värdelista 19 - Typ av arbetsflöde
WORKFLOW_TYPE = [
    "approval",
]

# Värdelista 20 - Arbetsflödes status
WORKFLOW_STATUS = [
    "approved",
    "canceled",
    "not_approved",
    "open",
]

# Värdelista 21 - Arbetsflödes prioritet
WORKFLOW_PRIORITY = [
    "high",
    "low",
    "standard",
]

# Värdelista 22 - Datum (utökad från ERMS för SVK-specifika behov)
DATE_TYPE_SVK = [
    "closed",
    "created",
    "decision_date",
    "end",
    "finished",
    "expedited",
    "modified",  # I betydelsen "senast ändrad"
    "opened",
    "originated",  # Se ERMS-SVK:112
    "received",
    "sent",
    "start",
]

# Kombinerade listor (ERMS + SVK tillägg)
ALL_AGENT_TYPES = [
    # Standard ERMS agent types
    "administrator", "agent", "archiver", "authorising_person", "borrower",
    "counterpart", "creator", "custodian", "deliverer", "dispatcher", "editor",
    "ipp_owner", "main_signatory", "mover", "opening_person", "other_signatory",
    "owner", "reader", "recipient", "receiver", "relocator", "responsible_person",
    "sender", "user", "other",
    # SVK extensions (används med otherAgentType)
] + AGENT_TYPE_EXTENSIONS

# Valideringsfunktioner
def validate_org_number(org_number: str) -> bool:
    """Validera att organisationsnummer har rätt format (10 siffror)"""
    return isinstance(org_number, str) and len(org_number) == 10 and org_number.isdigit()

def validate_person_number(person_number: str) -> bool:
    """Validera att personnummer har rätt format (12 siffror)"""
    return isinstance(person_number, str) and len(person_number) == 12 and person_number.isdigit()

def validate_case_number(case_number: str) -> bool:
    """Validera ärendenummer format: [diariekod] [årtal]-[löpnummer]"""
    import re
    pattern = r'^[A-Ö]+ \d{4}-\d{4}$'
    return bool(re.match(pattern, case_number))

def validate_document_number(doc_number: str) -> bool:
    """Validera dokumentnummer format: [ärendenummer]:[löpnummer]"""
    import re
    pattern = r'^[A-Ö]+ \d{4}-\d{4}:[1-9][0-9]*$'
    return bool(re.match(pattern, doc_number))
