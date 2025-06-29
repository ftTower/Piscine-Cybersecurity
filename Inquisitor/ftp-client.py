# ftp_client_test.py
import ftplib
import os
import time

# ... (FTP_HOST, FTP_PORT, FTP_USER, FTP_PASS, etc. remain the same) ...

def create_test_files():
    print(f"Creating {TEST_FILE_UPLOAD}...")
    with open(TEST_FILE_UPLOAD, "w") as f:
        f.write("This is a test file to upload.\n")
        f.write("It contains multiple lines for observation.\n")
    print(f"Creating {TEST_FILE_DOWNLOAD} on server (simulated)...")
    # This file needs to be in the root of the chroot directory for the FTP user
    # which corresponds to the ./data folder on the host.
    with open("./data/" + TEST_FILE_DOWNLOAD, "w") as f: # This line is already correct for host path
        f.write("This file was already on the FTP server for download testing.\n")

def connect_and_transfer():
    ftp = None
    try:
        print(f"Connecting to FTP server at {FTP_HOST}:{FTP_PORT}...")
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        print("Login successful!")

        # After login, the FTP user is typically in their home directory,
        # which is also their chroot directory.
        # Let's change to the 'ftp_data' subdirectory first.
        # The 'ftp_data' directory exists inside the chroot because of the volume mount.
        print("Changing current directory on FTP server to /ftp_data...")
        ftp.cwd("ftp_data") # <--- ADD THIS LINE!

        # List files on the server (now within /ftp_data)
        print("\nFiles on server (in /ftp_data):")
        ftp.dir()

        # Upload a file
        print(f"\nUploading {TEST_FILE_UPLOAD} to /ftp_data...")
        with open(TEST_FILE_UPLOAD, "rb") as fp:
            ftp.storbinary(f"STOR {TEST_FILE_UPLOAD}", fp)
        print(f"Uploaded {TEST_FILE_UPLOAD}.")

        # List files again to confirm upload
        print("\nFiles on server after upload (in /ftp_data):")
        ftp.dir()

        # Download a file
        print(f"\nDownloading {TEST_FILE_DOWNLOAD} from /ftp_data...")
        with open(f"downloaded_{TEST_FILE_DOWNLOAD}", "wb") as fp:
            ftp.retrbinary(f"RETR {TEST_FILE_DOWNLOAD}", fp.write)
        print(f"Downloaded downloaded_{TEST_FILE_DOWNLOAD}.")

        # Rename a file (for observing control channel commands)
        old_name = TEST_FILE_UPLOAD
        new_name = "renamed_test_file.txt"
        print(f"\nRenaming {old_name} to {new_name} in /ftp_data...")
        ftp.rename(old_name, new_name)
        print(f"Renamed {old_name} to {new_name}.")

        # Delete a file (for observing control channel commands)
        print(f"\nDeleting {new_name} from /ftp_data...")
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
    os.makedirs("./data", exist_ok=True)
    create_test_files()
    time.sleep(1)

    print("\n--- Starting FTP Client Test ---")
    connect_and_transfer()
    print("--- FTP Client Test Finished ---")

    if os.path.exists(TEST_FILE_UPLOAD):
        os.remove(TEST_FILE_UPLOAD)
    if os.path.exists(f"downloaded_{TEST_FILE_DOWNLOAD}"):
        os.remove(f"downloaded_{TEST_FILE_DOWNLOAD}")