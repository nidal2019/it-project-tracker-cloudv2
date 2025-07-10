import streamlit as st
import pandas as pd
import datetime
import requests
import io

# إعدادات
GITHUB_XLSX_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/IT_Project_Task_Planning.xlsx"

st.set_page_config(page_title="IT Project Tracker", layout="wide")

st.title("📊 IT Project Task Tracker (Cloud Edition)")
st.markdown("هذا التطبيق يعرض المهام ويسمح لك بإضافة مهمة جديدة مباشرة إلى ملف Excel على GitHub (يجب تنزيل الملف محليًا لتعديله).")

# تحميل البيانات من GitHub
import requests
import io

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nidal2019/it-project-tracker-cloudv2/main/IT_Project_Task_Planning_CLOUD.xlsx"
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
        df = pd.read_excel(io.BytesIO(content))
        return df
    else:
        st.error("❌ لم يتم العثور على ملف Excel من الرابط.")
        return pd.DataFrame()

df = load_data()

# عرض الإحصائيات
st.subheader("إحصائيات المهام")
col1, col2, col3 = st.columns(3)
col1.metric("✅ مكتملة", str((df['Status'] == 'Completed').sum()))
col2.metric("🕓 قيد التنفيذ", str((df['Status'] == 'In Progress').sum()))
col3.metric("⚠️ متأخرة", str((df['Status'] == 'Delayed').sum()))

# عرض المهام
st.subheader("قائمة المهام")
st.dataframe(df, use_container_width=True)

# نموذج إضافة مهمة
st.subheader("➕ إضافة مهمة جديدة")

with st.form("add_task_form"):
    task_name = st.text_input("Task Name")
    assigned_to = st.text_input("Assigned To")
    status = st.selectbox("Status", ["Not Started", "In Progress", "Completed", "Delayed"])
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    start_date = st.date_input("Start Date", datetime.date.today())
    due_date = st.date_input("Due Date", datetime.date.today() + datetime.timedelta(days=7))
    submitted = st.form_submit_button("📤 إضافة المهمة (محليًا فقط)")

    if submitted:
        st.warning("⚠️ هذا النموذج لا يمكنه حفظ المهمة إلى GitHub مباشرة. قم بتحميل ملف Excel وتحديثه محليًا.")
        st.code("GitHub لا يدعم الكتابة المباشرة عبر Streamlit - قم بتحديث الملف يدويًا أو استخدم تكامل خارج الخدمة.")