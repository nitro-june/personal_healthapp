import sys
import os
import shutil
from datetime import datetime

# Third-party
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.dates as mdates
from scipy.interpolate import make_interp_spline, PchipInterpolator
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Local
from src_python.functions_healthapp import *
from src_python.functions_tests import *
from src_python.create_report import generate_report
import src_python.ui_tracking_dialogues as tracking_dialogues
from src_python.ui_tracking_dialogues import *
from src_python.ui_updateuser_dialogues import *

# ---------- Create Databse if needed -----------
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "healthapp.db")
create_db_path = os.path.join(current_dir, "src_python", "create_db.py")

if not os.path.exists(db_path):
    print("Database does not exist, creating database...")
    previous_cwd = os.getcwd()
    try:
        os.chdir(current_dir)
        with open(create_db_path, "r", encoding="utf-8") as f:
            exec(f.read())
    finally:
        os.chdir(previous_cwd)
else:
    print(f"{db_path} already exists. Skipping create_db.py execution.")

# --------- Read Style Files ---------
with open("MaterialDark.qss", "r") as f:
    _style = f.read()
tracking_dialogues._style = _style

# ----------- Custom Widgets for GUI -----------
class MatplotlibWidget(QWidget):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent)

        # Matplotlib figure and canvas
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axes = self.figure.add_subplot(111)

        # Navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Layout for canvas and toolbar
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # PNG Overlay as a child of the QWidget, not the canvas
        self.overlay_label = QLabel(self)
        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.overlay_label.setScaledContents(True)
        self.overlay_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.overlay_label.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Correct positioning relative to the widget itself
        if self.overlay_label.isVisible() and not self.overlay_label.pixmap().isNull():
            pixmap = self.overlay_label.pixmap()
            lbl_width = pixmap.width()
            lbl_height = pixmap.height()
            widget_width = self.width()
            widget_height = self.height()

            # Always keep in bottom-left of the widget
            x = 0
            y = widget_height - lbl_height
            self.overlay_label.setGeometry(x, y, lbl_width, lbl_height)

    def set_overlay(self, image_path, width=None, height=None, corner='bottom-left'):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return

        if width and height:
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.overlay_label.setPixmap(pixmap)
        self.overlay_label.show()

        lbl_width = pixmap.width()
        lbl_height = pixmap.height()
        widget_width = self.width()
        widget_height = self.height()

        # Position in chosen corner relative to the QWidget
        if corner == 'bottom-left':
            x = 0
            y = widget_height - lbl_height
        elif corner == 'bottom-right':
            x = widget_width - lbl_width
            y = widget_height - lbl_height
        elif corner == 'top-left':
            x = 0
            y = 0
        elif corner == 'top-right':
            x = widget_width - lbl_width
            y = 0
        else:  # center
            x = (widget_width - lbl_width) // 2
            y = (widget_height - lbl_height) // 2

        self.overlay_label.setGeometry(x, y, lbl_width, lbl_height)

    def plot_dates_smooth(self, dates_str, y_values, color='blue', marker=None, linestyle='-', **kwargs):
        if not dates_str or not y_values:
            return  # prevent empty input

        # Parse dates and sort
        dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates_str]
        x = mdates.date2num(dates)
        y = np.array(y_values)

        # Ensure strictly increasing x
        sorted_idx = np.argsort(x)
        x = x[sorted_idx]
        y = y[sorted_idx]

        self.axes.cla()  # clear old plots

        try:
            if len(x) > 5:
                x_smooth = np.linspace(x.min(), x.max(), 200)
                spline = make_interp_spline(x, y, k=2)
                y_smooth = np.clip(spline(x_smooth), y.min(), y.max())
                self.axes.plot(mdates.num2date(x_smooth), y_smooth, color=color, marker=marker, linestyle=linestyle,
                               **kwargs)
                self.axes.plot(mdates.num2date(x), y, 'o', color=color)
            elif 3 <= len(x) <= 5:
                x_smooth = np.linspace(x.min(), x.max(), 50)
                pchip = PchipInterpolator(x, y)
                y_smooth = np.clip(pchip(x_smooth), y.min(), y.max())
                self.axes.plot(mdates.num2date(x_smooth), y_smooth, color=color, marker=marker, linestyle=linestyle,
                               **kwargs)
                self.axes.plot(mdates.num2date(x), y, 'o', color=color)
            else:
                # less than 3 points: just plot raw points
                self.axes.plot(mdates.num2date(x), y, color=color, marker='o', linestyle=linestyle, **kwargs)
        except Exception as e:
            print("Plotting error:", e)
            # fallback: raw points
            self.axes.plot(mdates.num2date(x), y, color=color, marker='o', linestyle=linestyle)

        # Format axes
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.axes.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.figure.autofmt_xdate()
        self.axes.grid(True)

        # Only draw if canvas exists
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.draw()

    def clear(self):
        self.axes.cla()
        self.canvas.draw()

    def set_yaxis(self, yaxis, step=1):
        self.axes.set_ylim(0, yaxis)
        self.axes.set_yticks(range(0, yaxis + 1, step))

class UserSelfHarm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("This is a test!")

        layout = QVBoxLayout()

        test_text = QLabel("Hello world!")

        layout.addWidget(test_text)

        # PNG Overlay
        self.overlay_label = QLabel(self)
        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.overlay_label.setScaledContents(True)
        self.overlay_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.overlay_label.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay_label.isVisible() and not self.overlay_label.pixmap().isNull():
            pixmap = self.overlay_label.pixmap()
            lbl_width = pixmap.width()
            lbl_height = pixmap.height()
            widget_width = self.width()
            widget_height = self.height()

            # Keep it in bottom-left (or chosen corner)
            x = 0
            y = widget_height - lbl_height
            self.overlay_label.setGeometry(x, y, lbl_width, lbl_height)

    def set_overlay(self, image_path, width=None, height=None, corner='bottom-left'):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return

        # Scale the pixmap if width/height provided
        if width and height:
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.overlay_label.setPixmap(pixmap)
        self.overlay_label.show()

        # Position the overlay
        lbl_width = pixmap.width()
        lbl_height = pixmap.height()
        widget_width = self.width()
        widget_height = self.height()

        if corner == 'bottom-left':
            x = 0
            y = widget_height - lbl_height
        elif corner == 'bottom-right':
            x = widget_width - lbl_width
            y = widget_height - lbl_height
        elif corner == 'top-left':
            x = 0
            y = 0
        elif corner == 'top-right':
            x = widget_width - lbl_width
            y = 0
        else:  # center
            x = (widget_width - lbl_width) // 2
            y = (widget_height - lbl_height) // 2

        self.overlay_label.setGeometry(x, y, lbl_width, lbl_height)

class UserDrugAbuse(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("This is a test!")

        layout = QVBoxLayout()

        test_text = QLabel("Hello world!")

        layout.addWidget(test_text)

        # PNG Overlay
        self.overlay_label = QLabel(self)
        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.overlay_label.setScaledContents(True)
        self.overlay_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.overlay_label.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay_label.isVisible() and not self.overlay_label.pixmap().isNull():
            pixmap = self.overlay_label.pixmap()
            lbl_width = pixmap.width()
            lbl_height = pixmap.height()
            widget_width = self.width()
            widget_height = self.height()

            # Keep it in bottom-left (or chosen corner)
            x = 0
            y = widget_height - lbl_height
            self.overlay_label.setGeometry(x, y, lbl_width, lbl_height)

    def set_overlay(self, image_path, width=None, height=None, corner='bottom-left'):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return

        # Scale the pixmap if width/height provided
        if width and height:
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.overlay_label.setPixmap(pixmap)
        self.overlay_label.show()

        # Position the overlay
        lbl_width = pixmap.width()
        lbl_height = pixmap.height()
        widget_width = self.width()
        widget_height = self.height()

        if corner == 'bottom-left':
            x = 0
            y = widget_height - lbl_height
        elif corner == 'bottom-right':
            x = widget_width - lbl_width
            y = widget_height - lbl_height
        elif corner == 'top-left':
            x = 0
            y = 0
        elif corner == 'top-right':
            x = widget_width - lbl_width
            y = 0
        else:  # center
            x = (widget_width - lbl_width) // 2
            y = (widget_height - lbl_height) // 2

        self.overlay_label.setGeometry(x, y, lbl_width, lbl_height)

class ScrollingLabel(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        # Setup for widget
        self.setMinimumHeight(40)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)

        # Animation settings
        self.animation = QPropertyAnimation(self.label, b"pos")
        self.animation.setDuration(13000)
        self.animation.setLoopCount(-1)

    def showEvent(self, event):
        super().showEvent(event)
        self.start_animation()

    # Animation is started using the label
    def start_animation(self):
        self.label.adjustSize()
        container_width = self.width()
        start_pos = QPoint(container_width, 0)
        end_pos = QPoint(-self.label.width(), 0)
        self.label.move(start_pos)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # restart animation when resized
        self.animation.stop()
        self.start_animation()

# ----------- User Dialog Windows -----------
class CreateUserWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup class
        self.setWindowTitle("Create User")
        self.setWindowIcon(QIcon("resources/images/logo.ico"))

        win_width = 800
        win_height = 600
        self.resize(win_width, win_height)

        self.center()

        self.setStyleSheet(_style)
        layout = QGridLayout()

        # Add content
        titel1 = QLabel("Please enter your user information:")
        titel2 = QLabel("Please select which items you would like to track:")

        titel1.setObjectName("CreateUserTitle")
        titel2.setObjectName("CreateUserSubtitle")

        layout.addWidget(titel1, 0, 0,  alignment = Qt.AlignLeft)
        layout.addWidget(titel2, 6, 0, alignment = Qt.AlignLeft)

        layout.addWidget(QLabel("First Name"), 1, 0)
        layout.addWidget(QLabel("Last Name"), 2, 0)
        layout.addWidget(QLabel("Gender"), 3, 0)
        layout.addWidget(QLabel("Age"), 4, 0)
        layout.addWidget(QLabel("E-Mail"), 5, 0)

        self.fn_input = QLineEdit()
        self.ln_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.age_input = QLineEdit()
        self.email_input = QLineEdit()

        layout.addWidget(self.fn_input, 1, 1)
        layout.addWidget(self.ln_input, 2, 1)
        layout.addWidget(self.gender_input, 3, 1)
        layout.addWidget(self.age_input, 4, 1)
        layout.addWidget(self.email_input, 5, 1)

        layout.addWidget(QLabel("Overall Mood"), 7, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Sleep"), 8, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Anxiety"), 9, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Depression"), 10, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Self Harm"), 11, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Alcohol Abuse"), 12, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Drug Abuse"), 13, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Eating Habits"), 14, 0, alignment = Qt.AlignLeft)

        self.check_input_mood = QCheckBox()
        self.check_input_sleep = QCheckBox()
        self.check_input_anxiety = QCheckBox()
        self.check_input_depression = QCheckBox()
        self.check_input_self_harm = QCheckBox()
        self.check_input_alcohol = QCheckBox()
        self.check_input_drugs = QCheckBox()
        self.check_input_eating = QCheckBox()

        layout.addWidget(self.check_input_mood, 7, 1, alignment = Qt.AlignRight)
        layout.addWidget(self.check_input_sleep, 8, 1, alignment = Qt.AlignRight)
        layout.addWidget(self.check_input_anxiety, 9, 1, alignment = Qt.AlignRight)
        layout.addWidget(self.check_input_depression, 10, 1, alignment = Qt.AlignRight)
        layout.addWidget(self.check_input_self_harm, 11, 1, alignment = Qt.AlignRight)
        layout.addWidget(self.check_input_alcohol, 12, 1, alignment = Qt.AlignRight)
        layout.addWidget(self.check_input_drugs, 13, 1, alignment = Qt.AlignRight)
        layout.addWidget(self.check_input_eating, 14, 1, alignment = Qt.AlignRight)

        # Creating send button and setting style
        create_user_button = QPushButton("Create User")
        create_user_button.clicked.connect(self.on_create_clicked)
        create_user_button.setObjectName("CreateUserButton")

        layout.addWidget(create_user_button, 16, 1, alignment = Qt.AlignRight)

        self.setLayout(layout)

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

    # Function for creating user and setting trackables
    def on_create_clicked(self):
        fn_input_text = self.fn_input.text()
        ln_input_text = self.ln_input.text()
        gender_input_text = self.gender_input.text()
        try:
            age_input_text = int(self.age_input.text())
        except:
            QMessageBox.warning(self, "Input Error", "Age must be a number.")
            return
        email_input_text = self.email_input.text()

        try:
            insert_user(fn_input_text, ln_input_text, gender_input_text, age_input_text, email_input_text)
        except Exception as e:
            QMessageBox.critical(self, "DB Error", f"Failed to insert user: {e}")
            return

        result = get_user_id_by_email(email_input_text)
        # normalize result shape like previous code (tuple) for compatibility
        if result is not None:
            result = (result,)
        if result is None:
            QMessageBox.warning(self, "Error", "User was not created correctly.")
            return
        user_id = result[0]

        # Checkboxes
        try:
            if self.check_input_mood.isChecked():
                track_mood(user_id)
            if self.check_input_sleep.isChecked():
                track_sleep(user_id)
            if self.check_input_anxiety.isChecked():
                track_anxiety(user_id)
            if self.check_input_depression.isChecked():
                track_depression(user_id)
            if self.check_input_self_harm.isChecked():
                track_self_harm(user_id)
            if self.check_input_alcohol.isChecked():
                track_alcohol_abuse(user_id)
            if self.check_input_drugs.isChecked():
                track_drug_abuse(user_id)
            if self.check_input_eating.isChecked():
                track_eating_habits(user_id)
        except Exception as e:
            QMessageBox.critical(self, "Tracking Error", f"Failed to track items: {e}")
            return

        QMessageBox.information(self, "Success", f"User '{fn_input_text} {ln_input_text}' created successfully!")

        self.accept()

class UserIdDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup class and variables
        self.setWindowTitle("Login")
        self.user_ID = None

        layout = QVBoxLayout()

        # Add content
        layout.addWidget(QLabel("Enter User E-Mail:"))
        self.input_line = QLineEdit()
        layout.addWidget(self.input_line)

        ok_btn = QPushButton("Submit")
        ok_btn.clicked.connect(self.submit)
        layout.addWidget(ok_btn)

        self.setLayout(layout)

    # Method that checks email and returns userID for the main window
    def submit(self):
        try:
            email_value = self.input_line.text().strip()

            with connect_db() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT userID FROM users WHERE LOWER(email) = LOWER(?)",
                    (email_value,)
                )
                result = cur.fetchone()

            if result is None:
                # Show a warning message box
                QMessageBox.warning(
                    self,
                    "User Not Found",
                    f"No user found with email '{email_value}'"
                )
                return

            user_result = result[0]

            self.user_ID = user_result  # store input
            self.accept()  # close dialog if completed

        except Exception as e:
            print("Error retrieving userID:", e)
        
class DeleteUserId(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup Window
        self.setWindowTitle("Delete User")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Enter UserID:"))
        self.input_line = QLineEdit()
        layout.addWidget(self.input_line)

        submit_btn = QPushButton("Delete")
        submit_btn.clicked.connect(self.submit)

        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit(self):
        text = self.input_line.text().strip()
        if not text.isdigit():
            QMessageBox.warning(self, "Invalid Input", "UserID must be a number.")
            return

        user_id = int(text)

        # Intermediate pop-up to confirm
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to permanently delete user {user_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return  # user cancelled

        delete_user(user_id)
        self.accept()

#   ----------- Main Window -----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.user_ID = None

        # Set Application Defaults
        self.setWindowTitle("HealthApp")
        self.setWindowIcon(QIcon("resources/images/logo.ico"))

        # Window Sizes in 16:9
        self.setMinimumSize(QSize(1200, 675))
        self.setMaximumSize(QSize(geometry.width(), geometry.height()))
        self.resize(1200, 675)

        self.setStyleSheet(_style)

        # -------------------- Menubar --------------------
        menubar = self.menuBar()

        # User menu actions
        user_menu = menubar.addMenu("User")
        create_user_action = user_menu.addAction("Create User")
        create_user_action.triggered.connect(self.create_user_box)
        change_user_action = user_menu.addAction("Change User")
        change_user_action.triggered.connect(self.open_user_dialog)
        modify_user_action = user_menu.addAction("Modify User")
        modify_user_action.triggered.connect(self.create_user_change)
        delete_user_action = user_menu.addAction("Delete User")
        delete_user_action.triggered.connect(self.create_delete_user)

        # Tracking menu actions
        tracking_menu = menubar.addMenu("Tracking")
        track_mood_action = tracking_menu.addAction("Track Mood")
        track_mood_action.triggered.connect(self.create_tracking_mood_box)
        track_anxiety_action = tracking_menu.addAction("Track Anxiety")
        track_anxiety_action.triggered.connect(self.create_tracking_anxiety_box)
        track_depression_action = tracking_menu.addAction("Track Depression")
        track_depression_action.triggered.connect(self.create_tracking_depression_box)
        track_sleep_action = tracking_menu.addAction("Track Sleep")
        track_sleep_action.triggered.connect(self.create_tracking_sleep_box)
        track_self_harm_action = tracking_menu.addAction("Track Self Harm")
        track_self_harm_action.triggered.connect(self.create_tracking_self_harm_box)
        track_alcohol_abuse_action = tracking_menu.addAction("Track Alcohol Abuse")
        track_alcohol_abuse_action.triggered.connect(self.create_tracking_alcohol_abuse_box)
        track_drug_abuse_action = tracking_menu.addAction("Track Drug Abuse")
        track_drug_abuse_action.triggered.connect(self.create_tracking_drug_abuse_box)
        track_eating_habits_action = tracking_menu.addAction("Track Eating Habits")
        track_eating_habits_action.triggered.connect(self.create_tracking_eating_habits_box)

        # Application actions
        application_menu = menubar.addMenu("Actions")
        change_style_action = application_menu.addAction("Change Style")
        change_style_action.triggered.connect(self.toggle_style)
        select_pfp_action = application_menu.addAction("Select Profile Image")
        select_pfp_action.triggered.connect(self.choose_and_copy_user_pfp)
        create_report_action = application_menu.addAction("Create Report")
        create_report_action.triggered.connect(self.generate_report)
        exit_application_action = application_menu.addAction("Exit Application")
        exit_application_action.triggered.connect(self.close)

        # -------------------- Scrolling Label --------------------
        # Create a toolbar to hold the scrolling label
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setAllowedAreas(Qt.TopToolBarArea)
        toolbar.setObjectName("MainToolBar")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Create the scrolling label
        scrolling_label = ScrollingLabel(give_message() + "                 " + give_message())
        scrolling_label.setFixedHeight(30)
        scrolling_label.setObjectName("AppScrollingLabel")
        toolbar.addWidget(scrolling_label)

        self.status = self.statusBar()
        self.status_label = QLabel()
        status_font = self.status_label.font()
        status_font.setPointSize(status_font.pointSize() + 2)
        self.status_label.setFont(status_font)
        self.status.addPermanentWidget(self.status_label)
        self.update_status()

        # --------- For Docking Widgets ----------
        central_widget = QWidget()
        central_widget.setFixedSize(1, 1)
        self.setCentralWidget(central_widget)

        self.setDockNestingEnabled(True)

        self.docks_left = []
        self.docks_right = []
        self.docks_tabbed = []
        self.docks_initialized = False

    # -------------------- Methods --------------------
    # Creates or removes dockable widgets when userID is updated
    def update_dockables(self):
        # Remove existing docks if they exist
        for dock in self.docks_left + self.docks_right:
            if dock is not None:
                self.removeDockWidget(dock)
                dock.deleteLater()

        for dock in self.docks_tabbed:
            self.removeDockWidget(dock)
            dock.deleteLater()

        self.docks_tabbed.clear()
        self.docks_left.clear()
        self.docks_right.clear()

        # Create a dock for user information, which is always set
        test_user_info = UserInfoTest(self.user_ID)
        self.create_dock("User Information", [test_user_info], side="right", max_width=300, max_height=200)

        # Trackables are selected and created into dockable widgets
        trackables_me = get_user_trackables(self.user_ID)
        tabbed_widgets = []
        widgets_tab_names = []

        for item in trackables_me:
            if item[1] == 1:  # Anxiety
                anxiety_date, anxiety_value = [], []
                values_anxiety = get_values(item[0])
                for v in values_anxiety:
                    anxiety_date.append(v[0])
                    anxiety_value.append(v[1])

                plot_anxiety = MatplotlibWidget()
                plot_anxiety.plot_dates_smooth(anxiety_date, anxiety_value, color='blue', marker=None, linestyle='-', linewidth=2)
                plot_anxiety.set_yaxis(21)
                plot_anxiety.set_overlay("resources/images/forapp1.png", width=230, height=200, corner="bottom-left")

                tabbed_widgets.append(plot_anxiety)
                widgets_tab_names.append("Anxiety Data")

            if item[1] == 2:
                mood_date, mood_value = [], []
                values_mood = get_values(item[0])
                for item2 in values_mood:
                    mood_date.append(item2[0])
                    mood_value.append(item2[1])

                plot_mood = MatplotlibWidget()
                plot_mood.plot_dates_smooth(mood_date, mood_value, color='blue', marker=None, linestyle='-', linewidth=2)
                plot_mood.set_yaxis(10)
                plot_mood.set_overlay("resources/images/forapp1.png", width=230, height=200, corner="bottom-left")

                tabbed_widgets.append(plot_mood)
                widgets_tab_names.append("Mood Data")

            if item[1] == 3:
                sleep_q_date, sleep_q_value = [], []
                values_sleep_q = get_values(item[0])

                for item2 in values_sleep_q:
                    sleep_q_date.append(item2[0])
                    sleep_q_value.append(item2[1])

                plot_sleep_q = MatplotlibWidget()
                plot_sleep_q.plot_dates_smooth(sleep_q_date, sleep_q_value, color='blue', marker=None, linestyle='-', linewidth=2)
                plot_sleep_q.set_yaxis(10)
                plot_sleep_q.set_overlay("resources/images/forapp1.png", width=230, height=200, corner="bottom-left")

                tabbed_widgets.append(plot_sleep_q)
                widgets_tab_names.append("Sleep Quality Data")

            if item[1] == 4:
                sleep_l_date, sleep_l_value = [], []
                values_sleep_l = get_values(item[0])

                for item2 in values_sleep_l:
                    sleep_l_date.append(item2[0])
                    sleep_l_value.append(item2[1])

                plot_sleep_l = MatplotlibWidget()
                plot_sleep_l.plot_dates_smooth(sleep_l_date, sleep_l_value, color='blue', marker=None, linestyle='-', linewidth=2)
                plot_sleep_l.set_yaxis(10)
                plot_sleep_l.set_overlay("resources/images/forapp1.png", width=230, height=200, corner="bottom-left")

                tabbed_widgets.append(plot_sleep_l)
                widgets_tab_names.append("Sleep Length Data")

            """
            if item[1] == 5:
                self_harm_value = []
                self_harm_date = []
                values_self_harm = get_values(item[0])

                for item2 in values_self_harm:
                    self_harm_date.append(item2[0])
                    self_harm_value.append(item2[1])

                plot_self_harm = UserSelfHarm()
                plot_self_harm.set_overlay(select_image_path(self_harm_value), width=300, height=300, corner="bottom-left")
                #plot_self_harm.setFixedSize(250, 250)
                #plot_self_harm.setStyleSheet("QLabel { background-image: url(checkmark.png); background-size: cover; }")

                self.create_dock("Self Harm Data", [plot_self_harm], side="right", max_width=300, max_height=300)
            """

            if item[1] == 6:
                alcohol_abuse_date, alcohol_abuse_value = [], []
                values_alcohol_abuse = get_values(item[0])

                for item2 in values_alcohol_abuse:
                    alcohol_abuse_date.append(item2[0])
                    alcohol_abuse_value.append(item2[1])

                plot_alcohol_abuse = MatplotlibWidget()
                plot_alcohol_abuse.plot_dates_smooth(alcohol_abuse_date, alcohol_abuse_value, color='blue', marker=None, linestyle='-', linewidth=2)
                plot_alcohol_abuse.set_yaxis(12)
                plot_alcohol_abuse.set_overlay("resources/images/forapp1.png", width=230, height=200, corner="bottom-left")

                tabbed_widgets.append(plot_alcohol_abuse)
                widgets_tab_names.append("Alcohol Abuse Data")

            """
            if item[1] == 7:
                drug_abuse_value = []
                drug_abuse_date = []
                values_drug_abuse = get_values(item[0])

                for item2 in values_self_harm:
                    drug_abuse_date.append(item2[0])
                    drug_abuse_value.append(item2[1])

                #plot_drug_abuse = QLabel("TEST")
                #plot_drug_abuse.setFixedSize(250, 250)
                plot_drug_abuse = UserSelfHarm()

                #plot_drug_abuse.setStyleSheet("QLabel { background-image: url(" + image_selection_drug_abuse + "); background-size: cover; }")
                plot_drug_abuse.set_overlay(select_image_path(drug_abuse_value), width=300, height=300, corner="bottom-left")

                self.create_dock("Drug Abuse Data", [plot_drug_abuse], side="right", max_width=300, max_height=300)
            """

            if item[1] == 8:  # Eating Habits
                eating_habits_date, eating_habits_value = [], []
                values_eating_habits = get_values(item[0])

                for item2 in values_eating_habits:
                    eating_habits_date.append(item2[0])
                    eating_habits_value.append(item2[1])

                plot_eating_habits = MatplotlibWidget()
                plot_eating_habits.plot_dates_smooth(
                    eating_habits_date,
                    eating_habits_value,
                    color='blue',
                    marker=None,
                    linestyle='-',
                    linewidth=2
                )
                plot_eating_habits.set_yaxis(78, step=5)
                plot_eating_habits.set_overlay("resources/images/forapp1.png", width=230, height=200, corner="bottom-left")

                tabbed_widgets.append(plot_eating_habits)
                widgets_tab_names.append("Eating Habits Data")

            if item[1] == 9:  # Depression
                depression_date, depression_value = [], []
                values_depression = get_values(item[0])

                for item2 in values_depression:
                    depression_date.append(item2[0])
                    depression_value.append(item2[1])

                plot_depression = MatplotlibWidget()
                plot_depression.plot_dates_smooth(
                    depression_date,
                    depression_value,
                    color='blue',
                    marker=None,
                    linestyle='-',
                    linewidth=2
                )
                plot_depression.set_yaxis(27)
                plot_depression.set_overlay("resources/images/forapp1.png", width=230, height=200, corner="bottom-left")

                tabbed_widgets.append(plot_depression)
                widgets_tab_names.append("Depression Data")

        # Widgets, which should be tabbed are stored in a list and given to helper function
        self.create_tabbed_dock("Data Tab", tabbed_widgets, widgets_tab_names, side="left")

        self.docks_initialized = True

    # Status bar for userID is updated on select
    def update_status(self):
        self.status_label.setText(f"Current User ID: {self.user_ID}")

    # userID window is opened -> widgets in main, which require this ID are updated
    def open_user_dialog(self):
        dialog = UserIdDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.user_ID = dialog.user_ID
            update_login(self.user_ID)
            self.update_status()
            self.update_dockables()

    # Creates dockable widgets in main window
    def create_dock(self, title, widgets, side="left", max_width=None, max_height=None):
        """
        Create a dock, add it to the left/right, split evenly, and optionally set max size.
        """
        dock = QDockWidget(title, self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        for w in widgets:
            layout.addWidget(w)
        dock.setWidget(content_widget)

        # Set maximum size if provided
        if max_width or max_height:
            content_widget.setMaximumSize(
                max_width if max_width else QWIDGETSIZE_MAX,
                max_height if max_height else QWIDGETSIZE_MAX
            )

        if side.lower() == "left":
            self.addDockWidget(Qt.LeftDockWidgetArea, dock)
            if self.docks_left:
                self.splitDockWidget(self.docks_left[-1], dock, Qt.Vertical)
            self.docks_left.append(dock)
        elif side.lower() == "right":
            self.addDockWidget(Qt.RightDockWidgetArea, dock)
            if self.docks_right:
                self.splitDockWidget(self.docks_right[-1], dock, Qt.Vertical)
            self.docks_right.append(dock)

        return dock

    # Creates a docked widget, which has several tabs
    def create_tabbed_dock(self, title, widgets, widget_names, side="right"):
        """
        Create a single dock with multiple widgets as tabs.
        """
        first_dock = None
        for i, w in enumerate(widgets):
            dock = QDockWidget(widget_names[i], self)
            dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
            dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
            dock.setWidget(w)

            if side.lower() == "left":
                self.addDockWidget(Qt.LeftDockWidgetArea, dock)
            else:
                self.addDockWidget(Qt.RightDockWidgetArea, dock)

            if first_dock:
                # Widgets are merged as tab onto first dockable
                self.tabifyDockWidget(first_dock, dock)
            else:
                # First widget is docked
                first_dock = dock

            self.docks_tabbed.append(dock)

        return first_dock

    def generate_report(self):

        if self.user_ID is None:
            QMessageBox.warning(self, "Error", "No user logged in.")
            return

        generate_report(self.user_ID)

    def toggle_style(self):
        """Toggle between dark and light QSS styles at runtime."""
        global _style
        try:
            base = os.path.dirname(__file__)
            dark_path = os.path.join(base, "MaterialDark.qss")
            light_path = os.path.join(base, "MaterialLight.qss")
            current = getattr(self, 'current_style', 'dark')
            new_path = light_path if current == 'dark' else dark_path
            with open(new_path, 'r', encoding='utf-8') as f:
                new_style = f.read()

            # Update module-level _style so newly created dialogs use the new style
            _style = new_style
            tracking_dialogues._style = new_style

            # Apply at application level so existing widgets update
            app = QApplication.instance()
            if app:
                app.setStyleSheet(new_style)

            # Toggle state
            self.current_style = 'light' if current == 'dark' else 'dark'
            QMessageBox.information(self, "Style Changed", f"Style switched to {self.current_style} mode.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to change style: {e}")

    def choose_and_copy_user_pfp(self):
        try:
            # Ask the user to select a file
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Profile Picture", "", "Images (*.png *.jpg *.jpeg *.bmp)"
            )

            if not file_path:
                print("No file selected")
                return None

            # Read bytes once and keep them for future SQL BLOB insertion.
            with open(file_path, "rb") as img_file:
                self.user_pfp_bytes = img_file.read()

            # Persist BLOB to DB only when a user is selected.
            if self.user_ID is not None:
                insert_pfp(self.user_ID, self.user_pfp_bytes)

            # Persist raw bytes for debugging/export purposes.
            img_byte_path = os.path.join(os.path.dirname(__file__), "img_byte.txt")
            with open(img_byte_path, "wb") as img_out:
                img_out.write(self.user_pfp_bytes)

            # Target folder relative to the script
            target_folder = os.path.join(os.path.dirname(__file__), "resources", "images")
            os.makedirs(target_folder, exist_ok=True)

            # Destination path
            dest_file = os.path.join(target_folder, "user_pfp" + os.path.splitext(file_path)[1])

            # Copy the selected file
            shutil.copy(file_path, dest_file)

            print(f"File copied to {dest_file}")
            return dest_file
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to set profile picture: {e}")
            return None

    # ---------- Methods to open classes/widgets used in action bar of main menu ----------
    def create_delete_user(self):
        dialog = DeleteUserId(self)
        dialog.exec_()

    def create_user_box(self):
        dialog = CreateUserWindow(self)
        dialog.exec_()

    def create_user_change(self):
        dialog = UpdateUserDialog(self.user_ID, self)
        dialog.exec_()

    def create_tracking_mood_box(self):
        dialog = TrackMoodWindow(self.user_ID, self)
        dialog.exec_()

    def create_tracking_anxiety_box(self):
        dialog = TrackAnxietyWindow(self.user_ID, self)
        dialog.exec_()

    def create_tracking_depression_box(self):
        dialog = TrackDepressionWindow(self.user_ID, self)
        dialog.exec_()

    def create_tracking_sleep_box(self):
        dialog = TrackSleepWindow(self.user_ID, self)
        dialog.exec_()

    def create_tracking_self_harm_box(self):
        dialog = TrackSelfHarmWindow(self.user_ID, self)
        dialog.exec_()

    def create_tracking_alcohol_abuse_box(self):
        dialog = TrackAlcoholAbuseWindow(self.user_ID, self)
        dialog.exec_()

    def create_tracking_drug_abuse_box(self):
        dialog = TrackDrugAbuseWindow(self.user_ID, self)
        dialog.exec_()

    def create_tracking_eating_habits_box(self):
        dialog = TrackEatingHabitsWindow(self.user_ID, self)
        dialog.exec_()

    def resizeEvent(self, event):
        aspect_ratio = 16 / 9
        w = self.width()
        h = self.height()
        new_height = int(w / aspect_ratio)
        if new_height != h:
            self.resize(w, new_height)
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    geometry = screen.geometry()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
