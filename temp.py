import os


def binary(path):
    try:
        with open(path, 'rb') as f:
            return b'\x00' in f.read(4096)
        
    except Exception:
        return True

def tree(path, indent="", is_last=True):
    all_data = []
    name = os.path.basename(path) 
    # ├ or └ の分岐
    branch = "└── " if is_last else "├──"
    print(indent + branch + name)


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
            tree(full_path, indent, last)

    else:
        if binary(path):
            return

        try:
            with open(path, encoding="UTF-8")as f:
                    content = f.read()
                    all_data.append({
                        "path":path,
                        "content":content
            })
        except:
            print("ファイルエラー：",path)
        

# ★ここで開始（カレントディレクトリ）
start_path = "main"
print(os.path.abspath(start_path))
tree(start_path, "", True)
