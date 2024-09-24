import time
import threading
from api_library.Publisher import Publisher
from api_library.Subscriber import Subscriber

# Function to simulate Client A
def client_a_ping_pong(num_messages, topic_a_to_b, topic_b_to_a):
    try:
        pub_a = Publisher()
        sub_a = Subscriber()

        # Create the topics for communication
        pub_a.createTopic(topic_a_to_b)
        pub_a.createTopic(topic_b_to_a)

        print(f"Client A: Starting ping-pong with {num_messages} messages...")

        for i in range(num_messages):
            message_a = f"Ping {i + 1} from Client A"
            print(f"Client A: Sending message to '{topic_a_to_b}': {message_a}")
            pub_a.send(topic_a_to_b, message_a)

            # Wait to pull the response from Client B
            response = sub_a.pull(topic_b_to_a)
            print(f"Client A: Received response from Client B: {response}")

    except Exception as e:
        print(f"Client A: Error: {e}")

# Function to simulate Client B
def client_b_ping_pong(num_messages, topic_a_to_b, topic_b_to_a):
    try:
        pub_b = Publisher()
        sub_b = Subscriber()

        print(f"Client B: Starting ping-pong with {num_messages} messages...")

        for i in range(num_messages):
            # Wait to pull the message from Client A
            message_b = sub_b.pull(topic_a_to_b)
            print(f"Client B: Received message from Client A: {message_b}")

            response_b = f"Pong {i + 1} from Client B"
            print(f"Client B: Sending response to '{topic_b_to_a}': {response_b}")
            pub_b.send(topic_b_to_a, response_b)

    except Exception as e:
        print(f"Client B: Error: {e}")

# Function to start the ping-pong test between two clients
def ping_pong_test(num_messages):
    topic_a_to_b = "Topic1"
    topic_b_to_a = "Topic2"

    # Create threads for Client A and Client B
    client_a_thread = threading.Thread(target=client_a_ping_pong, args=(num_messages, topic_a_to_b, topic_b_to_a))
    client_b_thread = threading.Thread(target=client_b_ping_pong, args=(num_messages, topic_a_to_b, topic_b_to_a))

    # Start both clients simultaneously
    start_time = time.time()
    client_a_thread.start()
    client_b_thread.start()

    # Wait for both threads to complete
    client_a_thread.join()
    client_b_thread.join()

    total_time = time.time() - start_time
    print(f"\nPing-Pong Test completed with {num_messages} messages.")
    print(f"Total time for {num_messages} message exchanges: {total_time:.4f} seconds")
    print(f"Average time per message exchange: {total_time / num_messages:.4f} seconds")

if __name__ == "__main__":
    print("Starting Ping-Pong Test...\n")
    
    num_messages = 100  # Adjust this based on your server load
    ping_pong_test(num_messages)
