import streamlit as st
import pandas as pd
from datetime import date
import calendar
import os
from openai import OpenAI
from dotenv import load_dotenv

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

st.title("My App")

st.title("📚 Student Assignment Tracker")

# Store assignments
if "assignments" not in st.session_state:
    st.session_state.assignments = []

st.sidebar.header("Add New Assignment")

assignment_name = st.sidebar.text_input("Assignment name")
class_name = st.sidebar.selectbox("Class / Subject", ["Math", "English", "Science", "Social Studies", "PE", "World Language", "Art", "Music", "Other"])
due_date = st.sidebar.date_input("Due date", date.today())
priority = st.sidebar.number_input("Priority level", min_value=1, max_value=10)
details = st.sidebar.text_area("Assignment details")
time = st.sidebar.number_input("Approximate time to complete (mins)", min_value=1, max_value=1000)

if st.sidebar.button("Add Assignment"):
    if assignment_name:
        st.session_state.assignments.append({
            "Assignment": assignment_name,
            "Class": class_name,
            "Due Date": due_date,
            "Priority": priority,
            "Details": details,
            "Time": time,
        })
        st.sidebar.success("Assignment added!")
    else:
        st.sidebar.error("Please enter an assignment name.")
st.sidebar.header("Add new class")
classame= st.sidebar.text_input("class name")
start = st.sidebar.number_input("what time does the class start", min_value=0.00, max_value=24.00)
end = st.sidebar.number_input("what time does the class end", min_value=0.00, max_value=24.00)
days = st.sidebar.multiselect("what days is the class on?", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
if st.sidebar.button("Add Class"):
    if classame:
        st.session_state.cl.append({
            "Class name": classame,
            "Start Time": start,
            "End Time": end,
            "Days": days,
        })
        st.sidebar.success("Class added!")
    else:
        st.sidebar.error("Please enter a class name.")

st.sidebar.header("Schedule maker")
minutes = st.sidebar.number_input("About how many minutes can you work a day?", min_value=1, max_value=999)
sleep = st.sidebar.number_input("At about what time (pm) do you go to sleep?", min_value=7, max_value=12)

    
df = pd.DataFrame(st.session_state.assignments)

st.header("Assignments")

tab1, tab2, tab3, tab4= st.tabs(["📖Assignments📖", "📅Calender📅", "📄Details📄", "🗓️schedule🗓️"])


def generate_schedule(assignments, minutes_available, sl):
    assignment_text = ""

    for a in assignments:
        assignment_text += f"""
- Assignment: {a['Assignment']}
  Class: {a['Class']}
  Due Date: {a['Due Date']}
  Priority: {a['Priority']}/10
  Time : {a['Time']} hours
  Details: {a['Details']}
"""

    prompt = f"""
You are a student scheduling assistant.
Your goal is to create a schedule for the student for the next week based on their assignments
Their assignments and details are {assignments}
Their available time each day is {minutes_available} minutes
They have to go to sleep at {sl} pm

Please make an appropriate schedule for the student
use a lot of emojis
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text



with tab1:
    st.header("All Assignments")

    if df.empty:
        st.info("No assignments added yet.")
    else:
        df_sorted = df.sort_values("Due Date")
        st.dataframe(df_sorted, use_container_width=True)

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
                st.write(f"⏰time: {row['Time']}")

with tab4:
    st.header("Schedule Maker")
    if st.button("Generate Schedule"):
        with st.spinner("making schedule..."):
            schedule = generate_schedule(st.session_state.assignments, minutes, sleep)

            st.write(schedule)

if "selected_assignment" in st.session_state:
    assignment = st.session_state.selected_assignment

    st.divider()
    st.subheader("Selected Assignment")

    st.write(f"📚 Class: {assignment['Class']}")
    st.write(f"📅 Due Date: {assignment['Due Date']}")
    st.write(f"⚡ Priority: {assignment['Priority']}")
    st.write(f"📝 Details: {assignment['Details']}")









