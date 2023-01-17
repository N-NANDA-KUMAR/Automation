import os
import pymongo
from datetime import datetime
from mail import send_stats_mail

DATABASE = "click_to_call"
COLLECTION = "report"

current_date_time  = datetime.now()
tempDate = datetime.strftime(current_date_time,"%d/%m/%Y")
tempDate2 = datetime.strftime(current_date_time,"%Y_%m_%d")
print(tempDate)
print(tempDate2)

tempDate = "05/07/2022"
tempDate2 = "2022_07_05"

mongo_client = pymongo.MongoClient("mongodb://harsha:harsha%24123587@172.19.1.141:6003")
collection = mongo_client[DATABASE][COLLECTION]

fallback_list = list(collection.find({'tempDate':{'$in':[tempDate]},"call_analysis":1,"call_status":'ANSWERED'}))
serviced_list = list(collection.find({'tempDate':{'$in':[tempDate]},"services_count":{'$gte':1},"call_status":'ANSWERED'}))

print(len(fallback_list))
print(len(serviced_list))

fallback_path = './click2call-fallback'
serviced_path = './click2call-serviced'

fallback_file = 'click2call-fallback.txt'
serviced_file = 'click2call-serviced.txt'


def check_path(pathname):
    if os.path.exists(pathname):
        os.system(f"rm -rf {pathname}")
        os.mkdir(pathname)
    else:
        os.mkdir(pathname)
        

def generate_analysis_report(report_list,pathname,filename):
    dict_={}
    for a in report_list:
        with open(f'{pathname}/{filename}','a') as f:
            if 'conversation_log' in a:
                dict_['customerCRTId'] = str(a['customerCRTId'])
                dict_['conversation_log'] = str(a['conversation_log'])              
                dict_['phone_number'] = str(a['phone_number'])
                f.write(str(dict_)+'\n\n')


def to_schedule_job():
    check_path(fallback_path)
    check_path(serviced_path)

    generate_analysis_report(fallback_list, fallback_path, fallback_file)
    generate_analysis_report(serviced_list, serviced_path, serviced_file)

    send_stats_mail(f'click2call-fallback/{fallback_file}',fallback_file,f'click2call-serviced/{serviced_file}',serviced_file,tempDate)


if __name__ == "__main__":
    check_path(fallback_path)
    check_path(serviced_path)

    generate_analysis_report(fallback_list, fallback_path, fallback_file)
    generate_analysis_report(serviced_list, serviced_path, serviced_file)

    send_stats_mail(f'click2call-fallback/{fallback_file}',fallback_file,f'click2call-serviced/{serviced_file}',serviced_file,tempDate)



