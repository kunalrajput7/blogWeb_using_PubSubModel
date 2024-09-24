from api_library.Publisher import Publisher

def publisher_client():
    try:
        print("Initializing Publisher...")
        pub = Publisher()
        
        # Register the publisher and get the ID
        print("Registering Publisher...")
        pid = pub.registerPublisher()
        print(f"Publisher ID: {pid}")
        
        # Create a dictionary of topics and their corresponding list of messages
        topics_messages = {
            "Sports": [
                "Hello, Kunal here, this is a message about Sports!",
                "The game last night was thrilling!",
                "Don't forget to check the scores!"
            ],
            "Technology": [
                "Here's an update on the latest tech trends.",
                "AI is revolutionizing many industries.",
                "Check out the new smartphone releases!"
            ],
            "Health": [
                "Don't forget to take care of your health!",
                "Stay hydrated and eat your greens!",
                "Regular exercise is key to a healthy life."
            ],
        }
        
        # Loop through the dictionary to create topics and send messages
        for topic, messages in topics_messages.items():
            print(f"Attempting to create topic '{topic}'...")
            create_status = pub.createTopic(topic)
            
            if create_status == 'Topic already exists':
                print(f"Topic '{topic}' already exists.")
            else:
                print(f"Topic '{topic}' created.")
            
            # Send each message to the topic
            for message in messages:
                print(f"Sending message to '{topic}'...")
                pub.send(topic, message)
                print(f"Message sent to '{topic}': {message}")
        
        # Demonstrate deletion of the "Health" topic
        delete_topic = "Health"
        print(f"\nAttempting to delete topic '{delete_topic}'...")
        delete_status = pub.deleteTopic(delete_topic)
        print(f"Deletion status for topic '{delete_topic}': {delete_status}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    publisher_client()
