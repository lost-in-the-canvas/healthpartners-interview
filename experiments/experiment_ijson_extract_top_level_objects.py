import ijson

def extract_top_level_objects(filename):
    with open(filename, 'rb') as file:
        parser = ijson.parse(file)

        current_object = None
        for prefix, event, value in parser:
            if prefix == '' and event == 'start_array':
                continue
            elif prefix == '' and event == 'end_array':
                break
            elif event == 'start_map':
                current_object = {}
            elif event == 'end_map':
                # Print that a top-level object has been found
                print("Found top-level object:", current_object)
                yield current_object
                current_object = None
            elif current_object is not None:
                current_object[prefix] = value

# Usage
filename = './experiments/data/in/you_json_file.json'
for obj in extract_top_level_objects(filename):
    print(obj)
