import os, json, requests, tzlocal
from datetime import datetime
from pprint import pprint
global entry, details, data, database, each_keys, key_set, title, link, date,content

path_to_json = '../threat_intelligence/'
files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

def filter(json_files):

    filtered = ['settings-v2.json','sites.json']
    for items in filtered:
        json_files.remove(items)

def notion_read():

    secret_file = open('.secret.json')
    load_secret = json.load(secret_file)
    secret = load_secret['secret']
    database = load_secret['database']
    
    url = 'https://api.notion.com/v1/databases/<DATABASE-ID>' 

    headers = {

        "Authorization": f'Bearer {secret}',
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    secret_file.close()

    response = requests.get(url, headers=headers)

    print(response.text)

def notion_send(title,link,date,content):

    secret_file = open('.secret.json')
    load_secret = json.load(secret_file)

    secret = load_secret['secret']
    database = load_secret['database']

    url = 'https://api.notion.com/v1/pages'

    headers = {
        "Authorization": f'Bearer {secret}',
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    secret_file.close()


    data_input = {

        "parent": { "database_id": f"{database}" },
            "properties": {
        "Alert": {
            "title": [
            {
                "text": {
                "content": f"{title}",
                },
            }
            ]
        },
        "Link": {
            "url": f"{link}"
        },
        "Content": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": f"{content}"
                },
            }
            ]
        },
        "Status":{
            "status": {
                "name": "Not started"
            }
        },
        "Date":{
            "date": {
                "start": f"{date}",
                "end": f"{date}",
                "time_zone": "Europe/London"
            }
        },\
            }
    }
    response = requests.post(url, headers=headers, json=data_input)
    print(response.json())

def print_json(dataset):
    for entry, details in dataset.items():
    	#Will need restructing 
        key_set = [entry]
        sorted_set = [entry]

        key_set = list(dict.fromkeys(key_set))
        each_key = key_set.pop()

        title = dataset[each_key]['title']
        link = dataset[each_key]['url']
        content = dataset[each_key]['content']

        unix_timestamp = float(dataset[each_key]['date'])
        local_timezone = tzlocal.get_localzone()
        local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)

        dates = local_time.strftime("%Y-%m-%dT%H:%M:00")
        #print(title)
        #print(link)
        #print(content)
        notion_send(title,link,dates,content)
        
def open_json(json_files,path_to_json):

    filter(json_files)

    for file in json_files:

        with open(path_to_json + file, 'r') as f:

            data = json.load(f)
            dataset = data['entries']

            print_json(dataset)

def selector():
    open_json(files,path_to_json)
    
selector()
notion_read()

#Still need to download the data and make it do comparsions to the json it retrives from notion 

