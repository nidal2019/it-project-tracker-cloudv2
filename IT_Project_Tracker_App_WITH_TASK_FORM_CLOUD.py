import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import io
import requests

# تحميل البيانات من GitHub باستخدام requests
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nidal2019/it-project-tracker-cloudv2/main/IT_Project_Task_Planning_CLOUD.xlsx"
    response = requests.get(url)
    df = pd.read_excel(io.BytesIO(response.content), engine="openpyxl")
    return df

# تحميل البيانات
df = load_data()

# ترويسة التطبيق
st.set_page_config(page_title="IT Project Task Tracker (Cloud Edition)", layout="wide")
st.title("📊 IT Project Task Tracker (Cloud Edition)")
st.markdown("⬇️ يجب تنزيل الملف مجانًا لتحميل Excel على GitHub (اضغط هنا لإنشاء ملف جديد يحتوي على بيانات مهمة جديدة) إلى ملف")

# واجهة المستخدم لإضافة مهمة جديدة
with st.form(key='task_form'):
    st.subheader("➕ Add New Task")
    task_description = st.text_input("Task Description")
    task_owner = st.text_input("Task Owner")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    status = st.selectbox("Status", ["Not Started", "In Progress", "Completed", "Blocked"])
    submit_button = st.form_submit_button(label="Add Task")

# إضافة المهمة الجديدة إلى البيانات
if submit_button:
    new_task = {
        "Task Description": task_description,
        "Task Owner": task_owner,
        "Start Date": start_date,
        "End Date": end_date,
        "Status": status
    }
    df = df._append(new_task, ignore_index=True)
    st.success("✅ Task added successfully!")

# رسم المخطط الزمني (Gantt Chart)
st.subheader("📅 Project Timeline (Gantt Chart)")
fig = px.timeline(
    df,
    x_start="Start Date",
    x_end="End Date",
    y="Task Description",
    color="Status",
    title="Project Gantt Chart"
)
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig, use_container_width=True)

# تنزيل الملف المعدل
st.subheader("⬇️ Download Updated File")
updated_file = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV File", data=updated_file, file_name="updated_tasks.csv", mime="text/csv")
