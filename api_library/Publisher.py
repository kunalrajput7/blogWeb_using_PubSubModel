import socket
import json

class Publisher:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port

    def _send_request(self, data):
        try:
            # Create a socket connection
            print(f"Connecting to server at {self.host}:{self.port}...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                # Send the request
                s.sendall(json.dumps(data).encode())
                # Receive the response
                response = s.recv(1024).decode()
                print(f"Response received from server: {response}")
                return json.loads(response)
        except Exception as e:
            print(f"Error in communication with server: {e}")
            raise

    def registerPublisher(self):
        request_data = {'action': 'registerPublisher'}
        response = self._send_request(request_data)
        return response.get('pid')

    def createTopic(self, topic):
        request_data = {
            'action': 'createTopic',
            'pid': 1,  # Replace with actual publisher ID if needed
            'topic': topic
        }
        response = self._send_request(request_data)
        return response.get('status')
    
    def deleteTopic(self, topic):
        request_data = {
            'action': 'deleteTopic',
            'pid': 1,  # Replace with actual publisher ID if needed
            'topic': topic
        }
        response = self._send_request(request_data)
        return response.get('status')

    def send(self, topic, message):
        request_data = {
            'action': 'send',
            'pid': 1,  # Replace with actual publisher ID if needed
            'topic': topic,
            'message': message
        }
        response = self._send_request(request_data)
        return response.get('status')
