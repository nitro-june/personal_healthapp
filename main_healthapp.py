import PyQt5 as PyQt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import sqlite3

from refactor.functions_healthapp import *
from refactor.functions_tests import *

with open("MaterialDark.qss", "r") as f:
    _style = f.read()

# TEMPORARY userID until I have implemented a way to get the userID
user_ID = 2

class ScrollingLabel(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        self.setMinimumHeight(40)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)

        # Animation
        self.animation = QPropertyAnimation(self.label, b"pos")
        self.animation.setDuration(13000)
        self.animation.setLoopCount(-1)

    def showEvent(self, event):
        super().showEvent(event)
        self.start_animation()  # now widget has proper width

    def start_animation(self):
        self.label.adjustSize()  # ensures width is correct
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

# ---------- Action Windows for Tracking -----------
class TrackMoodWindow(QDialog):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)

        self.user_ID = user_ID

        self.setWindowTitle("Mood Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 100
        win_width = 300
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        mood_label = QLabel("Your current mood:")

        self.mood_combobox = QComboBox()
        for i in range(0, 11):
            self.mood_combobox.addItem(str(i))

        self.mood_submit_button = QPushButton("Submit")
        self.mood_submit_button.clicked.connect(lambda: (self.submit_mood(), self.close()))

        layout.addWidget(mood_label)
        layout.addWidget(self.mood_combobox)
        layout.addWidget(self.mood_submit_button)

        self.setLayout(layout)

    def submit_mood(self):
        try:
            sql_conn = sqlite3.connect("healthapp.db")
            sql_cursor = sql_conn.cursor()

            date_now = datetime.now().date().isoformat()
            mood_value = self.mood_combobox.currentIndex()

            sql_cursor.execute(
                "SELECT user_trackablesID "
                "FROM user_trackables "
                "WHERE trackableID = 2 AND userID = ?",
                (self.user_ID,)
            )

            result = sql_cursor.fetchone()
            if result is None:
                print("No trackable found for this user.")
                return

            trackable_id = result[0]

            sql_cursor.execute(
                "INSERT INTO user_trackables_entries "
                "(user_trackablesID, entry_date, value) "
                "VALUES (?, ?, ?)",
                (trackable_id, date_now, mood_value)
            )

            sql_conn.commit()

        except Exception as e:
            print("Error submitting mood:", e)

        finally:
            sql_conn.close()

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

class TrackAnxietyWindow(QDialog):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)

        self.user_ID = user_ID

        self.setWindowTitle("Anxiety Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 700
        win_width = 600
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        gad7_label_explanation = QLabel("""How often have you been bothered by the following problems?
        0 = Not at all
        1 = Several days
        2 = More than half the days
        3 = Nearly every day
        """)

        gad7_label_q1 = QLabel("Feeling nervous, anxious, or on edge.")
        gad7_label_q2 = QLabel("Not being able to stop or control worrying.")
        gad7_label_q3 = QLabel("Worry too much about different things.")
        gad7_label_q4 = QLabel("Having trouble relaxing.")
        gad7_label_q5 = QLabel("Being so restless that it is hard to sit still.")
        gad7_label_q6 = QLabel("Becoming easily annoyed or irritable.")
        gad7_label_q7 = QLabel("Feeling afraid, as if something awful might happen.")

        self.gad7_combobox_q1 = QComboBox()
        for i in range(0, 4):
            self.gad7_combobox_q1.addItem(str(i))

        self.gad7_combobox_q2 = QComboBox()
        for i in range(0, 4):
            self.gad7_combobox_q2.addItem(str(i))

        self.gad7_combobox_q3 = QComboBox()
        for i in range(0, 4):
            self.gad7_combobox_q3.addItem(str(i))

        self.gad7_combobox_q4 = QComboBox()
        for i in range(0, 4):
            self.gad7_combobox_q4.addItem(str(i))

        self.gad7_combobox_q5 = QComboBox()
        for i in range(0, 4):
            self.gad7_combobox_q5.addItem(str(i))

        self.gad7_combobox_q6 = QComboBox()
        for i in range(0, 4):
            self.gad7_combobox_q6.addItem(str(i))

        self.gad7_combobox_q7 = QComboBox()
        for i in range(0, 4):
            self.gad7_combobox_q7.addItem(str(i))

        self.gad7_combobox_list = (self.gad7_combobox_q1, self.gad7_combobox_q2, self.gad7_combobox_q3, self.gad7_combobox_q4, self.gad7_combobox_q5, self.gad7_combobox_q6, self.gad7_combobox_q7)

        self.anxiety_submit_button = QPushButton("Submit")
        self.anxiety_submit_button.clicked.connect(lambda: (self.submit_anxiety(), self.close()))

        layout.addWidget(gad7_label_explanation)
        layout.addWidget(gad7_label_q1)
        layout.addWidget(self.gad7_combobox_q1)
        layout.addWidget(gad7_label_q2)
        layout.addWidget(self.gad7_combobox_q2)
        layout.addWidget(gad7_label_q3)
        layout.addWidget(self.gad7_combobox_q3)
        layout.addWidget(gad7_label_q4)
        layout.addWidget(self.gad7_combobox_q4)
        layout.addWidget(gad7_label_q5)
        layout.addWidget(self.gad7_combobox_q5)
        layout.addWidget(gad7_label_q6)
        layout.addWidget(self.gad7_combobox_q6)
        layout.addWidget(gad7_label_q7)
        layout.addWidget(self.gad7_combobox_q7)
        layout.addWidget(self.anxiety_submit_button)

        self.setLayout(layout)

    def submit_anxiety(self):
        try:
            sql_conn = sqlite3.connect("healthapp.db")
            sql_cursor = sql_conn.cursor()

            date_now = datetime.now().date().isoformat()
            anxiety_value = gad7_scoring(self.gad7_combobox_list)

            sql_cursor.execute(
                "SELECT user_trackablesID "
                "FROM user_trackables "
                "WHERE trackableID = 1 AND userID = ?",
                (self.user_ID,)
            )

            result = sql_cursor.fetchone()
            if result is None:
                print("No trackable found for this user.")
                return

            trackable_id = result[0]

            sql_cursor.execute(
                "INSERT INTO user_trackables_entries "
                "(user_trackablesID, entry_date, value) "
                "VALUES (?, ?, ?)",
                (trackable_id, date_now, anxiety_value)
            )

            sql_conn.commit()

        except Exception as e:
            print("Error submitting mood:", e)

        finally:
            sql_conn.close()

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

class TrackDepressionWindow(QDialog):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)

        self.user_ID = user_ID

        self.setWindowTitle("Depression Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 800
        win_width = 600
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        phq9_label_explanation = QLabel("How often have you been bothered by the following problems?")

        phq9_label_q1 = QLabel("Little interest or pleasure in doing things.")
        phq9_label_q2 = QLabel("Feeling down, depressed, or hopeless.")
        phq9_label_q3 = QLabel("Trouble falling or staying asleep, or sleeping too much.")
        phq9_label_q4 = QLabel("Feeling tired or having little energy.")
        phq9_label_q5 = QLabel("Poor apetite or overeating.")
        phq9_label_q6 = QLabel(
            "Feeling bad about yourself - or that you are a failure or have let yourself or your family down.")
        phq9_label_q7 = QLabel("Trouble concentrating on things, such as reading the newspaper or watching television")
        phq9_label_q8 = QLabel(
            "Moving or speaking so slowly that other people could have noticed? Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual.")
        phq9_label_q9 = QLabel("Thoughts that you would be better off dead or of hurting yourself in some way.")

        self.phq9_combobox_q1 = QComboBox()
        for i in range(0, 4):
            self.phq9_combobox_q1.addItem(str(i))

        self.phq9_combobox_q2 = QComboBox()
        for i in range(0, 4):
            self.phq9_combobox_q2.addItem(str(i))

        self.phq9_combobox_q3 = QComboBox()
        for i in range(0, 4):
            self.phq9_combobox_q3.addItem(str(i))

        self.phq9_combobox_q4 = QComboBox()
        for i in range(0, 4):
            self.phq9_combobox_q4.addItem(str(i))

        self.phq9_combobox_q5 = QComboBox()
        for i in range(0, 4):
            self.phq9_combobox_q5.addItem(str(i))

        self.phq9_combobox_q6 = QComboBox()
        for i in range(0, 4):
            self.phq9_combobox_q6.addItem(str(i))

        self.phq9_combobox_q7 = QComboBox()
        for i in range(0, 4):
            self.phq9_combobox_q7.addItem(str(i))

        self.phq9_combobox_q8 = QComboBox()
        for i in range(0, 4):
            self.phq9_combobox_q8.addItem(str(i))

        self.phq9_combobox_q9 = QComboBox()
        for i in range(0, 4):
            self.phq9_combobox_q9.addItem(str(i))

        self.phq9_combobox_list = (self.phq9_combobox_q1, self.phq9_combobox_q2, self.phq9_combobox_q3, self.phq9_combobox_q4, self.phq9_combobox_q5, self.phq9_combobox_q6, self.phq9_combobox_q7 , self.phq9_combobox_q8 , self.phq9_combobox_q9)

        self.depression_submit_button = QPushButton("Submit")
        self.depression_submit_button.clicked.connect(lambda: (self.submit_depression(), self.close()))

        layout.addWidget(phq9_label_explanation)
        layout.addWidget(phq9_label_q1)
        layout.addWidget(self.phq9_combobox_q1)
        layout.addWidget(phq9_label_q2)
        layout.addWidget(self.phq9_combobox_q2)
        layout.addWidget(phq9_label_q3)
        layout.addWidget(self.phq9_combobox_q3)
        layout.addWidget(phq9_label_q4)
        layout.addWidget(self.phq9_combobox_q4)
        layout.addWidget(phq9_label_q5)
        layout.addWidget(self.phq9_combobox_q5)
        layout.addWidget(phq9_label_q6)
        layout.addWidget(self.phq9_combobox_q6)
        layout.addWidget(phq9_label_q7)
        layout.addWidget(self.phq9_combobox_q7)
        layout.addWidget(phq9_label_q8)
        layout.addWidget(self.phq9_combobox_q8)
        layout.addWidget(phq9_label_q9)
        layout.addWidget(self.phq9_combobox_q9)
        layout.addWidget(self.depression_submit_button)

        self.setLayout(layout)

    def submit_depression(self):
        try:
            sql_conn = sqlite3.connect("healthapp.db")
            sql_cursor = sql_conn.cursor()

            date_now = datetime.now().date().isoformat()
            depression_value = phq9_scoring(self.phq9_combobox_list)
            q9_bool = phq9_q9(self.phq9_combobox_list[8])

            sql_cursor.execute(
                "SELECT user_trackablesID "
                "FROM user_trackables "
                "WHERE trackableID = 9 AND userID = ?",
                (self.user_ID,)
            )

            result = sql_cursor.fetchone()
            if result is None:
                print("No trackable found for this user.")
                return

            trackable_id = result[0]

            sql_cursor.execute(
                "INSERT INTO user_trackables_entries"
                "(user_trackablesID, entry_date, value)"
                "VALUES (?, ?, ?)",
                (trackable_id, date_now, depression_value)
            )

            if q9_bool:
                sql_cursor.execute(
                "INSERT INTO bool_user_trackables"
                "(user_trackablesID, bool_value)"
                "VALUES (?, ?)",
                (trackable_id, q9_bool)
                )

            sql_conn.commit()

        except Exception as e:
            print("Error submitting depression value:", e)

        finally:
            sql_conn.close()

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4


        self.move(x, y)

class TrackSleepWindow(QDialog):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)

        self.user_ID = user_ID

        self.setWindowTitle("Sleep Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 150
        win_width = 300
        self.resize(win_width, win_height)
        self.center()
        self.setFixedSize(win_width, win_height)

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        sleep_quality_label = QLabel("Sleep Quality")
        sleep_length_label = QLabel("Sleep Length")

        self.sleep_quality_combobox = QComboBox()
        for i in range(0, 11):
            self.sleep_quality_combobox.addItem(str(i))

        self.sleep_length_combobox = QComboBox()
        for i in range(0, 11):
            self.sleep_length_combobox.addItem(str(i))

        self.sleep_submit_button = QPushButton("Submit")
        self.sleep_submit_button.clicked.connect(lambda: (self.submit_sleep(), self.close()))

        layout.addWidget(sleep_quality_label)
        layout.addWidget(self.sleep_quality_combobox)
        layout.addWidget(sleep_length_label)
        layout.addWidget(self.sleep_length_combobox)
        layout.addWidget(self.sleep_submit_button)

        self.setLayout(layout)

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

    def submit_sleep(self):
        try:
            sql_conn = sqlite3.connect("healthapp.db")
            sql_cursor = sql_conn.cursor()

            date_now = datetime.now().date().isoformat()
            sleep_quality_value = self.sleep_quality_combobox.currentIndex()
            sleep_length_value = self.sleep_length_combobox.currentIndex()

            sql_cursor.execute(
                "SELECT user_trackablesID "
                "FROM user_trackables "
                "WHERE trackableID = 3 OR trackableID = 4 AND userID = ?"
                "ORDER BY trackableID ASC",
                (self.user_ID,)
            )

            result = sql_cursor.fetchall()
            if result is None:
                print("No trackable found for this user.")
                return

            trackable_id_quality = result[0][0]
            trackable_id_length = result[1][0]

            sql_cursor.execute(
                "INSERT INTO user_trackables_entries"
                "(user_trackablesID, entry_date, value)"
                "VALUES (?, ?, ?)",
                (trackable_id_quality, date_now, sleep_quality_value)
            )

            sql_cursor.execute(
                "INSERT INTO user_trackables_entries"
                "(user_trackablesID, entry_date, value)"
                "VALUES (?, ?, ?)",
                (trackable_id_length, date_now, sleep_length_value)
            )

            sql_conn.commit()

        except Exception as e:
            print("Error submitting sleep values:", e)

        finally:
            sql_conn.close()

class TrackSelfHarmWindow(QDialog):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Self Harm Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 800
        win_width = 600
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()



        widget = QWidget()
        widget.setLayout(layout)
        self.setLayout(layout)

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4


        self.move(x, y)

class TrackAlcoholAbuseWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Alcohol Abuse Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 800
        win_width = 600
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setLayout(layout)

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

class TrackDrugAbuseWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Drug Abuse Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 800
        win_width = 600
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setLayout(layout)

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

class TrackEatingHabitsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eating Habits Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 800
        win_width = 600
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setLayout(layout)

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

 # ----------- User Dialog Windows -----------
class CreateUserWindow(QDialog):
    def __init__(self, parent=None):
            # Initialize window + information
        super().__init__(parent)
        self.setWindowTitle("Create User")
        self.setWindowIcon(QIcon("logo.ico"))

        win_width = 800
        win_height = 600
        self.resize(win_width, win_height)

        self.center()

            # Setting stylesheets and layout
        self.setStyleSheet(_style)

        layout = QGridLayout()

        titel1 = QLabel("Please enter your user information:")
        titel2 = QLabel("Please select which items you would like to track:")

        titel1.setStyleSheet("""
            font-size: 16pt;
            font-weight: bold;
            font-family: "Times New Roman", Times, serif;
            margin-bottom: 10px;
        """)
        titel2.setStyleSheet("""
            font-size: 16pt;
            font-weight: bold;
            font-family: "Times New Roman", Times, serif;
            margin-top: 30px;
            margin-bottom: 10px;
        """)

            # Adding widgets
        layout.addWidget(titel1, 0, 0,  alignment = Qt.AlignLeft)
        layout.addWidget(titel2, 6, 0, alignment = Qt.AlignLeft)

        layout.addWidget(QLabel("First Name"), 1, 0)
        layout.addWidget(QLabel("Last Name"), 2, 0)
        layout.addWidget(QLabel("Gender"), 3, 0)
        layout.addWidget(QLabel("Age"), 4, 0)
        layout.addWidget(QLabel("E-Mail"), 5, 0)

        fn_input = QLineEdit()
        ln_input = QLineEdit()
        gender_input = QLineEdit()
        age_input = QLineEdit()
        email_input = QLineEdit()

        layout.addWidget(fn_input, 1, 1)
        layout.addWidget(ln_input, 2, 1)
        layout.addWidget(gender_input, 3, 1)
        layout.addWidget(age_input, 4, 1)
        layout.addWidget(email_input, 5, 1)

        layout.addWidget(QLabel("Overall Mood"), 7, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Sleep"), 8, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Anxiety"), 9, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Depression"), 10, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Self Harm"), 11, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Alcohol Abuse"), 12, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Drug Abuse"), 13, 0, alignment = Qt.AlignLeft)
        layout.addWidget(QLabel("Eating Habits"), 14, 0, alignment = Qt.AlignLeft)

        check_input_mood = QCheckBox()
        check_input_sleep = QCheckBox()
        check_input_anxiety = QCheckBox()
        check_input_depression = QCheckBox()
        check_input_self_harm = QCheckBox()
        check_input_alcohol = QCheckBox()
        check_input_drugs = QCheckBox()
        check_input_eating = QCheckBox()

        layout.addWidget(check_input_mood, 7, 1, alignment = Qt.AlignRight)
        layout.addWidget(check_input_sleep, 8, 1, alignment = Qt.AlignRight)
        layout.addWidget(check_input_anxiety, 9, 1, alignment = Qt.AlignRight)
        layout.addWidget(check_input_depression, 10, 1, alignment = Qt.AlignRight)
        layout.addWidget(check_input_self_harm, 11, 1, alignment = Qt.AlignRight)
        layout.addWidget(check_input_alcohol, 12, 1, alignment = Qt.AlignRight)
        layout.addWidget(check_input_drugs, 13, 1, alignment = Qt.AlignRight)
        layout.addWidget(check_input_eating, 14, 1, alignment = Qt.AlignRight)

            # Creating send button and setting style
        create_user_button = QPushButton("Create User")
        create_user_button.clicked.connect(lambda: self.on_create_clicked(fn_input, ln_input, gender_input, age_input, email_input, check_input_mood, check_input_sleep, check_input_anxiety, check_input_depression, check_input_self_harm, check_input_alcohol, check_input_drugs, check_input_eating))

        create_user_button.setStyleSheet("""
            	border-style: solid;
	            border-color: #050a0e;
	            border-width: 1px;
	            border-radius: 5px;
	            color: #d3dae3;
	            padding: 2px;
                background-color: #100E19;
                font-size: 16px;
        """)

        layout.addWidget(create_user_button, 16, 1, alignment = Qt.AlignRight)

        widget = QWidget()
        widget.setLayout(layout)
        self.setLayout(layout)

        # Defining functions necesarry for window
    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

        # Function for creating user and setting trackables
    def on_create_clicked(self, fn_input, ln_input, gender_input, age_input, email_input, check_input_mood, check_input_sleep, check_input_anxiety, check_input_depression, check_input_self_harm, check_input_alcohol, check_input_drugs, check_input_eating):
        fn_input_text = fn_input.text()
        ln_input_text = ln_input.text()
        gender_input_text = gender_input.text()
        try:
            age_input_text = int(age_input.text())
        except:
            QMessageBox.warning(self, "Input Error", "Age must be a number.")
            return
        email_input_text = email_input.text()
        health_func.insert_user(fn_input_text, ln_input_text, gender_input_text, age_input_text, email_input_text)

        sql_conn = sqlite3.connect("healthapp.db")
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute("SELECT userID FROM users WHERE email = ?", (email_input_text,))
        userID = sql_cursor.fetchone()[0]
        sql_conn.close()

        clicked_mood = check_input_mood.isChecked()
        clicked_sleep = check_input_sleep.isChecked()
        clicked_anxiety = check_input_anxiety.isChecked()
        clicked_depression = check_input_depression.isChecked()
        clicked_self_harm = check_input_self_harm.isChecked()
        clicked_alcohol = check_input_alcohol.isChecked()
        clicked_drugs = check_input_drugs.isChecked()
        clicked_eating = check_input_eating.isChecked()

        if clicked_mood:
            health_func.track_mood(userID)
        if clicked_sleep:
            health_func.track_sleep(userID)
        if clicked_anxiety:
            health_func.track_anxiety(userID)
        if clicked_depression:
            health_func.track_depression(userID)
        if clicked_self_harm:
            health_func.track_self_harm(userID)
        if clicked_alcohol:
            health_func.track_alcohol_abuse(userID)
        if clicked_drugs:
            health_func.track_drug_abuse(userID)
        if clicked_eating:
            health_func.track_eating_habits(userID)


#   ----------- Main Window -----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Application Defaults
        self.setWindowTitle("HealthApp")
        self.setWindowIcon(QIcon("logo.ico"))

        # Window Sizes in 16:9
        self.setMinimumSize(QSize(854, 480))
        self.setMaximumSize(QSize(1920, 1080))
        self.resize(1280, 720)

        self.setStyleSheet(_style)

        # -------------------- Menubar --------------------
        menubar = self.menuBar()

        # User menu actions
        user_menu = menubar.addMenu("User")
        create_user_action = user_menu.addAction("Create User")
        create_user_action.triggered.connect(self.create_user_box)
        change_user_action = user_menu.addAction("Change User")
        modify_user_action = user_menu.addAction("Modify User")
        delete_user_action = user_menu.addAction("Delete User")

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
        exit_application_action = application_menu.addAction("Exit")
        exit_application_action.triggered.connect(self.close)

        # -------------------- Scrolling Label --------------------
        # Create a toolbar to hold the scrolling label
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setAllowedAreas(Qt.TopToolBarArea)
        toolbar.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Create the scrolling label
        scrolling_label = ScrollingLabel(give_message())
        scrolling_label.setFixedHeight(30)
        scrolling_label.setStyleSheet("background: transparent; color: #a9b7c6; font-family: 'Arial'; font-size: 18px; font-weight: bold;")  # adjust color if needed
        toolbar.addWidget(scrolling_label)

    # -------------------- Methods --------------------
    def create_user_box(self):
        dialog = CreateUserWindow(self)
        dialog.exec_()

    def create_tracking_mood_box(self):
        dialog = TrackMoodWindow(user_ID)
        dialog.exec_()

    def create_tracking_anxiety_box(self):
        dialog = TrackAnxietyWindow(user_ID)
        dialog.exec_()

    def create_tracking_depression_box(self):
        dialog = TrackDepressionWindow(user_ID)
        dialog.exec_()

    def create_tracking_sleep_box(self):
        dialog = TrackSleepWindow(user_ID)
        dialog.exec_()

    def create_tracking_self_harm_box(self):
        dialog = TrackSelfHarmWindow(user_ID)
        dialog.exec_()

    def create_tracking_alcohol_abuse_box(self):
        dialog = TrackAlcoholAbuseWindow(self)
        dialog.exec_()

    def create_tracking_drug_abuse_box(self):
        dialog = TrackDrugAbuseWindow(self)
        dialog.exec_()

    def create_tracking_eating_habits_box(self):
        dialog = TrackEatingHabitsWindow(self)
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())