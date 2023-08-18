import requests
import pandas
import json
import datetime

class TeamsAlerter:
    def __init__(self):
        with open('./message_template/file_link_msg_template.json', 'r', encoding='utf-8') as f:
            self.json_template = f.read()

        with open('./message_template/list_logging_template.json', 'r', encoding='utf-8') as f:
            self.list_json_template = f.read()
        with open('./message_template/teams_alert_template.json', 'r', encoding='utf-8') as f:
            self.message_json_template = f.read()
    def sendPOSTreq(self, headers, url = None, data = None):
      try:
        # response = requests.post(url=url, headers=headers, data=data)
        response = requests.request(method='POST', url=url, headers=headers, data=data)
        return response
      except Exception as err:
        print(err)

    def send_alert_to_teams(self, message:str='', val_url:str=''):
        agent_url = 'https://hannstar.webhook.office.com/webhookb2/d04a9a4a-d535-4fc3-ab6a-0e8a69247128@4385aed4-a143-4812-8d76-480d22a7505f/IncomingWebhook/befa9ff10e25469fb67d1777aa8ddf5b/ac26c2d0-4ca1-4338-bf22-31bfad7cd462'
        json_body = self.json_template

        message = message.replace('<', '\\\<').replace('>', '\\\>').replace('\n', '<br />')\
            .replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;').replace(',', '\\\,').replace('"', '\\\\"')
        json_body = json_body.replace('{{website_url}}', val_url)
        json_body = json_body.replace('{{message}}', message)
        print('---------------------------------------------------')
        # print(json_body)

        json_headers = {
            'Content-Type': 'application/json',
        }
        # json_body = json.loads(json_body)
        # json_body = json.dumps(json_body, indent=4)
        response = self.sendPOSTreq(headers=json_headers, data=json_body.encode(), url=agent_url)
        print(response)
        print(response.content)

    def alert_list_to_teams(self, message_list:list[str], val_url:str=''):
        agent_url = 'https://hannstar.webhook.office.com/webhookb2/d04a9a4a-d535-4fc3-ab6a-0e8a69247128@4385aed4-a143-4812-8d76-480d22a7505f/IncomingWebhook/befa9ff10e25469fb67d1777aa8ddf5b/ac26c2d0-4ca1-4338-bf22-31bfad7cd462'
        json_body = self.message_json_template

        logging_list_str = ''
        for i,message in enumerate(message_list):
            template = self.list_json_template
            message = message.replace('<', '\\\<').replace('>', '\\\>').replace('\n', '\\n\\n')\
                .replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;').replace(',', '\\\,').replace('"', '\\\"')

            template = template.replace('{{img_expand_id}}', 'img_expand_'+str(i))
            template = template.replace('{{block_detail_id}}', 'block_detail_' + str(i))
            template = template.replace('{{img_collapse_id}}', 'img_collapse_' + str(i))


            e_category = '*\\\[#'+ str(i) +']<' + message.split(']:')[0][1:] + '\\\>*'
            logging = message.split(']:')[1]

            today_datetime = datetime.datetime.today()

            template = template.replace('{{warning_content}}', logging)
            template = template.replace('{{warning_category}}', e_category)
            template = template.replace('{{time_stamp}}', today_datetime.isoformat())
            template = template.replace('{{mention_user}}', "")
            logging_list_str += template +'\n'
            print(e_category)
            print(logging)

        print('---------------------------------------------------')
        json_body = json_body.replace('{{val_url}}', val_url).replace("{{list_logging}}", logging_list_str)

        json_headers = {
            'Content-Type': 'application/json',
        }

        with open('./test.json', 'w', encoding='utf-8') as f:
            f.write(json_body)
        # section_json = json.dumps(json_body, indent=4)
        # print(json_body)
        response = self.sendPOSTreq(headers=json_headers, data=json_body.encode(), url=agent_url)
        print(response)
        print(response.content)



if __name__ == '__main__':
    ta = TeamsAlerter()
    ta.send_alert_to_teams(message='###test<sags>hascascaskc,,,,,jaksck\ttaskajcskj\\tckasjck\njaskcjaksjcksckacak', val_url='https://test.com')

