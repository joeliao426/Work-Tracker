import streamlit as st
import pandas as pd
from datetime import date
import calendar
import os
from openai import OpenAI
from dotenv import load_dotenv

if "classes" not in st.session_state:
    st.session_state.classes = []

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.markdown("""
<style>
.stApp {
    background-color: #E0FFFF;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Student Assignment Tracker")

# Store assignments
if "assignments" not in st.session_state:
    st.session_state.assignments = []

st.sidebar.title("Required Information")


st.sidebar.header("Schedule information")
#minutes = st.sidebar.number_input("How many minutes can you work each day?", min_value=1, max_value=1440, value=120)
minutes = st.sidebar.text_input("What time can you work each day? (Example: Wednesday = 5-6 PM, Thursday = 6-6:30 PM)")
#sleep = st.sidebar.number_input("What time (pm) do you go to sleep?", min_value=7, max_value=, value=9)
sleep = st.sidebar.text_input("What time do you go to sleep? (Example: 8PM)")
extrainfo = st.sidebar.text_area("Other important information")


st.sidebar.header("Assignment information")
assignment_name = st.sidebar.text_input("Assignment name")
class_name = st.sidebar.text_input("Class / Subject")
due_date = st.sidebar.date_input("Due date", date.today())
priority = st.sidebar.number_input("Priority level", min_value=1, max_value=10)
details = st.sidebar.text_area("Assignment details")
time = st.sidebar.number_input("Approximate time to complete from current progress (mins)", min_value=1, max_value=10000)
progress = st.sidebar.text_input("How much have you gotten done already?")

if st.sidebar.button("Add Assignment"):
    if assignment_name:
        st.session_state.assignments.append({
            "Assignment": assignment_name,
            "Class": class_name,
            "Due Date": due_date,
            "Priority": priority,
            "Details": details,
            "Time": time,
            "Progress": progress,
   
        })
        st.sidebar.success("Assignment added!")
    else:
        st.sidebar.error("Please enter an assignment name.")


st.sidebar.header("Class information")
classame= st.sidebar.text_input("Class name")
start = st.sidebar.number_input("What time does the class start", min_value=0.00, max_value=24.00)
end = st.sidebar.number_input("What time does the class end", min_value=0.00, max_value=24.00)
days = st.sidebar.multiselect("What days are the class on?", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
if st.sidebar.button("Add Class"):
    if classame:
        st.session_state.classes.append({
            "Class Name": classame,
            "Start Time": start,
            "End Time": end,
            "Days": days,
        })
        st.sidebar.success("Class added!")
    else:
        st.sidebar.error("Please enter a class name.")


   

st.header("Assignments")

tab1, tab2, tab3, tab4= st.tabs(["📖Assignments📖", "📅Calender📅", "📄Details📄", "🗓️Schedule🗓️"])


def generate_schedule(assignments, minutes_available, sl, exinfo):
    assignment_text = ""

    for a in assignments:
        assignment_text += f"""
- Assignment: {a['Assignment']}
  Class: {a['Class']}
  Due Date: {a['Due Date']}
  Priority: {a['Priority']}/10
  Time : {a['Time']} hours
  Details: {a['Details']}
  Progress: {a['Progress']}

"""

    prompt = f"""
You are a student scheduling assistant.
Your goal is to create a schedule for the student for the next week based on their assignments and any other information they give you.
Their assignments and details are {assignments}
Their available time each day is {minutes_available} 
They have to go to sleep at {sl} pm
Make sure you take into account their personal needs in {exinfo}

Please make an appropriate schedule for the student
Try to keep the same format for your schedule everytime
"""
#tell it to respond to any chat messages and add a chat

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text



with tab1:
    df = pd.DataFrame(st.session_state.assignments)

    st.header("All Assignments")

    if df.empty:
        st.info("No assignments added yet.")
    else:

        df = df.sort_values("Due Date").reset_index(drop=True)
        df.index += 1

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            key="assignments_editor"
        )
       
        st.session_state.assignments = edited_df.to_dict("records")

    st.subheader("Classes")
    if st.session_state.classes:
        class_df = pd.DataFrame(st.session_state.classes)

        class_df = class_df.sort_values("Class Name").reset_index(drop=True)
        class_df.index += 1

        edited_df = st.data_editor(
            class_df,
            use_container_width=True,
            key="class_editor")
    else:
        st.info("No classes added yet.")

with tab2:
    st.header("Calendar View")

    today = date.today()
    selected_month = st.selectbox(
        "Select Month",
        list(range(1, 13)),
        index=today.month - 1,
        format_func=lambda x: calendar.month_name[x]
    )

    selected_year = st.number_input(
        "Select Year",
        min_value=2024,
        max_value=2035,
        value=today.year
    )

    cal = calendar.monthcalendar(selected_year, selected_month)

    st.subheader(f"{calendar.month_name[selected_month]} {selected_year}")

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)

    for i, day in enumerate(days):
        cols[i].markdown(f"**{day}**")

    for week in cal:
        cols = st.columns(7)

        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            else:
                current_date = date(selected_year, selected_month, day)
                cols[i].markdown(f"### {day}")

                if not df.empty:
                    due_assignments = df[df["Due Date"] == current_date]

                    for idx, row in due_assignments.iterrows():
                        if cols[i].button(
                        f"📌 {row['Assignment']}",
                        key=f"calendar_{idx}"
                    ):
                            st.session_state.selected_assignment = row.to_dict()

with tab3:
    st.header("Assignment Details")

    if df.empty:
        st.info("No assignments yet.")
    else:
        for _, row in df.iterrows():
            with st.expander(f"📌 {row['Assignment']}"):
                st.write(f"📚 Class: {row['Class']}")
                st.write(f"📅 Due Date: {row['Due Date']}")
                st.write(f"⚡ Priority: {row['Priority']}")
                st.write(f"📝 Details: {row['Details']}")
                st.write(f"⏰Time: {row['Time']}")

with tab4:
    st.header("Schedule Maker")
    if st.button("Generate Schedule"):
        with st.spinner("Making schedule..."):
            schedule = generate_schedule(st.session_state.assignments, minutes, sleep, extrainfo)

            st.write(schedule)

#t.divider
#f "showchat" not in st.session_state:
   #st.session_state.show_chat = False
   

if "selected_assignment" in st.session_state:
    assignment = st.session_state.selected_assignment

    st.divider()
    st.subheader("Selected Assignment")

    st.write(f"📚 Class: {assignment['Class']}")
    st.write(f"📅 Due Date: {assignment['Due Date']}")
    st.write(f"⚡ Priority: {assignment['Priority']}")
    st.write(f"📝 Details: {assignment['Details']}")