from flask import Flask, render_template, send_file, request, send_from_directory
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from credentials import EMAIL_ADDRESS, PASSWORD

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("/static/html/index.html")

@app.route('/downloads')
def downloads():
    platform=request.args.get('platform')
    version=request.args.get('version')
    if platform and version:
        file_extension=''
        if platform=='windows':
            file_extension='.exe'
        elif platform=='macos':
            file_extension='.dmg'
        return send_file('/static/downloads/version_{}/KDG_PhotoEditor{}'.format(version, file_extension), attachment_filename='KDG_PhotoEditor{}'.format(file_extension))
    return render_template("/static/html/downloads.html")

@app.route('/about')
def about():
    return render_template('/static/html/about.html')

@app.route('/report_bug', methods=["GET", "POST"])
def report_bug():
    email=request.form.get('email')
    if email:
        software_error=request.form.get('software_error')
        #ICloud server
        s=SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(EMAIL_ADDRESS, PASSWORD)
        msg=MIMEMultipart()
        msg['From']=EMAIL_ADDRESS
        msg['To']=email
        msg['Subject']='Thanks for the bug report!'
        #msg['Body']='Dear {}\nI would like to thank you for your report on the bug you have found. I will reply when the bug has been fixed\nMany thanks,\nKieran Grayshon'.format(request.form.get('name'))
        msg.attach(MIMEText('Dear {}\nI would like to thank you for your report on the bug you have found. I will reply when the bug has been fixed\nMany thanks,\nKieran Grayshon'.format(request.form.get('name')), 'plain'))
        s.send_message(msg)

        msg=MIMEMultipart()
        msg['From']=EMAIL_ADDRESS
        msg['To']=EMAIL_ADDRESS
        msg['Subject']='A bug'
        #msg['Body']='A bug report has come in for the KDG_PhotoEditor here it is below:\n{}'.format(software_error)
        msg.attach(MIMEText('A bug report has come in for the KDG_PhotoEditor here it is below:\n{}'.format(software_error), 'plain'))
        s.send_message(msg)

        s.quit()

        return render_template('/static/html/report_thanks.html')
    else:
        return render_template('/static/html/report_bug.html')

@app.route('/static', methods=["GET"])
def static_serve():
    return send_from_directory('templates/static', request.args.get('path'))

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
