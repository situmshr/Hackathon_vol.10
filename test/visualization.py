import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

def create_heatmap(geojson_path, data, title):

    # GeoJSONファイルの読み込み
    gdf = gpd.read_file(geojson_path)
    gdf['data'] = data

    # ヒートマップの作成
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    gdf.plot(column='data', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    plt.title(title)
    plt.show()

#GeoJSONファイルpath
AssetsPath = '../assets/japan_prefectures.geojson'
#一旦、乱数で都道府県別価格を与える。本当はモデルが吐き出した値
data = np.random.default_rng().integers(1000, 10000, 47)

create_heatmap(AssetsPath, data, 'membership fee')
