# ALX_prodev Database Seed Script

This project contains a Python script (`seed.py`) that implements a simple ETL pipeline to download user data from S3 and load it into a MySQL database.

## 🚀 Features

- **Download CSV from S3** - Fetches dataset using Python's `requests` library
- **Automatic Database Setup** - Creates database and table if they don't exist
- **UUID Generation** - Automatically generates unique UUID for each user
- **Duplicate Prevention** - Uses `INSERT IGNORE` with unique email constraint
- **CSV Ingestion** - Reads data with proper field mapping using `csv.DictReader()`

## 🗄️ Database Schema

The `user_data` table structure:

| Field   | Type          | Description                     |
|---------|---------------|---------------------------------|
| user_id | CHAR(36)      | Primary Key (UUID)             |
| name    | VARCHAR(255)  | User's name (required)         |
| email   | VARCHAR(255)  | User's email (unique + required)|
| age     | INT           | Age (unsigned, required)       |

## 📂 File Structure
project/
│-- seed.py
│-- user_data.csv # Automatically downloaded
│-- README.md

text

## 🧠 How the Script Works

### 1. Extract - Download the CSV
```python
response = requests.get(url)
with open("user_data.csv", "w", encoding="utf-8") as f:
    f.write(response.text)
2. Transform - Process Data
Generate UUID for each user

Map CSV fields to database columns

Handle data type conversions

3. Load - Database Operations
python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)

user_id = str(uuid.uuid4())
cursor.execute(query, (user_id, row["name"], row["email"], row["age"]))
🛠️ How to Run
1. Install Dependencies
bash
pip install mysql-connector-python requests
2. Ensure MySQL is Running
Make sure your MySQL server is active and accessible.

3. Run the Script
bash
python3 seed.py
4. Expected Output
text
ALX_prodev Database successfully created
Table 'user_data' created successfully
🔍 Example Output
Using a test script, you can verify the inserted data:

python
[('uuid...', 'John Doe', 'example@mail.com', 34), (...)]
📬 Important Notes
The CSV URL contains temporary access credentials that will expire

INSERT IGNORE prevents duplicate emails from crashing the script

Safe to rerun - won't create duplicate rows due to unique email constraint

Age field uses unsigned INT to prevent negative values

✅ Summary
This project demonstrates real backend engineering skills including:

File handling and HTTP requests

MySQL database creation and management

UUID generation and primary key design

Safe CSV data ingestion

Error handling and duplicate prevention

Basic ETL pipeline design

SQL table design with proper constraints

🔧 Technical Details
Database: MySQL

Primary Key: UUID (Universally Unique Identifier)

Unique Constraint: Email field

Data Validation: Required fields and proper data types

Error Handling: Graceful handling of duplicates and connection issues

The script provides a robust foundation for data ingestion pipelines and can be easily extended for more complex ETL processes.