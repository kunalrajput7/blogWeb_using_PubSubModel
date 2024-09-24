import time
import threading
import uuid
from api_library.Publisher import Publisher
import matplotlib.pyplot as plt


def create_topic_once(topic_name):
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

def send_benchmark(topic_name, message, pid):
    try:
        pub = Publisher()
        pub.registerPublisher()
        start_time = time.time()
        status = pub.send(topic_name, message)
        end_time = time.time()
        return status, end_time - start_time
    except Exception as e:
        return f"Error: {e}", 0 

def benchmark_send(num_clients, topic_name="Hello Kunal"):

    create_status, _ = create_topic_once(topic_name)
    if "Error" in create_status:
        print("Error creating the topic. Aborting benchmark.")
        return 0

    threads = []
    results = []
    start_time = time.time()

    for i in range(num_clients):
        message = f"Message {i + 1} from {topic_name} {uuid.uuid4()}"
        thread = threading.Thread(target=lambda idx=i: results.append(send_benchmark(topic_name, message, idx + 1)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    total_requests = num_clients
    throughput = total_requests / total_time if total_time > 0 else 0

    success_count = sum(1 for result in results if "Error" not in result[0])
    print(f"\nBenchmark completed with {num_clients} clients.")
    print(f"Total time for {num_clients} clients to send messages: {total_time:.4f} seconds")
    print(f"Average time per client: {total_time / total_requests:.4f} seconds")
    print(f"Maximum throughput: {throughput:.2f} messages/second")
    print(f"Successful message sends: {success_count}/{total_requests}\n")

    return throughput 

if __name__ == "__main__":
    print("Starting benchmark for send()...\n")

    num_clients = 1
    max_clients = 1000

    throughputs = []
    client_counts = []

    while num_clients <= max_clients:
        throughput = benchmark_send(num_clients)
        throughputs.append(throughput)
        client_counts.append(num_clients)
        num_clients *= 2

    plt.figure(figsize=(10, 6))
    plt.plot(client_counts, throughputs, marker='o')
    plt.xscale('log')
    plt.xlabel('Number of Clients (log scale)')
    plt.ylabel('Throughput (messages/second)')
    plt.title('Throughput Benchmark for send()')
    plt.grid(True)
    plt.xticks(client_counts)
    plt.show()
