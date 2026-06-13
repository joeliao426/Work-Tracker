# Work-Tracker
Hi, this is Work tracker made by Carolyn Ji and Joe Liao.

The purpose of this app is to provide a tool for students to keep track of their upcoming due assignments. This is especially important for middle school student, because they just started having much more classes, it is very difficult for them to keep track of all the assignments from their different classes. So this app allows them to input all their assignments, as well as their classes and deatils. Then, the students can see their upcoming assignments on a calender, and AI is also used to help the student create an appropriate schedule based on their available time, assignment due date, priority, and time to complete.

To build this app, we used python for the coding, streamlit for the UI, as well as openAI to generate the schedule.

We used AI to generate a scheudle for the students. We did this by giving the AI a prompt, telling it that its a schedule maker for the student based on the information given. Then, we inputted all the informationg iven by the student, includign all the assignment details and extra information so the AI could use that to make a desirably schedule for the student

Instructions:
1. To start, navigate to the left sidebar, here you will find a lot of places you can input information. Start by completing the Schedule information, including the time available each day, the sleep time, and any extra information you want to include.
2. To add an assignment, scroll down to the "Assignment Information" section, and enter in all the deatils including assignment name, subject, due date, priority (1=lowest, 10=highest), time needed to complete, and progree. After that, click add asignment and you will see your assignment pop up in the "Assignments" tab. To add a class, scroll down to the "class information" tab and add the class name, start and end time, and the days it's on. After that, click "add class" and you should see it pop up in the "class" section of the assignments tab. You can sort the class and assignments information based on their name, time, deatils, priority, or any other input.
3. Next, go to the "calender" tab. Here you will see a calender view. Select the year and month your want to see, after that, you can see all the assignments in that month and their due date.
4. To view more on an assignment, you can click on it in the calender tab, then go to the "details" tab where you can see the information of the selected assignment, you can also do this by going to the details tab and straight up selecting the assignment you want to see.
5. Lastly, to generate a schedule, go to the "schedule" tab and click "generate schedule", wait for a minute and then the AI will generate a schedule for you based on the information you have entered.
