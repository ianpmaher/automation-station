from dotenv import load_dotenv
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

load_dotenv()
DESTINATION_EMAIL = os.getenv("EMAIL_DESTINATION")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SERVER = os.getenv("EMAIL_SERVER")

def send_email_with_pdf(sender_email, recipient_email, subject, body, pdf_file, smtp_server, smtp_port, login, password):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Open the file to be sent
    with open(pdf_file, 'rb') as attachment:
        # Create a MIMEBase object
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Encode to base64
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(pdf_file)}')

    # Attach the PDF to the email
    msg.attach(part)

    # Set up the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(login, password)

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

    print(f"Email sent to {recipient_email} with {pdf_file} attached.")


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
    sender = 'youremail@example.com'
    recipient = DESTINATION_EMAIL
    subject = 'PDF Report'
    body = 'Please find the attached PDF report.'
    pdf_file_path = 'downloads/report869.pdf' # Path to the PDF file

    # Your SMTP server credentials
    smtp_server = EMAIL_SERVER
    smtp_port = 587
    login = EMAIL_SENDER
    password = EMAIL_PASSWORD

    # Send the email
    send_email_with_pdf(sender, recipient, subject, body, pdf_file_path, smtp_server, smtp_port, login, password)