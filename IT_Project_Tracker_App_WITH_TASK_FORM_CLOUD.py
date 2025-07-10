
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 IT Project Task Tracker (Cloud Edition)")

# Load task data
excel_file = "IT_Project_Task_Planning_CLOUD.xlsx"
sheet_name = "Tasks"
try:
    df_tasks = pd.read_excel(excel_file, sheet_name=sheet_name)
except FileNotFoundError:
    st.error(f"❌ File '{excel_file}' not found.")
    st.stop()

# Task entry form
with st.expander("➕ Add New Task"):
    with st.form("task_form", clear_on_submit=True):
        task_description = st.text_input("Task Description")
        task_owner = st.text_input("Task Owner")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
        submitted = st.form_submit_button("Add Task")

        if submitted:
            if task_description and task_owner:
                new_task = {
                    "Task": task_description,
                    "Owner": task_owner,
                    "Start": pd.to_datetime(start_date),
                    "End": pd.to_datetime(end_date),
                    "Status": status,
                }
                df_tasks = pd.concat([df_tasks, pd.DataFrame([new_task])], ignore_index=True)
                df_tasks.to_excel(excel_file, sheet_name=sheet_name, index=False)
                st.success("✅ Task added successfully!")
            else:
                st.warning("⚠️ Please fill in both Task Description and Owner.")

# Show Gantt Chart
with st.expander("📅 Project Timeline (Gantt Chart)"):
    if df_tasks.empty:
        st.info("No tasks to show.")
    else:
        try:
            fig = px.timeline(
                df_tasks,
                x_start="Start",
                x_end="End",
                y="Task",
                color="Status",
                title="Project Gantt Chart"
            )
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error generating Gantt chart: {e}")
