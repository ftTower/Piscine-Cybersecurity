# Vaccine - SQL Injection Detection Tool

**Vaccine** is a command-line tool for detecting SQL injection vulnerabilities in web applications. It offers a comprehensive suite of tests, including time-based and error-based injections, and can identify the underlying database engine. If a vulnerability is found, Vaccine can extract valuable information such as vulnerable parameters, database names, table names, column names, and (planned) perform a complete database dump.

---

## Features

- **SQL Injection Detection**: Identifies vulnerabilities using multiple techniques.
- **Database Engine Identification**: Automatically detects the database engine (MySQL, PostgreSQL, SQL Server, Oracle, SQLite) to tailor injection attempts.
- **Multiple Injection Methods**: Supports both time-based and error-based SQL injection.
- **Vulnerable Parameter Identification**: Pinpoints which URL parameters are susceptible.
- **Information Extraction**:
    - Vulnerable parameters and payloads used
    - Database names
    - Table names
    - Column names
    - Complete database dump *(planned)*
- **HTTP Method Support**: Supports both GET and POST requests.
- **Data Storage**: Stores scan results in a specified or default archive file.

---

## Getting Started

### Prerequisites

- Python 3.x
- `pip` (Python package installer)
- `make` (for Makefile commands)
- Docker (for setting up the SQLi-Labs environment)
- Required Python libraries: `requests`, `selenium`, `urllib.parse`

### Installation

1. **Clone the repository:**
     ```bash
     git clone https://github.com/your-username/vaccine.git
     cd vaccine
     ```

2. **Install Python dependencies:**
     ```bash
     pip install -r requirements.txt
     ```

3. **(Optional) Setup SQLi-Labs for Testing:**
     This project includes a Makefile target to set up a local SQLi-Labs environment using Docker for safe, legal testing.
     ```bash
     make labs
     ```
     The lab will be accessible at [http://localhost:1338/](http://localhost:1338/).

---

## Configuration

By default, scan results are stored in a default file unless the `-o` option is specified. You can configure this file in `utils/utils.py` or `core/main.py` if needed.

---

## Usage

Run Vaccine from the command line:

```bash
./vaccine [-o <archive_file>] [-X <request_type>] URL
```

**Options:**
- `-o <archive_file>`: Output file for scan results (default: `results.json`)
- `-X <request_type>`: HTTP method (`GET` or `POST`, default: `GET`)

**Examples:**

- Basic GET request scan:
    ```bash
    ./vaccine http://localhost:1338/Less-1/
    ```

- Scan with POST method and custom output file:
    ```bash
    ./vaccine -X POST -o my_scan_results.json http://localhost:1338/Less-11/
    ```

- Running with `make` (after setting up labs):
    ```bash
    make run
    ```
    This executes: `python3 ./core/main.py http://localhost:1338/`

---

## Project Structure

```
core/
    main.py               # Main entry point
navigation/
    crawler.py            # Web crawler for URL discovery
injection/
    get_db_detector.py    # DB detection & vulnerabilities via GET
    post_db_detector.py   # (Planned) DB detection via POST
    get_inject.py         # (Planned) Detailed GET injection
    post_inject.py        # (Planned) Detailed POST injection
utils/
    ainsi.py              # Colored output
    utils.py              # File operations, helpers
Makefile                # Build, clean, run commands
```

---

## Makefile Commands

- `make labs`: Set up SQLi-Labs Docker environment
- `make clean_labs`: Tear down SQLi-Labs Docker environment
- `make run`: Run the main script with a predefined URL
- `make clean`: Remove Python bytecode and `__pycache__`
- `make fclean`: Clean project and labs
- `make re`: Rebuild and restart everything

---

## Disclaimer

**For educational and authorized penetration testing only.**  
Do not use this tool on systems without explicit permission. Unauthorized testing is illegal and unethical. The authors are not responsible for misuse or damage caused by this tool.
