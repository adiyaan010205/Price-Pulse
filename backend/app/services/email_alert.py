import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import List
import sendgrid
from sendgrid.helpers.mail import Mail

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    
    def send_price_alert(self, recipient_email: str, product_name: str, 
                        old_price: float, new_price: float, product_url: str):
        """Send price drop alert email"""
        subject = f"Price Drop Alert: {product_name}"
        
        html_content = f"""
        <html>
            <body>
                <h2>🎉 Great News! Price Drop Detected</h2>
                <p>The price for <strong>{product_name}</strong> has dropped!</p>
                <ul>
                    <li>Previous Price: <s>${old_price:.2f}</s></li>
                    <li>New Price: <strong>${new_price:.2f}</strong></li>
                    <li>You Save: ${old_price - new_price:.2f}</li>
                </ul>
                <p><a href="{product_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Product</a></p>
            </body>
        </html>
        """
        
        if self.sendgrid_api_key:
            return self._send_with_sendgrid(recipient_email, subject, html_content)
        else:
            return self._send_with_smtp(recipient_email, subject, html_content)
    
    def _send_with_smtp(self, recipient_email: str, subject: str, html_content: str):
        """Send email using SMTP"""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.smtp_user
            message["To"] = recipient_email
            
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_user, recipient_email, message.as_string())
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _send_with_sendgrid(self, recipient_email: str, subject: str, html_content: str):
        """Send email using SendGrid"""
        try:
            sg = sendgrid.SendGridAPIClient(api_key=self.sendgrid_api_key)
            message = Mail(
                from_email=self.smtp_user,
                to_emails=recipient_email,
                subject=subject,
                html_content=html_content
            )
            
            response = sg.send(message)
            return response.status_code == 202
        except Exception as e:
            print(f"Error sending email with SendGrid: {e}")
            return False

email_service = EmailService()
