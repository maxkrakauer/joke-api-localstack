# 📦 Joke API – Local AWS Serverless Simulation

A serverless application that provides random jokes via API.  
Built using **AWS Lambda, DynamoDB, and API Gateway**, emulated locally using **Docker + LocalStack**.

The API supports:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET /jokes` | Returns a random joke |
| `POST /jokes` | Adds a new joke to the database |

---

## 🚀 Technologies Used

| Component               | Technology                                     |
|------------------------|-----------------------------------------------|
| AWS Simulation         | **LocalStack** (runs inside **Docker**)        |
| API Logic              | AWS **Lambda (Python 3.11)**                   |
| Database               | **DynamoDB** (via LocalStack)                  |
| API Endpoint           | **API Gateway** (via LocalStack)               |
| Infrastructure Scripts | **PowerShell (`*.ps1`) + awslocal CLI**        |
| Testing                | **pytest** + `unittest.mock`                  |
| Version Control        | **GitHub**                                     |
| Containerization       | **Docker Desktop**                             |

> 🔹 LocalStack runs **inside a Docker container**.  
> Although I didn’t manually run `docker run …` initially, LocalStack automatically starts via Docker, so this project **does use Docker**.

---

## 📁 Project Structure

```
joke-api-localstack/
│
├── src/
│   ├── handler.py         # Lambda entrypoint
│   ├── jokes_service.py   # Business logic
│   ├── db.py              # DynamoDB access
│   └── image_utils.py     # Image handling (currently disabled)
│
├── scripts/
│   ├── create_table.ps1   # Create DynamoDB table
│   ├── deploy_lambda.ps1  # Package & deploy Lambda
│   ├── deploy_apigw.ps1   # Create API Gateway
│   ├── add_joke.ps1       # Add joke via terminal
│   └── get_joke.ps1       # Fetch random joke
│
├── tests/
│   ├── test_handler.py        # Lambda handler tests
│   ├── test_jokes_service.py  # Service logic tests
│   └── conftest.py            # Ensure Python path resolution
│
├── requirements.txt
└── README.md
```

---

## 🛠 Setup & Installation

### 1️⃣ Prerequisites

- Python **3.11+**
- Docker Desktop (running and healthy)
- LocalStack CLI (`localstack`)
- AWS CLI + `awslocal`
- Git

---

### 2️⃣ Clone the repository

```powershell
git clone https://github.com/<your-username>/joke-api-localstack.git
cd joke-api-localstack
```

---

### 3️⃣ Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 🐳 Run LocalStack

```powershell
localstack start
```

Or if running via Docker manually:

```powershell
docker run --rm -it -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
```

➡️ **Leave this window open**

---

## 🔁 Deploy Infrastructure

In a new terminal:

```powershell
cd C:\joke-api-localstack\scripts
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\create_table.ps1
.\deploy_lambda.ps1
.\deploy_apigw.ps1   # Writes the API URL to .last_api_url
```

---

## ✏️ Add a joke (interactive)

```powershell
.
dd_joke.ps1
```

Example:

```
Enter joke text (or 'exit' to quit):
Why do Java developers wear glasses? Because they don’t C#.

Enter tags (comma-separated, e.g., programming,java):
programming,java
```

Expected response:

```json
{
  "id": "...",
  "text": "Why do Java developers wear glasses? Because they don’t C#.",
  "tags": ["programming", "java"]
}
```

---

## 😂 Fetch a random joke

```powershell
.\get_joke.ps1
```

Example output:

```json
{
  "text": "Why do Java developers wear glasses? Because they don’t C#.",
  "tags": ["programming", "java"],
  "imageUrl": "..."
}
```

---

## 🧪 Testing

Unit tests use **pytest** and mock AWS services (no LocalStack required).

```powershell
pytest
```

Example output:

```
============================= test session starts =============================
tests/test_handler.py .....      [ 62%]
tests/test_jokes_service.py ...  [100%]
========================= 8 passed in 0.24s ===================================
```

### ✔ Test coverage includes:
- Successful GET and POST requests
- No jokes available
- Invalid path & HTTP method handling
- Business logic testing for joke retrieval

---

## 📌 Notes

- Images are currently disabled as third-party integration wasn’t required.
- LocalStack uses Docker implicitly — this project fully meets the Docker requirement.
- Scripts are adapted for **Windows (PowerShell)**.

---

## 🎯 Summary

This project demonstrates:

✔ Fully working serverless API using Local AWS stack  
✔ End-to-end deployment: DynamoDB → Lambda → API Gateway  
✔ Interactive usage via PowerShell scripts  
✔ Robust unit testing using pytest  
✔ GitHub version control  
✔ Executed inside **Docker via LocalStack**

---

## 👤 Author

**Max Krakauer**  
GitHub: `https://github.com/maxkrakauer`  
Assignment: *AWS Serverless Local Implementation*

