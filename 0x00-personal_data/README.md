# 0x00. Personal data

This project focuses on protecting personal identifying information (PII) in application logs. It includes creating utility functions, formatters, loggers, and database operations that demonstrate secure handling of sensitive data.

## Tasks

### 0. Regex-ing

**File:** `filtered_logger.py`

- Implements `filter_datum(fields, redaction, message, separator)`
- Obfuscates sensitive fields using a single regex with `re.sub`

**Example:**
```python
fields = ["password", "date_of_birth"]
message = "name=bob;email=bob@dylan.com;password=secret;date_of_birth=03/04/1993;"
print(filter_datum(fields, 'xxx', message, ';'))
# Output: name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
```

---

### 1. Log formatter

**File:** `filtered_logger.py`

- Implements `RedactingFormatter` class
- Redacts values of specified fields in log messages using `filter_datum`
- Inherits from `logging.Formatter`

**Example:**
```python
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
record = logging.LogRecord("my_logger", logging.INFO, None, None, "email=bob@dylan.com;ssn=000-123-0000;password=secret;", None, None)
print(formatter.format(record))
# Output: [HOLBERTON] my_logger INFO YYYY-MM-DD HH:MM:SS: email=***;ssn=***;password=***;
```

---

### 2. Create logger

**File:** `filtered_logger.py`

- Implements `get_logger()` which returns a configured `logging.Logger`
- Logger name: `user_data`
- Logger has `StreamHandler` with `RedactingFormatter`
- No propagation
- Defines constant `PII_FIELDS` (tuple of 5 sensitive fields)

**Example:**
```python
logger = get_logger()
logger.info("name=Jane;email=jane@doe.com;ssn=123-45-6789;password=passwd123;phone=555-1234")
# Output: redacted log message
```

---

### 3. Connect to secure database

**File:** `filtered_logger.py`

- Implements `get_db()` that returns a `mysql.connector.connection.MySQLConnection` object
- Credentials fetched from environment variables:
  - `PERSONAL_DATA_DB_USERNAME` (default: `"root"`)
  - `PERSONAL_DATA_DB_PASSWORD` (default: `""`)
  - `PERSONAL_DATA_DB_HOST` (default: `"localhost"`)
  - `PERSONAL_DATA_DB_NAME`

**Example:**
```python
db = get_db()
cursor = db.cursor()
cursor.execute("SELECT * FROM users;")
```

---

### 4. Read and filter data

**File:** `filtered_logger.py`

- Implements `main()` function
- Connects to DB using `get_db`
- Fetches all rows from `users` table
- Logs each row using the redacting logger

**Fields to redact:**
- `name`
- `email`
- `phone`
- `ssn`
- `password`

**Execution:**
```bash
$ PERSONAL_DATA_DB_USERNAME=root PERSONAL_DATA_DB_PASSWORD=root PERSONAL_DATA_DB_HOST=localhost PERSONAL_DATA_DB_NAME=my_db ./filtered_logger.py
```

---

## Requirements

- Python 3.x
- `mysql-connector-python` (`pip install mysql-connector-python`)
- No credentials hardcoded
- Logging output must redact PII

## Author

OMAR MOHUMED 
