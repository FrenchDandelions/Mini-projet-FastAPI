from .utils import Argument, send_request
import os


class Client:
    def __init__(self, arg: str = None):
        """
        Initialize the Client instance by parsing command line arguments.

        Args:
            arg (str, optional): Argument string to be parsed. Defaults to None.

        Attributes:
            args: Parsed arguments from Argument class.
            command (str): The command extracted from the parsed arguments.
        """
        self.args = Argument(arg).args
        self.command = self.args.command

    
    def run(self):
        """
        Execute the command method based on the parsed command argument.

        This method dynamically calls the corresponding dataset-related method
        using the `command` argument. It passes `ID` or `path` parameters if
        provided in the arguments. Raises NotImplementedError if the command
        method does not exist.

        Raises:
            NotImplementedError: If no method is implemented for the given command.
        """
        method = getattr(self, f'{self.command}_dataset', None)
        if not method:
            raise NotImplementedError(f'Method not implemented for command: {self.command}')
        
        if hasattr(self.args, "id"):
            res = method(ID = self.args.id)
        elif hasattr(self.args, "file"):
            res = method(path = self.args.file)
        else:
            res = method()
        # print(res)
        return res


    @staticmethod
    def list_dataset(url: str = "http://localhost:8000",
                        endpoint:str = "/datasets/"):
        """
        Custom Client static method to send a GET request to
        our server to retrieve the list of all the uploaded
        datasets.

        Parameters:
            url      (str): The base URL of the API server (default = 'http://localhost:8000').
            endpoint (str): The endpoint to hit (default = '/datasets/').

        Returns:
            dict: JSON response containing the list of the datasets or error info.
        """
        response = send_request(base_url=url, endpoint=endpoint)
        print("Response status code:", response.status_code)
        if response.status_code != 200:
            print(response.json)
            return response
        print("Body:")
        print(response.json())
        return response


    @staticmethod
    def upload_dataset(url: str = "http://localhost:8000",
                        path: str = None,
                        endpoint:str = "/datasets/"):
        """
        Custom Client static method to send a POST request to
        upload a CSV dataset file to the server.

        Parameters:
            url      (str): The base URL of the API server (default = 'http://localhost:8000').
            path     (str): Local file path to the file dataset.
            endpoint (str): The endpoint to hit (default = '/datasets/').

        Returns:
            dict: JSON response containing the dataset ID or error info.

        Raises:
            ValueError: If no file path is provided.
            FileNotFoundError: If the specified file does not exist.
        """
        if path is None:
            raise ValueError("No database file path was given")
        elif os.path.exists(path) is False:
            raise FileNotFoundError("No file found")
        with open(path, 'rb') as file:
            files = {
                'file': (path.split('/')[-1], file, "text/csv")
                }
            response = send_request(base_url=url,
                                    endpoint=endpoint,
                                    method="post",
                                    files=files)
        print("Response status code:", response.status_code)
        if response.status_code != 200:
            print(response.json)
            return response
        print("Body:")
        print(response.json())
        return response


    @staticmethod
    def info_dataset(url: str = "http://localhost:8000",
                        endpoint: str = "/datasets/",
                        ID: str = None):
        """
        Custom Client static method to send a GET request to
        retrieve metadata information about a specific dataset.

        Parameters:
            url      (str): The base URL of the API server (default = 'http://localhost:8000').
            endpoint (str): The endpoint to hit (default = '/datasets/').
            ID       (str): ID of the dataset to retrieve info for.

        Returns:
            dict: JSON response containing the dataset metadata or error info.

        Raises:
            ValueError: If no dataset ID is provided.
        """
        if ID is None:
            raise ValueError("No dataset id was given")
        endpoint += ID.rstrip("/") + "/"
        response = send_request(base_url=url,
                                endpoint=endpoint)
        print("Response status code:", response.status_code)
        if response.status_code != 200:
            print(response.json)
            return response
        print("Body:")
        print(response.json())
        return response


    @staticmethod
    def delete_dataset(url: str = "http://localhost:8000",
                        endpoint: str = "/datasets/",
                        ID: str = None):
        """
        Custom Client static method to send a DELETE request to
        remove a specific dataset from the server.

        Parameters:
            url      (str): The base URL of the API server (default = 'http://localhost:8000').
            endpoint (str): The endpoint to hit (default = '/datasets/').
            ID       (str): ID of the dataset to delete.

        Returns:
            dict: JSON response indicating success or failure or error info.

        Raises:
            ValueError: If no dataset ID is provided.
        """
        if ID is None:
            raise ValueError("No dataset id was given")
        endpoint += ID.rstrip("/") + "/"
        response = send_request(base_url=url,
                                endpoint=endpoint,
                                method="delete")
        print("Response status code:", response.status_code)
        if response.status_code != 200:
            print(response.json)
            return response

        print("Body:")
        print(response.json())
        return response


    @staticmethod
    def export_dataset(url: str = "http://localhost:8000",
                        endpoint: str = "/datasets/",
                        ID: str = None):
        """
        Custom Client static method to send a GET request to
        export a dataset in Excel format (.xlsx) and save it locally.

        Parameters:
            url      (str): The base URL of the API server (default = 'http://localhost:8000').
            endpoint (str): The endpoint to hit (default = '/datasets/').
            ID       (str): ID of the dataset to export.

        Returns:
            Response: HTTP response containing the file data or error info.

        Raises:
            ValueError: If no dataset ID is provided.
        """
        if ID is None:
            raise ValueError("No dataset id was given")
        endpoint += ID.rstrip("/") + "/excel/"
        response = send_request(base_url=url,
                                endpoint=endpoint)
        print("Response status code:", response.status_code)
        if response.status_code != 200:
            print(response.json)
            return response
        content_disposition = response.headers.get("content-disposition", "")
        filename = "output.xlsx" #default filename just in case
        if "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"')
        print(f"Saving file as: {filename}")
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"File saved: {filename}")
        return response


    @staticmethod
    def stats_dataset(url: str = "http://localhost:8000",
                        endpoint: str = "/datasets/",
                        ID: str = None):
        """
        Custom Client static method to send a GET request to
        retrieve statistical information about a dataset.

        Parameters:
            url      (str): The base URL of the API server (default = 'http://localhost:8000').
            endpoint (str): The endpoint to hit (default = '/datasets/').
            ID       (str): ID of the dataset to get statistics for.

        Returns:
            dict: JSON response containing statistical summaries or error info.

        Raises:
            ValueError: If no dataset ID is provided.
        """
        if ID is None:
            raise ValueError("No dataset id was given")
        endpoint += ID.rstrip("/") + "/stats/"
        response = send_request(base_url=url,
                                endpoint=endpoint)
        print("Response status code:", response.status_code)
        if response.status_code != 200:
            print(response.json)
            return response
        print("Body:")
        print(response.json())
        return response


    @staticmethod
    def plot_dataset(url: str = "http://localhost:8000",
                        endpoint: str = "/datasets/",
                        ID: str = None):
        """
        Custom Client static method to send a GET request to
        retrieve a PDF plot visualization of a dataset and save it locally.

        Parameters:
            url      (str): The base URL of the API server (default = 'http://localhost:8000').
            endpoint (str): The endpoint to hit (default = '/datasets/').
            ID       (str): ID of the dataset to plot.

        Returns:
            Response: HTTP response containing the PDF file or error info.

        Raises:
            ValueError: If no dataset ID is provided.
        """
        if ID is None:
            raise ValueError("No dataset id was given")
        endpoint += ID.rstrip("/") + "/plot/"
        response = send_request(base_url=url,
                                endpoint=endpoint)
        print("Response status code:", response.status_code)
        if response.status_code != 200:
            print(response.json)
            return response
        content_disposition = response.headers.get("content-disposition", "")
        filename = "output.pdf" #default filename just in case (again)
        if "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"')
        print(f"Saving file as: {filename}")
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"File saved: {filename}")
        return response
