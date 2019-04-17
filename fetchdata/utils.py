import json

def json_dump(o):
   print(json.dumps(o,
                    indent=2,
                    sort_keys=True))
