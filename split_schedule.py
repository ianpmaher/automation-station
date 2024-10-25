import os
import re
import csv
from PyPDF2 import PdfReader, PdfWriter

# Function to load student names from the CSV (no header)
def load_student_names_no_header(csv_path):
    student_names = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                last_name, first_name = row[0].strip('"'), row[1].strip()
                student_names.append(f"{first_name} {last_name}")
    return student_names

# Function to split the PDF and rename based on student names
def split_pdf_by_student_names(input_pdf_path, student_names, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read the PDF file
    with open(input_pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        
        # Loop through each page and assign a student's name to the file
        for page_num, student_name in enumerate(student_names):
            writer = PdfWriter()
            page = reader.pages[page_num]
            writer.add_page(page)
            
            # Create the output file name with "FirstName LastName schedule.pdf"
            output_filename = f"{student_name} schedule {page_num + 1}.pdf"
            output_filepath = os.path.join(output_folder, output_filename)
            
            # Write the page to a new PDF file
            with open(output_filepath, 'wb') as output_pdf:
                writer.write(output_pdf)

            print(f"Page {page_num + 1} saved as {output_filename}")

# Load the student names from the CSV file
csv_path = 'senior_names.csv'
student_names = load_student_names_no_header(csv_path)

# Path to the uploaded PDF and the output folder
input_pdf_path = 'report980.pdf'
output_folder = 'output_schedules'

# Split the PDF by student names
split_pdf_by_student_names(input_pdf_path, student_names, output_folder)