import time
import threading
from api_library.Publisher import Publisher

# Function that each publisher client will run to register
def register_publisher_benchmark(pid):
    try:
        pub = Publisher()
        print(f"Publisher {pid}: Registering publisher...")
        start_time = time.time()
        pub.registerPublisher()
        end_time = time.time()
        print(f"Publisher {pid}: Registration completed in {end_time - start_time:.4f} seconds")
    except Exception as e:
        print(f"Publisher {pid}: Error while registering publisher: {e}")

# Function to benchmark the server's throughput for registerPublisher
def benchmark_register_publisher(num_clients):
    threads = []
    start_time = time.time()

    for i in range(num_clients):
        thread = threading.Thread(target=register_publisher_benchmark, args=(i + 1,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    total_requests = num_clients  # Number of publishers registered
    throughput = total_requests / total_time if total_time > 0 else 0  # Calculate throughput

    print(f"\nBenchmark completed with {num_clients} clients.")
    print(f"Total time for {num_clients} clients to register: {total_time:.4f} seconds")
    print(f"Average time per client: {total_time / num_clients:.4f} seconds")
    print(f"Maximum throughput: {throughput:.2f} registrations/second\n")  # Print throughput

if __name__ == "__main__":
    print("Starting benchmark for registerPublisher()...\n")

    num_clients = 1
    max_clients = 1000  # Adjust as needed

    while num_clients <= max_clients:
        print(f"Benchmarking with {num_clients} clients:")
        benchmark_register_publisher(num_clients)
        num_clients *= 2  # Double the number of clients each iteration
