# Client

How to use the client:

Run commands inside the Client directory:

  python main.py <command> [options]

Commands:

- **list**             List all datasets
- **upload -f <file>** Upload a CSV file
- **info <id>**        Show info about a dataset
- **delete <id>**      Delete a dataset
- **export <id>**      Export dataset as Excel
- **stats <id>**       Show dataset statistics
- **plot <id>**        Generate histogram PDF

Example:

  python main.py upload -f sample_data.csv
  python main.py list

Run 'python main.py -h' for help.
