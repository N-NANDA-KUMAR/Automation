import os
import pymongo
import pysftp
from datetime import datetime


HOSTNAME = "sft.bajajallianz.com"
USERNAME = "gnani@balicin"
PASSWORD = "n7y96R305393"
DATABASE = "click_to_call"
COLLECTION = "report"


current_date_time  = datetime.now()
tempDate = datetime.strftime(current_date_time,"%d/%m/%Y")
tempDate_audio = datetime.strftime(current_date_time,"%Y_%m_%d")
print(tempDate)
print(tempDate_audio)

tempdate_dict = {tempDate:tempDate_audio}
# tempDate_audio = "2022_07_02"
# tempdate_dict = {"02/07/2022":"2022_07_02"}

mongo_client = pymongo.MongoClient("mongodb://harsha:harsha%24123587@172.19.1.141:6003")
collection = mongo_client[DATABASE][COLLECTION]

def download_audios(tempdate_dict):
    for i,j in tempdate_dict.items():
        list_=[str(a['customerCRTId']) for a in collection.find({'tempDate':{'$in':[i]},'call_status':"ANSWERED"})]

        path = './call_audios'
        if os.path.exists(path):
            os.system(f"rm -rf {path}")
            os.mkdir(path)
        else:
            os.mkdir(path)

        for a in list_:
            os.system("scp -i cam.pem ubuntu@172.16.2.23:/gnanicallshare/prod-click2call-eng/"+str(j)+"/*"+str(a)+"* "+str(path))

        os.system("zip "+str(path)+"/call_audios_"+str(j)+".zip "+path+"/*")

def sftp_push():
    with pysftp.Connection("sft.bajajallianz.com", username = USERNAME, password = PASSWORD) as sftp:
        print("----------------connected------------")
        # ls  = sftp.listdir()
        # print(ls)
        
        local_path = f"./call_audios/call_audios_{tempDate_audio}.zip"
        # local_path = f"/home/nanda/balic_automation/call_audios/call_audios_2022_06_28.zip"
        sftp.put(local_path)
        print("-----------------completed-------------")
        sftp.close()


if __name__ == "__main__":
    download_audios(tempdate_dict)
    sftp_push()



    

