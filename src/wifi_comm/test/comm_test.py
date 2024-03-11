import socket

def comm():
	count = 0
	
	while True:
		client_socket, client_address = server_socket.accept()
		print ("connection from ", client_address)
		while True:
			data = client_socket.recv(1024)
			if not data:
				break
			
			decoded = data.decode()
			print(count, 'received :', decoded)
			send_data = "[Hi, I'm TH KIM. I got this Message.] => " + decoded
			encoded_send_data = send_data.encode('utf-8')
			sent = client_socket.send(encoded_send_data)
			
			if sent == 0:
				print("socket connection broken")
			print(sent)
		print("Disconnected")
		client_socket.close()
		count = count+1


if __name__ == "__main__":
	server_port = 8090
	max_users = 5 #maximum number of queued connections

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("0.0.0.0", server_port))
	server_socket.listen(max_users)

	print ("Waiting for client on port ",server_port)

	comm()
	
	server_socket.close()
