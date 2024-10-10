from dotenv import load_dotenv
import subprocess
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import glob

load_dotenv()
DESTINATION_EMAILS = os.getenv("EMAIL_DESTINATION").split(',')
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SERVER = os.getenv("EMAIL_SERVER")

def get_most_recent_pdf(directory):
    pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
    if not pdf_files:
        return None
    most_recent_pdf = max(pdf_files, key=os.path.getmtime)
    return most_recent_pdf

def send_email_with_pdfs(sender_email, recipient_email, subject, body, pdf_files, smtp_server, smtp_port, login, password):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach each PDF file
    for pdf_file in pdf_files:
        if pdf_file is not None:
            with open(pdf_file, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_file)}')
                msg.attach(part)

    # Set up the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(login, password)

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

    print(f"Email sent to {recipient_email} with {len(pdf_files)} PDF(s) attached.")    

# Example usage 
# if __name__ == '__main__':
#     sender = 'youremail@example.com'
#     recipient = 'recipient@example.com'
#     subject = 'PDF Report'
#     body = 'Please find the attached PDF report.'
#     pdf_file_path = '/path/to/your/pdf_file.pdf'

#     # Your SMTP server credentials
#     smtp_server = 'smtp.example.com'
#     smtp_port = 587
#     login = 'youremail@example.com'
#     password = 'yourpassword'

#     # Send the email
#     send_email_with_pdf(sender, recipient, subject, body, pdf_file_path, smtp_server, smtp_port, login, password)

if __name__ == '__main__':
    # Run the scripts to generate PDFs
    # scripts = ['attendance_bulletin.py', 'consecutive_absences.py', 'principals_attendance_DOWNLOADS.py']
    scripts = ['combo_bulletin.py', 'consecutive_absences.py', 'principals_attendance_DOWNLOADS.py']
    for script in scripts:
        subprocess.run(['python3', script])

    # Get the most recent PDFs from the specified directories
    pdf1 = get_most_recent_pdf('downloads/consecutive')
    pdf2 = get_most_recent_pdf('downloads/combo')
    pdf3 = get_most_recent_pdf('downloads/principalattendance')

    # Create a list of the most recent PDFs
    recent_pdfs = [pdf1, pdf2, pdf3]

    # Your email details
    sender = EMAIL_SENDER
    # recipient = DESTINATION_EMAIL    
    subject = 'Generated Reports'
    body = 'Please find the most recent reports attached.'

    # Your SMTP server credentials
    smtp_server = EMAIL_SERVER
    smtp_port = 587
    login = EMAIL_SENDER
    password = EMAIL_PASSWORD

    # Send the email with the most recent PDFs attached
    for recipient in DESTINATION_EMAILS:
        send_email_with_pdfs(sender, recipient.strip(), subject, body, recent_pdfs, smtp_server, smtp_port, login, password)