from flask import render_template, request, url_for
import shutil
import os
from main_app import app
import uuid

UPLOAD_FOLDER = "upload"

def binary(path):
    try:
        with open(path, 'rb') as f:
            return b'\x00' in f.read(4096)
        
    except Exception:
        return True



def tree(path, indent="", is_last=True, all_data=None, tree_lines=None):
    if all_data == None:
        all_data = []

    if tree_lines == None:
        tree_lines = []


    name = os.path.basename(path)
    if name in ["__pycache__", ".git"]:
        return tree_lines, all_data 


    # ├ or └ の分岐
    branch = "└── " if is_last else "├── "
    tree_itmes = indent + branch + name
    print(tree_itmes)
    tree_lines.append(tree_itmes)




    # 次の階層用インデント作成
    if is_last:
        indent += "    "
    else:
        indent += "│   "

    # ディレクトリなら中身取得
    if os.path.isdir(path):
        items = os.listdir(path)
    
        for i, item in enumerate(items):
            full_path = os.path.join(path, item)
            last = i == len(items) - 1
            tree(full_path, indent, last, all_data, tree_lines)
    

    else:
        if not binary(path):
            try:
                with open(path, encoding="UTF-8")as f:
                        content = f.read()
                        all_data.append({
                            "path":path,
                            "content":content
                })
            except:
                print("ファイルエラー：",path)

    return tree_lines,all_data


            



@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/tree' , methods=["POST"])
def tree_system():
    user_id = uuid.uuid1()
    upload_folder = os.path.join("upload", str(user_id))
    files = request.files.getlist("files")
    print(files)
    os.makedirs(upload_folder,exist_ok=True)


    for file in files:
        path = os.path.join(upload_folder, file.filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file.save(path)

    tree_lines, all_data = tree(upload_folder)

    print(tree_lines)
    print(all_data)
    for i in tree_lines:
        print(i)

    
    shutil.rmtree(upload_folder)
    return render_template(
        'index.html',
        tree_lines = tree_lines,
        all_data = all_data
    )
