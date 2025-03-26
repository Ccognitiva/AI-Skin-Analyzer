import os
import gdown

def download_and_extract_dataset(dataset_url: str, dataset_folder: str = "dataset", dataset_zip: str = "dataset.zip"):
    """
    Downloads and extracts the dataset if not already present.

    :param dataset_url: Google Drive URL of the dataset.
    :param dataset_folder: Folder where the dataset should be extracted.
    :param dataset_zip: Temporary ZIP file name.
    """
    if not os.path.exists(dataset_folder):
        print(f"Dataset not found. Downloading from {dataset_url}...")
        gdown.download(dataset_url, dataset_zip, quiet=False)

        print("Extracting dataset...")
        os.system(f"unzip {dataset_zip} -d .")

        print("Cleaning up...")
        os.remove(dataset_zip)

        print(f"Dataset ready in '{dataset_folder}'")
    else:
        print(f"Dataset already exists in '{dataset_folder}'. Skipping download.")

