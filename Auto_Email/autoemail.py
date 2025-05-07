import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==== 1. Đọc thông tin từ các file văn bản ====

# Đọc email và mật khẩu ứng dụng
with open('C:/pyth/Auto_Email/pass.txt', 'r') as f:
    sender_email = f.readline().strip()
    app_password = f.readline().strip()

# Đọc nội dung gửi email
with open('C:\pyth\Auto_Email\email_send.txt', 'r', encoding='utf-8') as a:
    receiver_email = a.readline().strip()
    subject = a.readline().strip()
    body = a.read().strip()

# Đọc tiêu chí lọc email đến
with open('C:\pyth\Auto_Email\email_search.txt', 'r') as b:
    search_criteria = b.read().strip()


# ==== 2. Gửi Email ====
def send_email():
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Email đã được gửi.")
    except Exception as e:
        print("❌ Lỗi khi gửi email:", e)


# ==== 3. Nhận Email từ Inbox ====
def receive_emails():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(sender_email, app_password)
        mail.select("inbox")

        status, data = mail.search(None, search_criteria)
        mail_ids = data[0].split()

        if not mail_ids:
            print("📭 Không tìm thấy email phù hợp.")
            return

        print(f"📨 Tìm thấy {len(mail_ids)} email phù hợp.")

        for i in mail_ids:
            status, msg_data = mail.fetch(i, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg["subject"]
                    from_ = msg["from"]
                    print(f"\n🔹 From: {from_}")
                    print(f"🔹 Subject: {subject}")

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                print("🔹 Nội dung:")
                                print(part.get_payload(decode=True).decode("utf-8"))
                    else:
                        print("🔹 Nội dung:")
                        print(msg.get_payload(decode=True).decode("utf-8"))
        mail.logout()
    except Exception as e:
        print("❌ Lỗi khi đọc email:", e)


# ==== 4. Thực thi ====
send_email()
receive_emails()
