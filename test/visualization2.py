import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def create_heatmap(geojson_path, data, order, title):

    # GeoJSONファイルの読み込み
    gdf = gpd.read_file(geojson_path)
    # GeoJSONの都道府県の順番をソート
    gdf['nam'] = pd.Categorical(gdf['nam'], categories=order, ordered=True)
    gdf = gdf.sort_values('nam').reset_index(drop=True)

    gdf['data'] = data
    print(gdf)

    # ヒートマップの作成
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    gdf.plot(column='data', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    plt.title(title)
    plt.show()

#GeoJSONファイルpath
geojson_path = '../assets/japan_prefectures.geojson'

order = [
    "Hokkai Do", "Aomori Ken", "Iwate Ken", "Miyagi Ken", "Akita Ken", "Yamagata Ken", "Fukushima Ken", "Ibaraki Ken",
    "Tochigi Ken", "Gunma Ken", "Saitama Ken", "Chiba Ken", "Tokyo To", "Kanagawa Ken", "Niigata Ken", "Toyama Ken",
    "Ishikawa Ken", "Fukui Ken", "Yamanashi Ken", "Nagano Ken", "Gifu Ken", "Shizuoka Ken", "Aichi Ken", "Mie Ken",
    "Shiga Ken", "Kyoto Fu", "Osaka Fu", "Hyogo Ken", "Nara Ken", "Wakayama Ken", "Tottori Ken", "Shimane Ken",
    "Okayama Ken", "Hiroshima Ken", "Yamaguchi Ken", "Tokushima Ken", "Kagawa Ken", "Ehime Ken", "Kochi Ken", 
    "Fukuoka Ken", "Saga Ken", "Nagasaki Ken", "Kumamoto Ken", "Oita Ken", "Miyazaki Ken", "Kagoshima Ken", "Okinawa Ken"
]

results_path = '../results/simulation_v3/month_1.csv'
df = pd.read_csv(results_path)
print(df['Price'])
#一旦、乱数で都道府県別価格を与える。本当はモデルが吐き出した値
# data = np.random.default_rng().integers(1000, 10000, 47)

create_heatmap(geojson_path, df['Price'], order, 'membership fee')
