import time
import threading
from api_library.Subscriber import Subscriber

# Function that each subscriber client will run to subscribe to a topic
def subscribe_benchmark(sid, topic):
    try:
        sub = Subscriber()
        print(f"Subscriber {sid}: Subscribing to topic '{topic}'...")
        start_time = time.time()
        sub.subscribe(topic)
        end_time = time.time()
        print(f"Subscriber {sid}: Subscription to '{topic}' completed in {end_time - start_time:.4f} seconds")
    except Exception as e:
        print(f"Subscriber {sid}: Error while subscribing to '{topic}': {e}")

# Function to benchmark the server's throughput for subscribe
def benchmark_subscribe(num_clients, topic):
    threads = []
    start_time = time.time()

    for i in range(num_clients):
        thread = threading.Thread(target=subscribe_benchmark, args=(i + 1, topic))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    print(f"\nBenchmark completed with {num_clients} clients.")
    print(f"Total time for {num_clients} clients to subscribe: {total_time:.4f} seconds")
    print(f"Average time per client: {total_time / num_clients:.4f} seconds\n")

if __name__ == "__main__":
    print("Starting benchmark for subscribe()...\n")

    num_clients = 1
    max_clients = 1000  # Adjust as needed
    topic = "Sports"  # Change the topic as needed

    while num_clients <= max_clients:
        print(f"Benchmarking with {num_clients} clients:")
        benchmark_subscribe(num_clients, topic)
        num_clients *= 2  # Double the number of clients each iteration
