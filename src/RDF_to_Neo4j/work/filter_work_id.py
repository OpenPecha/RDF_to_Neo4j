import requests


def get_all_pecha_ids():
    """Get all pecha IDs from Pecha Backend API using pagination and save to txt file"""
    url = "https://api-l25bgmwqoa-uc.a.run.app/metadata/filter"
    all_pecha_ids = []
    page = 1
    limit = 100
    
    try:
        while True:
            request_body = {"filter": {}, "page": page, "limit": limit}
            response = requests.post(url, json=request_body, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            metadata_array = data.get('metadata', [])
            
            for pecha_obj in metadata_array:
                if 'id' in pecha_obj:
                    all_pecha_ids.append(pecha_obj['id'])
            
            if len(metadata_array) < limit:
                break
            page += 1
        
        # Save to file
        with open('pecha_ids.txt', 'w') as f:
            for pecha_id in all_pecha_ids:
                f.write(f"{pecha_id}\n")
        
        print(f"Saved {len(all_pecha_ids)} pecha IDs to pecha_ids.txt")
        
    except Exception as e:
        print(f"Error getting pecha IDs: {e}")

def get_translation_and_commentary(text_id):
    """Get related translation and commentary texts for a pecha ID"""
    url = f"https://api-aq25662yyq-uc.a.run.app/metadata/{text_id}/related?traversal=full_tree&relationships=translation&Ccommentary"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract all pecha IDs from the response
        pecha_ids = []
        for item in data:
            if item['id'] not in pecha_ids:
                pecha_ids.append(item['id'])
        
        return pecha_ids
    except Exception as e:
        print(f"Error getting translation and commentary for {text_id}: {e}")
        return []
    
def add_pecha_ids_to_txt(pecha_ids):
    """Add pecha IDs to txt file"""
    # Read existing pecha IDs
    existing_ids = set()
    try:
        with open('pecha_ids.txt', 'r') as f:
            existing_ids = {line.strip() for line in f}
    except FileNotFoundError:
        pass
    # Filter out IDs that already exist
    pecha_ids = [pid for pid in pecha_ids if pid not in existing_ids]

    with open('pecha_ids.txt', 'a') as f:
        for pecha_id in pecha_ids:
            f.write(f"{pecha_id}\n")

if __name__ == "__main__":
    pecha_ids = get_translation_and_commentary("I1E4F8487")
    add_pecha_ids_to_txt(pecha_ids)


# I27877531 Dorjee Choepa
# I999EDD0C Sherab Nyingpo
# I60262E03 Chonjuk
# I1E4F8487 Phakdu