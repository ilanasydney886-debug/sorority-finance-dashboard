import streamlit as st
import pandas as pd
from database import SessionLocal
import models

# Connect to your new sorority database
db = SessionLocal()

st.set_page_config(page_title="Chapter Finance Dashboard", layout="wide")
st.title("Sorority Financial Transparency Portal")
st.markdown("### Treasurer's Real-Time Budget Oversight")

# 1. Load Data into Pandas (The tool for data analysis)
members = db.query(models.Member).all()
transactions = db.query(models.Transaction).all()

df_members = pd.DataFrame([{
    "Name": m.name, "PC": m.pc_year, "Paid": m.dues_paid, "Owed": m.dues_total - m.dues_paid
} for m in members])

df_trans = pd.DataFrame([{
    "Item": t.description, "Category": t.category, "Cost": t.amount
} for t in transactions])

# 2. Top Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Total Dues Collected", f"${df_members['Paid'].sum():,.2f}")
c2.metric("Outstanding Balance", f"${df_members['Owed'].sum():,.2f}")
c3.metric("Total Chapter Spending", f"${df_trans['Cost'].sum():,.2f}")

st.divider()

# 3. Charts
left, right = st.columns(2)

with left:
    st.subheader("Expenses by Category")
    # This groups your formal, recruitment, and shirts into a bar chart
    chart_data = df_trans.groupby("Category")["Cost"].sum()
    st.bar_chart(chart_data)

with right:
    st.subheader("Collection Rate")
    total_paid = df_members['Paid'].sum()
    total_expected = df_members['Paid'].sum() + df_members['Owed'].sum()
    percent = (total_paid / total_expected)
    st.write(f"We have collected **{percent*100:.1f}%** of this semester's dues.")
    st.progress(percent)

# 4. Detailed Table
st.subheader("Member Payment Status")
st.dataframe(df_members, use_container_width=True)

# 5. Sidebar Form to Add New Transactions
with st.sidebar:
    st.header("Add New Expense")
    with st.form("expense_form"):
        desc = st.text_input("Description")
        cat = st.selectbox("Category", ["Social", "Philanthropy", "Recruitment", "Admin"])
        amt = st.number_input("Amount", min_value=0.0)
        submit = st.form_submit_button("Log Expense")

        if submit:
            new_tx = models.Transaction(description=desc, category=cat, amount=amt)
            db.add(new_tx)
            db.commit()
            st.success("Transaction Logged!")
            st.rerun() # This refreshes the charts instantly!