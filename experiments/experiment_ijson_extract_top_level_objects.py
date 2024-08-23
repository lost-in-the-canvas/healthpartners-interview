import ijson
import json

def parse_json_file(file_path):
    with open(file_path, 'rb') as file:
        parser = ijson.parse(file)
        top_level_array = False
        array_stack = 0
        top_level_object = False
        object_stack = 0
        for prefix, event, value in parser:
            if event == 'start_array':
                if not top_level_array:
                    top_level_array = True
                    continue
                else:
                    array_stack += 1
            if event == 'start_map':
                if not top_level_object:
                    top_level_object = True
                    builder = ijson.ObjectBuilder()
                else:
                    object_stack += 1
            if event == 'end_map':
                if not top_level_object:
                    raise Exception('end_map without a top level object')
                else:
                    if object_stack == 0:
                        top_level_object = False
                        yield builder.value
                    else:
                        object_stack -= 1
            if event == 'end_array':
                if not top_level_array:
                    raise Exception('end_array without a top level array')
                else:
                    if array_stack == 0:
                        top_level_array = False
                    else:
                        array_stack -= 1
            builder.event(event, value)

# Open the JSON file
file_path = './experiments/data/in/you_json_file.json'
for obj in parse_json_file(file_path):
    print(obj)
