import time
import threading
from api_library.Publisher import Publisher
from api_library.Subscriber import Subscriber

# Function that each publisher client will run to register, create a topic, and send a message
def publisher_workflow(pid, topic, message):
    try:
        pub = Publisher()
        print(f"Publisher {pid}: Registering publisher...")
        pub.registerPublisher()  # Register the publisher
        print(f"Publisher {pid}: Registering completed. Creating topic '{topic}'...")
        pub.createTopic(topic)  # Create the topic
        print(f"Publisher {pid}: Topic '{topic}' created. Sending message: {message}")
        pub.send(topic, message)  # Send the message
        print(f"Publisher {pid}: Message sent to topic '{topic}'.")
    except Exception as e:
        print(f"Publisher {pid}: Error during publisher workflow: {e}")

# Function that each subscriber client will run to register, subscribe, and pull messages from a topic
def subscriber_workflow(sid, topic):
    try:
        sub = Subscriber()
        print(f"Subscriber {sid}: Registering subscriber...")
        sub.registerSubscriber()  # Register the subscriber
        print(f"Subscriber {sid}: Registering completed. Subscribing to topic '{topic}'...")
        sub.subscribe(topic)  # Subscribe to the topic
        print(f"Subscriber {sid}: Subscribed successfully. Now pulling messages...")

        start_time = time.time()
        messages = sub.pull(topic)  # Pull messages after subscribing
        end_time = time.time()

        print(f"Subscriber {sid}: Pulling messages from '{topic}' completed in {end_time - start_time:.4f} seconds")
        print(f"Subscriber {sid}: Messages received: {messages}")
    except Exception as e:
        print(f"Subscriber {sid}: Error while pulling messages from '{topic}': {e}")

# Function to benchmark the server's throughput for subscribe and pull
def benchmark_subscribe_and_pull(num_clients, topic, message):
    # Create publisher threads
    publisher_threads = []
    for i in range(num_clients):
        thread = threading.Thread(target=publisher_workflow, args=(i + 1, topic, message))
        publisher_threads.append(thread)
        thread.start()

    # Wait for all publisher threads to complete
    for thread in publisher_threads:
        thread.join()

    # Create subscriber threads
    subscriber_threads = []
    start_time = time.time()

    for i in range(num_clients):
        thread = threading.Thread(target=subscriber_workflow, args=(i + 1, topic))
        subscriber_threads.append(thread)
        thread.start()

    # Wait for all subscriber threads to complete
    for thread in subscriber_threads:
        thread.join()

    total_time = time.time() - start_time
    print(f"\nBenchmark completed with {num_clients} clients.")
    print(f"Total time for {num_clients} clients to subscribe and pull messages: {total_time:.4f} seconds")
    print(f"Average time per client: {total_time / (2 * num_clients):.4f} seconds")  # Average per client for both publisher and subscriber

    # Calculate maximum throughput
    max_throughput = num_clients / total_time if total_time > 0 else 0
    print(f"Maximum throughput: {max_throughput:.2f} clients per second\n")

if __name__ == "__main__":
    print("Starting benchmark for subscribe and pull...\n")

    num_clients = 1
    max_clients = 1000  # Adjust as needed
    topic = "Sports"  # Change the topic as needed
    message = "Latest sports news"  # The message the publisher will send

    while num_clients <= max_clients:
        print(f"Benchmarking with {num_clients} clients:")
        benchmark_subscribe_and_pull(num_clients, topic, message)
        num_clients *= 2  # Double the number of clients each iteration
