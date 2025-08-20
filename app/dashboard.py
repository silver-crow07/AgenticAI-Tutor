import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

PROGRESS_FILE = "data/progress_log.json"

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return pd.DataFrame(columns=["name", "class", "subject", "score"])
    with open(PROGRESS_FILE, "r") as file:
        data = json.load(file)
    return pd.DataFrame(data)

def show_progress_charts(df):
    if df.empty:
        st.info("No progress data available yet.")
        return

    st.subheader("📊 Overall Performance")
    classwise = df.groupby("class")["score"].mean()
    subjectwise = df.groupby("subject")["score"].mean()

    st.write("### Average Score by Class")
    fig1, ax1 = plt.subplots()
    classwise.plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

    st.write("### Average Score by Subject")
    fig2, ax2 = plt.subplots()
    subjectwise.plot(kind='bar', ax=ax2, color='orange')
    st.pyplot(fig2)

    st.write("### Individual Scores Table")
    st.dataframe(df)

def main():
    st.title("📈 Student Progress Dashboard")
    st.write("Track student quiz performance over time.")

    df = load_progress()
    show_progress_charts(df)

if __name__ == "__main__":
    main()

