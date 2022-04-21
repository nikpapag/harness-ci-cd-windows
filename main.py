import os
import time
import requests
import json
import re,sys


apiKey=os.getenv('PLUGIN_HARNESS_API_KEY') or ""
accountID=os.getenv('PLUGIN_HARNESS_ACCOUNT_ID') or ""
appId=os.getenv('PLUGIN_HARNESS_APPLICATION_ID') or ""
service=os.getenv('PLUGIN_HARNESS_SERVICE') or ""
webhook=os.getenv('PLUGIN_HARNESS_WEBHOOK_ID') or ""
build_number=os.getenv('PLUGIN_HARNESS_BUILD_NUMBER') or ""
artifact_source_name=os.getenv('PLUGIN_HARNESS_ARTIFACT_SOURCE_NAME') or ""
artifact_settings=os.getenv('PLUGIN_HARNESS_ARTIFACT_SOURCE_ENABLED') or "FALSE"
parameter_settings=os.getenv('PLUGIN_HARNESS_PARAMETERS_ENABLED') or "FALSE"
pipeline_parameters=os.getenv('PLUGIN_HARNESS_PIPELINE_PARAMETERS') or ''

pipeline_parameters=str(pipeline_parameters).replace(" ","")

# change the JSON string into a JSON objectx
jsonObject = json.loads(str(pipeline_parameters).replace(" ",""))



#Parameters only if needed
parameters_payload=json.dumps({})
if parameter_settings in("TRUE"):
    parameters_payload={
        "parameters": jsonObject
    }
    parameters_payload=str(parameters_payload).replace("'",'"')



#Application id is always part of the payload
payload = json.dumps({
  "application": appId,
})


artifacts_payload=json.dumps({})
if artifact_settings in("TRUE"):
    artifacts_payload={
        "artifacts": [
            {
                "artifactSourceName": artifact_source_name,
                "service": service,
                "buildNumber": build_number
            }
        ],
    }
    artifacts_payload=str(artifacts_payload).replace("'",'"')


url = "https://app.harness.io/gateway/api/webhooks/"+webhook+"?accountId="+accountID
headers ={
    "Content-Type": "application/json",

}

merged_payload = {**json.loads(payload), **json.loads(artifacts_payload),**json.loads(parameters_payload)}
merged_payload=str(merged_payload).replace("'",'"')


print(merged_payload)

response=""

payload = json.dumps(merged_payload)


try:
    response = requests.request("POST", url, headers=headers, data=merged_payload)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(response.text)
    raise SystemExit(err)


response_txt=response.json()
print(response_txt['uiUrl'])

requestId = response_txt['requestId']
apiURL= response_txt['apiUrl']

executionId= apiURL.split('/')[8]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    WHITE = '\033[37m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_cd_status():
    print("Checking status for CD Pipeline", flush=True)
    current_status="STARTING"
    time.sleep(2)
    print("execution status: " +bcolors.WHITE+current_status+ bcolors.ENDC)
    while True:
        headers={
             'X-Api-Key': apiKey
        }
        url='https://app.harness.io/gateway/api/external/v1/executions/'+executionId+'/status?accountId='+accountID+'&appId='+appId
        status= requests.get(url,headers=headers)
        cd_status=''
        try:
            cd_status=status.json()['status']
        except:
            print(status.request)
            print(status.json())
            print(status.text)
            print(status.status_code)

        time.sleep(5)
        if cd_status not in ('SUCCESS','FAILED','EXPIRED','ABORTED'):
            if cd_status not in(current_status):
                if cd_status in ('RUNNING'):
                    print("Status Changed", flush=True)
                    print("execution status " + bcolors.OKGREEN + cd_status + bcolors.ENDC, flush=True)
                    current_status=cd_status
                    time.sleep(5)
                else:
                    print("Status Changed")
                    print("execution status " + bcolors.OKCYAN + cd_status + bcolors.ENDC, flush=True )
                    current_status = cd_status
                    time.sleep(5)
        else:
            if cd_status in ('SUCCESS'):
                print("Status Changed", flush=True)
                print("execution status " + bcolors.OKGREEN + cd_status + bcolors.ENDC, flush=True )
                time.sleep(5)
                break;
            elif cd_status in ('EXPIRED', 'ABORTED'):
                print("Status Changed", flush=True)
                print("execution status " + bcolors.WARNING + cd_status + bcolors.ENDC, flush=True)
                time.sleep(5)
                break;
            else:
                print("Status Changed", flush=True)
                print("execution status " + bcolors.FAIL + cd_status + bcolors.ENDC, flush=True)
                time.sleep(5)
                break;
        time.sleep(5)

check_cd_status()
