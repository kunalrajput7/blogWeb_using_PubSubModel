from api_library.Publisher import Publisher

def publisher_client():
    try:
        print("Initializing Publisher...")
        pub = Publisher()
        
        # Register the publisher and get the ID
        print("Registering Publisher...")
        pid = pub.registerPublisher()
        print(f"Publisher ID: {pid}")
        
        # Create a topic if it doesn't already exist
        topic = "Sports"
        print(f"Attempting to create topic '{topic}'...")
        create_status = pub.createTopic(topic)
        
        if create_status == 'Topic already exists':
            print(f"Topic '{topic}' already exists.")
        else:
            print(f"Topic '{topic}' created.")
        
        # Send a message to the topic
        print(f"Sending message to '{topic}'...")
        pub.send(topic, "Hello, Kunal here, this is a message about Sports!")
        print(f"Message sent to '{topic}'")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    publisher_client()
