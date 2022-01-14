import requests
import pathlib
import os

cwd = str(pathlib.Path().resolve())
# print(cwd)


def createFolder(cwd, dir_name):
    try:
        if not os.path.exists(cwd+dir_name):
            os.makedirs(cwd+dir_name)
            print('Directory has been made.')
    except OSError:
        print ('Error: Creating directory. ' +  dir_name)
 
 
createFolder(cwd, '/data')
dir_path = cwd + '/data'

with open('request_log', 'w') as f:
    url = 'https://drive.google.com/file/d/137RyRjvTBkBiIfeYBNZBtViDHQ6_Ewsp/view'
    response = requests.get(url, stream=True)
    f.write(response)
    print('response for the url given has been logged.')
    f.close()