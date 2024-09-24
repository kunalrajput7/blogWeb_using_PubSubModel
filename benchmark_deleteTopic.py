import time
import threading
from api_library.Publisher import Publisher
import matplotlib.pyplot as plt

# Function to create a topic once
def create_topic_benchmark(topic_name):
    try:
        pub = Publisher()
        pub.registerPublisher()
        start_time = time.time()
        status = pub.createTopic(topic_name)
        end_time = time.time()
        print(f"Topic '{topic_name}' created in {end_time - start_time:.4f} seconds")
        return status, end_time - start_time
    except Exception as e:
        print(f"Error creating topic: {e}")
        return f"Error: {e}", 0 

# Function to delete a topic
def delete_topic_benchmark(topic_name, pid):
    try:
        pub = Publisher()
        pub.registerPublisher()  # Ensure the publisher is registered
        start_time = time.time()
        status = pub.deleteTopic(topic_name)
        end_time = time.time()
        return status, end_time - start_time
    except Exception as e:
        return f"Error: {e}", 0 

# Benchmark deleteTopic function
def benchmark_delete_topic(num_clients, topic_name="Hello Kunal"):

    # Create the topic once before starting the benchmark
    create_status, _ = create_topic_benchmark(topic_name)
    if "Error" in create_status:
        print("Error creating the topic. Aborting benchmark.")
        return 0

    threads = []
    results = []
    start_time = time.time()

    # Spawn threads to delete the topic concurrently
    for i in range(num_clients):
        thread = threading.Thread(target=lambda idx=i: results.append(delete_topic_benchmark(topic_name, idx + 1)))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    total_requests = num_clients
    throughput = total_requests / total_time if total_time > 0 else 0

    # Count the successful deletions
    success_count = sum(1 for result in results if "Error" not in result[0])
    print(f"\nBenchmark completed with {num_clients} clients.")
    print(f"Total time for {num_clients} clients to delete topics: {total_time:.4f} seconds")
    print(f"Average time per client: {total_time / total_requests:.4f} seconds")
    print(f"Maximum throughput: {throughput:.2f} topics/second")
    print(f"Successful topic deletions: {success_count}/{total_requests}\n")

    return throughput 

if __name__ == "__main__":
    print("Starting benchmark for deleteTopic()...\n")

    num_clients = 1
    max_clients = 1000

    throughputs = []
    client_counts = []

    # Increment clients for benchmarking
    while num_clients <= max_clients:
        throughput = benchmark_delete_topic(num_clients)
        throughputs.append(throughput)
        client_counts.append(num_clients)
        num_clients *= 2  # Increase the number of clients exponentially

    # Plot the throughput graph
    plt.figure(figsize=(10, 6))
    plt.plot(client_counts, throughputs, marker='o')
    plt.xscale('log')
    plt.xlabel('Number of Clients (log scale)')
    plt.ylabel('Throughput (topics/second)')
    plt.title('Throughput Benchmark for deleteTopic()')
    plt.grid(True)
    plt.xticks(client_counts)
    plt.show()
