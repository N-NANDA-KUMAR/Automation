
import os
from os import path

from flask import Flask
from flask_mail import Mail, Message

from pretty_html_table import build_table
import pandas  as pd

async_mode = None
app = Flask('GNANI_API_SERVICE')
app.config['SECRET_KEY'] = 'secret!'
app.config['MAIL_USERNAME'] = 'vb.services@gnani.co' 
app.config['MAIL_PASSWORD'] = 'pqOr96V@Hd59Xgkh'
app.config['MAIL_SERVER'] = "smtp.office365.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# EMAIL_OPS_TEAM = ["nanda.kumar@gnani.ai", "divya.r@gnani.ai", "sowmya.bc@gnani.ai", "pavan@gnani.ai"]
EMAIL_OPS_TEAM = ["nanda.kumar@gnani.ai"]


def send_stats_mail(filepath1, filename1, filepath2, filename2,tempDate, key = ""):
    """
    send email
    :param start_date:
    :param count:
    :param end_date:
    :return:
    """
    mail_ops_team = ','.join(EMAIL_OPS_TEAM)
    print("Entering the function - send_stats_mail ! " + str(mail_ops_team))
    
    try:
        with app.app_context():
            msg = Message(subject="Analysis - " + 'Balic Inbound for  ' + str(tempDate),
                          sender="vb.services@gnani.co",
                          recipients=(mail_ops_team.split(","))
                          )
            msg.body = f"Hi, stats for {tempDate}" \
                        + '\n\n' + "Please find attached zip file"
            
            with app.open_resource(filepath1) as fp:
                msg.attach(filename1,'text/csv', fp.read())
            with app.open_resource(filepath2) as fp:
                msg.attach(filename2,'text/csv', fp.read())
            
            if os.path.exists(filepath1):
                os.remove(filepath1)
                os.remove(filepath2)
            else:
                print("The file does not exist")
            mail.send(msg)
    
    except BaseException as exception:
        print(exception)
        print("Unable to send_stats_mail due to connectivity issue with the email server")
        print("Exiting the function - send_stats_mail !")