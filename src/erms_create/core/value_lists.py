"""
Standard ERMS Value Lists
========================

These are the official value lists from the ERMS specification.
Do not modify these - they are part of the international standard.
"""

# Aggregation types
AGGREGATION_TYPE = [
    "caseFile",
    "class",
    "component",
    "file", 
    "subfile",
    "volume",
    "own_aggregation_definition",
]

# Record physical or digital status
RECORD_PHYSICAL_OR_DIGITAL = [
    "physical",
    "digital", 
    "physical_and_digital",
    "does_not_apply",
]

# Date types
DATE_TYPE = [
    "aggregated",
    "appraisal",
    "archived", 
    "archiving",
    "captured",
    "checked_in",
    "checked_out",
    "classification",
    "closed",
    "confidentiality_assessed",
    "created",
    "decision",
    "decision_date",
    "decision_deadline", 
    "decrypted",
    "deleted",
    "destroyed",
    "dispatch",
    "encrypted",
    "end",
    "expedited",
    "expiration",
    "finished",
    "first_used",
    "last_addition",
    "last_addition_timestamp",
    "last_reviewed",
    "loan",
    "main_signature",
    "modified",
    "moved",
    "opened",
    "opening_date",
    "originated", 
    "other_signature",
    "ownership_start",
    "prepared",
    "received",
    "received_at_location",
    "relocated",
    "rendered",
    "reviewed",
    "sent",
    "start",
    "take_back",
    "transferred",
    "other",
]

# Agent types  
AGENT_TYPE = [
    "administrator",
    "agent",
    "archiver",
    "authorising_person",
    "borrower",
    "counterpart", 
    "creator",
    "custodian",
    "deliverer",
    "dispatcher",
    "editor",
    "ipp_owner",
    "main_signatory",
    "mover",
    "opening_person",
    "other_signatory",
    "owner",
    "reader",
    "recipient",
    "receiver",
    "relocator",
    "responsible_person",
    "sender",
    "user",
    "other",
]

# Maintenance status
MAINTENANCE_STATUS = [
    "cancelled",
    "created", 
    "deleted",
    "derived",
    "new",
    "revised",
    "unknown",
    "updated",
]

# Event types
EVENT_TYPE = [
    "created",
    "revised",
    "deleted",
    "cancelled", 
    "derived",
    "updated",
    "unknown",
]

# Relation types
RELATION_TYPE = [
    "replaces",
    "is_replaced_with",
    "reference",
    "referenced_by",
    "demands",
    "needed_by",
    "contains",
    "part_of",
    "other_format_version",
    "another_format_version_of",
    "has_version", 
    "is_version_of",
    "is_redacted_version_of",
    "has_redacted_version",
    "rendition_version_of",
    "has_rendition_version",
    "is_child_of",
    "is_parent_of",
    "moved",
    "moved_from",
    "deleted",
    "own_relation_definition",
]

# Status values
STATUS = [
    "ad_acta",
    "closed",
    "expedited",
    "initiated", 
    "in_progress",
    "obliterated",
    "on_hold",
    "open",
    "prepared",
    "received",
]

# Direction types
DIRECTION_TYPE = [
    "incoming",
    "outgoing",
    "internal_memo_for_follow-up",
    "internal_memo_without_follow-up", 
    "case_draft",
    "other",
]

# Restriction types
RESTRICTION_TYPE = [
    "confidential",
    "gdpr",
    "integrity", 
    "other_type",
]

# Address types
ADDRESS_TYPE = [
    "postal_address",
    "postal_code",
    "postal_city",
    "post_box",
    "municipality_code",
    "municipality",
    "parish",
    "parish_code",
    "province",
    "county",
    "country",
    "other",
]

# Contact types  
CONTACT_TYPE = [
    "phonenumber",
    "mobilenumber",
    "fax",
    "email",
    "homepage",
    "other",
]

# Disposal date types
DISPOSAL_DATE_TYPE = [
    "action_due",
    "applied",
    "confirmation_due",
    "disposal_date",
    "lifted",
    "overdue_alert",
    "retention_period_start",
    "retention_period_end",
    "other_date",
]
