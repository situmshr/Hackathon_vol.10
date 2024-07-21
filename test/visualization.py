import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# ランダムデータの生成
data = np.random.integers[1000,5000](47)

# 日本の地理情報を取得
# (ここではGeoJSONファイルを使用する例)
url = 'https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson'
gdf = gpd.read_file(url)

# 都道府県データにランダムデータを追加
gdf['data'] = data

# ヒートマップの作成
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
gdf.plot(column='data', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
plt.title('membership fee')
plt.show()
