import time
import threading
from api_library.Publisher import Publisher

# Function that each publisher client will run to send a message
def send_benchmark(pid, topic, message):
    try:
        pub = Publisher()
        print(f"Publisher {pid}: Sending message to topic '{topic}'...")
        start_time = time.time()
        pub.send(topic, message)
        end_time = time.time()
        print(f"Publisher {pid}: Sending message to '{topic}' completed in {end_time - start_time:.4f} seconds")
    except Exception as e:
        print(f"Publisher {pid}: Error while sending message to '{topic}': {e}")

# Function to benchmark the server's throughput for send
def benchmark_send(num_clients, topic, message):
    threads = []
    start_time = time.time()

    for i in range(num_clients):
        thread = threading.Thread(target=send_benchmark, args=(i + 1, topic, message))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    print(f"\nBenchmark completed with {num_clients} clients.")
    print(f"Total time for {num_clients} clients to send messages: {total_time:.4f} seconds")
    print(f"Average time per client: {total_time / num_clients:.4f} seconds\n")

if __name__ == "__main__":
    print("Starting benchmark for send()...\n")

    num_clients = 1
    max_clients = 1000  # Adjust as needed
    topic = "Sports"  # Change the topic as needed
    message = "Hello from the Publisher!"  # Change the message as needed

    while num_clients <= max_clients:
        print(f"Benchmarking with {num_clients} clients:")
        benchmark_send(num_clients, topic, message)
        num_clients *= 2  # Double the number of clients each iteration
