import socket
import json

class Subscriber:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port

    def _send_request(self, data):
        try:
            print(f"Connecting to server at {self.host}:{self.port}...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(json.dumps(data).encode())
                response = s.recv(1024).decode()
                print(f"Response received from server: {response}")
                return json.loads(response)
        except Exception as e:
            print(f"Error in communication with server: {e}")
            raise

    def registerSubscriber(self):
        request_data = {'action': 'registerSubscriber'}
        response = self._send_request(request_data)
        return response.get('sid')

    def subscribe(self, topic):
        request_data = {
            'action': 'subscribe',
            'sid': 1,  # Replace with actual subscriber ID if needed
            'topic': topic
        }
        response = self._send_request(request_data)
        return response.get('status')

    def pull(self, topic):
        request_data = {
            'action': 'pull',
            'sid': 1,  # Replace with actual subscriber ID if needed
            'topic': topic
        }
        response = self._send_request(request_data)
        return response.get('messages', [])
