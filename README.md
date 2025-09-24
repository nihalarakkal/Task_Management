# Task_Management
We are enhancing the Task Management Application by allowing users to submit a short report and their worked hours when they complete a task. This will help track what was done on each task and how much time it took.
Features
User Roles

SuperAdmin: Full control; can manage users (add/edit/delete), promote/demote admins, view all tasks, and generate task reports.

Admin: Can assign tasks to users, edit/delete tasks, view reports.

User: Can view tasks assigned to them, mark tasks as completed, submit completion reports and worked hours.

Task Management

Add, edit, delete tasks.

Assign tasks to users.

Track task status (pending, in_progress, completed).

Completion report and worked hours are required when marking tasks as completed.

Authentication

Login and logout functionality.

Redirect based on role after login.

Forms

TaskForm: Add or edit tasks.

CompletionForm: Submit completion report and worked hours.

UserForm: Add users with role and password.

Admin Panel

Full CRUD operations for tasks and users.

Task completion validation.

Role management for admins.



Setup Instructions
**1. Clone the repository**
git clone <your-repo-url>
cd task_management_app
**
**2. Create a virtual environment****
python -m venv venv


Activate it:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

**3. Install dependencies**
pip install -r requirements.txt


requirements.txt should include:

Django==5.2.6
djangorestframework

**4. Apply migrations**
python manage.py makemigrations
python manage.py migrate

**5. Create a superuser**
python manage.py createsuperuser


Follow prompts to create a superadmin account.
from tasks.models import User

# Get the user you just created
user = User.objects.get(username='superadmin')
user.role = 'superadmin'
user.is_staff = True  # Required to access admin panel
user.is_superuser = True  # Optional for admin privileges
user.save()

i have already created== username=superadmin, password="supersecurepassword"

**6. Run the development server**
python manage.py runserver


Open your browser: http://127.0.0.1:8000/

Login page: /

SuperAdmin dashboard: /superadmin/

Admin dashboard: /admin/

User dashboard: /user/
