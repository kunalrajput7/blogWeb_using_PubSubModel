
# Project Title

A brief description of what this project does and who it's for

# **Publisher-Subscriber Model with Client-Server Architecture**

## **Overview**
This project implements a basic publisher-subscriber model using a client-server architecture. The system allows publishers to create topics, send messages on those topics, and subscribers to subscribe to topics and pull messages. The project is implemented in Python with TCP socket communication. Additionally, a benchmarking script is provided to measure the server's throughput using a ping-pong message exchange test.


## **Prerequisites**
Make sure you have the following installed:
- Python 3.x
- Required dependencies (Install using the command below):
```  
pip install -r requirements.txt
```


## How to Run
#### 1. Starting the Server

Before running any clients, you need to start the server. This is responsible for handling communication between publishers and subscribers.

```
python server.py
```

#### 2. Running Publisher and Subscriber Clients

You can create a publisher and subscriber using the provided publisher_client.py and subscriber_client.py or create custom clients.

####  Publisher Example:
```
python publisher_client.py
```
####  Subscriber Example:
```
python subscriber_client.py
```
####  3. Running the Ping-Pong Test

To measure the server's maximum throughput using two clients communicating back and forth (ping-pong style), run the following script:
```
python ping_pong_test.py
```
This test exchanges a specified number of messages between two topics to measure the server’s throughput in terms of messages per second.

#### 4. Benchmarking

You can also run the benchmarking script to measure performance for creating topics, sending messages, and other actions:
```
python benchmark_[api_name_to_be_)benchmarked].py
```
The benchmark will display the average time taken for the server to handle different requests.



# Project Breakdown

### Publisher Class
Located in api_library/Publisher.py, this class allows publishers to:

- registerPublisher(): Registers a publisher and returns a unique pid.
- createTopic(topic): Creates a new topic.
- deleteTopic(topic): Deletes an existing topic.
- send(topic, message): Sends a message to a specific topic.

### Subscriber Class
Located in api_library/Subscriber.py, this class allows subscribers to:

- registerSubscriber(): Registers a subscriber and returns a unique sid.
- subscribe(topic): Subscribes the subscriber to a specific topic.
- pull(topic): Pulls all available messages from a subscribed topic.


### Ping-Pong Test

Located in ping_pong_test.py, this script simulates message exchanges between two clients:

Client A: Subscribes to topic_1 and sends messages to topic_2.
Client B: Subscribes to topic_2 and sends messages to topic_1.
The test measures the total time taken for the exchange of messages and calculates the server's throughput in messages per second.


### Server
The server located in server.py handles all incoming connections, manages publishers, subscribers, and the message buffers for each topic.

### Benchmarking
The benchmarking script located in benchmark.py measures server performance by performing operations like topic creation, message sending, and more. It calculates the time taken per client request and overall server throughput.


### Output Example
Upon successful execution of the ping_pong_test.py, the output might look like:

```
Starting Ping-Pong Test...

Client A received: ['Message 1 from Client B']
Client A sent message 1 to Topic 2
Client B received: ['Message 1 from Client A']
Client B sent message 1 to Topic 1
...

Ping-Pong Test completed.
Total time: 2.3501 seconds
Messages exchanged: 200
Maximum throughput: 85.10 messages/second
```

### Testing & Validation

- The system has been tested using various scenarios:
- Registering publishers and subscribers.
- Creating, subscribing to, and pulling messages from topics.
- Measuring server throughput via the ping-pong test and benchmarking scripts.


### Conclusion

This project demonstrates a scalable and efficient publisher-subscriber architecture with basic message passing. The system's throughput can be further optimized by improving socket communication or handling larger-scale tests.