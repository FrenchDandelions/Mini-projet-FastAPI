if __package__ is None:
    import sys
    import os
    # Add parent directory to sys.path (project root)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    # Set the package name to Client, so relative imports inside Client/ work
    __package__ = "Client"

from Client import Client

if __name__ == "__main__":
    try:
        client = Client()
        client.run()
    except Exception as e:
        print("Failed to send request:", e)
