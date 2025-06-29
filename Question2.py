import streamlit as st
df = pd.read_csv("university_student_dashboard_data.csv")
st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("University Student Dashboard")
years = df["Year"].unique()
selected_years = st.sidebar.multiselect("Select Year(s):", sorted(years), default=sorted(years))
filtered_df = df[df["Year"].isin(selected_years)]
total_applications = filtered_df["Applications"].sum()
total_admissions = filtered_df["Admitted"].sum()
total_enrollments = filtered_df["Enrolled"].sum()
avg_retention = filtered_df["Retention Rate (%)"].mean()
avg_satisfaction = filtered_df["Student Satisfaction (%)"].mean()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Applications", f"{total_applications:,}")
col2.metric("Total Admissions", f"{total_admissions:,}")
col3.metric("Total Enrollments", f"{total_enrollments:,}")
col4.metric("Avg Retention Rate", f"{avg_retention:.1f}%")
col5.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}%")
tab1, tab2 = st.tabs(["Trends Over Time", "Department Analysis"])
with tab1:
    st.subheader("Trends Over Time")
    trend_cols = ["Applications", "Admitted", "Enrolled", "Retention Rate (%)", "Student Satisfaction (%)"]
    for col in trend_cols:
        fig, ax = plt.subplots()
        sns.lineplot(data=filtered_df, x="Year", y=col, hue="Term", marker="o", ax=ax)
        ax.set_title(f"{col} by Year")
        st.pyplot(fig)
with tab2:
    st.subheader("Enrollment by Department")
    dept_df = filtered_df[["Year", "Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]]
    dept_df = dept_df.melt(id_vars=["Year"], var_name="Department", value_name="Enrollment")
    dept_df["Department"] = dept_df["Department"].str.replace(" Enrolled", "")
    fig, ax = plt.subplots()
    sns.lineplot(data=dept_df, x="Year", y="Enrollment", hue="Department", marker="o", ax=ax)
    ax.set_title("Department-wise Enrollment Trends")
    st.pyplot(fig)
