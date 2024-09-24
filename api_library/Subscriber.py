import socket
import json

class Subscriber:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.sid = None

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
        self.sid = response.get('sid')
        print(f"Subscriber registered with SID: {self.sid}")
        return self.sid

    def subscribe(self, topic):
        if not self.sid:
            raise Exception("Subscriber not registered. Call registerSubscriber first.")

        request_data = {
        'action': 'subscribe',
        'sid': self.sid,
        'topic': topic
    }
        response = self._send_request(request_data)
        # Check the response for the subscription status
        if response:
            return response.get('status', 'Subscription failed')
        return response.get('status')

    def pull(self, topic):
        if not self.sid:
            raise Exception("Subscriber not registered. Call registerSubscriber first.")

        request_data = {
            'action': 'pull',
            'sid': self.sid,  # Use the actual subscriber ID
            'topic': topic
        }
        response = self._send_request(request_data)
        return response.get('messages', [])
