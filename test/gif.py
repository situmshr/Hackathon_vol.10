from PIL import Image
import os
from path_info import 

# PNGファイルがあるフォルダのパス
folder_path = '../js/picv5/'
# 出力GIFのファイルパス
output_path = 'simulation_v3.gif'

# フォルダ内のPNGファイルを取得してソート
files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])

# 画像を開いてリストに追加
images = [Image.open(os.path.join(folder_path, file)) for file in files]

# GIFを作成
images[0].save(output_path, save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)
