# 🚀 FastAPI Backend for AI Skin Analyzer

This is the FastAPI backend for the AI Skin Analyzer project, handling authentication, skin analysis, user profile tracking, and more.

## **📌 Setup Instructions**

### **1️⃣ Create and Activate a Virtual Environment**

Before installing dependencies, it's recommended to create a virtual environment to keep the project isolated.

#### **🔹 On Windows (CMD or PowerShell)**

```sh
python -m venv venv
venv\Scripts\activate
```

#### **🔹 On macOS / Linux (Terminal)**

```sh
python3 -m venv venv
source venv/bin/activate
```

---

### **2️⃣ Install Dependencies**

Once the virtual environment is activated, install all required dependencies using:

```sh
pip install -r requirements.txt
```

This will install FastAPI, SQLAlchemy, CORS middleware, and other necessary packages.

---

### **3️⃣ Run the FastAPI App**

After installing dependencies, start the application using:

```sh
uvicorn main:app --reload
```

- The `--reload` flag enables automatic reloading when code changes (useful during development).
- By default, the app runs on **`http://127.0.0.1:8000`**.

---

### **4️⃣ Test the API**

Once the server is running, open your browser and visit:

- **Swagger UI:** 👉 `http://127.0.0.1:8000/docs`
- **Redoc UI:** 👉 `http://127.0.0.1:8000/redoc`

---

### **5️⃣ Environment Variables**

If the project requires environment variables (like database credentials), create a `.env` file in the project root and add:

```
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your_secret_key
```

Make sure to load this in the app using **python-dotenv**.

---

### **6️⃣ Database Migration (If Using SQLAlchemy & Alembic)**

If your project uses **SQLAlchemy and Alembic** for database migrations, initialize and run migrations:

```sh
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

### **7️⃣ Deployment Notes**

- **For Production:** Use `uvicorn main:app --host 0.0.0.0 --port 8000`.
- **For Docker:** If using Docker, ensure you have a `Dockerfile` and use `docker-compose up`.

---

### **📌 Additional Notes**

- Make sure to activate the virtual environment each time you work on the project.
- If dependencies change, update `requirements.txt` using:

```sh
pip freeze > requirements.txt
```
