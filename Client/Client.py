from utils import Argument, send_request
import os


class Client:
    def __init__(self, arg: str = None):
        self.args = Argument(arg).args
        self.command = self.args.command

    
    def run(self):
        """  """
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
        return


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
            dict: JSON response containing the list of the datasets.
        """
        response = send_request(base_url=url, endpoint=endpoint)
        print("Response status code:", response.status_code)
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
        print("Body:")
        print(response.json())
        return response


    @staticmethod
    def info_dataset(url: str = "http://localhost:8000",
                        endpoint: str = "/datasets/",
                        ID: str = None):
        if ID is None:
            raise ValueError("No dataset id was given")
        endpoint += ID.rstrip("/") + "/"
        response = send_request(base_url=url,
                                endpoint=endpoint)
        print("Response status code:", response.status_code)
        print("Body:")
        print(response.json())
        return response


    @staticmethod
    def delete_dataset(url: str = "http://localhost:8000",
                        endpoint: str = "/datasets/",
                        ID: str = None):
        if ID is None:
            raise ValueError("No dataset id was given")
        endpoint += ID.rstrip("/") + "/"
        response = send_request(base_url=url,
                                endpoint=endpoint,
                                method="delete")
        print("Response status code:", response.status_code)
        print("Body:")
        print(response.json())
        return response


    @staticmethod
    def export_dataset(url: str = "http://localhost:8000",
                        endpoint: str = "/datasets/",
                        ID: str = None):
        if ID is None:
            raise ValueError("No dataset id was given")
        endpoint += ID.rstrip("/") + "/excel/"
        response = send_request(base_url=url,
                                endpoint=endpoint)
        print("Response status code:", response.status_code)
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
        if ID is None:
            raise ValueError("No dataset id was given")
        endpoint += ID.rstrip("/") + "/stats/"
        response = send_request(base_url=url,
                                endpoint=endpoint)
        print("Response status code:", response.status_code)
        print("Body:")
        print(response.json())
        return response


    @staticmethod
    def plot_dataset(ID: str = None):
        if ID is None:
            raise ValueError("No dataset id was given")
        return