**Task Management Application**
Project Overview

We are enhancing the Task Management Application by allowing users to submit a short report and their worked hours when completing a task. This feature helps track what was done on each task and the time spent, improving productivity monitoring and reporting.

****Features**
User Roles**

**SuperAdmin:**

Full control of the system

Manage users (add/edit/delete)

Promote/demote admins

View all tasks and generate reports

**Admin:**

Assign tasks to users

Edit or delete tasks

View task reports

**User:**

View tasks assigned to them

Mark tasks as completed

Submit completion reports and worked hours

**Task Management**

Add, edit, delete tasks

Assign tasks to users

Track task status (pending, in_progress, completed)

Completion report and worked hours required when marking tasks as completed

**Authentication**

Login and logout functionality

Role-based redirects after login

**Forms**

TaskForm: Add or edit tasks

CompletionForm: Submit completion report and worked hours

UserForm: Add users with role and password
**Admin Panel**

Full CRUD operations for tasks and users

Task completion validation

Role management for admins

**Setup Instructions**
1. Clone the repository
git clone https://github.com/nihalarakkal/Task_Management.git
cd task_management_app

2. Create a virtual environment
python -m venv venv


Activate it:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt


Dependencies include:

Django==5.2.6
djangorestframework

4. Apply migrations
python manage.py makemigrations
python manage.py migrate

5. Create superuser
python manage.py createsuperuser


Follow prompts to create a superadmin account.

Since a superuser is already created:

Username: superadmin

Password: supersecurepassword

Optional: Verify and set superadmin fields manually:

from tasks.models import User

user = User.objects.get(username='superadmin')
user.role = 'superadmin'
user.is_staff = True
user.is_superuser = True
user.save()

6. Run the development server
python manage.py runserver


Open your browser: http://127.0.0.1:8000/

Access URLs

Login page: /

SuperAdmin dashboard: /superadmin/

Admin dashboard: /admin/

User dashboard: /user/
