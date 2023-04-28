import json

def load_json(path):
    # Abre o arquivo JSON
    with open(path) as f:
        # Lê o conteúdo do arquivo como uma string
        json_str = f.read()
    # Decodifica o JSON em um objeto Python
    return json.loads(json_str)