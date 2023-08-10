import requests
import pandas
import json

def sendPOSTreq(headers, url = None, data = None):
  try:
    # response = requests.post(url=url, headers=headers, data=data)
    response = requests.request(method='POST', url=url, headers=headers, data=data)
    return response
  except Exception as err:
    print(err)

def send_alert_to_teams(message:str='', val_url:str=''):
    agent_url = 'https://hannstar.webhook.office.com/webhookb2/d04a9a4a-d535-4fc3-ab6a-0e8a69247128@4385aed4-a143-4812-8d76-480d22a7505f/IncomingWebhook/5510dced4dfc4acb9eab871b65ddd427/ac26c2d0-4ca1-4338-bf22-31bfad7cd462'
    with open('./message_template/file_link_msg_template.json', 'r', encoding='utf-8') as f:
        json_template = f.read()
        json_body = json_template

        print('---------------------------------------------------')
        print(json_body)
        json_headers = {
            'Content-Type': 'application/json',
        }


        json_body = json.loads(json_body)

        json_body = json.dumps(json_body, indent = 4)
        response = sendPOSTreq(headers=json_headers, data=json_body, url=agent_url)
        print(response)



if __name__ == '__main__':
    send_alert_to_teams()

