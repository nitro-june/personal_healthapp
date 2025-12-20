from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from jupyter_lsp.specs import sql
from datetime import datetime

# Logic for combobox PYQT

    # GAD7 scoring - Anxiety
def gad7_scoring(comboboxes):
    q1 = comboboxes[0].currentIndex()
    q2 = comboboxes[1].currentIndex()
    q3 = comboboxes[2].currentIndex()
    q4 = comboboxes[3].currentIndex()
    q5 = comboboxes[4].currentIndex()
    q6 = comboboxes[5].currentIndex()
    q7 = comboboxes[6].currentIndex()

    total_score = q1 + q2 + q3 + q4 + q5 + q6 + q7
    return total_score

    # PHQ9 scoring - Depression
def phq9_scoring(comboboxes):
    q1 = comboboxes[0].currentIndex()
    q2 = comboboxes[1].currentIndex()
    q3 = comboboxes[2].currentIndex()
    q4 = comboboxes[3].currentIndex()
    q5 = comboboxes[4].currentIndex()
    q6 = comboboxes[5].currentIndex()
    q7 = comboboxes[6].currentIndex()
    q8 = comboboxes[7].currentIndex()
    q9 = comboboxes[8].currentIndex()

    total_score = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
    return total_score

def phq9_q9(q9):
    q9 = q9.currentIndex()

    if q9 != 0:
        return True
    else:
        return False

    # AUDIT-C scoring - Alcohol abuse
def auditc_scoring(auditc_1, auditc_2, auditc_3):
    q1 = auditc_1.currentIndex()
    q2 = auditc_2.currentIndex()
    q3 = auditc_3.currentIndex()

    total_score = q1 + q2 + q3
    return total_score

    # Eat26 scoring - Eating habits
def eat26_calculate_values(combobox_input):
    q = combobox_input.comboBox.currentIndex()
    if q == 3:
        return 1
    elif q == 4:
        return 2
    elif q == 5:
        return 3
    else:
        return 0

def eat26_scoring(comboboxes):
    total_score = 0

    # questions 1–25
    for cb in comboboxes[:-1]:
        total_score += eat26_calculate_values(cb)

    # question 26 (reverse scored)
    q26_index = comboboxes[-1].comboBox.currentIndex()

    if q26_index == 0:
        q26_score = 3
    elif q26_index == 1:
        q26_score = 2
    elif q26_index == 2:
        q26_score = 1
    else:
        q26_score = 0

    total_score += q26_score
    return total_score