import time
import random
import requests
from os.path import exists

# Settings
INTERVALS = [2, 3, 5, 8]
"""INTERVALS (list): list of ints representing a choice of seconds to wait between requests"""
FILTER = True
"""FILTER (boolean): whether to filter out destination files that already exists (without even making the request to download)"""
AFILE = 'agents.txt'
"""AFILE (string): filename containing default list of user agent choices"""

# Since you can't raise in a lambda
def _raise_value(msg):
	raise ValueError(msg)

# Interpret a file as a list of strings
def _load_file_as_list(filename):
	with open(filename, 'r') as strings_file:
		return [line.strip() for line in strings_file]

# This is a "switch statement" of behaviors for the agent setting
_agent_ldr_ = {
	'list': (lambda h: h['list'] if 'list' in h else _raise_value("'list' option required if list is used for agent")),
	'file': (lambda h: _load_file_as_list(h['file']) if 'agents-file' in h else _raise_value("'file' option required if file is used for agent")),
	'default': (lambda h: _load_file_as_list(AFILE)),
}

def download(pairs, **kwargs):
	"""Given a list of (source url, destination filename) pairs, download all of them
	
	Inputs:
		pairs:		List of (string, string) pairs representing source URL to be downloaded and destination filename to put it
		options:
			agent:	user-agent to claim in the header file
				None -		the default requests user-agent will be used
				list -	choose from the list of agents provided in list
				file - choose from the list of agents found in the file file
				default - 	equivalent to file with file = "agents.txt"
			filter:		whether to filter out existing files (default true)
			intervals:	list of numbers of seconds from which to sample wait times between requests (default [2, 3, 5, 8])
			headers:	map of headers to use in the requests (default {})
	Output:
		None
	"""
	headers = {}
	settings = {}
	
	# Apply settings
	if 'agent' in kwargs:
		# Options are 'list', 'file', and 'default' (equivalent to 'file' with 'file' equal to 'agents.txt')
		# 'list' requires 'list' argument
		# 'file' requires 'file' argument
		settings['agents'] = _agent_ldr_.get(kwargs['agent'], (lambda h: _raise_value("'%s' not a valid value for 'agent'" % h['agent'])))(kwargs)
	settings['filter'] = kwargs.get('filter', FILTER)
	settings['intervals'] = kwargs.get('intervals', INTERVALS)
	headers = kwargs.get('headers', {})
	
	# Download each URL in the list
	for url, filename in pairs:
		# If filter is True, do not download if the file is already written
		if settings['filter'] and not exists(filename):
			# Break out once we download
			while True:
				# Choose a random user agent to represent ourselves
				if 'agents' in settings:
					headers['user-agent'] = random.choice(settings['agents'])
				try:
					# Wait a random amount of time to avoid a regular request profile (i.e. requested URLs are likely to be served by the same server)
					time.sleep(random.choice(settings['intervals']))
					
					# Get that bread!
					response = requests.get(url, headers=headers)
					
					# Write it out to a file
					with open(filename, "w") as text_file:
						print(response.text, file=text_file)
					break
				except:
					# This is not suited to general exceptions in the above (e.g. file write exception would cause an unnecessary loop)
					print('Unexpected error:', sys.exc_info()[0])