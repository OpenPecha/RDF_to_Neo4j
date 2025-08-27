import json
from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import SKOS, RDFS
from RDF_to_Neo4j.utils import process_title_literal, get_ttl, wylie_to_tibetan

# Define namespaces
BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")

def process_literal(literal):
    text = str(literal) 
    lang_code = literal.language if hasattr(literal, 'language') else None

    if lang_code == 'bo-x-ewts':
        converted_text = wylie_to_tibetan(text)
        return {'bo': converted_text}
    else:
        return {lang_code: text}


def extract_person_data(person_id, graph):
    person_data = {
        "bdrc_id": person_id,
        "name": [],
        "alt_names": []
    }
    persons = []
    
    try:
        # Get main name from prefLabel
        pref_labels = list(graph.objects(BDR[person_id], SKOS.prefLabel))
        if pref_labels:
            for pref_label in pref_labels:
                person_data["name"].append(process_literal(pref_label))
        
        all_names = []
        for names in person_data["name"]:
            for _, name in names.items():
                all_names.append(name)

        person_names = list(graph.objects(BDR[person_id], BDO["personName"]))
        for person_name_entity in person_names:
            labels = list(graph.objects(person_name_entity, RDFS.label))
            for label in labels:
                processed_name = process_literal(label)
                name = list(processed_name.values())
                if name not in all_names:
                    persons.append(processed_name)
            person_data["alt_names"].append(persons)
            persons = []
    except Exception as e:
        print(f"Error extracting data for person {person_id}: {e}")
    return person_data



def write_to_json(data, folder):
    with open(f"./data/{folder}.json", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_person_file(dir):
    person_files = {}
    for folder in Path(dir).iterdir():
        if folder.is_dir():
            files = []
            for file in folder.iterdir():
                if file.suffix == ".trig":
                    files.append(file)
            person_files[folder.name] = files
    return person_files


def main():
    person_files = get_person_file("./persons")
    all_persons_data = []
    
    for folder_name, files in person_files.items():
        folder_data = []
        if folder_name == '52':
            continue
        print(f"Processing folder: {folder_name} ({len(files)} files)")
        if Path(f"./data/{folder_name}.json").exists():
            continue
        for person_file in person_files[folder_name]:
            person_id = person_file.stem
            # person_id = 'P9972'
            ttl = get_ttl(person_id)
            person_graph = Graph()
            person_graph.parse(data=ttl, format="ttl")
            if person_graph:
                person_data = extract_person_data(person_id, person_graph)
                folder_data.append(person_data)
            else:
                print(f"Error parsing {person_file}")
        
        if folder_data:
            write_to_json(folder_data, folder_name)
            print(f"Wrote {len(folder_data)} persons for folder {folder_name}")
            folder_data = {}


if __name__ == "__main__":
    main()


    # 3c, 33, d9