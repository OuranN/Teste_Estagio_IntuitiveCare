import zipfile
import os

RAW_DIR = "data/test1/raw"
EXTRACTED_DIR = "data/test1/extracted"


def extract_all_zips():
    os.makedirs(EXTRACTED_DIR, exist_ok=True)

    extracted_files = []

    for file in os.listdir(RAW_DIR):
        if file.endswith(".zip"):
            zip_path = os.path.join(RAW_DIR, file)

            print(f"Extraindo {file}...")

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(EXTRACTED_DIR)

                extracted_files.extend(zip_ref.namelist())

    return extracted_files
