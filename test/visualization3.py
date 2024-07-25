import geopandas as gpd
import plotly.graph_objects as go
import pandas as pd
import plotly.colors as colors

def create_heatmap(geojson_path, price, demand, order, title):
    # GeoJSONファイルの読み込み
    gdf = gpd.read_file(geojson_path)
    # 投影法の修正
    gdf = gdf.to_crs(epsg=4326)
    # GeoJSONの都道府県の順番をソート
    gdf['nam'] = pd.Categorical(gdf['nam'], categories=order, ordered=True)
    gdf = gdf.sort_values('nam').reset_index(drop=True)

    gdf['price'] = price
    gdf['demand'] = demand
    
    # 緯度・経度情報を抽出
    gdf['lon'] = gdf.geometry.centroid.x
    gdf['lat'] = gdf.geometry.centroid.y

    # 色のスケールを定義
    colorscale = 'Viridis'
    min_price, max_price = gdf['price'].min(), gdf['price'].max()

    # 地図を背景に設定
    fig = go.Figure(go.Choroplethmapbox(
        geojson=gdf.geometry.__geo_interface__,
        locations=gdf.index,
        z=gdf['price'],
        colorscale=colorscale,
        marker_opacity=0.5,
        marker_line_width=0
    ))

    # 3Dの棒グラフを作成
    for i, row in gdf.iterrows():
        # priceを色にマッピング
        norm_price = (row['price'] - min_price) / (max_price - min_price)
        color = colors.sample_colorscale(colorscale, norm_price)[0]  # 最初の色を取り出す

        fig.add_trace(go.Scattermapbox(
            lon=[row['lon']],
            lat=[row['lat']],
            mode='markers',
            marker=dict(
                size=5,
                color=color,
                opacity=0.8
            ),
            text=f"{row['nam']}<br>Demand: {row['demand']}<br>Price: {row['price']}"
        ))

        fig.add_trace(go.Scattermapbox(
            lon=[row['lon'], row['lon']],
            lat=[row['lat'], row['lat']],
            mode='lines',
            line=dict(
                color=color,
                width=10
            ),
            text=f"{row['nam']}<br>Demand: {row['demand']}<br>Price: {row['price']}"
        ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=4,
        mapbox_center={"lat": 36.2048, "lon": 138.2529},
        title=title,
        height=800,
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    fig.show()

# 使用例
geojson_path = '../assets/japan_prefectures.geojson'

results_path = '../results/simulation_v3/month_1.csv'
df = pd.read_csv(results_path)
title = '日本の都道府県ごとの需要と価格の3D可視化'
order = [
    "Hokkai Do", "Aomori Ken", "Iwate Ken", "Miyagi Ken", "Akita Ken", "Yamagata Ken", "Fukushima Ken", "Ibaraki Ken",
    "Tochigi Ken", "Gunma Ken", "Saitama Ken", "Chiba Ken", "Tokyo To", "Kanagawa Ken", "Niigata Ken", "Toyama Ken",
    "Ishikawa Ken", "Fukui Ken", "Yamanashi Ken", "Nagano Ken", "Gifu Ken", "Shizuoka Ken", "Aichi Ken", "Mie Ken",
    "Shiga Ken", "Kyoto Fu", "Osaka Fu", "Hyogo Ken", "Nara Ken", "Wakayama Ken", "Tottori Ken", "Shimane Ken",
    "Okayama Ken", "Hiroshima Ken", "Yamaguchi Ken", "Tokushima Ken", "Kagawa Ken", "Ehime Ken", "Kochi Ken", 
    "Fukuoka Ken", "Saga Ken", "Nagasaki Ken", "Kumamoto Ken", "Oita Ken", "Miyazaki Ken", "Kagoshima Ken", "Okinawa Ken"
]
create_heatmap(geojson_path, df['Price'], df['Demand'], order, title)


# import geopandas as gpd
# import plotly.graph_objects as go
# import pandas as pd
# import plotly.colors as colors

# def create_3d_bar_plot(geojson_path, price, demand, order, title):
#     # GeoJSONファイルの読み込み
#     gdf = gpd.read_file(geojson_path)
#     # 投影法の修正
#     gdf = gdf.to_crs(epsg=4326)
#     # GeoJSONの都道府県の順番をソート
#     gdf['nam'] = pd.Categorical(gdf['nam'], categories=order, ordered=True)
#     gdf = gdf.sort_values('nam').reset_index(drop=True)

#     gdf['price'] = price
#     gdf['demand'] = demand
    
#     # 緯度・経度情報を抽出
#     gdf['lon'] = gdf.geometry.centroid.x
#     gdf['lat'] = gdf.geometry.centroid.y

#     # 色のスケールを定義
#     colorscale = 'Viridis'
#     min_price, max_price = gdf['price'].min(), gdf['price'].max()

#     fig = go.Figure()

#     for i, row in gdf.iterrows():
#         # priceを色にマッピング
#         norm_price = (row['price'] - min_price) / (max_price - min_price)
#         color = colors.sample_colorscale(colorscale, norm_price)[0]  # 最初の色を取り出す

#         fig.add_trace(go.Scatter3d(
#             x=[row['lon']],
#             y=[row['lat']],
#             z=[0],
#             mode='markers',
#             marker=dict(
#                 size=5,
#                 color=color,
#                 opacity=0.8
#             ),
#             text=f"{row['nam']}<br>Demand: {row['demand']}<br>Price: {row['price']}",
#             textposition='top center'
#         ))

#         fig.add_trace(go.Scatter3d(
#             x=[row['lon']],
#             y=[row['lat']],
#             z=[0, row['demand']],  # 高さを需要に基づいて設定
#             mode='lines',
#             line=dict(
#                 color=row['price'],
#                 colorscale='Viridis',
#                 width=5
#             )
#         ))

        

#     fig.update_layout(
#         title=title,
#         height=800,
#         scene=dict(
#             xaxis_title='Longitude',
#             yaxis_title='Latitude',
#             zaxis_title='Demand',
#             aspectmode='data',
#             camera_eye=dict(x=1.5, y=1.5, z=0.5)
#         )
#     )

#     fig.show()

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
# create_3d_bar_plot(geojson_path, df['Price'], df['Demand'], order, title)


