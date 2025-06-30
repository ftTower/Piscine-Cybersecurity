import ftplib
import os
import time

FTP_HOST = "localhost" 
FTP_PORT = 21
FTP_USER = "ftpuser"
FTP_PASS = "ftppassword"
TEST_FILE_UPLOAD = "upload_test.txt"
TEST_FILE_DOWNLOAD = "download_test.txt"

def create_test_files():
    original_umask = os.umask(0o000)
    try:
        with open(TEST_FILE_UPLOAD, "w") as f:
            f.write("This is a test file to upload.\n")
            f.write("It contains multiple lines for observation.\n")
        os.chmod(TEST_FILE_UPLOAD, 0o666)
        os.makedirs("./ftp_data", exist_ok=True)
        download_file_path_on_host = os.path.join("./data", TEST_FILE_DOWNLOAD)
        with open(download_file_path_on_host, "w") as f:
            f.write("This file was already on the FTP server for download testing.\n")
        os.chmod(download_file_path_on_host, 0o666)
    finally:
        os.umask(original_umask)
        
def connect_and_transfer():
    ftp = None
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.dir()
        with open(TEST_FILE_UPLOAD, "rb") as fp:
            ftp.storbinary(f"STOR {TEST_FILE_UPLOAD}", fp)
        ftp.dir()
        with open(f"downloaded_{TEST_FILE_DOWNLOAD}", "wb") as fp:
            ftp.retrbinary(f"RETR {TEST_FILE_DOWNLOAD}", fp.write)
        old_name = TEST_FILE_UPLOAD
        new_name = "renamed_test_file.txt"
        ftp.rename(old_name, new_name)
        ftp.delete(new_name)
    except ftplib.all_errors as e:
        print(f"FTP Error: {e}")
    except ConnectionRefusedError:
        print(f"Connection refused. Ensure the FTP server is running on {FTP_HOST}:{FTP_PORT}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if ftp:
            ftp.quit()

if __name__ == "__main__":
    os.makedirs("./data", exist_ok=True)
    create_test_files()
    time.sleep(1)
    connect_and_transfer()
    if os.path.exists(TEST_FILE_UPLOAD):
        os.remove(TEST_FILE_UPLOAD)
    if os.path.exists(f"downloaded_{TEST_FILE_DOWNLOAD}"):
        os.remove(f"downloaded_{TEST_FILE_DOWNLOAD}")
