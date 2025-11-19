# Virtuous-Aplos Sync API

This application is a lightweight **API service** designed to **synchronize data between Virtuous and Aplos**, helping streamline financial and donor-management workflows.

It is built with [**Flask**](https://flask.palletsprojects.com/en/stable/) and is easy to set up locally using a Python virtual environment

## Setup Instructions

### 1. Create and Activate a Virtual Environment

```bash
cd path/to/your/project
py -m venv venv
venv/Scripts/activate.bat
```

### 2. Install Project Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Use Flask's built-in server to start the API.

```bash
flask --app app run
```

The API will start on:

```
http://127.0.0.1:5000
```

### Notes

- Ensure your environment variables (API keys, secrets, etc.) are properly set before running the app.
