# Expense-Project

Expense-Project is a full-stack application designed to help users keep track of their income and expenses. This project enables users to register, log in, and manage their financial data with features such as email authentication, password reset, and data visualization.

## Features

- **User Authentication**: 
  - User registration with email verification.
  - Login and password reset functionality with email verification, just like in real-world applications.
  
- **Income and Expense Management**:
  - Add, edit, and search income and expenses.
  - Detailed summary with graphical representation using Chart.js.

- **Currency Management**:
  - Option to change currency based on user preference.
  
- **Account Management**:
  - Edit or delete the user account.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Charting**: Chart.js for visualizing income and expense summaries
- **Backend**: Django
- **Database**: PostgreSQL

## Getting Started

### Prerequisites

- Python 3.x
- PostgreSQL
- Django
- `pip` for managing Python packages

### Installation

1. **Clone the Repository**:
    ```bash
    git clone [https://github.com/your-username/Expense-Project.git](https://github.com/utkarsh050505/Expense-Project.git)
    cd Expense-Project
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Database Configuration**:
    - Ensure PostgreSQL is installed and running.
    - Create a database for the project and configure your database settings in `settings.py`.

5. **Email Configuration**:
    - At the very end of `settings.py`, add the email and password through which you want to send validation and password reset links:
    ```python
    EMAIL_HOST_USER = 'your-email@example.com'
    EMAIL_HOST_PASSWORD = 'your-email-password'
    ```

6. **Apply Migrations**:
    ```bash
    python manage.py migrate
    ```

7. **Run the Server**:
    ```bash
    python manage.py runserver
    ```

8. **Access the Application**:
    Open your web browser and navigate to `http://127.0.0.1:8000`.

## Usage

1. **Register** as a new user and verify your email.
2. **Log in** and start adding income and expenses.
3. View your income and expense summary on a graphical chart.
4. Change currency, edit your account, or delete it if needed.
5. Use the password reset feature if you forget your password.

## Contact

For questions or suggestions, please reach out at [utkarsh.mandal5@gmail.com](mailto:utkarsh.mandal5@gmail.com).

---

Enjoy tracking your finances with Expense-Project!

