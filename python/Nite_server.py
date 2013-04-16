# Echo server program
import socket
import random
import json



HOST = '' #'localhost'	# Symbolic name meaning all available interfaces
PORT = 33000		# Arbitrary non-privileged port

def createUser(id):
	x = random.uniform(0.0, 1.0)
	y = random.uniform(0.0, 1.0)
	dist = random.uniform(0.0, 14.0)
	cmd = '{\"id\":'
	cmd += str(id)
	cmd += ',\"x\":'
	cmd += str(x)
	cmd += ',\"y\":'
	cmd += str(y)
	cmd += ',\"dist\":'
	cmd += str(dist)
	cmd += '}'
	return cmd

if __name__ == '__main__':

	print 'Try to connect to ' + HOST + ':' + str(PORT)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)

	shutdown = 0

	while not shutdown:

		conn, addr = s.accept()
		print 'Connected by', addr

		while 1:

			data = conn.recv(1024)
			cmd = ''

			if not data:
				break

			try:
				d = json.loads( data );	# create a dict from json string
			except:
				continue;

			if 'cmd' in d:
				c = d['cmd']
				if c == 'nbuser':
					nbUser = str(random.randint(0, 5))
					cmd = '{\"nbuser\":'+nbUser+'}'
					conn.sendall(cmd)

				elif c == 'users':
					cmd = '{\"users\":['
					cmd += createUser(1)
					cmd += ','
					if(random.randint(0, 2)):
						cmd += createUser(2)
						cmd += ','
					if(random.randint(0, 2)):
						cmd += createUser(4)
						cmd += ','
						cmd += createUser(3)
					cmd += ']}'
					conn.sendall(cmd)
				elif c == 'srv_shutdown':
					cmd = '{\"srv_shutdown\":true}'
					conn.sendall(cmd)
					shutdown = 1
					break
				elif c == 'disconnect': 
					cmd = '{\"disconnect\":true}'
					conn.sendall(cmd)
					break
			else:
				cmd = '{\"error\":\"cmd_not_found\"}'
				conn.sendall(cmd)

		conn.close()
		print ' CONNECTION CLOSED ';
