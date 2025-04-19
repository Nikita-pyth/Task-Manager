# Task-Manager

A web-based task management system designed for collaborative project tracking. Team administrators can create tasks for their assigned projects and delegate them to team members.

## Features

- Project-based task organisation  
- Role-based access control (team admin vs. member)  
- Assign tasks within the scope of a team  
- UI with task creation per project context  

## Tech Stack

- **Backend**: Python, Django  
- **Frontend**: Django Template Engine  
- **Auth**: Session-based authentication  

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/task-manager-app.git
cd task-manager-app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Inside `settings.py` in the `config` application, set your secret key:

```python
SECRET_KEY = 'your_secret_key_here'
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.
