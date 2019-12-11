import requests
import json
import re
import os
import csv

jsonData = None
userList = []
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

try:
    with open(BASE_PATH + '/nameList.json', 'r', encoding='utf-8') as f:
        try:
            jsonData = json.load(f)['userList']
        except Exception as e:
            print('json数据格式不正确：' + str(e))
except Exception as e:
    print('文件不存在：' + str(e))

headers = {
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36"}
message = {"actions": [
    {"id": "40;a", "descriptor": "aura://ApexActionController/ACTION$execute", "callingDescriptor": "UNKNOWN",
     "params": {"namespace": "", "classname": "ProfileService", "method": "fetchTrailheadData",
                "params": {"userId": "", "language": "en-US"}, "cacheable": False,
                "isContinuation": False}}]}
aura_context = {"mode": "PROD", "fwuid": "5fuxCiO1mNHGdvJphU5ELQ", "app": "c:ProfileApp",
                           "loaded": {"APPLICATION@markup://c:ProfileApp": ""}, "dn": [],
                           "globals": {"srcdoc": True}, "uad": True}
obj = requests.get('https://trailblazer.me/c/ProfileApp.app?aura.format=JSON&aura.formatAdapter=LIGHTNING_OUT')
aura_context.get("loaded")['APPLICATION@markup://c:ProfileApp'] = obj.json().get('auraConfig').get('context').get('loaded').get('APPLICATION@markup://c:ProfileApp')


if jsonData:
    for i in jsonData:
        exportData = {}
        exportData['userId'] = i['userId']
        exportData['EID'] = i['EID']
        exportData['URL'] = i['URL']
        exportData['userName'] = ''
        exportData['RankLabel'] = ''
        exportData['EarnedBadgeTotal'] = 0
        exportData['EarnedPointTotal'] = 0
        if not re.match(r'^https://trailhead(.*)', i['URL']) and not re.match(r'^https://trailblazer(.*)', i['URL']):
            exportData['error'] = 'Please enter a valid URL'
        else:
            print('Reading Data: ' + str(i) + '...')
            r = requests.get(i['URL'])
            tmp = re.findall(r'var profileData = JSON.parse\(\"(.+?)\"\)', r.text)[0].replace('\\', '')
            userInfo = json.loads(tmp)
            userName = userInfo.get('profileUser').get('LastName') + userInfo.get('profileUser').get('FirstName')
            exportData['userName'] = userName
            userId = userInfo.get('profileUser').get('Id')
            message.get("actions")[0].get("params").get("params")["userId"] = userId
            data = {"message": json.dumps(message), "aura.context": json.dumps(aura_context), "aura.token": ""}
            r = requests.post("https://trailblazer.me/aura?r=0&aura.ApexAction.execute=1", headers=headers,
                              data=data)
            if r.text.find('EarnedPointTotal') > 0:
                exportData['RankLabel'] = \
                    json.loads(r.json()['actions'][0]['returnValue']['returnValue']['body'])['value'][0][
                        'ProfileCounts'][
                        0][
                        'RankLabel']
                exportData['EarnedBadgeTotal'] = \
                    json.loads(r.json()['actions'][0]['returnValue']['returnValue']['body'])['value'][0][
                        'ProfileCounts'][
                        0][
                        'EarnedBadgeTotal']
                exportData['EarnedPointTotal'] = \
                    json.loads(r.json()['actions'][0]['returnValue']['returnValue']['body'])['value'][0][
                        'ProfileCounts'][
                        0][
                        'EarnedPointTotal']
                exportData['error'] = ''
            else:
                exportData['error'] = 'Please enter a valid URL'
        userList.append(exportData)
print('Done!')

with open(BASE_PATH + '/export.csv', "w", newline='', encoding='utf_8_sig') as f:
    writer = csv.writer(f, dialect='excel')
    writer.writerow(['No', '姓名', 'userName', 'EID', '等级', '勋章', '积分', 'URL', 'error'])
    for inx, val in enumerate(sorted(userList, key=lambda usr: usr['EarnedPointTotal'], reverse=True)):
        writer.writerow([str(inx + 1), val.get('userId'), val.get('userName'), val.get(
            'EID'), val.get('RankLabel'), str(val.get('EarnedBadgeTotal')), str(val.get('EarnedPointTotal')),
                         val.get('URL'), val.get('error')])
