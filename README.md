---

## 🧩 String Analysis & Filtering API

A FastAPI-based REST API that analyzes strings and provides powerful filtering features — including **palindrome detection**, **character statistics**, and **natural language query filtering**.

---

## 🚀 Features

✅ Analyze any string and store its properties in MongoDB
✅ Compute properties such as:

* Length
* Word count
* Unique characters
* Character frequency
* Palindrome status
  ✅ Filter stored strings using:
* **Query parameters** (e.g. `is_palindrome`, `min_length`, etc.)
* **Natural language queries** (e.g. *“all single word palindromic strings”*)
  ✅ Retrieve, view, and delete analyzed strings

---

## 🛠️ Tech Stack

| Component      | Description                                 |
| -------------- | ------------------------------------------- |
| **FastAPI**    | Python web framework for APIs               |
| **MongoDB**    | NoSQL database for storing string documents |
| **Pydantic**   | Data validation and serialization           |
| **Uvicorn**    | ASGI server for running FastAPI             |
| **re (Regex)** | Used for parsing natural language filters   |

---

## 📁 Project Structure

```
app/
│
├── main.py
├── routes/
│   └── strings.py             # Contains all string endpoints
│
├── utils/
│   └── helper.py              # Helper functions for string analysis
│
├── models/
│   └── model.py               # Pydantic models (Strings, Analyze_string)
│
├── config/
│   └── config.py              # MongoDB connection (string_collection)
│
└── requirements.txt
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/string-analysis-api.git
cd string-analysis-api
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure MongoDB

In `app/config/config.py`, set up your MongoDB connection:

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["string_db"]
string_collection = db["strings"]
```

Or use an environment variable:

```python
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["string_db"]
string_collection = db["strings"]
```

### 5️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

> 🚀 App will start on **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧪 API Endpoints

### 📍 1. POST `/strings`

Analyze and store a new string.

#### Request Body:

```json
{
  "value": "madam"
}
```

#### Success Response (201 Created)

```json
{
  "id": "5d41402abc4b2a76b9719d911017c592",
  "value": "madam",
  "properties": {
    "length": 5,
    "is_palindrome": true,
    "unique_characters": 3,
    "word_count": 1,
    "sha256_hash": "hash_here",
    "character_frequency_map": { "m": 2, "a": 2, "d": 1 }
  }
}
```

#### Error Responses:

* `400 Bad Request`: Missing or invalid value
* `409 Conflict`: String already exists in the system
* `422 Unprocessable Entity`: Invalid data type for "value"(must be string)

---

### 📍 2. GET `/strings`

Filter stored strings using query parameters.

#### Example:

```
/strings?is_palindrome=true&min_length=5&max_length=10&contains_character=a
```

#### Success Response:

```json
{
  "data": [ /* array of matched strings */ ],
  "count": 3,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5,
    "max_length": 10,
    "contains_character": "a"
  }
}
```

#### Error:

`404 Not Found` – No results or invalid filter values.

---

### 📍 3. GET `/strings/filter-by-natural-language`

Filter strings using plain English queries.

#### Examples:

| Query                                              | Filters Applied                            |
| -------------------------------------------------- | ------------------------------------------ |
| `all single word palindromic strings`              | `word_count=1, is_palindrome=true`         |
| `strings longer than 10 characters`                | `min_length=11`                            |
| `palindromic strings that contain the first vowel` | `is_palindrome=true, contains_character=a` |
| `strings containing the letter z`                  | `contains_character=z`                     |

#### Example Request:

```bash
curl "http://127.0.0.1:8000/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings"
```

#### Success Response:

```json
{
  "data": [ /* matched strings */ ],
  "count": 3,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
```

#### Errors:

* `400 Bad Request`: Unable to parse natural language query
* `404 Not Found`: No results
* `422 Unprocessable Entity`: Conflicting filters

---

### 📍 4. GET `/strings/{string_value}`

Retrieve the analysis for a specific string.

#### Example:

```
/strings/hello
```

#### Success:

```json
{
  "id": "sha256_hash_here",
  "value": "hello",
  "properties": { ... },
  "created_at": "2025-08-27T10:00:00Z"
}
```

#### Error:

`404 Not Found` – String not found in the database.

---

### 📍 5. DELETE `/strings/{string_value}`

Delete a specific string.

#### Example:

```
DELETE /strings/hello
```

#### Response:

`204 No Content`

---

## 🧠 Helper Functions (in `helper.py`)

* `length(string)`: Returns string length
* `is_palindrome(string)`: Checks if palindrome
* `unique_characters(string)`: Counts unique characters
* `word_count(string)`: Returns number of words
* `sha256_hash(string)`: Generates unique SHA-256 hash
* `character_frequency_map(string)`: Returns a dict of char frequencies

---

## 🧰 Development Tools

| Tool                | Command                                                    |
| ------------------- | ---------------------------------------------------------- |
| Run FastAPI app     | `uvicorn app.main:app --reload`                            |
| Access Swagger Docs | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)   |
| Access ReDoc        | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) |

---


## 🧑‍💻 Author

**Rashid**
Software Engineer
📧 Contact: [[rashidsamadina@gmail.com](mailto:rashidsamadina@gmail.com)]

---

