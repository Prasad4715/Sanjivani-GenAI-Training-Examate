
import requests
import certifi

from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


DOCUMENTS = {
    "motor_vehicles_amendment_act_2019.pdf":
        "https://cdnbbsr.s3waas.gov.in/s35dec707028b05bcbd3a1db5640f842c5/uploads/2025/01/20250108736472987.pdf",

    "maharashtra_motor_vehicles_rules_1989.pdf":
        "https://cdnbbsr.s3waas.gov.in/s35dec707028b05bcbd3a1db5640f842c5/uploads/2025/01/20250108634391784.pdf",

    "central_motor_vehicles_rules_1989.pdf":
        "https://cdnbbsr.s3waas.gov.in/s3d827f12e35eae370ba9c65b7f6026695/uploads/2025/01/20250113894003487.pdf"
}


def create_session():

    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)

    session.headers.update({
        "User-Agent": "ChalanCheck-DocumentFetcher/1.0"
    })

    return session


def download_document(session, filename, url):

    file_path = RAW_DIR / filename
    temporary_path = RAW_DIR / (filename + ".part")

    try:

        print(f"\nDownloading: {filename}")

        with session.get(
            url,
            timeout=(15, 120),
            verify=certifi.where(),
            stream=True
        ) as response:

            response.raise_for_status()

            with open(temporary_path, "wb") as file:

                for chunk in response.iter_content(
                    chunk_size=8192
                ):

                    if chunk:
                        file.write(chunk)

        # Validate PDF signature
        with open(temporary_path, "rb") as file:
            signature = file.read(5)

        if signature != b"%PDF-":
            raise ValueError("Downloaded file is not a valid PDF.")

        temporary_path.replace(file_path)

        print(f"Successfully downloaded: {filename}")
        print(f"File size: {file_path.stat().st_size} bytes")

        return True

    except requests.exceptions.SSLError as error:
        print(f"SSL Certificate Error: {error}")

    except requests.exceptions.Timeout:
        print(f"Download timed out: {filename}")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP Error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Network Error: {error}")

    except (OSError, ValueError) as error:
        print(f"File/PDF Error: {error}")

    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    return False


def fetch_documents():

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    session = create_session()

    successful = 0
    failed = 0

    try:

        for filename, url in DOCUMENTS.items():

            result = download_document(
                session,
                filename,
                url
            )

            if result:
                successful += 1
            else:
                failed += 1

    finally:
        session.close()

    print("\nDownload Summary")
    print("----------------")
    print("Total:", len(DOCUMENTS))
    print("Successful:", successful)
    print("Failed:", failed)


if __name__ == "__main__":
    fetch_documents()
