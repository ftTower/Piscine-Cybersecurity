# ftp_client_test.py
import ftplib
import os
import time

FTP_HOST = "localhost" # Or the IP of your Docker host if connecting externally, or 'ftp_server' if running from another container on the same network
FTP_PORT = 21
FTP_USER = "ftpuser"
FTP_PASS = "ftppassword"
TEST_FILE_UPLOAD = "upload_test.txt"
TEST_FILE_DOWNLOAD = "download_test.txt"

def create_test_files():
    print(f"Creating {TEST_FILE_UPLOAD}...")
    with open(TEST_FILE_UPLOAD, "w") as f:
        f.write("This is a test file to upload.\n")
        f.write("It contains multiple lines for observation.\n")
    print(f"Creating {TEST_FILE_DOWNLOAD} on server (simulated)...")
    # We'll rely on the server having a file, or upload one and then download it
    # For a fresh server, let's create it locally first and upload it.
    # To test download, ensure this file exists on the FTP server's mounted volume (./data)
    with open("./data/" + TEST_FILE_DOWNLOAD, "w") as f:
        f.write("This file was already on the FTP server for download testing.\n")

def connect_and_transfer():
    ftp = None
    try:
        print(f"Connecting to FTP server at {FTP_HOST}:{FTP_PORT}...")
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        print("Login successful!")

        # List files on the server
        print("\nFiles on server:")
        ftp.dir()

        # Upload a file
        print(f"\nUploading {TEST_FILE_UPLOAD}...")
        with open(TEST_FILE_UPLOAD, "rb") as fp:
            ftp.storbinary(f"STOR {TEST_FILE_UPLOAD}", fp)
        print(f"Uploaded {TEST_FILE_UPLOAD}.")

        # List files again to confirm upload
        print("\nFiles on server after upload:")
        ftp.dir()

        # Download a file
        print(f"\nDownloading {TEST_FILE_DOWNLOAD}...")
        with open(f"downloaded_{TEST_FILE_DOWNLOAD}", "wb") as fp:
            ftp.retrbinary(f"RETR {TEST_FILE_DOWNLOAD}", fp.write)
        print(f"Downloaded downloaded_{TEST_FILE_DOWNLOAD}.")

        # Rename a file (for observing control channel commands)
        old_name = TEST_FILE_UPLOAD
        new_name = "renamed_test_file.txt"
        print(f"\nRenaming {old_name} to {new_name}...")
        ftp.rename(old_name, new_name)
        print(f"Renamed {old_name} to {new_name}.")

        # Delete a file (for observing control channel commands)
        print(f"\nDeleting {new_name}...")
        ftp.delete(new_name)
        print(f"Deleted {new_name}.")

        print("\nFTP operations completed successfully.")

    except ftplib.all_errors as e:
        print(f"FTP Error: {e}")
    except ConnectionRefusedError:
        print(f"Connection refused. Ensure the FTP server is running on {FTP_HOST}:{FTP_PORT}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if ftp:
            ftp.quit()
            print("FTP connection closed.")

if __name__ == "__main__":
    # Ensure the data directory exists for the server
    os.makedirs("./data", exist_ok=True)
    create_test_files()
    time.sleep(1) # Give a moment for files to be written

    print("\n--- Starting FTP Client Test ---")
    connect_and_transfer()
    print("--- FTP Client Test Finished ---")

    # Clean up local test files
    if os.path.exists(TEST_FILE_UPLOAD):
        os.remove(TEST_FILE_UPLOAD)
    if os.path.exists(f"downloaded_{TEST_FILE_DOWNLOAD}"):
        os.remove(f"downloaded_{TEST_FILE_DOWNLOAD}")