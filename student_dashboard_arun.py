
import streamlit as st
import pandas as pd
import sqlite3

st.title("Student Placement Dashboard - SQL Insights")

# Connect to the database
conn = sqlite3.connect("students.db")

queries = {
    "1. Average problems solved": "SELECT AVG(problems_solved) FROM programming;",

    "2. Top 5 placement-ready students": '''
        SELECT s.name, place.mock_interview_score
        FROM students s
        JOIN placements place ON s.student_id = place.student_id
        WHERE place.placement_ready = 'Yes'
        ORDER BY place.mock_interview_score DESC
        LIMIT 5;''',

    "3. Average soft skill score": '''
        SELECT AVG((communication_score + teamwork_score + presentation_score)/3.0) as avg_soft_skill
        FROM soft_skills;''',

    "4. Students with internship experience": '''
        SELECT s.name FROM students s
        JOIN placements p ON s.student_id = p.student_id
        WHERE p.internship_experience = 'Yes';''',

    "5. Students solved more than 70 problems": '''
        SELECT s.name, p.problems_solved
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        WHERE p.problems_solved > 70;''',

    "6. Total students per programming level": '''
        SELECT 
            CASE 
                WHEN problems_solved < 40 THEN 'Beginner'
                WHEN problems_solved < 80 THEN 'Intermediate'
                ELSE 'Advanced'
            END as level, COUNT(*) as count
        FROM programming
        GROUP BY level;''',

    "7. Highest scoring soft skill student": '''
        SELECT s.name, 
               (ss.communication_score + ss.teamwork_score + ss.presentation_score)/3.0 as avg_score
        FROM students s
        JOIN soft_skills ss ON s.student_id = ss.student_id
        ORDER BY avg_score DESC LIMIT 1;''',

    "8. Distribution of placement readiness": '''
        SELECT placement_ready, COUNT(*) as count
        FROM placements 
        GROUP BY placement_ready;''',

    "9. Mock interview score stats": '''
        SELECT 
            MIN(mock_interview_score) AS Min_Score,
            MAX(mock_interview_score) AS Max_Score,
            AVG(mock_interview_score) AS Avg_Score
        FROM placements;''',

    "10. Recent Enrollments": '''
        SELECT name, enrollment_date 
        FROM students
        ORDER BY enrollment_date DESC LIMIT 5;'''
}

# Display queries as insights
for title, query in queries.items():
    st.subheader(title)
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)

# Close connection
conn.close()
