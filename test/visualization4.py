# import geopandas as gpd
# import plotly.graph_objects as go
# import pandas as pd
# import plotly.colors as colors
# import pydeck


# def create_heatmap(geojson_path, price, demand, order, title):
#     # GeoJSONファイルの読み込み
#     gdf = gpd.read_file(geojson_path)
#     # 投影法の修正
#     gdf = gdf.to_crs(epsg=4326)
#     # GeoJSONの都道府県の順番をソート
#     gdf['nam'] = pd.Categorical(gdf['nam'], categories=order, ordered=True)
#     gdf = gdf.sort_values('nam').reset_index(drop=True)

#     layer = pydeck.Layer(
#         "HexagonLayer",
#         data=gdf,
#         get_position=["lng", "lat"],
#         auto_highlight=True,
#         elevation_scale=50,
#         pickable=True,
#         elevation_range=[0, 3000],
#         extruded=True,
#         coverage=1,
#     )
#     view_state = pydeck.ViewState(
#     longitude=-1.415, latitude=52.2323, zoom=6, min_zoom=5, max_zoom=15, pitch=40.5, bearing=-27.36,
#     )
#     res = pydeck.Deck(layers=[layer], initial_view_state=view_state)
#     res.to_html("hexagon_layer.html")




# # 使用例
# geojson_path = '../assets/japan_prefectures.geojson'

# results_path = '../results/simulation_v3/month_1.csv'
# df = pd.read_csv(results_path)
# title = '日本の都道府県ごとの需要と価格の3D可視化'
# order = [
#     "Hokkai Do", "Aomori Ken", "Iwate Ken", "Miyagi Ken", "Akita Ken", "Yamagata Ken", "Fukushima Ken", "Ibaraki Ken",
#     "Tochigi Ken", "Gunma Ken", "Saitama Ken", "Chiba Ken", "Tokyo To", "Kanagawa Ken", "Niigata Ken", "Toyama Ken",
#     "Ishikawa Ken", "Fukui Ken", "Yamanashi Ken", "Nagano Ken", "Gifu Ken", "Shizuoka Ken", "Aichi Ken", "Mie Ken",
#     "Shiga Ken", "Kyoto Fu", "Osaka Fu", "Hyogo Ken", "Nara Ken", "Wakayama Ken", "Tottori Ken", "Shimane Ken",
#     "Okayama Ken", "Hiroshima Ken", "Yamaguchi Ken", "Tokushima Ken", "Kagawa Ken", "Ehime Ken", "Kochi Ken", 
#     "Fukuoka Ken", "Saga Ken", "Nagasaki Ken", "Kumamoto Ken", "Oita Ken", "Miyazaki Ken", "Kagoshima Ken", "Okinawa Ken"
# ]
# create_heatmap(geojson_path, df['Price'], df['Demand'], order, title)


# import pydeck as pdk

# # サンプルデータ
# data = [
#     {"lat": 35.0, "lng": 139.0, "height": 10000, "color": [255, 0, 0]},
#     {"lat": 35.1, "lng": 139.1, "height": 200, "color": [0, 255, 0]},
#     {"lat": 35.2, "lng": 139.2, "height": 150, "color": [0, 0, 255]},
# ]

# # ColumnLayer を使用して 3D バーグラフを作成
# layer = pdk.Layer(
#     "ColumnLayer",
#     data=data,
#     get_position=["lng", "lat"],
#     get_elevation="height",
#     get_fill_color="color",
#     radius=5000,
#     elevation_scale=1,
#     pickable=True,
#     extruded=True,
# )

# # デッキグラフのビューを設定
# view_state = pdk.ViewState(
#     latitude=35.1,
#     longitude=139.1,
#     zoom=10,
#     pitch=50,
# )

# # pydeck デッキグラフを作成
# deck = pdk.Deck(layers=[layer], initial_view_state=view_state)

# # デッキグラフを表示
# deck.to_html('deck_map.html')


import pydeck as pdk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

# カラーマップの作成（数値データを色に変換する関数）
def value_to_color(value, min_value, max_value, cmap_name='viridis'):
    norm = plt.Normalize(vmin=min_value, vmax=max_value)
    cmap = plt.get_cmap(cmap_name)
    rgba = cmap(norm(value))
    # matplotlibのRGBAをRGBに変換し、255スケールに変換
    return [int(255 * c) for c in rgba[:3]]

# 数値データをヒートマップの色に変換
def convert_to_heatmap(gdf):
    min_value = gdf['price'].min()
    max_value = gdf['price'].max()
    gdf['price_rgb'] = gdf['price'].apply(lambda x: value_to_color(x, min_value, max_value))

def make_data(geojson_path,price,demand,order):
    gdf = gpd.read_file(geojson_path)
    gdf['nam'] = pd.Categorical(gdf['nam'], categories=order, ordered=True)
    gdf = gdf.sort_values('nam').reset_index(drop=True)

    gdf['price'] = price
    gdf['demand'] = demand
    gdf = gdf.to_crs(epsg=3857)
    gdf['lon'] = gdf.geometry.centroid.x
    gdf['lat'] = gdf.geometry.centroid.y
    # gdf = gdf.to_crs(epsg=4326)
    convert_to_heatmap(gdf)
    print(gdf)
    return gdf

# CSVファイルの読み込み
# data = pd.read_csv('data.csv')
geojson_path = '../assets/japan_prefectures.geojson'
results_path = '../results/simulation_v3/month_1.csv'
df = pd.read_csv(results_path)

order = [
    "Hokkai Do", "Aomori Ken", "Iwate Ken", "Miyagi Ken", "Akita Ken", "Yamagata Ken", "Fukushima Ken", "Ibaraki Ken",
    "Tochigi Ken", "Gunma Ken", "Saitama Ken", "Chiba Ken", "Tokyo To", "Kanagawa Ken", "Niigata Ken", "Toyama Ken",
    "Ishikawa Ken", "Fukui Ken", "Yamanashi Ken", "Nagano Ken", "Gifu Ken", "Shizuoka Ken", "Aichi Ken", "Mie Ken",
    "Shiga Ken", "Kyoto Fu", "Osaka Fu", "Hyogo Ken", "Nara Ken", "Wakayama Ken", "Tottori Ken", "Shimane Ken",
    "Okayama Ken", "Hiroshima Ken", "Yamaguchi Ken", "Tokushima Ken", "Kagawa Ken", "Ehime Ken", "Kochi Ken", 
    "Fukuoka Ken", "Saga Ken", "Nagasaki Ken", "Kumamoto Ken", "Oita Ken", "Miyazaki Ken", "Kagoshima Ken", "Okinawa Ken"
]
data = make_data(geojson_path,df['Price'],df['Demand'],order)
# convert_to_heatmap(data)
# ColumnLayer を使用して 3D バーグラフを作成
layer = pdk.Layer(
    "ColumnLayer",
    data=data,
    get_position=["lng", "lat"],
    get_elevation="demand",
    get_fill_color="price_rgb",
    radius=5000,
    elevation_scale=1,
    pickable=True,
    extruded=True,
)

# デッキグラフのビューを設定
view_state = pdk.ViewState(
    latitude=35.1,
    longitude=139.1,
    zoom=5,
    pitch=50,
)

# pydeck デッキグラフを作成
deck = pdk.Deck(layers=[layer], initial_view_state=view_state)

# デッキグラフを HTML ファイルとして保存
deck.to_html('deck_map.html')
