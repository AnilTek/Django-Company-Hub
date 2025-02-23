# 🏢 Django Company Management System

This project is built using Django

---

## 🚀 Features

✅ **Company & Employee Account Management**  
✅ **Multi-language Support (.mo & .po files)**  
✅ **Gmail Account Activation and Reset Password**  
✅ **Employees Can Be Linked to Multiple Companies**  
✅ **Companies Can Manage Their Employees**  
✅ **Service Requests and Document Management for Companies**  

---

## 📌 Installation

Follow these steps to set up and run the project.

### 1️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure the .env File
Since the project supports Gmail authentication, create a **.env** file and add the following details:
```ini
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
EMAIL_PORT=587
```
For security reasons, it's recommended to use an **App Password** instead of storing your actual email password.

### 4️⃣ Prepare the Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a Superuser
```bash
python manage.py createsuperuser
```

### 6️⃣ Access the Admin Panel
Once the superuser is created, you can log in to the Django admin panel to manage database entries easily. 
To access the admin panel, open your browser and navigate to:
```bash
http://127.0.0.1:8000/admin/
```
Log in using the superuser credentials you created earlier. Inside the panel, you can view, add, modify, or delete data in the database.

### 7️⃣ Compile Language Files
```bash
python manage.py compilemessages
```
This command converts **.po** files into **.mo** files to enable multi-language support.

### 8️⃣ Start the Server
```bash
python manage.py runserver
```

---

## 🛠 Usage

- **Companies** can add employees, request services, and track activities.
- **Employees** can be linked to multiple companies and create service requests.
- **Service Requests** become active once all required documents are completed.
- **Gmail Account Activation** ensures user verification.
- **Gmail Reset Account Password** allows users to change their password via email.

---

## 📂 Project Structure

```
📦 Django-yeni-1
├── 📂 aniltek                 # Company and employee management
├── 📂 users                   # User authentication (Company & Employee registration)
├── 📂 tek                     # Service requests and document handling
├── 📂 locale                  # Multi-language support files (.po & .mo files)
├── 📂 templates
├── 📂 static
├── 📂 media  
├── 📜 manage.py               # Django management tool
├── 📜 requirements.txt        # Dependencies list
└── 📜 README.md               # Project documentation
```

---

## 🌍 Multi-Language Support

This project supports multiple languages using Django's localization system.
- **To add a new language:**
```bash
python manage.py makemessages -l new_language_code
```
- **To compile language updates:**
```bash
python manage.py compilemessages
```

![Image](https://github.com/user-attachments/assets/7fae54e4-1e30-4d5b-aa4f-7224d91a3a9b)
