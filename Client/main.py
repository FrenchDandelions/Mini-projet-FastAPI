from Client import Client

if __name__ == "__main__":
    try:
        client = Client()
        client.run()
    except Exception as e:
        print("Failed to send request:", e)
