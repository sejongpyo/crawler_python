import os

# Make directory for each website
def create_dir(directory):
    if not os.path.exists(directory):
        print(f'Create folder name : {directory}')
        os.makedirs(directory)

# Make queue and crawled files
def create_files(project_name, base_url):
    queue = project_name + 'queue.txt'
    crawled = project_name + 'crawled.txt'
    if not os.path.isfile(queue):
        make_file(queue, base_url)
    if not os.path.isfile(crawled):
        make_file(crawled, '')

# Make a new file
def make_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

# Insert data
def insert_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

# Delete data
def delete_file_data(path):
    with open(path, 'w'):
        pass #prevent overlapped inserting

# Read a file and convert each line to set items
def set_file(file_name):
    results = set()
    with open(file_name, 'rt') as file:
        for line in file:
            results.add(line.replace('\n', ''))
    return results