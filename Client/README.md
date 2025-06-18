# Client

How to use the client:

You can run commands using either Python or the standalone executable (if you've built it).

## Using Python

Run commands inside the `Client` directory:

```
python main.py <command> [options]
```

## Using the Built Executable

To use the standalone executable, you first need to build it and add it to your PATH.

### Build the executable:

* On Linux or macOS, run:

  ```
  ./build.sh
  ```

* On Windows (PowerShell), run:

  ```
  .\build.ps1
  ```

This will create a standalone executable called `myapp` (or `myapp.exe` on Windows) and copy it to a local bin directory.

Make sure that directory is in your PATH so you can run the command from anywhere.

### Then you can run:

```
myapp <command> [options]
```

## Commands

* **list**             List all datasets
* **upload -f <file>** Upload a CSV file
* **info <id>**        Show info about a dataset
* **delete <id>**      Delete a dataset
* **export <id>**      Export dataset as Excel
* **stats <id>**       Show dataset statistics
* **plot <id>**        Generate histogram PDF

## Example

Using Python:

```
python main.py upload -f sample_data_1.csv
python main.py list
```

Using the built executable:

```
myapp upload -f sample_data_1.csv
myapp list
```

Run `python main.py -h` or `myapp -h` for help.
