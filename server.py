import socket
import threading
import json

# Data structures to hold publishers, subscribers, topics, and messages
publishers = {}
subscribers = {}
topics = {}
topic_messages = {}
message_locks = threading.Lock()
subscriber_views = {}  # Track how many subscribers have pulled messages for each topic

def handle_client_connection(client_socket):
    request = client_socket.recv(1024).decode()
    request_data = json.loads(request)
    action = request_data.get('action')

    if action == 'registerPublisher':
        pid = len(publishers) + 1
        publishers[pid] = client_socket.getpeername()
        response = {'pid': pid}
        client_socket.sendall(json.dumps(response).encode())

    elif action == 'registerSubscriber':
        sid = len(subscribers) + 1
        subscribers[sid] = {'address': client_socket.getpeername(), 'subscriptions': set()}
        response = {'sid': sid}
        client_socket.sendall(json.dumps(response).encode())

    elif action == 'createTopic':
        pid = request_data.get('pid')
        topic = request_data.get('topic')
        if topic not in topics:
            topics[topic] = pid
            topic_messages[topic] = []
            subscriber_views[topic] = 0  # Initialize views count for the topic
            response = {'status': 'Topic created'}
        else:
            response = {'status': 'Topic already exists'}
        client_socket.sendall(json.dumps(response).encode())

    elif action == 'deleteTopic':
        pid = request_data.get('pid')
        topic = request_data.get('topic')
        if topic in topics and topics[topic] == pid:
            del topics[topic]
            del topic_messages[topic]
            del subscriber_views[topic]  # Remove views tracking
            response = {'status': 'Topic deleted'}
        else:
            response = {'status': 'Topic does not exist or unauthorized'}
        client_socket.sendall(json.dumps(response).encode())

    elif action == 'send':
        pid = request_data.get('pid')
        topic = request_data.get('topic')
        message = request_data.get('message')
        if topic in topics and topics[topic] == pid:
            with message_locks:
                topic_messages[topic].append(message)
            response = {'status': 'Message sent'}
        else:
            response = {'status': 'Topic does not exist or unauthorized'}
        client_socket.sendall(json.dumps(response).encode())

    elif action == 'subscribe':
        sid = request_data.get('sid')
        topic = request_data.get('topic')
        if topic in topics:
            subscribers[sid]['subscriptions'].add(topic)
            response = {'status': 'Subscribed to topic'}
        else:
            response = {'status': 'Topic does not exist'}
        client_socket.sendall(json.dumps(response).encode())

    elif action == 'pull':
        sid = request_data.get('sid')
        topic = request_data.get('topic')
        if topic in subscribers[sid]['subscriptions']:
            with message_locks:
                messages = topic_messages.get(topic, []).copy()
                # Increase the view count for this topic
                subscriber_views[topic] += 1
                # Check if all subscribers have pulled messages
                if subscriber_views[topic] >= len([s for s in subscribers if topic in subscribers[s]['subscriptions']]):
                    topic_messages[topic] = []  # Clear messages after all have pulled
                    subscriber_views[topic] = 0  # Reset view count for the topic
                response = {'messages': messages}
        else:
            response = {'messages': []}
        client_socket.sendall(json.dumps(response).encode())

    else:
        response = {'status': 'Invalid action'}
        client_socket.sendall(json.dumps(response).encode())

    client_socket.close()

def start_server(host='127.0.0.1', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_sock, address = server_socket.accept()
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()

if __name__ == "__main__":
    start_server()
