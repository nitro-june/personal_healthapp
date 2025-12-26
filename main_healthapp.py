import sys
import matplotlib
matplotlib.use('Qt5Agg')

import PyQt5 as PyQt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure

from refactor.functions_healthapp import *
from refactor.functions_tests import *

with open("MaterialDark.qss", "r") as f:
    _style = f.read()

# TEMPORARY userID until I have implemented a way to get the userID
# user_ID = 2

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

        win_height = 600
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

        win_height = 700
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
                "INSERT INTO user_trackables_entries "
                "(user_trackablesID, entry_date, value)"
                "VALUES (?, ?, ?)",
                (trackable_id, date_now, depression_value)
            )

            if q9_bool:
                sql_cursor.execute(
                "INSERT INTO bool_user_trackables "
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
                "INSERT INTO user_trackables_entries "
                "(user_trackablesID, entry_date, value)"
                "VALUES (?, ?, ?)",
                (trackable_id_quality, date_now, sleep_quality_value)
            )

            sql_cursor.execute(
                "INSERT INTO user_trackables_entries "
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

        self.user_ID = user_ID

        self.setWindowTitle("Self Harm Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 100
        win_width = 300
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        self_harm_label = QLabel("Did self-harm occur?")

        self.self_harm_combobox = QComboBox()
        self.self_harm_combobox.addItem("No")
        self.self_harm_combobox.addItem("Yes")

        self.self_harm_submit_button = QPushButton("Submit")
        self.self_harm_submit_button.clicked.connect(lambda: (self.submit_self_harm(), self.close()))

        layout.addWidget(self_harm_label)
        layout.addWidget(self.self_harm_combobox)
        layout.addWidget(self.self_harm_submit_button)

        self.setLayout(layout)

    def submit_self_harm(self):
        try:
            sql_conn = sqlite3.connect("healthapp.db")
            sql_cursor = sql_conn.cursor()

            date_now = datetime.now().date().isoformat()
            self_harm_bool = self.self_harm_combobox.currentIndex()

            sql_cursor.execute(
                "SELECT user_trackablesID "
                "FROM user_trackables "
                "WHERE trackableID = 5 AND userID = ?"
                "ORDER BY trackableID ASC",
                (self.user_ID,)
            )

            result = sql_cursor.fetchone()
            if result is None:
                print("No trackable found for this user.")
                return

            trackable_id = result[0]

            sql_cursor.execute(
                "INSERT INTO user_trackables_entries "
                "(user_trackablesID, entry_date, value)"
                "VALUES (?, ?, ?)",
                (trackable_id, date_now, self_harm_bool)
            )

            sql_conn.commit()

        except Exception as e:
            print("Error submitting sleep values:", e)

        finally:
            sql_conn.close()

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4


        self.move(x, y)

class TrackAlcoholAbuseWindow(QDialog):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)

        self.user_ID = user_ID

        self.setWindowTitle("Alcohol Abuse Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 300
        win_width = 300
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        alcohol_abuse_label = QLabel("Alcohol Abuse Explanation")
        auditc_label_q1 = QLabel("How often do you have a drink containing alcohol?")
        auditc_label_q2 = QLabel("How many drinks containing alcohol do you have on a typical day when you are drinking?")
        auditc_label_q3 = QLabel("How often do you have six or more drinks on one occasion?")

        self.auditc_combobox_q1 = QComboBox()
        self.auditc_combobox_q1.addItem("Never")
        self.auditc_combobox_q1.addItem("Monthly or less")
        self.auditc_combobox_q1.addItem("2-4 times a month")
        self.auditc_combobox_q1.addItem("2-3 times a week")
        self.auditc_combobox_q1.addItem("4 or more times a week")

        self.auditc_combobox_q2 = QComboBox()
        self.auditc_combobox_q2.addItem("1 or 2")
        self.auditc_combobox_q2.addItem("3 or 4")
        self.auditc_combobox_q2.addItem("5 or 6")
        self.auditc_combobox_q2.addItem("7 or 9")
        self.auditc_combobox_q2.addItem("10 or more")

        self.auditc_combobox_q3 = QComboBox()
        self.auditc_combobox_q3.addItem("Never")
        self.auditc_combobox_q3.addItem("Less than monthly")
        self.auditc_combobox_q3.addItem("Monthly")
        self.auditc_combobox_q3.addItem("Weekly")
        self.auditc_combobox_q3.addItem("Daily or almost daily")

        self.auditc_combobox_list = (self.auditc_combobox_q1, self.auditc_combobox_q2, self.auditc_combobox_q3)

        self.auditc_submit_button = QPushButton("Submit")
        self.auditc_submit_button.clicked.connect(lambda: (self.submit_alcohol_abuse(), self.close()))

        layout.addWidget(alcohol_abuse_label)
        layout.addWidget(auditc_label_q1)
        layout.addWidget(self.auditc_combobox_q1)
        layout.addWidget(auditc_label_q2)
        layout.addWidget(self.auditc_combobox_q2)
        layout.addWidget(auditc_label_q3)
        layout.addWidget(self.auditc_combobox_q3)
        layout.addWidget(self.auditc_submit_button)

        self.setLayout(layout)

    def submit_alcohol_abuse(self):
        try:
            sql_conn = sqlite3.connect("healthapp.db")
            sql_cursor = sql_conn.cursor()

            date_now = datetime.now().date().isoformat()
            alcohol_abuse_value = auditc_scoring(self.auditc_combobox_list)

            sql_cursor.execute(
                "SELECT user_trackablesID "
                "FROM user_trackables "
                "WHERE trackableID = 6 AND userID = ?"
                "ORDER BY trackableID ASC",
                (self.user_ID,)
            )

            result = sql_cursor.fetchone()
            if result is None:
                print("No trackable found for this user.")
                return

            trackable_id = result[0]

            sql_cursor.execute(
                "INSERT INTO user_trackables_entries "
                "(user_trackablesID, entry_date, value)"
                "VALUES (?, ?, ?)",
                (trackable_id, date_now, alcohol_abuse_value)
            )

            sql_conn.commit()

        except Exception as e:
            print("Error submitting alcohol abuse values:", e)

        finally:
            sql_conn.close()

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

class TrackDrugAbuseWindow(QDialog):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)

        self.user_ID = user_ID

        self.setWindowTitle("Drug Abuse Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 150
        win_width = 600
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        drug_abuse_label_q1 = QLabel("Have you recently used drugs more than you meant to?")
        drug_abuse_label_q2 = QLabel("Have you felt you wanted or needed to cut down on your drug use?")

        self.drug_abuse_combobox_q1 = QComboBox()
        self.drug_abuse_combobox_q1.addItem("No")
        self.drug_abuse_combobox_q1.addItem("Yes")

        self.drug_abuse_combobox_q2 = QComboBox()
        self.drug_abuse_combobox_q2.addItem("No")
        self.drug_abuse_combobox_q2.addItem("Yes")

        self.drug_abuse_submit_button = QPushButton("Submit")
        self.drug_abuse_submit_button.clicked.connect(lambda: (self.submit_drug_abuse(), self.close()))

        layout.addWidget(drug_abuse_label_q1)
        layout.addWidget(self.drug_abuse_combobox_q1)
        layout.addWidget(drug_abuse_label_q2)
        layout.addWidget(self.drug_abuse_combobox_q2)
        layout.addWidget(self.drug_abuse_submit_button)

        self.setLayout(layout)

    def submit_drug_abuse(self):
        try:
            sql_conn = sqlite3.connect("healthapp.db")
            sql_cursor = sql_conn.cursor()

            date_now = datetime.now().date().isoformat()
            drug_abuse_bool_q1 = self.drug_abuse_combobox_q1.currentIndex()
            drug_abuse_bool_q2 = self.drug_abuse_combobox_q2.currentIndex()
            drug_abuse_bool = 0

            if drug_abuse_bool_q1 == 1 or drug_abuse_bool_q2 == 1:
                drug_abuse_bool = 1

            sql_cursor.execute(
                "SELECT user_trackablesID "
                "FROM user_trackables "
                "WHERE trackableID = 7 AND userID = ?"
                "ORDER BY trackableID ASC",
                (self.user_ID,)
            )

            result = sql_cursor.fetchone()
            if result is None:
                print("No trackable found for this user.")
                return

            trackable_id = result[0]

            sql_cursor.execute(
                "INSERT INTO user_trackables_entries "
                "(user_trackablesID, entry_date, value)"
                "VALUES (?, ?, ?)",
                (trackable_id, date_now, drug_abuse_bool)
            )

            sql_conn.commit()

        except Exception as e:
            print("Error submitting drug abuse value:", e)

        finally:
            sql_conn.close()

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

class TrackEatingHabitsWindow(QDialog):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)

        self.user_ID = user_ID

        self.setWindowTitle("Eating Habits Questionaire")
        self.setWindowIcon(QIcon("logo.ico"))

        win_height = 600
        win_width = 800
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        content_widget.setStyleSheet(_style)

        eat26_label_explanation = QLabel("Explanation")
        eat26_label_q1 = QLabel("I am terrified about being overweight.")
        eat26_label_q2 = QLabel("I avoid eating when I am hungry.")
        eat26_label_q3 = QLabel("I find myself preoccupied with food.")
        eat26_label_q4 = QLabel("I have gone on eating binges where I felt that I may not be able to stop.")
        eat26_label_q5 = QLabel("I have cut my food into small pieces.")
        eat26_label_q6 = QLabel("I am aware of the calorie content of foods that I eat.")
        eat26_label_q7 = QLabel("I particularly avoid food with a high carbohydrates content. (i.e. bread, rice, potatoes, etc.)")
        eat26_label_q8 = QLabel("I feel that others would prefer if I ate more.")
        eat26_label_q9 = QLabel("I vomit after I have eaten.")
        eat26_label_q10 = QLabel("I feel extremely guilty after eating.")
        eat26_label_q11 = QLabel("I am preoccupied with a desire to be thinner.")
        eat26_label_q12 = QLabel("I think about burning up calories when I exercise.")
        eat26_label_q13 = QLabel("Other people think that I am too thin.")
        eat26_label_q14 = QLabel("I am preoccupied with the thought of having fat on my body.")
        eat26_label_q15 = QLabel("I take longer than others to eat my meals.")
        eat26_label_q16 = QLabel("I avoid foods with sugar in them.")
        eat26_label_q17 = QLabel("I eat diet foods.")
        eat26_label_q18 = QLabel("I feel that food controls my life.")
        eat26_label_q19 = QLabel("I display self control around food.")
        eat26_label_q20 = QLabel("I feel that others pressure me to eat.")
        eat26_label_q21 = QLabel("I give too much time and thought to food.")
        eat26_label_q22 = QLabel("I feel uncomfortable after eating sweets.")
        eat26_label_q23 = QLabel("I engage in dieting behaviour.")
        eat26_label_q24 = QLabel("I like my stomach to be empty.")
        eat26_label_q25 = QLabel("I have the impulse to vomit after meals.")
        eat26_label_q26 = QLabel("I enjoy trying new rich foods.")

        eat26_label_list = (eat26_label_q1, eat26_label_q2, eat26_label_q3, eat26_label_q4, eat26_label_q5, eat26_label_q6, eat26_label_q7, eat26_label_q8, eat26_label_q9, eat26_label_q10, eat26_label_q11, eat26_label_q12, eat26_label_q13, eat26_label_q14, eat26_label_q15, eat26_label_q16, eat26_label_q17, eat26_label_q18, eat26_label_q19, eat26_label_q20, eat26_label_q21, eat26_label_q22, eat26_label_q23, eat26_label_q24, eat26_label_q25, eat26_label_q26)

        self.eat26_combobox_q1 = QComboBox()
        self.eat26_combobox_q2 = QComboBox()
        self.eat26_combobox_q3 = QComboBox()
        self.eat26_combobox_q4 = QComboBox()
        self.eat26_combobox_q5 = QComboBox()
        self.eat26_combobox_q6 = QComboBox()
        self.eat26_combobox_q7 = QComboBox()
        self.eat26_combobox_q8 = QComboBox()
        self.eat26_combobox_q9 = QComboBox()
        self.eat26_combobox_q10 = QComboBox()
        self.eat26_combobox_q11 = QComboBox()
        self.eat26_combobox_q12 = QComboBox()
        self.eat26_combobox_q13 = QComboBox()
        self.eat26_combobox_q14 = QComboBox()
        self.eat26_combobox_q15 = QComboBox()
        self.eat26_combobox_q16 = QComboBox()
        self.eat26_combobox_q17 = QComboBox()
        self.eat26_combobox_q18 = QComboBox()
        self.eat26_combobox_q19 = QComboBox()
        self.eat26_combobox_q20 = QComboBox()
        self.eat26_combobox_q21 = QComboBox()
        self.eat26_combobox_q22 = QComboBox()
        self.eat26_combobox_q23 = QComboBox()
        self.eat26_combobox_q24 = QComboBox()
        self.eat26_combobox_q25 = QComboBox()
        self.eat26_combobox_q26 = QComboBox()

        self.eat26_combobox_list = (
            self.eat26_combobox_q1, self.eat26_combobox_q2, self.eat26_combobox_q3,
            self.eat26_combobox_q4, self.eat26_combobox_q5, self.eat26_combobox_q6,
            self.eat26_combobox_q7, self.eat26_combobox_q8, self.eat26_combobox_q9,
            self.eat26_combobox_q10, self.eat26_combobox_q11, self.eat26_combobox_q12,
            self.eat26_combobox_q13, self.eat26_combobox_q14, self.eat26_combobox_q15,
            self.eat26_combobox_q16, self.eat26_combobox_q17, self.eat26_combobox_q18,
            self.eat26_combobox_q19, self.eat26_combobox_q20, self.eat26_combobox_q21,
            self.eat26_combobox_q22, self.eat26_combobox_q23, self.eat26_combobox_q24,
            self.eat26_combobox_q25, self.eat26_combobox_q26
        )

        for cb in self.eat26_combobox_list:
            self.create_comboboxes_questions(cb)

        self.eating_habits_submit_button = QPushButton("Submit")
        self.eating_habits_submit_button.clicked.connect(lambda: (self.submit_eating_habits(), self.close()))

        content_layout.addWidget(eat26_label_explanation)

        for i in range(26):
            content_layout.addWidget(eat26_label_list[i])
            content_layout.addWidget(self.eat26_combobox_list[i])

        content_layout.addWidget(self.eating_habits_submit_button)

        content_widget.setAutoFillBackground(True)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)

        scroll.viewport().setStyleSheet("background: transparent;")

        layout.addWidget(scroll)

        self.setLayout(layout)

    def create_comboboxes_questions(self, combobox_input):
        combobox_input.addItem("Never")
        combobox_input.addItem("Rarely")
        combobox_input.addItem("Sometimes")
        combobox_input.addItem("Often")
        combobox_input.addItem("Usually")
        combobox_input.addItem("Always")

    def submit_eating_habits(self):
        try:
            sql_conn = sqlite3.connect("healthapp.db")
            sql_cursor = sql_conn.cursor()

            date_now = datetime.now().date().isoformat()

            eating_habits_value = eat26_scoring(self.eat26_combobox_list)

            sql_cursor.execute(
                "SELECT user_trackablesID "
                "FROM user_trackables "
                "WHERE trackableID = 8 AND userID = ?"
                "ORDER BY trackableID ASC",
                (self.user_ID,)
            )

            result = sql_cursor.fetchone()

            if result is None:
                # Show a warning message box
                QMessageBox.warning(
                    self,  # parent window
                    "User is currently not tracking eating habits.",  # title
                )
                return  # keep the dialog open

            trackable_id = result[0]

            sql_cursor.execute(
                "INSERT INTO user_trackables_entries "
                "(user_trackablesID, entry_date, value)"
                "VALUES (?, ?, ?)",
                (trackable_id, date_now, eating_habits_value)
            )

            sql_conn.commit()

        except Exception as e:
            print("Error submitting eating habits value:", e)

        finally:
            sql_conn.close()


    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)

class UserIDDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter User ID")
        self.user_ID = None  # This will store the result

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Enter User E-Mail:"))
        self.input_line = QLineEdit()
        layout.addWidget(self.input_line)

        ok_btn = QPushButton("Submit")
        ok_btn.clicked.connect(self.submit)
        layout.addWidget(ok_btn)

        self.setLayout(layout)

    def submit(self):
        try:
            sql_conn = sqlite3.connect("healthapp.db")
            sql_cursor = sql_conn.cursor()

            email_value = self.input_line.text().strip()

            sql_cursor.execute(
                "SELECT userID FROM users WHERE LOWER(email) = LOWER(?)",
                (email_value,)
            )

            result = sql_cursor.fetchone()

            if result is None:
                # Show a warning message box
                QMessageBox.warning(
                    self,  # parent window
                    "User Not Found",  # title
                    f"No user found with email '{email_value}'"  # message
                )
                return  # keep the dialog open

            user_result = result[0]

            self.user_ID = user_result  # store input
            self.accept()  # close dialog with QDialog.Accepted

        except Exception as e:
            print("Error retrieving userID:", e)

        finally:
            sql_conn.close()

# ----------- Matplotlib Figure Widget for Helper Dock -----------
class MatplotlibWidget(QWidget):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent)

        # Create the Matplotlib Figure and Canvas
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axes = self.figure.add_subplot(111)  # single subplot

        # Create the navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, x, y, **kwargs):
        self.axes.plot(x, y, **kwargs)
        self.canvas.draw()  # Refresh the canvas

    def clear(self):
        self.axes.cla()
        self.canvas.draw()

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

        self.setLayout(layout)

        # Defining functions necesarry for window
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

        sql_conn = sqlite3.connect("healthapp.db")
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute("SELECT userID FROM users WHERE email = ?", (email_input_text,))
        result = sql_cursor.fetchone()
        sql_conn.close()
        if result is None:
            QMessageBox.warning(self, "Error", "User was not created correctly.")
            return
        userID = result[0]

        # Checkboxes
        try:
            if self.check_input_mood.isChecked():
                track_mood(userID)
            if self.check_input_sleep.isChecked():
                track_sleep(userID)
            if self.check_input_anxiety.isChecked():
                track_anxiety(userID)
            if self.check_input_depression.isChecked():
                track_depression(userID)
            if self.check_input_self_harm.isChecked():
                track_self_harm(userID)
            if self.check_input_alcohol.isChecked():
                track_alcohol_abuse(userID)
            if self.check_input_drugs.isChecked():
                track_drug_abuse(userID)
            if self.check_input_eating.isChecked():
                track_eating_habits(userID)
        except Exception as e:
            QMessageBox.critical(self, "Tracking Error", f"Failed to track items: {e}")
            return

        QMessageBox.information(self, "Success", f"User '{fn_input_text} {ln_input_text}' created successfully!")

        self.accept()

#   ----------- Main Window -----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.user_ID = None

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
        change_user_action.triggered.connect(self.open_user_dialog)
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
        toolbar.setStyleSheet("background-color: #1e1d23")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Create the scrolling label
        scrolling_label = ScrollingLabel(give_message())
        scrolling_label.setFixedHeight(30)
        scrolling_label.setStyleSheet("background: transparent; color: #a9b7c6; font-family: 'Arial'; font-size: 18px; font-weight: bold;")  # adjust color if needed
        toolbar.addWidget(scrolling_label)

        self.status = self.statusBar()
        self.update_status()

        # --------- For Docking Widgets ----------
        central_widget = QWidget()
        central_widget.setFixedSize(1, 1)
        self.setCentralWidget(central_widget)

        self.setDockNestingEnabled(True)

        plot_widget1 = MatplotlibWidget()
        plot_widget1.plot([0,1,2,3,4], [10,1,20,3,40], color='blue', marker='o')
        plot_widget2 = MatplotlibWidget()
        plot_widget2.plot([0,1,2,3,4], [1,4,30,35,10], color='blue', marker='o')
        plot_widget3 = MatplotlibWidget()
        plot_widget3.plot([0,1,2,3,4], [10,1,20,3,40], color='blue', marker='o')
        plot_widget4 = MatplotlibWidget()
        plot_widget4.plot([0,1,2,3,4], [10,1,20,3,40], color='blue', marker='o')

        # Keep track of docks per side
        self.docks_left = []
        self.docks_right = []

        # Example docks
        self.create_dock("Plot1", widgets=[plot_widget1], side="left")
        self.create_dock("Plot2", widgets=[plot_widget2], side="left")

        self.create_dock("Plot3", widgets=[plot_widget3], side="right")
        self.create_dock("Plot4", widgets=[plot_widget4], side="right")

    # -------------------- Methods --------------------
    def update_status(self):
        self.status.showMessage(f"Current User ID: {self.user_ID}")

    def open_user_dialog(self):
        dialog = UserIDDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.user_ID = dialog.user_ID  # update main window variable
            self.update_status()

    def create_dock(self, title, widgets, side="left"):
        """
        Create a dock, add it to the left/right, and split evenly with existing docks.
        """
        dock = QDockWidget(title, self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        for w in widgets:
            layout.addWidget(w)
        dock.setWidget(content_widget)

        if side.lower() == "left":
            self.addDockWidget(Qt.LeftDockWidgetArea, dock)
            # Split with the last dock on the left (if exists)
            if self.docks_left:
                self.splitDockWidget(self.docks_left[-1], dock, Qt.Vertical)
            self.docks_left.append(dock)

        elif side.lower() == "right":
            self.addDockWidget(Qt.RightDockWidgetArea, dock)
            if self.docks_right:
                self.splitDockWidget(self.docks_right[-1], dock, Qt.Vertical)
            self.docks_right.append(dock)

        return dock

    def create_user_box(self):
        dialog = CreateUserWindow(self)
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())