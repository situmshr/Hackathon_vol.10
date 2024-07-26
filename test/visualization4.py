import pydeck as pdk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from path_info import DATA_DIR, OUTPUT_DIR
import os

# カラーマップの作成（数値データを色に変換する関数）
def value_to_color(value, min_value, max_value, cmap_name='Blues',alpha=0.5):
    norm = plt.Normalize(vmin=min_value, vmax=max_value)
    cmap = plt.get_cmap(cmap_name)
    rgba = list(cmap(norm(value)))
    rgba[3] = alpha
    # matplotlibのRGBAをRGBに変換し、255スケールに変換
    return [int(255 * c) for c in rgba[:3]] + [int(255 * rgba[3])]

# 数値データをヒートマップの色に変換
def convert_to_heatmap(gdf,all_price):
    min_value = all_price.min()
    max_value = all_price.max()
    gdf['price_rgb'] = gdf['price'].apply(lambda x: value_to_color(x, min_value, max_value))

def make_data(geojson_path,price,demand,order,lng,lat,all_price):
    gdf = gpd.read_file(geojson_path)
    gdf['nam'] = pd.Categorical(gdf['nam'], categories=order, ordered=True)
    gdf = gdf.sort_values('nam').reset_index(drop=True)

    gdf['price'] = price
    gdf['demand'] = demand
    gdf['lng'] = lng
    gdf['lat'] = lat
    convert_to_heatmap(gdf,all_price)
    print(gdf)
    return gdf

# CSVファイルの読み込み
# data = pd.read_csv('data.csv')
geojson_path = '../assets/japan_prefectures.geojson'
# results_path = '../results/simulation_v3/month_1.csv'
results_dir = '../results/simulation_v4/month-wise'
pos_path = '../assets/japan_prefectures_pos.csv'
# df = pd.read_csv(results_path)
pos_df = pd.read_csv(pos_path)

order = [
    "Hokkai Do", "Aomori Ken", "Iwate Ken", "Miyagi Ken", "Akita Ken", "Yamagata Ken", "Fukushima Ken", "Ibaraki Ken",
    "Tochigi Ken", "Gunma Ken", "Saitama Ken", "Chiba Ken", "Tokyo To", "Kanagawa Ken", "Niigata Ken", "Toyama Ken",
    "Ishikawa Ken", "Fukui Ken", "Yamanashi Ken", "Nagano Ken", "Gifu Ken", "Shizuoka Ken", "Aichi Ken", "Mie Ken",
    "Shiga Ken", "Kyoto Fu", "Osaka Fu", "Hyogo Ken", "Nara Ken", "Wakayama Ken", "Tottori Ken", "Shimane Ken",
    "Okayama Ken", "Hiroshima Ken", "Yamaguchi Ken", "Tokushima Ken", "Kagawa Ken", "Ehime Ken", "Kochi Ken", 
    "Fukuoka Ken", "Saga Ken", "Nagasaki Ken", "Kumamoto Ken", "Oita Ken", "Miyazaki Ken", "Kagoshima Ken", "Okinawa Ken"
]
all_df = []
for i in range(0, 101):
    df1 = []
    results_path = os.path.join(results_dir, f'month_{i}.csv')
    df1 = pd.read_csv(results_path)
    all_df.append(df1)
all_data = pd.concat(all_df, ignore_index=True)
all_price = all_data['Price']
    
for month in range(0,101):
    results_path = os.path.join(results_dir, f'month_{month}.csv')
    df = pd.read_csv(results_path)
    
    data = make_data(geojson_path,df['Price'],df['Demand'],order,pos_df['lng'],pos_df['lat'],all_price)
# convert_to_heatmap(data)
# ColumnLayer を使用して 3D バーグラフを作成
    layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["lng", "lat"],
        get_elevation="demand",
        get_fill_color="price_rgb",
        radius=10000,
        elevation_scale=0.7,
        pickable=True,
        extruded=True,
    )

    # デッキグラフのビューを設定
    view_state = pdk.ViewState(
        latitude=36.1,
        longitude=135.1,
        zoom=5.1,
        pitch=50,
    )

    # pydeck デッキグラフを作成
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)

    # デッキグラフを HTML ファイルとして保存
    deck.to_html(f'../html/deck_map_{month}.html')

import webbrowser
webbrowser.open('file:///Users/shota/programs/rand/Hackathon/Hackathon_vol.10/html/deck_map.html')