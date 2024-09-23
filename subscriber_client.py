from Subscriber import Subscriber

def subscriber_client():
    try:
        print("Initializing Subscriber...")
        sub = Subscriber()

        # Register the subscriber and get the ID
        print("Registering Subscriber...")
        sid = sub.registerSubscriber()
        print(f"Subscriber ID: {sid}")

        # Subscribe to the topic
        topic = "Sports"
        print(f"Subscribing to topic '{topic}'...")
        sub.subscribe(topic)
        print(f"Subscribed to topic '{topic}'")

        # Pull messages from the topic
        print(f"Pulling messages from topic '{topic}'...")
        messages = sub.pull(topic)

        if messages:
            print(f"Received messages: {messages}")
        else:
            print("No new messages.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    subscriber_client()
