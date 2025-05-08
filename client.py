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
