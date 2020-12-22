#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 9876

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		message = input("Send: ")
		byte_message = str.encode(message)
		s.sendall(byte_message)
		s.close()
