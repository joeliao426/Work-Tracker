# Student Assignment Tracker
This is Student Assignment Tracker, made by Carolyn Ji and Joe Liao.

The purpose of this app is to provide a tool for students to keep track of their upcoming due assignments. This is especially important for middle school students because they are transitioning to having more / harder classes, and it is very difficult for them to keep track of all the assignments from their different classes. So this app will ask them to input all their assignments, as well as conflicting classes and any other scheduling details. Then, the students can see their upcoming assignments on a calender, and AI will help the student create an appropriate schedule based on their available time, assignment due date, priority, and time to complete.

To build this app, we used python for the coding, streamlit for the UI, and OpenAI to generate the schedule.

We used AI to generate a schedule for the students. The AI can take the information the student gives them and generate a schedule using it. We did this by giving the AI a prompt: telling it that it's a schedule maker for the student, and that it must make schedules based on the information given. Then, we made it be able to read all the information given by the student, including all the assignment details and extra information so the AI could use that to make a desirable schedule for the student.

Instructions:
OPENING THE APP:
1. Navigate to your terminal and type "streamlit run .\[app name].py
2. This should open up the app in your browser

NAVIGATING THE APP
1. To start, navigate to the left sidebar, here you will find a lot of places you can input information. Start by completing the Schedule information, including the time available each day, the sleep time, and any extra information you want to include. It is recommended to include what day of the week and month it currently is, so the AI has no chance of assuming the wrong day.
2. To add an assignment, scroll down to the "Assignment Information" section, and enter in all the details, including assignment name, subject, due date, priority (1=lowest, 10=highest), time needed to complete, and progress. After that, click "add asignment" and you will see your assignment pop up in the "Assignments" tab. To add a class, scroll down to the "class information" tab and add the class name, start and end time, and the days it's on. After that, click "add class" and you should see it pop up in the "Classes" section of the assignments tab. You can sort the class and assignments information based on their name, time, deatils, priority, or any other input.
3. Next, go to the "Calender" tab. Here you will see a calender view. Select the year and month your want to view and you will be able to see all the assignments in that month and their due date.
4. To view more on an assignment, you can click on it in the calender tab, then go to the "details" tab, where you can see the information of the selected assignment. You can also do this by going straight to the details tab and selecting the assignment you want to see.
5. Lastly, to generate a schedule, go to the "Schedule" tab and click the "generate schedule" button. Wait for a minute and then the AI will generate a schedule for you based on the information you have entered.
