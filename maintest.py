import smtplib, ssl, csv, random, time, random
from email.message import EmailMessage
from datetime import datetime

replyto = 'Evade procrastination'
subject = 'Subscribe to premium help'
name = 'Homework Help'

counter = {}

with open("C:/Users/HP/Music/Python Projects/Emailgenerator/user.csv") as f:
    data = [row for row in csv.reader(f)]

file_list = ['./message1.txt']  # Single Email

with open('C:/Users/HP/Music/Python Projects/Emailgenerator/cleanedemails.csv', 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        random_user = random.choice(data)
        sender = random_user[0]
        password = random_user[1]

        if sender not in counter:
            counter[sender] = 0

        if counter[sender] >= 50:
            continue

        try:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
            server.login(sender, password)

            em = EmailMessage()
            em['from'] = f'{name} <{sender}>'
            em['Reply-To'] = replyto
            em['To'] = row
            em['subject'] = subject

            random_file = random.choice(file_list)
            with open(random_file, 'r') as file:
                html_msg = file.read()

            em.add_alternative(html_msg, subtype='html')
            server.send_message(em)

            # Update counter and print status
            counter[sender] += 1
            print(counter[sender], " emails sent", "From ", sender, "To ", row, "File ", random_file)

            # Save details to 'sentmails.csv'
            sent_details = [row[0], subject, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), sender]
            with open("sentmails.csv", "a", newline='') as sentfile:
                sentwriter = csv.writer(sentfile)
                sentwriter.writerow(sent_details)

            # Remove sent email from 'mails.csv'
            with open("cleaned_mails.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                rows = rows[1:]

            if rows:
                with open("cleaned_mails.csv", "w", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(rows)

            # Delete sent email from 'cleanedemails.csv'
            with open("cleaned_mails.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                cleaned_rows = list(reader)
                cleaned_rows = [r for r in cleaned_rows if r[0] != row[0]]

            with open("cleaned_mails.csv", "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(cleaned_rows)

            server.close()

            # Introduce a 20-second gap between emails
            random_sleep_time = random.uniform(30, 50)

            time.sleep(random_sleep_time)

        except smtplib.SMTPConnectError as e:
            print(f"Error connecting to the SMTP server for {sender}:", e)

        except smtplib.SMTPAuthenticationError as e:
            print(f"Error authenticating for {sender}:", e)

        except smtplib.SMTPException as e:
            print(f"SMTP error occurred for {sender}:", e)

print("Emails Sent")
for sender, count in counter.items():
    print(f"{sender}: {count}")

