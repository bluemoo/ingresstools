import requests
import json
import time
from actionlog import log_lines
class IngressChatMirror():
	def __init__(self):
		self.loglines = log_lines()

	def linechunkgen(self):
		for line in self.loglines:
			if line:
				yield line
			else:
				break

	def broadcastgen(self):
		actions = (json.loads(line) for line in self.linechunkgen())
		plexts = (action[2]['plext'] for action in actions)
		broadcasts = (plext for plext in plexts if plext["plextType"] == "SYSTEM_BROADCAST")
		return broadcasts

	def attackgen(self):
		broadcasts = self.broadcastgen()
		attack_messages = (broadcast for broadcast in broadcasts if is_attack_message(broadcast["markup"][1][1]['plain']))
		unique_pairs = set()
		for message in attack_messages:
			is_resistance = message['markup'][0][1]['team'] == 'RESISTANCE'
			player_name = message['markup'][0][1]['plain']
			portal_name = find_portal_name(message['markup'])
			unique_pairs.update([(is_resistance, player_name, portal_name)])

		return [AttackMessage(is_resistance, player_name, portal_name) for is_resistance, player_name, portal_name in unique_pairs]

def find_portal_name(markup):
	for element in markup:
		if element[0] == u'PORTAL':
			return element[1]['plain']
		
def is_attack_message(message):
	return 'destroyed' in message

class AttackMessage():
	def __init__(self, is_resistance, player_name, portal_name):
		self.is_resistance = is_resistance
		self.player_name = player_name
		self.portal_name = portal_name
	
	def __str__(self):
		prefix = 'RES: ' if self.is_resistance else 'ENL: '
		return prefix + self.player_name + ' attacked ' + self.portal_name

#mirror = IngressChatMirror()
#for attack in mirror.attackgen():
#	print unicode(attack)
	
	
	
	
	
	
	
	
	