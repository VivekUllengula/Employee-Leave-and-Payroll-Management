Employee Leave & Payroll Management System

📌 Project Overview
The Employee Leave & Payroll Management System is a backend application built with FastAPI and MongoDB.
It enables organizations to:
Manage employee records,
Handle leave requests and approvals,
Automate monthly payroll calculation with leave-based deductions,
Secure access with JWT authentication and role-based control (Admin/HR).

✨ Features
👨‍💼 Employee Management – Add, update, and manage employee records.
🗓️ Leave Management – Apply, approve, and track employee leaves.
💰 Payroll Automation – Auto-calculates payroll based on attendance & leaves.
🔒 Authentication & Authorization – JWT-secured login with role-based access (Admin, HR).
📊 Scalable Design – Modular architecture (Routes, Services, Models, Utils).

🛠️ Tech Stack
Backend: Python (FastAPI)
Database: MongoDB (via PyMongo/Motor)
Authentication: JWT, OAuth2PasswordBearer
Validation: Pydantic
Optional Frontend: React / Swagger UI

📂 Project Structure
app/
│── core/         # Configurations│── db/           # MongoDB connection│── models/       # Pydantic schemas│── routes/       # API endpoints│── services/     # Business logic (employees, leaves, payroll, users)│── utils/        # Auth, password hashing, token generation 

⚙️ Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/VivekUllengula/Employee-Leave-and-Payroll-Management.gitcd Employee-Leave-and-Payroll-Management

2️⃣ Create Virtual Environment & Install Dependencies
conda create -n payroll python=3.11 -y
conda activate payroll
pip install -r requirements.txt

3️⃣ Run MongoDB
Make sure MongoDB is running locally (or update connection in app/core/config.py).

4️⃣ Start the Server
uvicorn app.main:app --reload

5️⃣ Access API Docs
Swagger UI → http://127.0.0.1:8000/docs
Redoc → http://127.0.0.1:8000/redoc

🚀 API Endpoints
👤 User Authentication
POST /auth/register → Register user (Admin/HR)
POST /auth/login → Login & get JWT

👨‍💼 Employees
POST /employees/ → Add employee
GET /employees/ → Get all employees
PUT /employees/{id} → Update employee
DELETE /employees/{id} → Delete employee

🗓️ Leaves
POST /leaves/ → Apply for leave
GET /leaves/employee/{id} → View employee leaves
PUT /leaves/{id} → Update leave status

💰 Payroll
POST /payrolls/calculate/{employee_id} → Auto-calculate payroll
GET /payrolls/employee/{id} → View payroll history

📊 System Design
🔹 Architecture
flowchart TD
    User[User/Admin/HR] -->|Request| FastAPI
    FastAPI --> Routes
    Routes --> Services
    Services --> MongoDB[(MongoDB Database)]
    Services --> Auth[Auth & JWT Utils]
🔹 Database Schema
erDiagram
    USERS {
        string _id
        string email
        string hashed_password
        string full_name
        string role
    }
    EMPLOYEES {
        string _id
        string name
        string designation
        float salary
    }
    LEAVES {
        string _id
        string employee_id
        date start_date
        date end_date
        string status
    }
    PAYROLLS {
        string _id
        string employee_id
        string month
        float base_salary
        int leave_days
        float deductions
        float net_salary
    }
    USERS ||--o{ EMPLOYEES : manages
    EMPLOYEES ||--o{ LEAVES : applies
    EMPLOYEES ||--o{ PAYROLLS : receives
🔹 Leave & Payroll Workflow
flowchart LR
    A[Employee Applies Leave] --> B[HR/Admin Reviews Leave]
    B -->|Approved| C[Leave Recorded]
    B -->|Rejected| D[Leave Rejected]
    C --> E[Payroll Calculation]
    E --> F{Leaves > 2?}
    F -->|Yes| G[Deduct Salary]
    F -->|No| H[Full Salary]
    G --> I[Generate Payroll]
    H --> I[Generate Payroll]
🧪 Testing
Use Postman or Swagger UI to test APIs.
Example:
POST /auth/register{"email": "admin@example.com","password": "admin123","full_name": "Admin User","role": "admin" } 
📌 Future Enhancements
✅ Full-featured frontend (React / Next.js).
✅ Employee dashboards with salary slips.
✅ Email/SMS notifications for payroll and leave status.
✅ Integration with external HRMS systems.

🙌 Contributors
Vivek Ullengula (Developer)
Amit Parse (Trainer/Guide)