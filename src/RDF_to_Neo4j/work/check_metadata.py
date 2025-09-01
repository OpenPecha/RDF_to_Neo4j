import requests
import json
import os

def check_metadata(text_id):
    """Get related translation and commentary texts for a pecha ID"""
    url = f"https://api-aq25662yyq-uc.a.run.app/metadata/{text_id}"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        pecha = {
        "work_id": data['source'],
        "pecha_id": text_id,
        "title": data['title'],
        "source_url": data['source_url']
        }
        
        return pecha
    except Exception as e:
        print(f"Error getting translation and commentary for {text_id}: {e}")
        return None

def get_pecha_list():
    final_pecha = []
    pecha_ids = open("pecha_ids.txt").readlines()
    for pecha_id in pecha_ids:
        pecha = check_metadata(pecha_id.strip())
        if pecha:
            final_pecha.append(pecha) 

    with open("pecha_list.json", "w") as f:
        json.dump(final_pecha, f, indent=2, ensure_ascii=False)

def filter_bdrc_pecha():
    bdrc_pecha = []
    pecha_list = json.load(open("pecha_list.json"))
    for pecha in pecha_list:
        if pecha['work_id'] in ["Openpecha", "Openpecha AI", "Kumarajiva"]:
            continue
        elif pecha['source_url'] != None:
            bdrc_pecha.append(pecha)
        else:
            bdrc_pecha.append(pecha)

    with open("bdrc_pecha.json", "w") as f:
        json.dump(bdrc_pecha, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # get_pecha_list()
    filter_bdrc_pecha()