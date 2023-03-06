import smtplib

# set up the SMTP server
smtp = smtplib.SMTP('smtp.mail.yahoo.com', 587)
smtp.ehlo()
smtp.starttls()

# login to the SMTP server
smtp.login('gnjenga26@yahoo.com', 'L7^B!(/E7U3XQcR')

# send email message
from_address = 'gnjenga26@yahoo.com'
to_address = 'gracenjenga172@gmail.com'
subject = 'Test Email'
body = 'This is a test email.'
message = f'Subject: {subject}\n\n{body}'
smtp.sendmail(from_address, to_address, message)

# close the SMTP connection
smtp.quit()
