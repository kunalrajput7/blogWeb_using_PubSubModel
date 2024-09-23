from api_library.Publisher import Publisher

def publisher_client():
    try:
        print("Initializing Publisher...")
        pub = Publisher()
        
        # Register the publisher and get the ID
        print("Registering Publisher...")
        pid = pub.registerPublisher()
        print(f"Publisher ID: {pid}")
        
        # Create a topic
        print("Creating topic 'Sports'...")
        pub.createTopic("Sports")
        print("Created topic 'Sports'")
        
        # Send a message to the topic
        print("Sending message to 'Sports'...")
        pub.send("Sports", "Hello, Kunal here, this is a message about Sports!")
        print("Message sent to 'Sports'")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    publisher_client()
