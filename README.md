# COMPX234-A3
COMPX234-A3
# Server code for tuple space
import socket
import threading
from threading import Lock

class TupleSpace:
    def __init__(self):
        self.data = {}      # Store key-value pairs
        self.lock = Lock()  # Thread lock for synchronization

    def put(self, key, value):
        with self.lock:
            if key in self.data:
                return "ERR exists"    # Key already exists
            self.data[key] = value
            return "OK added"          # Successfully added

    def read(self, key):
        with self.lock:
            if key not in self.data:
                return "ERR not exist" # Key does not exist
            return f"OK {self.data[key]}"  # Return value

    def get(self, key):
        with self.lock:
            if key not in self.data:
                return "ERR not exist"
            value = self.data.pop(key)  # Remove and return value
            return f"OK {value}"

def handle_client(conn, addr, space):
    print(f"Client connected: {addr}")
    try:
        while True:
            msg = conn.recv(1024).decode().strip()
            if not msg:
                break
            parts = msg.split()
            if len(parts) < 3:
                res = "ERR format"  # Invalid message format
            else:
                cmd = parts[1]      # Operation: P (PUT), R (READ), G (GET)
                key = parts[2]
                if cmd == 'P' and len(parts) >= 4:
                    value = ' '.join(parts[3:])
                    res = space.put(key, value)
                elif cmd == 'R':
                    res = space.read(key)
                elif cmd == 'G':
                    res = space.get(key)
                else:
                    res = "ERR unknown"  # Unknown command
            conn.send(res.encode())  # Send response to client
    finally:
        conn.close()  # Close connection

def start_server(port=51234):
    space = TupleSpace()
    with socket.socket() as s:
        s.bind(('localhost', port))
        s.listen()
        print(f"Server started on port {port}")
        while True:
            conn, addr = s.accept()  # Accept new connection
            # Start a new thread for the client
            threading.Thread(target=handle_client, args=(conn, addr, space)).start()

if __name__ == "__main__":
    start_server()
# Client code to send requests to server
import socket
import sys

def run_client(host, port, file_path):
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 2:
                    print(f"Invalid line: {line}")
                    continue
                op = parts[0]  # Operation: PUT, READ, GET
                key = parts[1]
                # Build request message
                if op == 'PUT' and len(parts) >= 3:
                    value = ' '.join(parts[2:])
                    # Calculate message length (format: NNN P key value)
                    req = f"{len(line)+4:03d} P {key} {value}"
                elif op in ('READ', 'GET'):
                    req = f"{len(line)+4:03d} {op[0]} {key}"
                else:
                    print(f"Invalid operation: {line}")
                    continue
                # Send request to server
                with socket.socket() as s:
                    s.connect((host, port))
                    s.send(req.encode())
                    res = s.recv(1024).decode()
                    print(f"{line}: {res}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <request_file>")
        sys.exit()
    run_client(sys.argv[1], int(sys.argv[2]), sys.argv[3])
