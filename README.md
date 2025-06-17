# Mini Project: Dataset API & Client
## Overview
This project provides a simple Python-based REST API server and a command-line client to upload, manage, and analyze CSV datasets.

- **Server:** FastAPI-based backend with endpoints to upload datasets, list them, get info, export as Excel, generate stats, and plot histograms as PDFs.

- **Client:** Python CLI tool to interact with the API using commands corresponding to each server operation.

- **Tester:** Basic automated tests and sample data to verify functionality.

## Architecture
```
.
├── Server/         # API server code and Docker setup
├── Client/         # Command-line client code and requirements
└── tester/         # Tests and sample CSV data
```
- Server is containerized with Docker and orchestrated via docker-compose.

- Client is a standalone Python app usable from the command line.

- Data is stored as CSV files on disk and also held in-memory as pandas DataFrames for fast processing.

## How to Run
### Server
1. Navigate to the Server directory.

2. Build and start containers with:

```bash
make run
```
3. API will be available at http://localhost:8000.

### Client
1. Navigate to the Client directory.

2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Use the client CLI (e.g., to upload a file):

```bash
python main.py upload --file sample_data_1.csv
```
### Tests
1. Navigate to the tester directory.

2. Run tests with:

```bash
pytest test.py -s
```
## API Endpoints
- GET /datasets/ — List datasets

- POST /datasets/ — Upload a CSV dataset

- GET /datasets/{id}/ — Get dataset info (filename, size)

- DELETE /datasets/{id}/ — Delete a dataset

- GET /datasets/{id}/excel/ — Export dataset as Excel

- GET /datasets/{id}/stats/ — Get dataset stats as JSON

- GET /datasets/{id}/plot/ — Get histograms PDF of numerical columns

## Notes
- No user authentication is implemented.

- CSV processing is done in-memory for simplicity.

- Rate limiting and file locks are implemented on the server to handle concurrent access.