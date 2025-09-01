from pathlib import Path
import requests
import json
import datetime


# curl -X POST "http://127.0.0.1:5001/pecha-backend-dev/us-central1/api/v2/metadata" -H "Content-Type: application/json" -d 
# '{"type": "root", "bdrc": "W789012", "wiki": "Q789012", "date": "2024-01-15", "title": {"bo": "དམ་པའི་ཆོས་པདྨ་དཀར་པོ།", "en": "The Sacred White Lotus Dharma"}, "alt_titles": [{"bo": "པདྨ་དཀར་པོའི་མདོ།", "en": "White Lotus Sutra"}], "language": "bo", "contributions": [{"person_id": "AxFVSX0jOt_8iS-z", "role": "author"}]}'

def post_expression(payload):
    url = "https://api-l25bgmwqoa-uc.a.run.app/v2/metadata"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    status_code = response.status_code
    print(response_data)
    print(status_code)


def read_json(json_file):
    with open(json_file, "r") as f:
        return json.load(f)
    
def get_title(json_data):
    code = json_data["title"]["titles"]["main"]["code"]
    title = json_data["title"]["titles"]["main"]["text"]
    return {code: title}

def get_alternative_titles(json_data):
    alternative_titles = []
    for title in json_data["title"]["titles"]["alternative"]:
        code = title["code"]
        title = title["text"]
        alternative_titles.append({code: title})
    return alternative_titles
 

def get_payload(json_file):
    json_data = read_json(json_file)
    work_id = json_file.stem
    payload = {
        "type": "translation",
        "bdrc": work_id,
        "parent": "N/A",
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "title": get_title(json_data),
        "alt_titles": get_alternative_titles(json_data),
        "language": json_data["language"]["languages"][0],
        "contributions": [
            {
                "person_bdrc_id": json_data["contribution"][0]["person"]["bdrc"],
                "role": json_data["contribution"][0]["role"]["text"]
            }
            ]
        }
    return payload


if __name__ == "__main__":
    json_file = Path("work/WA0RK0013.json")
    payload = get_payload(json_file)
    post_expression(payload)