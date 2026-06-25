"""
send_match_reminders.py

FIFA World Cup 2026 Prediction Platform
Automatic pre-match email reminders

Run:
python jobs/send_match_reminders.py

Schedule:
Every 1 hour (GitHub Actions / Databricks Job / cron)
"""

import os
import logging
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


# ==========================================================
# CONFIG
# ==========================================================

load_dotenv()

NEON_URL = os.getenv("DATABASE_URL")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

FROM_EMAIL = os.getenv("FROM_EMAIL")

REMINDER_MINUTES = 120


# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("email-reminder")


# ==========================================================
# DB
# ==========================================================

def get_connection():
    return psycopg2.connect(
        NEON_URL,
        cursor_factory=RealDictCursor
    )


# ==========================================================
# MATCH QUERY
# ==========================================================

def get_upcoming_matches(conn):

    current = datetime.now(timezone.utc)
    future = current + timedelta(minutes=REMINDER_MINUTES)

    query = """
    SELECT
        match_id,
        team_1,
        team_2,
        match_date,
        kickoff_time,
        venue
    FROM match_master
    WHERE
        status='UPCOMING'
        AND (
            match_date + kickoff_time
        ) BETWEEN %s AND %s
    """

    with conn.cursor() as cur:
        cur.execute(query, (current, future))
        return cur.fetchall()


# ==========================================================
# USERS TO NOTIFY
# ==========================================================

def users_without_prediction(conn, match_id):

    query = """
    SELECT
        u.user_id,
        u.user_name,
        u.email

    FROM user_master u

    WHERE u.status='ACTIVE'

    AND NOT EXISTS (

        SELECT 1
        FROM prediction_fact p

        WHERE
            p.user_id=u.user_id
            AND p.match_id=%s
    )
    """

    with conn.cursor() as cur:
        cur.execute(query, (match_id,))
        return cur.fetchall()


# ==========================================================
# EMAIL
# ==========================================================

def send_email(
    recipient,
    username,
    team1,
    team2,
    kickoff
):

    subject = (
        f"⚽ Prediction closes soon: "
        f"{team1} vs {team2}"
    )

    body = f"""
Hello {username},

Your FIFA World Cup 2026 prediction window is closing.

Upcoming Match:
{team1} vs {team2}

Kickoff:
{kickoff}

Open the app and submit your prediction before kickoff.

Good luck.

FIFA World Cup Predictor
"""

    msg = MIMEMultipart()

    msg["From"] = FROM_EMAIL
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(
        MIMEText(body, "plain")
    )

    try:

        with smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT
        ) as server:

            server.starttls()

            server.login(
                EMAIL_USER,
                EMAIL_PASSWORD
            )

            server.send_message(msg)

        logger.info(
            "Email sent → %s",
            recipient
        )

        return True

    except Exception as e:

        logger.exception(
            "Email failed → %s",
            recipient
        )

        return False


# ==========================================================
# MAIN JOB
# ==========================================================

def run():

    logger.info("Starting reminder job")

    conn = get_connection()

    try:

        matches = get_upcoming_matches(conn)

        if not matches:
            logger.info(
                "No upcoming matches"
            )
            return

        for match in matches:

            users = users_without_prediction(
                conn,
                match["match_id"]
            )

            logger.info(
                "Match %s users=%s",
                match["match_id"],
                len(users)
            )

            for user in users:

                send_email(
                    user["email"],
                    user["user_name"],
                    match["team_1"],
                    match["team_2"],
                    match["kickoff_time"]
                )

    finally:
        conn.close()

    logger.info("Reminder job complete")


if __name__ == "__main__":
    run()
