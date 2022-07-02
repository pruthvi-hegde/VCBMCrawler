import os
import json

def get_files(filepath):
    file_list = []
    for base, dirs, files in os.walk(filepath):
        for filename in files:
            file_list.append(base + '/' + filename)
    return file_list


def merge_json_files(filename):
    result = []

    for f1 in filename:
        with open(f1, 'r') as infile:
            result.append(json.load(infile))

    file_content = json.dumps(result)
    with open('all_articles_metadata.json', 'w') as output_file:
        output_file.write(file_content)


if __name__ == "__main__":
    filename = get_files('articles_metadata')
    merge_json_files(filename)