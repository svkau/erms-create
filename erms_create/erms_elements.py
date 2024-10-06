from xml.etree.ElementTree import tostring

from lxml import etree


class Dates:
	def __init__(self):
		self.dates = etree.Element("dates")

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
			elm = etree.Element("date", dateType=type_of_date)
		else:
			elm = etree.Element("date", dateType="other", otherDateType=type_of_date)
		elm.text = date
		self.dates.append(elm)


class Agent:
	agent_types = [
		"administrator", "agent", "archiver", "authorising_person", "borrower", "contact_person",
		"counterpart", "creator", "custodian", "deliverer", "dispatcher", "editor", "ipp_owner",
		"main_signatory", "mover", "opening_person", "other_signatory", "owner", "reader", "recipient",
		"receiver", "relocator", "responsible_person", "sender", "user", "other",
	]

	def __init__(self, agent_type: str, name: str, organisation: str=None, unit_name: str=None,
				 id_number: str=None, id_type: str=None, role:	str=None, protected_identity: str=None):
		self.agent = etree.Element("agent", agentType=agent_type)
		self.name = etree.SubElement(self.agent, "name")
		self.name.text = name
		if organisation:
			self.organisation = etree.SubElement(self.agent, "organisation")
			self.organisation.text = organisation
		if unit_name:
			self.unit_name = etree.SubElement(self.agent, "unitName")
			self.unit_name.text = unit_name
		if id_number:
			if not id_type: id_type = "unknown"
			self.id_number = etree.SubElement(self.agent, "idNumber", idNumberType=id_type)
			self.id_number.text = id_number
		if role:
			self.role = etree.SubElement(self.agent, "role")
			self.role.text = role
		if protected_identity:
			self.protected_identity = etree.SubElement(self.agent, "protectedIdentity")
			self.protected_identity.text = "true"


class Agents:
	def __init__(self):
		self.agents = etree.Element("agents")

	def add_agent(self, agent_type, name, **kwargs):
		new_agent = Agent(agent_type, name, **kwargs)
		self.agents.append(new_agent.agent)
