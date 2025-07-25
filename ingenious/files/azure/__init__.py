from pathlib import Path

from azure.identity import (
    ClientSecretCredential,
    DefaultAzureCredential,
    ManagedIdentityCredential,
)
from azure.storage.blob import BlobServiceClient

from ingenious.files.files_repository import IFileStorage
from ingenious.models.config import (
    AuthenticationMethod as file_storage_AuthenticationMethod,
)
from ingenious.models.config import Config, FileStorageContainer


class azure_FileStorageRepository(IFileStorage):
    def __init__(self, config: Config, fs_config: FileStorageContainer):
        self.config = config
        self.fs_config = fs_config
        self.url = fs_config.url
        self.token = fs_config.token
        self.client_id = fs_config.client_id
        self.container_name = fs_config.container_name
        self.authentication_method = fs_config.authentication_method

        # Check if token is actually a connection string
        if self.token and "DefaultEndpointsProtocol" in self.token:
            # Use connection string authentication
            self.blob_service_client = BlobServiceClient.from_connection_string(
                self.token
            )
        elif self.authentication_method == file_storage_AuthenticationMethod.TOKEN:
            self.blob_service_client = BlobServiceClient(
                account_url=self.url, credential=self.token
            )

        if (
            self.authentication_method
            == file_storage_AuthenticationMethod.CLIENT_ID_AND_SECRET
        ):
            cred = ClientSecretCredential(self.client_id, self.token)
            self.blob_service_client = BlobServiceClient(
                account_url=self.url, credential=cred
            )

        if self.authentication_method == file_storage_AuthenticationMethod.MSI:
            self.blob_service_client = BlobServiceClient(
                account_url=self.url,
                credential=ManagedIdentityCredential(client_id=self.client_id),
            )
            print("======")
            print(self.client_id, self.url)

        if (
            self.authentication_method
            == file_storage_AuthenticationMethod.DEFAULT_CREDENTIAL
        ):
            self.blob_service_client = BlobServiceClient(
                account_url=self.url, credential=DefaultAzureCredential()
            )

    async def write_file(self, contents: str, file_name: str, file_path: str):
        """
        Asynchronously writes the given contents to a file in Azure Blob Storage.
        Args:
            contents (str): The contents to write to the file.
            file_name (str): The name of the file to write.
            file_path (str): The path within the storage container where the file will be written.
        Raises:
            Exception: If there is an error during the upload process.
        Example:
            await write_file("Hello, World!", "example.txt", "path/to/directory")
        """
        try:
            path = Path(self.fs_config.path) / Path(file_path) / Path(file_name)
            # Create the container if it does not exist
            container_client = self.blob_service_client.get_container_client(
                self.container_name
            )
            if not container_client.container_name:
                container_client.create_container()

            # Create a blob client
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=str(path)
            )

            # Upload the data
            blob_client.upload_blob(contents, overwrite=True)
            # print(f"Successfully uploaded {path} to container {self.container_name}.")
        except Exception as e:
            print(f"Failed to upload {path} to container {self.container_name}: {e}")

    async def read_file(self, file_name: str, file_path: str) -> str:
        """
        Download data from Azure Blob Storage.

        :param file_name: Name of the blob (file) to read.
        :param file_path: Path of the blob (file) to read.
        """

        try:
            path = Path(self.fs_config.path) / Path(file_path) / Path(file_name)
            print(path)
            # Create a blob client
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=str(path)
            )

            # encoding param is necessary for readall() to return str, otherwise it returns bytes
            downloader = blob_client.download_blob(max_concurrency=1, encoding="UTF-8")
            data = downloader.readall()

            # print(f"Successfully downloaded {path} from container {self.container_name}.")
            return data
        except Exception as e:
            print(
                f"Failed to download {path} from container {self.container_name}: {e}"
            )
            return ""

    async def delete_file(self, file_name: str, file_path: str):
        """
        Delete a blob from Azure Blob Storage.

        :param file_name: Name of the blob (file) to delete.
        :param file_path: Path of the blob (file) to delete.
        """

        try:
            path = Path(self.fs_config.path) / Path(file_path) / Path(file_name)
            # Create a blob client
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=str(path)
            )

            # Delete the blob
            blob_client.delete_blob()
            # print(f"Successfully deleted {path} from container {self.container_name}.")
        except Exception as e:
            print(f"Failed to delete {path} from container {self.container_name}: {e}")

    async def list_files(self, file_path: str):
        """
        List blobs in an Azure Blob container based on a path.

        :param file_path: Path within the storage container to list blobs from.
        """
        blobs = []
        try:
            path = Path(self.fs_config.path) / Path(file_path)
            prefix = str(path).replace(
                "\\", "/"
            )  # Ensure the path is in the correct format for Azure
            # List blobs in the container with the specified prefix
            container_client = self.blob_service_client.get_container_client(
                self.container_name
            )
            blobs = [
                blob.name
                for blob in container_client.list_blobs(name_starts_with=prefix)
            ]
            # print(f"Blobs in container {self.container_name} with prefix {prefix}: {blobs}")
            return blobs
        except Exception as e:
            print(
                f"Failed to list blobs in container {self.container_name} with prefix {prefix}: {e}"
            )
            return []

    async def check_if_file_exists(self, file_path: str, file_name: str) -> bool:
        """
        Check if a blob exists in an Azure Blob container.

        :param container_name: Name of the Azure Blob container.
        :param blob_name: Name of the blob (file) to check.
        :param connection_string: Connection string to Azure Storage account.
        :return: True if the blob exists, False otherwise.
        """

        try:
            path = Path(self.fs_config.path) / Path(file_path) / Path(file_name)
            # Create a blob client
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=str(path)
            )
            exists = blob_client.exists()
            # print(f"Blob {path} exists in container {self.container_name}: {exists}")
            return exists
        except Exception as e:
            print(
                f"Failed to check if blob {path} exists in container {self.container_name}: {e}"
            )
            return False

    async def get_base_path(self) -> str:
        """
        Get the base path of the Azure Blob container.

        :return: Base path of the Azure Blob container.
        """
        return self.url + "/" + self.fs_config.path
