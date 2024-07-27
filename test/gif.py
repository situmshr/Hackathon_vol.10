from PIL import Image
import os
import re

# PNGファイルがあるフォルダのパス
folder_path = '../js/picv4/'
# 出力GIFのファイルパス
output_path = 'gif/simulation_v4_middle.gif'

# 数字を抽出するための正規表現パターン
pattern = re.compile(r'\d+')

def sort_key(file_name):
    match = pattern.search(file_name)
    return int(match.group()) if match else -1

# フォルダ内のPNGファイルを取得してソート
files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')], key=sort_key)

# 画像を開いてリストに追加
images = [Image.open(os.path.join(folder_path, file)) for file in files]

# GIFを作成
images[0].save(output_path, save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)
