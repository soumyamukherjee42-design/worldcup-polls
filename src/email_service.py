"""
Email notification service for World Cup Predictions.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        try:
            self.server = st.secrets["email"]["smtp_server"]
            self.port = st.secrets["email"]["smtp_port"]
            self.sender = st.secrets["email"]["sender_email"]
            self.password = st.secrets["email"]["sender_password"]
        except KeyError:
            logger.error("Email secrets missing. Check your Streamlit Secrets.")
            self.sender = None

    def send_mass_email(self, bcc_list: list, subject: str, html_content: str) -> bool:
        """Sends a single email with recipients hidden in BCC to save time/resources."""
        if not self.sender or not bcc_list:
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"World Cup 2026 Predictions <{self.sender}>"
            # Keep "To" empty when using BCC so users don't see each other's emails
            
            part = MIMEText(html_content, "html")
            msg.attach(part)

            # Connect and send
            with smtplib.SMTP_SSL(self.server, self.port) as server:
                server.login(self.sender, self.password)
                # Send to the BCC list
                server.sendmail(self.sender, bcc_list, msg.as_string())
                
            logger.info(f"Successfully sent mass email to {len(bcc_list)} users.")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def send_leaderboard_update(self, users: list):
        """Notifies users that results are in and the leaderboard has changed."""
        emails = [u['email'] for u in users if u.get('email')]
        
        subject = "🏆 World Cup Leaderboard Updated!"
        html = """
        <html>
            <body>
                <h2 style='color:#1a472a;'>Match Results are In!</h2>
                <p>The latest World Cup matches have finished and the scores have been calculated.</p>
                <p>Did you move up the ranks? <b>Check the Leaderboard now to see your new global position!</b></p>
                <br>
                <a href='https://fifa-worldcup-polls.streamlit.app/' style='background:#e53238; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;'>View Leaderboard</a>
            </body>
        </html>
        """
        return self.send_mass_email(emails, subject, html)

    def send_prediction_reminder(self, users: list, match_count: int):
        """Reminds users to predict upcoming matches."""
        emails = [u['email'] for u in users if u.get('email')]
        
        subject = "⏰ Lock in your World Cup Predictions!"
        html = f"""
        <html>
            <body>
                <h2 style='color:#e53238;'>Don't miss out on points!</h2>
                <p>There are <b>{match_count} upcoming matches</b> kicking off soon.</p>
                <p>You haven't locked in your predictions yet. Head over to the platform before kickoff to make your picks and climb the leaderboard.</p>
                <br>
                <a href='https://fifa-worldcup-polls.streamlit.app/' style='background:#1a472a; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;'>Make Predictions</a>
            </body>
        </html>
        """
        return self.send_mass_email(emails, subject, html)
