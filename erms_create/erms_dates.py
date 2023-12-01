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
