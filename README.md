# STDP: Spatiotemporal Dynamic Pricing

このプロジェクトはdynamic pricingと言う動的に価格を変化させて利益の最大化を目指すシステムです。（あくまで例）

## インストール方法
### git clone して使う場合
```bash
git clone https://github.com/situmshr/Hackathon_vol.10.git
cd Hacathon_col.10.git
pip install .
```

### pip経由でモジュールのみインストールする場合
```bash
pip install dynpri
```

## 使い方
### 使用例
```python
import dynpri

setting_dict = {
        'project_dir': os.getcwd(),
        'data_dir': 'data1',
        'output_dir': 'simulation1',
        'trainsteps': 10,
        'dynamics_type': 'Non-Linear'
    }

optimizer = dynpri.MatchPriceOptimizer(setting_dict)
optimizer.main()

```
### setting_dict
- project_dir (optionl) : プロジェクトの位置を示す絶対パス
- data_dir (required) : 読み込みデータ置き場。project_dirからの相対パス
- output_dir (required) : 出力先ディレクトリ。project_dirからの相対パス
- train_steps (required) : 何ヶ月分予測するか。
- dynamics_type (optional) : 'Linear'（線形）, 'Non-Linear'(非線形)のどちらかを指定。デフォルトでは'Non-Linear'として実行される

### 読み込みデータ形式
${project_dir}/data/${data_dir}には以下の形式でcsvファイルを準備する
```bash
data/data1
├── JP-01_北海道.csv
├── JP-02_青森県.csv
├── JP-03_岩手県.csv
├── JP-04_宮城県.csv
├── JP-05_秋田県.csv
├── JP-06_山形県.csv
├── JP-07_福島県.csv
...
├── JP-46_鹿児島県.csv
└── JP-47_沖縄県.csv
```
それぞれのファイルは以下のような形式にする
```
step,p_values,n_values
0,3700,91550
1,3700,86947.38984
2,3700,82805.0407
3,3700,79076.92648
4,3700,75721.62367
5,3700,72701.85115
6,3700,69984.05588
7,3700,67538.04013
8,3700,65336.62596
9,3700,63355.35321
10,3700,61572.20773
```
- step : 月
- p_values : 価格
- n_values : ユーザ数
