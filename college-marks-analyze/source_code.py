import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Load the datasets
@st.cache_data
def load_data():
    subjects = ["ECL", "DSM", "BEE", "CAO"]
    dataframes = {}
    for subject in subjects:
        dataframes[subject] = pd.read_csv(f"datasets/{subject}.csv")
    return dataframes

dataframes = load_data()

st.title('Student Performance Analysis')

# Sidebar for filters
st.sidebar.header('Filters')
subject = st.sidebar.selectbox('Select Subject', list(dataframes.keys()))
branch = st.sidebar.selectbox('Select Branch', ['All'] + list(dataframes[subject]['Branch'].unique()))
exam_type = st.sidebar.selectbox('Select Exam Type', ['ISE 1', 'ISE 2', 'MSE', 'ESE'])

# Input for specific student details
st.sidebar.header('Student Details')
student_branch = st.sidebar.selectbox('Student Branch', list(dataframes[subject]['Branch'].unique()))
student_marks = {
    'ISE 1': st.sidebar.number_input('ISE 1 Marks', 0, 10),
    'ISE 2': st.sidebar.number_input('ISE 2 Marks', 0, 10),
    'MSE': st.sidebar.number_input('MSE Marks', 0, 30),
    'ESE': st.sidebar.number_input('ESE Marks', 0, 100)
}

# Filter data based on selection
df = dataframes[subject]
if branch != 'All':
    df = df[df['Branch'] == branch]

# Function to check if student's position should be shown
def show_student_position():
    return branch == student_branch or branch == 'All'

# Function to plot pie chart of branch distribution
def plot_branch_distribution(df):
    fig = px.pie(df, names='Branch', title=f'Branch Distribution - {subject}')
    st.plotly_chart(fig)

# Function to plot histograms of marks
def plot_marks_histogram(df, exam_type):
    fig = px.histogram(df, x=f'{exam_type} Marks', nbins=20, 
                       title=f'Distribution of {exam_type} Marks - {subject}')
    fig.update_layout(bargap=0.1)

    if show_student_position():
        # Add vertical line for the specific student
        student_mark = student_marks[exam_type]
        fig.add_vline(x=student_mark, line_dash="dash", line_color="red",
                      annotation_text="Student's Mark", annotation_position="top right")

    st.plotly_chart(fig)

# Function to plot line chart of average marks across exams
def plot_average_marks(df):
    avg_marks = df[['ISE 1 Marks', 'ISE 2 Marks', 'MSE Marks', 'ESE Marks']].mean()
    fig = px.line(x=avg_marks.index, y=avg_marks.values, markers=True,
                  title=f'Average Marks Across Exams - {subject}')
    fig.update_layout(xaxis_title='Exam Type', yaxis_title='Average Marks')

    if show_student_position():
        # Add points for the specific student
        student_marks_list = [student_marks['ISE 1'], student_marks['ISE 2'], student_marks['MSE'], student_marks['ESE']]
        fig.add_trace(go.Scatter(x=avg_marks.index, y=student_marks_list, mode='markers',
                                 name="Student's Marks", marker=dict(color='red', size=10)))

    st.plotly_chart(fig)

# Function to plot scatter plot between two exams
def plot_scatter(df, exam1, exam2):
    fig = px.scatter(df, x=f'{exam1} Marks', y=f'{exam2} Marks', color='Branch',
                     title=f'{exam1} vs {exam2} Marks - {subject}')

    if show_student_position():
        # Add point for the specific student
        student_x = student_marks[exam1]
        student_y = student_marks[exam2]
        fig.add_trace(go.Scatter(x=[student_x], y=[student_y], mode='markers',
                                 name="Student's Mark", marker=dict(color='red', size=10, symbol='star')))

    st.plotly_chart(fig)

# Function to plot correlation heatmap
def plot_correlation_heatmap(df):
    corr = df[['ISE 1 Marks', 'ISE 2 Marks', 'MSE Marks', 'ESE Marks']].corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto",
                    title=f'Correlation Between Exams - {subject}')
    st.plotly_chart(fig)

# Function to plot box plot of marks by branch
def plot_boxplot(df, exam_type):
    fig = px.box(df, x='Branch', y=f'{exam_type} Marks',
                 title=f'{exam_type} Marks by Branch - {subject}')

    if show_student_position():
        # Add point for the specific student
        student_mark = student_marks[exam_type]
        fig.add_trace(go.Scatter(x=[student_branch], y=[student_mark], mode='markers',
                                 name="Student's Mark", marker=dict(color='red', size=10, symbol='star')))

    st.plotly_chart(fig)

# Function to plot violin plot of marks by branch
def plot_violinplot(df, exam_type):
    fig = px.violin(df, x='Branch', y=f'{exam_type} Marks', box=True,
                    title=f'{exam_type} Marks Distribution by Branch - {subject}')

    if show_student_position():
        # Add point for the specific student
        student_mark = student_marks[exam_type]
        fig.add_trace(go.Scatter(x=[student_branch], y=[student_mark], mode='markers',
                                 name="Student's Mark", marker=dict(color='red', size=10, symbol='star')))

    st.plotly_chart(fig)

# New function to plot Radar Chart
def plot_radar_chart(df):
    avg_marks = df[['ISE 1 Marks', 'ISE 2 Marks', 'MSE Marks', 'ESE Marks']].mean()

    # Normalize the average marks and student marks to a 0-1 scale
    max_marks = {'ISE 1': 10, 'ISE 2': 10, 'MSE': 30, 'ESE': 100}
    avg_marks_normalized = avg_marks / [max_marks[exam] for exam in ['ISE 1', 'ISE 2', 'MSE', 'ESE']]
    student_marks_normalized = [student_marks[exam] / max_marks[exam] for exam in ['ISE 1', 'ISE 2', 'MSE', 'ESE']]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=avg_marks_normalized,
        theta=['ISE 1', 'ISE 2', 'MSE', 'ESE'],
        fill='toself',
        name='Branch Average'
    ))

    if show_student_position():
        fig.add_trace(go.Scatterpolar(
            r=student_marks_normalized,
            theta=['ISE 1', 'ISE 2', 'MSE', 'ESE'],
            fill='toself',
            name='Student'
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title=f'Radar Chart - Student vs Branch Average ({subject})'
    )

    st.plotly_chart(fig)

# New function to plot CDF
def plot_cdf(df, exam_type):
    marks = df[f'{exam_type} Marks'].sort_values()
    cdf = np.arange(1, len(marks) + 1) / len(marks)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=marks, y=cdf, mode='lines', name='CDF'))

    if show_student_position():
        student_mark = student_marks[exam_type]
        student_percentile = cdf[marks <= student_mark][-1] if any(marks <= student_mark) else 0
        fig.add_trace(go.Scatter(x=[student_mark], y=[student_percentile], mode='markers',
                                 name="Student's Mark", marker=dict(color='red', size=10, symbol='star')))

    fig.update_layout(
        title=f'Cumulative Distribution Function - {exam_type} Marks ({subject})',
        xaxis_title='Marks',
        yaxis_title='Cumulative Probability',
        yaxis=dict(tickformat='.0%')
    )

    st.plotly_chart(fig)

# Main content
st.header(f'Analysis for {subject}')

plot_branch_distribution(df)
plot_marks_histogram(df, exam_type)
plot_average_marks(df)
plot_scatter(df, 'ISE 1', 'ISE 2')
plot_scatter(df, 'MSE', 'ESE')
plot_correlation_heatmap(df)
plot_boxplot(df, exam_type)
plot_violinplot(df, exam_type)

# Add new plots
plot_radar_chart(df)
plot_cdf(df, exam_type)

# Display raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)