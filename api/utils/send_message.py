import email
import smtplib

from config.app_config import DevelopmentCfg


def send_message_to_email(contact: str, msg_text: str, to_email: str):
    msg = email.message.EmailMessage()
    msg['From'] = contact
    msg['To'] = to_email

    try:
        msg.set_content(msg_text)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(contact, DevelopmentCfg.EMAIL_PASSWORD)
            smtp.send_message(msg)

        return {"ok": True, "msg": "Sent successfully"}
    except Exception as e:
        return {"error": e.__str__()}
