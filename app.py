import os
from flask import Flask, request, jsonify, send_file, render_template
import logging
from services.services import saveCsv
import pandas as pd
import json

from time_table_gen.timetable_algorithm import timetable_algorithm
from seat_allocation.seat_allocation import seat_allocation_algorithm


app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Global variable to store uploaded CSV path
uploaded_csv_path = ''

#Request type change to post as we will be sending data from node server
@app.route('/generate_timetable', methods=['POST'])
def generate_timetable():
    """Generate a timetable based on uploaded student data.

    Loads student data from a CSV file and creates a timetable based on 
    subject overlaps. Implements a greedy coloring algorithm for scheduling 
    and generates a visual representation of the class network.

    Returns:
        JSON response with a success message or an error message.
    """
    try:
        #Saving uploaded csv locally
        startDate = request.form['startDate']
        startTime = request.form['startTime']
        rooms = json.loads(request.form['rooms'])
        file = saveCsv(request.files['file'])
        timetable_algorithm(file.filename, startDate, startTime)

        students = pd.read_csv("./uploads/"+file.filename)
        students.set_index("uid", inplace=True)
        students = students.fillna(value=False)
        students = students.T
        
        #Storing courses in dictornary with key as course and value as an array of students enrolled for that course
        courses = {}

        for course in students.index:
            courses[course] = []
            for student in students.columns:
                if students.loc[course][student]:
                    courses[course].append(student)
        
        #reading timetable
        timetable = pd.read_csv("./uploads/timetable.csv")
        timetable.rename(columns={"Unnamed: 0":"Date"}, inplace=True)
        timetable.set_index("Date", inplace=True)
        timetable.fillna(value=pd.NA, inplace=True)

        #Allocating seats for each day
        for date in timetable.index:
            course_list = []
            student_list = []
            for col in timetable.columns:
                if timetable.loc[date][col] is pd.NA:
                    continue
                course_name = timetable.loc[date][col]
                course_list = course_list + [course_name]*len(courses[course_name])
                student_list = student_list + courses[course_name]
            seat_allocation_algorithm(date.split(" ")[0], course_list, student_list, rooms) 


        return jsonify({
            "sucess":True
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "success":False  
        }),500
    



@app.route('/download_image', methods=['GET'])
def download_image():
    """Download the generated class network image.

    Returns:
        Image file as an attachment if it exists, otherwise returns an error message.
    """
    graph_image_path = 'class_network.png'
    if not os.path.isfile(graph_image_path):
        logging.error(f"Image file not found: {graph_image_path}")
        return jsonify({'error': 'Image file not found'}), 404
    return send_file(graph_image_path, as_attachment=True)

@app.route('/download_csv', methods=['GET'])
def download_csv():
    """Download the generated timetable CSV file.

    Returns:
        CSV file as an attachment if it exists, otherwise returns an error message.
    """
    timetable_csv_path = 'timetable.csv'
    if not os.path.isfile(timetable_csv_path):
        logging.error(f"File not found: {timetable_csv_path}")
        return jsonify({'error': 'File not found'}), 404
    return send_file(timetable_csv_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)   
    app.run(port=8000, debug=True)
