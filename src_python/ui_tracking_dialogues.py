from datetime import datetime

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src_python.functions_healthapp import (
    add_bool_user_entry,
    add_user_entry,
    get_user_trackable_id,
)
from src_python.functions_tests import (
    auditc_scoring,
    eat26_scoring,
    gad7_scoring,
    phq9_q9,
    phq9_scoring,
)

# Fallback style; main module injects active QSS at runtime.
_style = ""

# ---------- Action Windows for Tracking -----------

# All of these widgets follow the same pattern
# Class/Widget setup
# Add content of the class
# Defining a method that executes SQLite commands
class TrackMoodWindow(QDialog):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)

        self.user_ID = user_ID

        self.setWindowTitle("Mood Questionaire")
        self.setWindowIcon(QIcon("resources/images/logo.ico"))

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
            date_now = datetime.now().date().isoformat()
            mood_value = self.mood_combobox.currentIndex()

            trackable_id = get_user_trackable_id(self.user_ID, 2)
            if not trackable_id:
                print("No trackable found for this user.")
                return

            add_user_entry(trackable_id, mood_value, date_now)

        except Exception as e:
            print("Error submitting mood:", e)

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
        self.setWindowIcon(QIcon("resources/images/logo.ico"))

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

        self.gad7_combobox_list = (self.gad7_combobox_q1, self.gad7_combobox_q2, self.gad7_combobox_q3,
                                   self.gad7_combobox_q4, self.gad7_combobox_q5, self.gad7_combobox_q6,
                                   self.gad7_combobox_q7)

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
            date_now = datetime.now().date().isoformat()
            anxiety_value = gad7_scoring(self.gad7_combobox_list)

            trackable_id = get_user_trackable_id(self.user_ID, 1)
            if not trackable_id:
                print("No trackable found for this user.")
                return

            add_user_entry(trackable_id, anxiety_value, date_now)

        except Exception as e:
            print("Error submitting mood:", e)

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
        self.setWindowIcon(QIcon("resources/images/logo.ico"))

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

        self.phq9_combobox_list = (self.phq9_combobox_q1, self.phq9_combobox_q2, self.phq9_combobox_q3,
                                   self.phq9_combobox_q4, self.phq9_combobox_q5, self.phq9_combobox_q6,
                                   self.phq9_combobox_q7, self.phq9_combobox_q8, self.phq9_combobox_q9)

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
            date_now = datetime.now().date().isoformat()
            depression_value = phq9_scoring(self.phq9_combobox_list)
            q9_bool = phq9_q9(self.phq9_combobox_list[8])

            trackable_id = get_user_trackable_id(self.user_ID, 9)
            if not trackable_id:
                print("No trackable found for this user.")
                return

            add_user_entry(trackable_id, depression_value, date_now)

            if q9_bool:
                add_bool_user_entry(trackable_id, q9_bool)

        except Exception as e:
            print("Error submitting depression value:", e)

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
        self.setWindowIcon(QIcon("resources/images/logo.ico"))

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
            date_now = datetime.now().date().isoformat()
            sleep_quality_value = self.sleep_quality_combobox.currentIndex()
            sleep_length_value = self.sleep_length_combobox.currentIndex()

            trackable_id_quality = get_user_trackable_id(self.user_ID, 3)
            trackable_id_length = get_user_trackable_id(self.user_ID, 4)

            if not trackable_id_quality and not trackable_id_length:
                QMessageBox.warning(self, "Error", "Sleep trackables not set up for this user.")
                return

            if trackable_id_quality:
                add_user_entry(trackable_id_quality, sleep_quality_value, date_now)

            if trackable_id_length:
                add_user_entry(trackable_id_length, sleep_length_value, date_now)

        except Exception as e:
            print("Error submitting sleep values:", e)


class TrackSelfHarmWindow(QDialog):
    def __init__(self, user_ID, parent=None):
        super().__init__(parent)

        self.user_ID = user_ID

        self.setWindowTitle("Self Harm Questionaire")
        self.setWindowIcon(QIcon("resources/images/logo.ico"))

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
            date_now = datetime.now().date().isoformat()
            self_harm_bool = self.self_harm_combobox.currentIndex()

            trackable_id = get_user_trackable_id(self.user_ID, 5)
            if not trackable_id:
                print("No trackable found for this user.")
                return

            add_user_entry(trackable_id, self_harm_bool, date_now)

        except Exception as e:
            print("Error submitting sleep values:", e)

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
        self.setWindowIcon(QIcon("resources/images/logo.ico"))

        win_height = 300
        win_width = 300
        self.resize(win_width, win_height)
        self.center()

        self.setStyleSheet(_style)

        layout = QVBoxLayout()

        alcohol_abuse_label = QLabel("Alcohol Abuse Explanation")
        auditc_label_q1 = QLabel("How often do you have a drink containing alcohol?")
        auditc_label_q2 = QLabel(
            "How many drinks containing alcohol do you have on a typical day when you are drinking?")
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
            date_now = datetime.now().date().isoformat()
            alcohol_abuse_value = auditc_scoring(self.auditc_combobox_list)

            trackable_id = get_user_trackable_id(self.user_ID, 6)
            if not trackable_id:
                print("No trackable found for this user.")
                return

            add_user_entry(trackable_id, alcohol_abuse_value, date_now)

        except Exception as e:
            print("Error submitting alcohol abuse values:", e)

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
        self.setWindowIcon(QIcon("resources/images/logo.ico"))

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
            date_now = datetime.now().date().isoformat()
            drug_abuse_bool_q1 = self.drug_abuse_combobox_q1.currentIndex()
            drug_abuse_bool_q2 = self.drug_abuse_combobox_q2.currentIndex()
            drug_abuse_bool = 0

            if drug_abuse_bool_q1 == 1 or drug_abuse_bool_q2 == 1:
                drug_abuse_bool = 1

            trackable_id = get_user_trackable_id(self.user_ID, 7)
            if not trackable_id:
                print("No trackable found for this user.")
                return

            add_user_entry(trackable_id, drug_abuse_bool, date_now)

        except Exception as e:
            print("Error submitting drug abuse value:", e)

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
        self.setWindowIcon(QIcon("resources/images/logo.ico"))

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
        eat26_label_q1 = QLabel("I am terrified about being overweight or underweight.")
        eat26_label_q2 = QLabel("I avoid eating when I am hungry.")
        eat26_label_q3 = QLabel("I find myself preoccupied with food.")
        eat26_label_q4 = QLabel("I have gone on eating binges where I felt that I may not be able to stop.")
        eat26_label_q5 = QLabel("I have cut my food into small pieces.")
        eat26_label_q6 = QLabel("I feel that others pressure me to eat.")
        eat26_label_q7 = QLabel("I have engaged in secret eating. (eating in private / secret)")
        eat26_label_q8 = QLabel("I feel extremely guilty about eating.")
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

        eat26_label_list = (eat26_label_q1, eat26_label_q2, eat26_label_q3, eat26_label_q4, eat26_label_q5,
                            eat26_label_q6, eat26_label_q7, eat26_label_q8, eat26_label_q9, eat26_label_q10,
                            eat26_label_q11, eat26_label_q12, eat26_label_q13, eat26_label_q14, eat26_label_q15,
                            eat26_label_q16, eat26_label_q17, eat26_label_q18, eat26_label_q19, eat26_label_q20,
                            eat26_label_q21, eat26_label_q22, eat26_label_q23, eat26_label_q24, eat26_label_q25,
                            eat26_label_q26)

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
        scroll.setObjectName("EatingScroll")

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
            date_now = datetime.now().date().isoformat()

            eating_habits_value = eat26_scoring(self.eat26_combobox_list)

            trackable_id = get_user_trackable_id(self.user_ID, 8)

            if trackable_id is None:
                QMessageBox.warning(
                    self,
                    "User is currently not tracking eating habits.",
                )
                return

            add_user_entry(trackable_id, eating_habits_value, date_now)

        except Exception as e:
            print("Error submitting eating habits value:", e)

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = screen_geometry.width() // 4
        y = screen_geometry.height() // 4

        self.move(x, y)