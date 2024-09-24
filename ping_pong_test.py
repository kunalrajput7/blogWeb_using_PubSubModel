import time
import threading
from api_library.Publisher import Publisher
from api_library.Subscriber import Subscriber

# Message counts and topics
NUM_MESSAGES = 100  # Number of messages for ping-pong test
TOPIC_1 = "topic_1"
TOPIC_2 = "topic_2"

# Client A function
def client_a_ping_pong():
    sub = Subscriber()
    pub = Publisher()

    # Register and subscribe to Topic 1
    sub.registerSubscriber()
    sub.subscribe(TOPIC_1)

    for i in range(NUM_MESSAGES):
        # Pull message from Topic 1 (ping)
        messages = sub.pull(TOPIC_1)
        if messages:
            print(f"Client A received: {messages}")

        # Send message to Topic 2 (pong)
        pub.send(TOPIC_2, f"Message {i + 1} from Client A")
        print(f"Client A sent message {i + 1} to Topic 2")

# Client B function
def client_b_ping_pong():
    sub = Subscriber()
    pub = Publisher()

    # Register and subscribe to Topic 2
    sub.registerSubscriber()
    sub.subscribe(TOPIC_2)

    for i in range(NUM_MESSAGES):
        # Pull message from Topic 2 (pong)
        messages = sub.pull(TOPIC_2)
        if messages:
            print(f"Client B received: {messages}")

        # Send message to Topic 1 (ping)
        pub.send(TOPIC_1, f"Message {i + 1} from Client B")
        print(f"Client B sent message {i + 1} to Topic 1")

# Function to measure throughput
def measure_ping_pong_throughput():
    # Starting the clients as separate threads
    start_time = time.time()
    
    thread_a = threading.Thread(target=client_a_ping_pong)
    thread_b = threading.Thread(target=client_b_ping_pong)
    
    # Start both threads
    thread_a.start()
    thread_b.start()

    # Wait for both threads to finish
    thread_a.join()
    thread_b.join()

    end_time = time.time()
    
    total_time = end_time - start_time
    total_messages = NUM_MESSAGES * 2  # Total messages exchanged in both directions

    throughput = total_messages / total_time if total_time > 0 else 0

    print(f"\nPing-Pong Test completed.")
    print(f"Total time: {total_time:.4f} seconds")
    print(f"Messages exchanged: {total_messages}")
    print(f"Maximum throughput: {throughput:.2f} messages/second")

if __name__ == "__main__":
    print("Starting Ping-Pong Test...\n")
    measure_ping_pong_throughput()
