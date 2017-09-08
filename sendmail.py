import smtplib
import sys

sys.path.append("./")
import MYTRconfig

def send(mymsg):
        fromaddr = MYTRconfig.email
        toaddrs  = MYTRconfig.email
        username = MYTRconfig.email
        password = email_password
        server = smtplib.SMTP(email_server)
        server.ehlo()
        server.starttls()
        server.login(username,password)
        msg = "\r\n".join([
  "From: %s" % MYTRconfig.email, 
  "To: %s" % MYTRconfig.email,
  "Subject: Twitter Ripper Bot (local)",
  "",
  "%s" % mymsg
  ])
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()

