from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from src_python.functions_healthapp import (
    update_age,
    update_gender,
    update_email,
    update_fname,
    update_lname,
    get_user_info
)

# Fallback style; main module injects active QSS at runtime.
_style = ""

# ----- Class for user information -----

class UserInfoTest(QWidget):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)

        # Setup class widget
        self.user_ID = user_ID

        layout = QGridLayout(self)
        self.setLayout(layout)

        # Add content
        user_info = QLabel("User Information")
        user_info.setFont(QFont("Arial", 14))
        layout.addWidget(user_info, 0, 0, 1, 2)

        # SQLite command that gets entire user row, besides ID
        user_info_values = get_user_info(self.user_ID)
        if not user_info_values:
            layout.addWidget(QLabel("No user information found."), 1, 0)
            return

        # Adds user information to content
        full_name = f"{str(user_info_values[0])} {str(user_info_values[1])}"
        layout.addWidget(QLabel("Name:"), 1, 0)
        layout.addWidget(QLabel(full_name), 1, 1)

        layout.addWidget(QLabel("Age:"), 2, 0)
        layout.addWidget(QLabel(str(user_info_values[3])), 2, 1)

        layout.addWidget(QLabel("Gender:"), 3, 0)
        layout.addWidget(QLabel(str(user_info_values[2])), 3, 1)

        layout.addWidget(QLabel("E-Mail:"), 4, 0)
        layout.addWidget(QLabel(str(user_info_values[6])), 4, 1)

        layout.addWidget(QLabel("Created on:"), 5, 0)
        layout.addWidget(QLabel(str(user_info_values[4])), 5, 1)

        layout.addWidget(QLabel("Last login:"), 6, 0)
        layout.addWidget(QLabel(str(user_info_values[5])), 6, 1)

# ----- Classes for Widgets to change user information -----

class UpdateUserDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Update User")
        self.user_id = user_id

        layout = QVBoxLayout()

        layout.addWidget(UserInfoTest(self.user_id))

        self.update_fn = QPushButton("Update First Name")
        self.update_fn.clicked.connect(self.open_change_fn)
        self.update_ln = QPushButton("Update Last Name")
        self.update_ln.clicked.connect(self.open_change_ln)
        self.update_gender = QPushButton("Update Gender")
        self.update_gender.clicked.connect(self.open_change_gender)
        self.update_age = QPushButton("Update Age")
        self.update_age.clicked.connect(self.open_change_age)
        self.update_email = QPushButton("Update Email")
        self.update_email.clicked.connect(self.open_change_email)

        if self.user_id is not None:
            layout.addWidget(self.update_fn)
            layout.addWidget(self.update_ln)
            layout.addWidget(self.update_gender)
            layout.addWidget(self.update_age)
            layout.addWidget(self.update_email)

        self.setLayout(layout)

    def open_change_fn(self):
        dialog = ChangeFn(self.user_id, self)
        dialog.exec_()

    def open_change_ln(self):
        dialog = ChangeLn(self.user_id, self)
        dialog.exec_()

    def open_change_gender(self):
        dialog = ChangeGender(self.user_id, self)
        dialog.exec_()

    def open_change_age(self):
        dialog = ChangeAge(self.user_id, self)
        dialog.exec_()

    def open_change_email(self):
        dialog = ChangeEmail(self.user_id, self)
        dialog.exec_()

# ----------- Action Windows for updating user infromation -----------

class ChangeFn(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Change First Name")
        self.user_id = user_id
        request_user_dialog = pyqtSignal()

        layout = QVBoxLayout()

        self.new_fname = QLineEdit()
        self.submit_fname_button = QPushButton("Submit")
        self.submit_fname_button.clicked.connect(self.submit_fname)

        layout.addWidget(QLabel("Enter New First Name:"))
        layout.addWidget(self.new_fname)
        layout.addWidget(self.submit_fname_button)

        self.setLayout(layout)

    def submit_fname(self):
        try:
            new_fname_text = self.new_fname.text()

            if not new_fname_text.strip():
                print("First name is empty")
                return

            if self.user_id is None:
                print("user_id is None")
                return

            update_fname(self.user_id, new_fname_text)
            self.accept()

        except Exception as e:
            print("submit_fname error:", repr(e))

class ChangeLn(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Change Last Name")
        self.user_id = user_id

        layout = QVBoxLayout()

        self.new_lname = QLineEdit()
        self.submit_lname_button = QPushButton("Submit")
        self.submit_lname_button.clicked.connect(self.submit_lname)

        layout.addWidget(QLabel("Enter New Last Name:"))
        layout.addWidget(self.new_lname)
        layout.addWidget(self.submit_lname_button)

        self.setLayout(layout)

    def submit_lname(self):
        try:
            new_lname_text = self.new_lname.text()

            if not new_lname_text.strip():
                print("Last name is empty")
                return

            if self.user_id is None:
                print("user_id is None")
                return

            update_lname(self.user_id, new_lname_text)
            self.accept()

        except Exception as e:
            print("submit_lname error:", repr(e))

class ChangeGender(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Change Gender")
        self.user_id = user_id

        layout = QVBoxLayout()

        self.new_gender = QLineEdit()
        self.submit_gender_button = QPushButton("Submit")
        self.submit_gender_button.clicked.connect(self.submit_gender)

        layout.addWidget(QLabel("Enter New Gender:"))
        layout.addWidget(self.new_gender)
        layout.addWidget(self.submit_gender_button)

        self.setLayout(layout)

    def submit_gender(self):
        try:
            new_gender_text = self.new_gender.text()

            if not new_gender_text.strip():
                print("Gender is empty")
                return

            if self.user_id is None:
                print("user_id is None")
                return

            update_gender(self.user_id, new_gender_text)
            self.accept()

        except Exception as e:
            print("submit_gender error:", repr(e))

class ChangeAge(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Change Age")
        self.user_id = user_id

        layout = QVBoxLayout()

        self.new_age = QLineEdit()
        self.submit_age_button = QPushButton("Submit")
        self.submit_age_button.clicked.connect(self.submit_age)

        layout.addWidget(QLabel("Enter New Age:"))
        layout.addWidget(self.new_age)
        layout.addWidget(self.submit_age_button)

        self.setLayout(layout)

    def submit_age(self):
        try:
            age_text = self.new_age.text().strip()

            if not age_text:
                self.show_error("Age cannot be empty.")
                return

            if self.user_id is None:
                self.show_error("User ID is missing.")
                return

            try:
                age_value = int(age_text)
            except ValueError:
                self.show_error("Please enter a valid integer for age.")
                return

            update_age(self.user_id, age_value)

            self.accept()

        except Exception as e:
            self.show_error(f"Unexpected error: {e}")

    def show_error(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Input Error")
        msg_box.setText(message)
        msg_box.exec_()

class ChangeEmail(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Change E-Mail")
        self.user_id = user_id

        layout = QVBoxLayout()

        self.new_email = QLineEdit()
        self.submit_email_button = QPushButton("Submit")
        self.submit_email_button.clicked.connect(self.submit_email)

        layout.addWidget(QLabel("Enter New E-Mail:"))
        layout.addWidget(self.new_email)
        layout.addWidget(self.submit_email_button)

        self.setLayout(layout)

    def submit_email(self):
        try:
            new_email_text = self.new_email.text()

            if not new_email_text.strip():
                print("E-Mail is empty")
                return

            if self.user_id is None:
                print("user_id is None")
                return

            update_email(self.user_id, new_email_text)
            self.accept()

        except Exception as e:
            print("submit_email error:", repr(e))
