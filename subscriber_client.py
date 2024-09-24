from api_library.Subscriber import Subscriber

def subscriber_client():
    try:
        print("Initializing Subscriber...")
        sub = Subscriber()

        # Register the subscriber and get the ID
        print("Registering Subscriber...")
        sid = sub.registerSubscriber()
        print(f"Subscriber ID: {sid}")

        # List of topics to subscribe to
        topics = ["Sports", "Technology", "Health"]  # Added a non-existent topic for testing

        # Subscribe to each topic
        for topic in topics.copy():  # Use a copy to avoid modifying the list while iterating
            print(f"Subscribing to topic '{topic}'...")
            subscribe_status = sub.subscribe(topic)
            if subscribe_status == "Topic does not exist":
                print(f"Failed to subscribe: {subscribe_status} for topic '{topic}'")
                topics.remove(topic)  # Remove the topic from the list if it doesn't exist
            else:
                print(f"Subscribed to topic '{topic}'")

        # Pull messages from each remaining topic
        for topic in topics:
            print(f"Pulling messages from topic '{topic}'...")
            messages = sub.pull(topic)

            if messages:
                print(f"Received messages from '{topic}': {messages}")
            else:
                print(f"No new messages in '{topic}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    subscriber_client()
