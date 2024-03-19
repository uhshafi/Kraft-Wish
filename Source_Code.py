import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QDateEdit
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, QDate

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class EmailSender(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Kraft Wish - Master the Art of Birthday Wishes!')
        self.setWindowIcon(QIcon("C:/Users/Shafi/Documents/Python Projects/Kraft Wish/logo.png"))
        self.setFixedSize(960, 540)  # Set window size to match Discord's windowed size

        font = QFont()
        font.setPointSize(12)

        # Add background image
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("C:/Users/Shafi/Documents/Python Projects/Kraft Wish/Design.png"))
        self.background_label.setGeometry(0, 0, 960, 540)

        # Add logo
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("C:/Users/Shafi/Documents/Python Projects/Kraft Wish/logo1.png"))
        self.logo_label.setGeometry(20, 20, 200, 200)

        self.setStyleSheet("""
            color: white;
            font-size: 12pt;
        """)

        self.sender_email_label = QLabel('Your Email:', self)
        self.sender_email_label.move(250, 20)
        self.sender_email_label.setFont(font)
        self.sender_email_entry = QLineEdit(self)
        self.sender_email_entry.move(380, 20)
        self.sender_email_entry.resize(300, 30)
        self.sender_email_entry.setStyleSheet("border: 2px solid #ccc; border-radius: 15px; padding: 5px; color: black;")

        self.password_label = QLabel('Your Password:', self)
        self.password_label.move(250, 70)
        self.password_label.setFont(font)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.move(380, 70)
        self.password_entry.resize(300, 30)
        self.password_entry.setStyleSheet("border: 2px solid #ccc; border-radius: 15px; padding: 5px; color: black;")

        self.receiver_email_label = QLabel("Recipient's Email:", self)
        self.receiver_email_label.move(250, 120)
        self.receiver_email_label.setFont(font)
        self.receiver_email_entry = QLineEdit(self)
        self.receiver_email_entry.move(380, 120)
        self.receiver_email_entry.resize(300, 30)
        self.receiver_email_entry.setStyleSheet("border: 2px solid #ccc; border-radius: 15px; padding: 5px; color: black;")

        self.message_label = QLabel('Message:', self)
        self.message_label.move(250, 170)
        self.message_label.setFont(font)
        self.message_entry = QTextEdit(self)
        self.message_entry.move(380, 170)
        self.message_entry.resize(300, 200)
        self.message_entry.setStyleSheet("color: black; border: none; border-radius: 15px; padding: 5px;")

        self.date_label = QLabel('Choose Date:', self)
        self.date_label.move(250, 390)
        self.date_label.setFont(font)
        self.date_edit = QDateEdit(self)
        self.date_edit.move(380, 390)
        self.date_edit.resize(150, 30)  # Adjust the size of the QDateEdit widget
        self.date_edit.setStyleSheet("border: 2px solid #ccc; border-radius: 15px; padding: 5px; color: black;")
        self.date_edit.setDate(QDate.currentDate())

        self.send_button = QPushButton('Send Email', self)
        self.send_button.setGeometry(380, 450, 300, 50)
        self.send_button.clicked.connect(self.send_email)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0070c9;  /* Apple blue */
                color: #f6f6f6;  /* Light gray */
                border: none;
                border-radius: 25px; /* Make the button more round */
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #005192; /* Darker blue on hover */
            }
        """)

        self.show()

    def send_email(self):
        sender_email = self.sender_email_entry.text()
        password = self.password_entry.text()
        receiver_email = self.receiver_email_entry.text()
        message = self.message_entry.toPlainText()
        send_date = self.date_edit.date().toString(Qt.DateFormat.ISODate)

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "Happy Birthday!"
            msg.attach(MIMEText(message, 'plain'))

            # Connect to Gmail's SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)

            # Send the message
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()

            QMessageBox.information(self, 'Success', 'Email sent successfully!', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e), QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmailSender()
    sys.exit(app.exec())
