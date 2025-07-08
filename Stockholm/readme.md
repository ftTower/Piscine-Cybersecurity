# Stockholm Ransomware Tool


## Description
Stockholm is a Python-based ransomware simulation tool designed for educational and cybersecurity training purposes. It encrypts files within a specified directory and provides functionality to decrypt them using a generated or provided key. The tool includes options for silent operation, version display, and help documentation.

## Features
- **File Encryption**: Encrypts all files in the specified directory using the `cryptography` library.
- **File Decryption**: Decrypts files using a provided decryption key.
- **Silent Mode**: Suppresses output to the terminal for a quieter operation.
- **Help Menu**: Displays usage instructions and available options.
- **Version Information**: Displays the current version of the tool and system information.

## Usage
Run the script with the following options:

![Stockholm](https://github.com/ftTower/Piscine-Cybersecurity/blob/main/.assets/Stockholm/need_help%3F.png)

### Options
- `--help` or `--h`: Display the help menu with usage instructions.
- `--version` or `--v`: Show the current version of the tool and system information.
- `--r <key>`: Reverse the encryption process using the provided decryption key.
- `--silent` or `--s`: Suppress output to the terminal.

### Example Commands


1. **Encrypt Files**:
    ```bash
    python3 stockholm.py
    ```
![Stockholm](https://github.com/ftTower/Piscine-Cybersecurity/blob/main/.assets/Stockholm/encryption.png)

![Stockholm](https://github.com/ftTower/Piscine-Cybersecurity/blob/main/.assets/Stockholm/files_encrypted.png)


2. **Decrypt Files**:
    ```bash
    python3 stockholm.py --reverse <decryption_key>
    ```
![Stockholm](https://github.com/ftTower/Piscine-Cybersecurity/blob/main/.assets/Stockholm/reverse.png)

> **Note:** The `make reverse` option is included for educational and security training purposes. It uses the `filekey.key` generated and stored during encryption. In a real ransomware attack, the decryption key would typically be deleted or withheld, making recovery without the key impossible.

![Stockholm](https://github.com/ftTower/Piscine-Cybersecurity/blob/main/.assets/Stockholm/files_content.png)

3. **Display Help**:
    ```bash
    python3 stockholm.py --help
    ```

4. **Show Version**:
    ```bash
    python3 stockholm.py --version
    ```

5. **Silent Mode**:
    ```bash
    python3 stockholm.py --silent
    ```

## How It Works
1. **Encryption**:
    - The tool generates a unique encryption key using the `cryptography` library.
    - All files in the specified directory (`Folders_to_encrypt`) are encrypted.
    - The encryption key is saved to a file named `filekey.key`.

2. **Decryption**:
    - The tool uses the provided decryption key to decrypt the files.
    - If the key is invalid, an error is raised.

3. **File Crawling**:
    - The tool recursively scans the specified directory to identify all files for encryption or decryption.

4. **Output**:
    - The tool displays the progress of encryption or decryption unless silent mode is enabled.

## Requirements
- Python 3.x
- Required Python libraries:
  - `cryptography`
  - `art`
  - `scanf`

Install the required libraries using pip:
