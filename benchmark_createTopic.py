import time
import threading
import uuid
import matplotlib.pyplot as plt
from api_library.Publisher import Publisher

# Function that each publisher client will run to create a topic
def create_topic_benchmark(topic_name, pid):
    try:
        pub = Publisher()
        start_time = time.time()
        status = pub.createTopic(topic_name)
        end_time = time.time()
        return status, end_time - start_time
    except Exception as e:
        return f"Error: {e}", 0 

# Function to benchmark the server's throughput for createTopic
def benchmark_create_topic(num_clients, topic_prefix="Hello Kunal"):
    threads = []
    results = []
    start_time = time.time()

    for i in range(num_clients):
        topic_name = f"{topic_prefix}_{i + 1}_{uuid.uuid4()}"
        thread = threading.Thread(target=lambda idx=i: results.append(create_topic_benchmark(topic_name, idx + 1)))
        threads.append(thread)
        thread.start()

    # So here we wait for all threads to complete
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    total_requests = num_clients
    throughput = total_requests / total_time if total_time > 0 else 0  # This function calculates throughput

    # Aethetically print all the summary of results lol
    success_count = sum(1 for result in results if "Error" not in result[0])
    print(f"\nBenchmark completed with {num_clients} clients.")
    print(f"Total time for {num_clients} clients to create topics: {total_time:.4f} seconds")
    print(f"Average time per client: {total_time / total_requests:.4f} seconds")
    print(f"Maximum throughput: {throughput:.2f} topics/second")
    print(f"Successful topic creations: {success_count}/{total_requests}\n")  # Print success count

    return throughput 

if __name__ == "__main__":
    print("Starting benchmark for createTopic()...\n")

    num_clients = 1
    max_clients = 1000  # Setting a reasonable upper limit to avoid overloading the server

    throughputs = []
    client_counts = []

    while num_clients <= max_clients:
        throughput = benchmark_create_topic(num_clients)
        throughputs.append(throughput)
        client_counts.append(num_clients)
        num_clients *= 2  #Here we double the number of clients each iteration for progressive testing

    # Here we simpply plot the throughput graph
    plt.figure(figsize=(10, 6))
    plt.plot(client_counts, throughputs, marker='o')
    plt.xscale('log')
    plt.xlabel('Number of Clients (log scale)')
    plt.ylabel('Throughput (topics/second)')
    plt.title('Throughput Benchmark for createTopic()')
    plt.grid(True)
    plt.xticks(client_counts)
    plt.show()
