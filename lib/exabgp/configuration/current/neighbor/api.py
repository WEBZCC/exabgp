# encoding: utf-8
"""
parse_process.py

Created by Thomas Mangin on 2015-06-05.
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""

from exabgp.configuration.current.core import Section
from exabgp.configuration.current.parser import boolean
from exabgp.configuration.current.neighbor.parser import processes

from exabgp.bgp.message import Message


class ParseAPI (Section):
	syntax = \
		'syntax:\n' \
		'process {\n' \
		'   processes [ name-of-processes ];\n' \
		'   neighbor-changes;\n' \
		'   send {\n' \
		'      parsed;\n' \
		'      packets;\n' \
		'      consolidate;\n' \
		'      open;\n' \
		'      update;\n' \
		'      notification;\n' \
		'      keepalive;\n' \
		'      refresh;\n' \
		'      operational;\n' \
		'   }\n' \
		'   receive {\n' \
		'      parsed;\n' \
		'      packets;\n' \
		'      consolidate;\n' \
		'      open;\n' \
		'      update;\n' \
		'      notification;\n' \
		'      keepalive;\n' \
		'      refresh;\n' \
		'      operational;\n' \
		'   }\n' \
		'}\n\n' \

	name = 'api'

	known = {
		'processes':        processes,
		'neighbor-changes': boolean,
	}

	action = {
		'processes':        'set',
		'neighbor-changes': 'set',
	}

	default = {
		'neighbor-changes': True,
	}

	DEFAULT_API = {
		'neighbor-changes': False
	}

	def __init__ (self, tokeniser, scope, error, logger):
		Section.__init__(self,tokeniser,scope,error,logger)

	def clear (self):
		pass

	def pre (self):
		self.scope.to_context()
		return True

	def post (self):
		self.scope.to_context(self.name)
		local = {
			'neighbor-changes':self.scope.get('neighbor-changes',False)
		}
		for way in ('send','receive'):
			data = self.scope.pop(way,{})
			for name in ('parsed','packets','consolidate'):
				local["%s-%s" % (way,name)] = data.get(name,False)
			for name in ('open', 'update', 'notification', 'keepalive', 'refresh', 'operational'):
				local["%s-%d" % (way,Message.code(name))] = data.get(name,False)
		for k,v in local.items():
			self.scope.set(k,v)
		return True


for way in ('send','receive'):
	for name in ('parsed','packets','consolidate'):
		ParseAPI.DEFAULT_API["%s-%s" % (way,name)] = False
	for name in ('open', 'update', 'notification', 'keepalive', 'refresh', 'operational'):
		ParseAPI.DEFAULT_API["%s-%d" % (way,Message.code(name))] = False


class _ParseDirection (Section):
	syntax = ParseAPI.syntax

	action = {
		'parsed':       'set',
		'packets':      'set',
		'consolidate':  'set',
		'open':         'set',
		'update':       'set',
		'notification': 'set',
		'keepalive':    'set',
		'refresh':      'set',
		'operational':  'set',
	}

	known = {
		'parsed':       boolean,
		'packets':      boolean,
		'consolidate':  boolean,
		'open':         boolean,
		'update':       boolean,
		'notification': boolean,
		'keepalive':    boolean,
		'refresh':      boolean,
		'operational':  boolean,
	}

	default = {
		'parsed':       True,
		'packets':      True,
		'consolidate':  True,
		'open':         True,
		'update':       True,
		'notification': True,
		'keepalive':    True,
		'refresh':      True,
		'operational':  True,
	}

	def __init__ (self, tokeniser, scope, error, logger):
		Section.__init__(self,tokeniser,scope,error,logger)

	def pre (self):
		self.scope.to_context()
		return True

	def post (self):
		return True


class ParseSend (_ParseDirection):
	name = 'api/send'


class ParseReceive (_ParseDirection):
	name = 'api/receive'


	# we want to have a socket for the cli
	# if self.fifo:
	# 	_cli_name = 'CLI'
	# 	configuration.processes[_cli_name] = {
	# 		'neighbor': '*',
	# 		'encoder': 'json',
	# 		'run': [sys.executable, sys.argv[0]],
	#
	# 		'neighbor-changes': False,
	#
	# 		'receive-consolidate': False,
	# 		'receive-packets': False,
	# 		'receive-parsed': False,
	#
	# 		'send-consolidate': False,
	# 		'send-packets': False,
	# 		'send-parsed': False,
	# 	}
	#
	# 	for receive in ['send','receive']:
	# 		for message in [
	# 			Message.CODE.NOTIFICATION,
	# 			Message.CODE.OPEN,
	# 			Message.CODE.KEEPALIVE,
	# 			Message.CODE.UPDATE,
	# 			Message.CODE.ROUTE_REFRESH,
	# 			Message.CODE.OPERATIONAL
	# 		]:
	# 			configuration.processes[_cli_name]['%s-%d' % (receive,message)] = False
	#
	# for name in configuration.processes.keys():
	# 	process = configuration.processes[name]
	#
	# 	neighbor.api.set('neighbor-changes',process.get('neighbor-changes',False))
	#
	# 	for receive in ['send','receive']:
	# 		for option in ['packets','consolidate','parsed']:
	# 			neighbor.api.set_value(receive,option,process.get('%s-%s' % (receive,option),False))
	#
	# 		for message in [
	# 			Message.CODE.NOTIFICATION,
	# 			Message.CODE.OPEN,
	# 			Message.CODE.KEEPALIVE,
	# 			Message.CODE.UPDATE,
	# 			Message.CODE.ROUTE_REFRESH,
	# 			Message.CODE.OPERATIONAL
	# 		]:
	# 			neighbor.api.set_message(receive,message,process.get('%s-%d' % (receive,message),False))

	# XXX: check that if we have any message, we have parsed/packets
	# XXX: and vice-versa
