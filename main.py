from fetch_emails import get_unread_emails
from summarize_emails import summarize_emails
from send_digest import send_email

emails, application_count = get_unread_emails()
digest = summarize_emails(emails)
final_digest = f"Applications submitted today: {application_count}\n\n{digest}"
send_email(final_digest)
