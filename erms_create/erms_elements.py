from lxml import etree
from erms_create import ns


class Dates:
	def __init__(self):
		self.element = etree.Element(ns.ERMS + "dates", nsmap=ns.ERMS_NSMAP)

	def add_date(self, date, type_of_date):
		date_types = [
			"appraisal", "archived", "archiving", "captured", "checked_in", "checked_out",
			"classification", "closed", "confidentiality_assessed", "created", "decision",
			"decision_date", "decision_deadline", "decrypted", "deleted", "destroyed",
			"dispatch", "encrypted", "end", "expedited", "expiration", "finished", "first_used",
			"last_addition", "last_addition_timestamp", "last_reviewed", "loan", "main_signature",
			"modified", "moved", "opened", "opening_date", "originated", "other_signature",
			"ownership_start", "prepared", "received", "received_at_location", "relocated",
			"rendered", "reviewed", "sent", "start", "take_back", "transferred",
		]
		if type_of_date in date_types:
			elm = etree.Element(ns.ERMS + "date", dateType=type_of_date, nsmap=ns.ERMS_NSMAP)
		else:
			elm = etree.Element(ns.ERMS + "date", dateType="other", otherDateType=type_of_date, nsmap=ns.ERMS_NSMAP)
		elm.text = date
		self.element.append(elm)


class Agent:
	agent_types = [
		"administrator", "agent", "archiver", "authorising_person", "borrower", "contact_person",
		"counterpart", "creator", "custodian", "deliverer", "dispatcher", "editor", "ipp_owner",
		"main_signatory", "mover", "opening_person", "other_signatory", "owner", "reader", "recipient",
		"receiver", "relocator", "responsible_person", "sender", "user", "other",
	]

	def __init__(self, agent_type: str, name: str, organisation: str=None, unit_name: str=None,
				 id_number: str=None, id_type: str=None, role:	str=None, protected_identity: str=None):
		self.element = etree.Element(ns.ERMS + "agent", agentType=agent_type, nsmap=ns.ERMS_NSMAP)
		self.name = etree.SubElement(self.element, ns.ERMS + "name", nsmap=ns.ERMS_NSMAP)
		self.name.text = name
		if organisation:
			self.organisation = etree.SubElement(self.element, ns.ERMS + "organisation", nsmap=ns.ERMS_NSMAP)
			self.organisation.text = organisation
		if unit_name:
			self.unit_name = etree.SubElement(self.element, ns.ERMS + "unitName", nsmap=ns.ERMS_NSMAP)
			self.unit_name.text = unit_name
		if id_number:
			if not id_type: id_type = "unknown"
			self.id_number = etree.SubElement(self.element, ns.ERMS + "idNumber", idNumberType=id_type, nsmap=ns.ERMS_NSMAP)
			self.id_number.text = id_number
		if role:
			self.role = etree.SubElement(self.element, ns.ERMS + "role", nsmap=ns.ERMS_NSMAP)
			self.role.text = role
		if protected_identity:
			self.protected_identity = etree.SubElement(self.element, ns.ERMS + "protectedIdentity", nsmap=ns.ERMS_NSMAP)
			self.protected_identity.text = "true"


class Agents:
	def __init__(self):
		self.element = etree.Element(ns.ERMS + "agents", nsmap=ns.ERMS_NSMAP)

	def add_agent(self, agent_type, name, **kwargs):
		new_agent = Agent(agent_type, name, **kwargs)
		self.element.append(new_agent.element)
