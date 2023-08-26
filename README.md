# Problem Statement
Manually extract the timetable as HTML from the IN4SIT webpage and parse it into a csv.
The file generated should be a .csv which can be imported into Google Calendar.

# How to use
0. Install python lmao
1. Download convert.py and create a 'source.txt' file in the same directory
2. Log into IN4SIT
3. Open the [shortcut](https://in4sit.singaporetech.edu.sg/psc/CSSISSTD/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL) in the same browser
4. Open Inspect Element (CTRL + SHIFT + I)
5. Copy the \<body\> and paste it in 'source.txt'
6. Run convert.py (double click)
7. Import 'output.csv' into Google Calendar

# How it works
0. Magic
1. Clean up all the useless HTML tags and keeps the important bits (run spellchecks here as well)
2. Split data by course, then do further cleaning to remove headers and labels
3. Extract important info into their own global variables
4. Use the variables to construct a calendar event (in .csv format)
5. Merge all the lists and output as a .csv file

# Alternatives (but they didn't work for me lolz)
[SIT Timetable Grabber](https://chrome.google.com/webstore/detail/sit-timetable-grabber/cnffedmfildfgejcckjcmhabbdkpcibh/)

[Timetable Grabber - SIT](https://github.com/JustBrandonLim/timetable-grabber-sit)

# Credits
I made it. Thanks to Google and stackoverflow for answering my questions. No thanks to the school for not having an option to export as CSV/ICS.

---

# dev notes pls ignore

## CSV Headers
! Remember: Surround data with " if it has commas

Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private

Final exam,05/30/2020,10:00 AM,05/30/2020,1:00 PM,False,50 multiple choice questions and two essay questions,"Columbia, Schermerhorn 614",True


## data reference

<course_info> // breaks down into <course_id> - <name_of_course>

<Status> // can just ignore, it's all probably enrolled
<Units> // number up to 2dp for some reason
<Grading> // graded or pass/fail

// at the start of each component
<Class_Nbr> // unique id for the class
<Section> // `ALL` or a letter-number pair like `P4`, L-Lecture / P-Laboratory / W-Workshop
<Component> // Lecture/Laboratory/Workshop

// repeats
<Days_and_Times> // time of the class
<Room> // usually the same, Online or room id in the form of <campus>-<room_id> like `SP-SR2E`
<Instructor> // name of instructor in full caps, trailing ` .` to clean up
<Start/End_Date> // formatted as `DD/MM/YYYY - DD/MM/YYYY`
