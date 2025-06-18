# Mini Project: Dataset API & Client

## Overview

This project provides a simple Python-based REST API server and a command-line client to upload, manage, and analyze CSV datasets.

* **Server:** FastAPI backend with endpoints to upload datasets, list them, get info, export as Excel, generate stats, and plot histograms as PDFs.

* **Client:** Python CLI tool to interact with the API using commands corresponding to each server operation.

* **Tester:** Basic automated tests and sample data to verify functionality.

## Architecture

```
.
├── Server/         # API server code and Docker setup
├── Client/         # Command-line client code and requirements
└── tester/         # Tests and sample CSV data
```

* Server is containerized with Docker and orchestrated via docker-compose.

* Client is a standalone Python app usable from the command line or as a built executable.

* Data is stored as CSV files on disk and also held in-memory as pandas DataFrames for fast processing.

## How to Run

### Server

1. Navigate to the `Server` directory.

2. Build and start containers with:

   ```bash
   make run
   ```

3. API will be available at [http://localhost:8000](http://localhost:8000).

### Client

You can use the client via Python or as a standalone executable.

#### Using Python

1. Navigate to the `Client` directory.

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run commands like:

   ```bash
   python main.py upload --file sample_data_1.csv
   ```

#### Using the Built Executable

To build the standalone executable and use it globally:

* On Linux or macOS, run:

  ```bash
  ./build.sh
  ```

* On Windows (PowerShell), run:

  ```powershell
  .\build.ps1
  ```

This will create a standalone executable named `myapp` (or `myapp.exe` on Windows) and copy it to a local bin directory.

Make sure that directory is in your `PATH` so you can run the command from anywhere.

Then you can run client commands as:

```bash
myapp upload --file sample_data_1.csv
myapp list
```

### Tests

1. Navigate to the `tester` directory.

2. Run tests with:

   ```bash
   pytest test.py -s
   ```

## API Endpoints

* `GET /datasets/` — List datasets

* `POST /datasets/` — Upload a CSV dataset

* `GET /datasets/{id}/` — Get dataset info (filename, size)

* `DELETE /datasets/{id}/` — Delete a dataset

* `GET /datasets/{id}/excel/` — Export dataset as Excel

* `GET /datasets/{id}/stats/` — Get dataset stats as JSON

* `GET /datasets/{id}/plot/` — Get histograms PDF of numerical columns

## Notes

* No user authentication is implemented.

* CSV processing is done in-memory for simplicity.

* Rate limiting and file locks are implemented on the server to handle concurrent access.
