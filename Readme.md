
## Group details
```
Group Number - 1 
Names -
Anchal Rajawat    231000001
Ayush Menon       231000002
Abhi Ranjan       231000003
Aditya Singh      231000004
Aditya Nayak      231000005
```
## Explanation Video
[Watch the video](./ExplainationVideo_Grp-1.mp4)


# REST-Based Distributed Key-Value Store (Node A + Node B)
This project is a simple implementation of a REST-based distributed key-value store with primary–replica replication, built using Python + Flask.

## What is This Project?
This project demonstrates how a primary node (Node A) handles writes and replicates them to a secondary node (Node B).  
Node B can also simulate failures to test consistency and fault handling.

## System Architecture (Short Description)
- Node A handles PUT/GET requests, stores the data locally, and forwards updates to Node B.
- Node B stores replicated values and can return failures when needed.
- Node A keeps track of replication success/failure using a `/status/<key>` endpoint.
- A simple HTML UI is provided for testing.

## Folder Structure
```
project/
│
├── code/
│   ├── NodeA.py
│   ├── NodeB.py
│   └── UI/
│       └── Index.html
│
└── README.md
```

## How to Install Dependencies

Install required packages:
```bash
pip install flask requests
```

## How to Run the Project

### 1. Run Node B (Replica)
Open Terminal 1: (inside the project folder)
```bash
cd code
python node_b.py
```
Runs on: `http://localhost:5001`

### 2. Run Node A (Primary)
Open Terminal 2: (inside the project folder)
```bash
cd code
python node_a.py
```
Runs on: `http://localhost:5000`

### 3. Open the UI (Optional)
Open:
```
code/ui/index.html
```
Or run:
```bash
cd ui
python -m http.server 8000
```
Then visit:
```
http://localhost:8000
```

## Testing the Endpoints
You can test the API using **Windows PowerShell**, **curl**, or the **simple HTML UI** included in the project.  
A GUI option like **Postman** can also be used to send the same requests.

Below are the example commands for each operation.

---

### ✔ PUT (Node A → Node B)
Store a key-value pair on Node A and trigger replication.

#### PowerShell:
```powershell
Invoke-RestMethod -Method Put `
  -Uri "http://localhost:5000/key/foo" `
  -ContentType "application/json" `
  -Body '{"value":"hello"}'
```

#### curl:
```bash
curl -X PUT http://localhost:5000/key/foo \
     -H "Content-Type: application/json" \
     -d "{\"value\":\"hello\"}"
```

---

### ✔ GET from Node A
Retrieve the value stored on Node A.

#### PowerShell:
```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:5000/key/foo"
```

#### curl:
```bash
curl http://localhost:5000/key/foo
```

---

### ✔ GET from Node B (check replication)
Retrieve the value from the replica node.

#### PowerShell:
```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:5001/key/foo"
```

#### curl:
```bash
curl http://localhost:5001/key/foo
```

---

### ✔ Check Replication Status (Node A)
Shows whether replication succeeded or failed.

#### PowerShell:
```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:5000/status/foo"
```

#### curl:
```bash
curl http://localhost:5000/status/foo
```

---

### ✔ Simulate Failure on Node B
Send `"__fail__"` as value → Node B returns HTTP 500.  
Node A marks replication as **replication_failed**.

#### PowerShell:
```powershell
Invoke-RestMethod -Method Put `
  -Uri "http://localhost:5000/key/bad" `
  -ContentType "application/json" `
  -Body '{"value":"__fail__"}'
```

#### curl:
```bash
curl -X PUT http://localhost:5000/key/bad \
     -H "Content-Type: application/json" \
     -d "{\"value\":\"__fail__\"}"
```

---

## Summary
This project demonstrates:
- REST communication between two nodes  
- Primary–replica replication  
- Failure simulation using special values  
- Consistency checking through status endpoint  
- A simple browser-based UI for easy manual testing  


