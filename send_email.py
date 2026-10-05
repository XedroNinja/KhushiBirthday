"""Sends one email when a new page opens (runs daily at 12:00 am IST via GitHub Actions)."""
import json,os,smtplib,datetime as dt
from email.mime.text import MIMEText
IST=dt.timezone(dt.timedelta(hours=5,minutes=30))
today=str(dt.datetime.now(IST).date())
force=os.environ.get('FORCE_DATE')
today=force or today
SITE='https://xedroninja.github.io/KhushiBirthday/'
TO=['khushi207verma@gmail.com','harshilsharma808@gmail.com']
pages=json.load(open('schedule.json',encoding='utf8'))
p=next((x for x in pages if x['date']==today),None)
if not p:
    print('No page opens today:',today);raise SystemExit
last=p['page']==len(pages)
subj='Happy birthday, Khushi' if last else f"Page {p['page']} of {len(pages)} is open"
body=(f"Happy birthday, Khushi.\n\nThe last page of our book is open:\n{SITE}\n" if last else
      f"A new page just opened in our scrapbook.\n\nPage {p['page']} of {len(pages)}: {p['title']}\n{p['sub']}\n\nRead it here:\n{SITE}\n")
u,pw=os.environ['GMAIL_USER'],os.environ['GMAIL_APP_PASSWORD']
m=MIMEText(body,'plain','utf-8');m['Subject']=subj;m['From']=u;m['To']=', '.join(TO)
with smtplib.SMTP_SSL('smtp.gmail.com',465) as s:
    s.login(u,pw);s.sendmail(u,TO,m.as_string())
print('Sent:',subj)
