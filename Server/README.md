# Server

How to run the server:

- Build the Docker images:
  make build

- Start the server:
  make up

- Build and start together:
  make run

- Stop the server and remove images:
  make down

- Restart the server:
  make restart

The server handles dataset uploads and requests at /datasets.
Rate limit is 15 requests per minute per IP and endpoint.
