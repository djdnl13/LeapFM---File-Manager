from __future__ import division
import shutil         #Contains functions for operating files
import os         #imports the os
import sys
import subprocess
import mimetypes
from flask import Flask, Response, request, jsonify, render_template


app = Flask(__name__)

# getting OS
platform = sys.platform

# initializing mymetype
mimetypes.init()

def humanize_bytes(bytes, precision=1):
    abbrevs = (
        (1<<50, 'PB'),
        (1<<40, 'TB'),
        (1<<30, 'GB'),
        (1<<20, 'MB'),
        (1<<10, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)


def Read():        #For reading files
    path=input("Enter the location of file to read:")
    file=open(path,"r")
    print(file.read()) 
    input('Press Enter...')
    file.close()

@app.route("/list_path", methods=['POST'])
def dirlist(): #Listing files in a directory
    path = request.values.get('path')
    print (path)
    if not os.path.isdir(path):
        return jsonify({})

    sortlist = sorted(os.listdir(path)) #Sorting and listing files
    i = 0

    data = []
    array_list = []
    array_content = []
    while i<len(sortlist):
      if os.path.isfile(path+'/' + sortlist[i]):
        array_content.append(dict(name=sortlist[i], type='file', size=humanize_bytes(os.path.getsize(path + '/' + sortlist[i])), mimetype = mimetypes.guess_type(sortlist[i])[0]))
      elif os.path.isdir(path+'/' + sortlist[i]):
        array_content.append(dict(name=sortlist[i], type='folder', size=humanize_bytes(os.path.getsize(path + '/' + sortlist[i]))))
      i+=1
            
    array_list.append(dict(count=len(array_content), content=array_content))    

    data.append(dict(full_path=path, short_path=os.path.basename(path),list=array_list))

    return jsonify(data)    

def Openfile():
    path = input('Enter the location of Program:')
    try:
        print(platform)
        if platform == "win32":
          os.startfile(path)
        elif platform == "darwin":
          subprocess.call(["open", path])
        else:
          subprocess.call(["xdg-open", path])
          
    except:
        print('File not found')


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
