import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class EmailSender:
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 465
        self.sender = os.environ.get("EMAIL_SENDER")
        self.password = os.environ.get("EMAIL_PASSWORD")

        # Validate that password is set
        if not self.password:
            raise ValueError(
                "EMAIL_PASSWORD is not set in .env file. "
            )

    def send_email(self, to: str, subject: str, text: str):
        try:
            # Create SSL context
            context = ssl.create_default_context()

            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender
            message["To"] = to
            message["Subject"] = subject

            # Add body to email
            message.attach(MIMEText(text, "html", _charset='utf-8'))

            # Create SMTP connection and send email
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, to, message.as_string())

            print(f"✓ Email sent successfully to {to}")
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"Authentication failed: {e}")
            print("\nTroubleshooting:")
            print(
                "1. Make sure you're using an App Password, not your regular Gmail password")
            print(
                "2. Generate an App Password at: https://myaccount.google.com/apppasswords")
            print("3. Enable 2-Step Verification if you haven't already")
            print("4. Set the App Password as EMAIL_PASSWORD in your .env file")
            return False
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


if __name__ == '__main__':
    email_sender = EmailSender()
    email_sender.send_email("camellia.gh@gmail.com",
                            "Hello", "I am learning Python")
