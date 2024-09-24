import socket
import json

class Publisher:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.pid = self.registerPublisher()

    def _send_request(self, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(json.dumps(data).encode())
                response = s.recv(1024).decode()
                return json.loads(response)
        except Exception as e:
            print(f"Error in communication with server: {e}")
            return None

    def registerPublisher(self):
        request_data = {'action': 'registerPublisher'}
        response = self._send_request(request_data)
        if response:
            return response.get('pid')
        return None

    def createTopic(self, topic):
        request_data = {
            'action': 'createTopic',
            'pid': self.pid,
            'topic': topic
        }
        response = self._send_request(request_data)
        return response.get('status') if response else 'Error communicating with server'

    def deleteTopic(self, topic):
        request_data = {
            'action': 'deleteTopic',
            'pid': self.pid,  # Use the actual publisher ID
            'topic': topic
        }
        response = self._send_request(request_data)
        return response.get('status') if response else 'Error communicating with server'

    def send(self, topic, message):
        request_data = {
            'action': 'send',
            'pid': self.pid,  # Use the actual publisher ID
            'topic': topic,
            'message': message
        }
        response = self._send_request(request_data)
        return response.get('status') if response else 'Error communicating with server'
