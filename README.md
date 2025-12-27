# Personal Mental-Health Tracker

<br/>

<p align="center">
  <img width="300" height="300" src="logo.jpg">
</p>

<br/>

An easy way to keep track of your mental health, without giving your data away to companies that might use that data for their own purposes.

---

## Summary

The mental-health tracker is mostly built in python and uses sqlite to localy save the data you input. Then this data is displayed on the convenient dashboard, which you can always customize the layout of yourself. Many of the trackables are similar to commonly used screening tests for depression or anxiety.

The UI is mostly built using PyQt5 and Matplotlib.

The print to PDF feature for the trackables uses ... (Build this with quick description or integration of an LLM or something similar?) -> basically reads out the scores. writes a short description based on medical "diagnosis and screenings" and lists the graphs of how the user feels.

--- 

## Features

### Trackables

You are able to track following things in the app:
- **Mood** -> on a scale of **0 - 10**
- **Anxiety** -> on a scale of **0 - 15**
- **Depression** -> on a scale of **0 - 27**
- **Sleep**
  - **Sleep Quality** -> on a scale of **0 - 10**
  - **Sleep Length** -> on a scale of **0 - 10**
- **Self Harm** -> **yes or no**
- **Alcohol abuse** -> on a scale of **0 - 12**
- **Drug Abuse** -> **yes or no**
- **Eating Habits** -> on a scale of **0 -78**

These values may seem very abstract and nonsensical, but most of these scales are based on screening tests used for specific issues:

The **anxiety scale** is based on the **GAD-7** screening test, which is used to determine the severity of anxiety. It is commonly used for general anxiety disorder, but also performs well for other anxiety disorders.

The **depression scale** is based on the **PHQ-9** screening test, which is commonly used to screen, diagonose, monitor and measure the severity of depression. It is important to note, that even if you score below mild severity (**0 - 4**), if **question 9** is answered with anything else than "Not at all", further assessment by a trained professional is advised.

The questionaire for **alcohol abuse** is based on the **AUDIT-C** *(Alcohol Use Disorder Identification Test)*.

The questionaire for **"drug abuse"** is based on **TICS** *(Two-Item Conjoint Screen for Alcohol and Other Drug Problems)*.

The questionaire for **eating habits** is based on **EAT-26**, which is the most widely used standardized self-report test for the measure of symptoms and concerns regarding eating disorders.

### Miscellaneous

- A scrolling text of a randomly chosen sentance, which are kind and positive.
- Possibility for multiple users -> *currently it is a local application with a stand-alone-database, so there's no reason for multiple users* - theoretically changing the application to use a file-share-database should be possible
-

---

## Basic Usage

### Create a User

### Select a User

### Track your Data

### Displaying your Data

### Creating a PDF from your Data

---

### Disclaimer

**This app does not provide medical advice.**

*This app is for informational purposes only and does not replace professional medical advice. Always consult a licensed healthcare provider for concerns about your health.*

### Crisis Support

**If you or your loved ones are in need of support, there are many available resources:**

#### Germany

- **112** - Emergency Services
- **116 117** - Non-life-threatining medical assistance
- **0800 111 0 111 /  0800 111 0 222** - hotline for psychological crisis -> *around 2026 a planned **113** number will be implemented*

#### United States

- **911** - Emergency Services
- **741741** - Crisis Text Line -> *text "HOME"* to the specified number
- **1-800-662-HELP (4357)** - SAMHSA National Helpline (substance use & mental health information)
- **1-877-565-8860** - The Trevor Project -> *support for LGBTQ+ youth*

#### Canada

- **911** - Emergency Services
- **741741** - Crisis Text Line -> *text "HOME"* to the specified number
- **1-833-456-4566** - Canada Suicide Prevention Services

### Useful Resources

- **[The Trevor Project](https://www.thetrevorproject.org/)**  - crisis support, education and research for young LGTBQ+ identifying people
- **[The National HIV Curriculum](https://www.hiv.uw.edu/)** led by the University of Washington has great resources, which I used as a source to implement some of the quetionaires and scales.
- **[Schwulenberatung Berlin](https://schwulenberatungberlin.de/)** - a non-profit organization that helps queer people in Berlin.