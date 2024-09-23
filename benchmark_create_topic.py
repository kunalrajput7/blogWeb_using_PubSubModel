import time
import threading
import uuid
from api_library.Publisher import Publisher

# Function that each publisher client will run to create a topic
def create_topic_benchmark(topic_name, pid):
    try:
        pub = Publisher()
        print(f"Publisher {pid}: Creating topic '{topic_name}'...")
        start_time = time.time()
        pub.createTopic(topic_name)
        end_time = time.time()
        print(f"Publisher {pid}: Topic '{topic_name}' created in {end_time - start_time:.4f} seconds")
    except Exception as e:
        print(f"Publisher {pid}: Error while creating topic '{topic_name}': {e}")

# Function to benchmark the server's throughput for createTopic
def benchmark_create_topic(num_clients, topic_prefix="Hello Kunal"):
    threads = []
    start_time = time.time()

    for i in range(num_clients):
        topic_name = f"{topic_prefix}_{i+1}_{uuid.uuid4()}"
        thread = threading.Thread(target=create_topic_benchmark, args=(topic_name, i+1))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    print(f"\nBenchmark completed with {num_clients} clients.")
    print(f"Total time for {num_clients} clients to create topics: {total_time:.4f} seconds")
    print(f"Average time per client: {total_time / num_clients:.4f} seconds\n")

if __name__ == "__main__":
    print("Starting benchmark for createTopic()...\n")

    # Number of clients to benchmark
    num_clients = 1
    max_clients = 1000  # Set a reasonable upper limit to avoid overloading the server

    while num_clients <= max_clients:
        print(f"Benchmarking with {num_clients} clients:")
        benchmark_create_topic(num_clients)
        num_clients *= 2  # Double the number of clients each iteration for progressive testing
