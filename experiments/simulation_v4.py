import os
import sys
from path_info import PROJECT_DIR, DATA_DIR, OUTPUT_DIR
sys.path.append(PROJECT_DIR)

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.utils_simulation import GroundTruthDynamics2

class Experiment:
    def __init__(self, setting_dict):
        # Ground truth の 価格-需要 dynamics の設定
        self.setting_dict = setting_dict
        self.timesteps = setting_dict['Timesteps']
        self.df_main = pd.read_csv(setting_dict['data_file'], index_col=0)
        self.p_code_list = self.df_main['Prefecture_Code'].unique()
        self.p_name_list = self.df_main['Prefecture_JP'].unique()

    def preprocess(self):
        self.df_main['Total_subs_l'] = 0
        self.df_main['Total_subl_u'] = self.df_main['Total_Population'] * 0.1
        self.df_main['Total_subs_init'] = float(np.floor(self.df_main['Total_subs'].mean()))
        self.df_main['Subs_price_init'] = 3700
        self.df_main['Subs_price_l'] = 0

        margin = 1000
        scaler = MinMaxScaler()
        self.df_main['Scaled_Population'] = scaler.fit_transform(self.df_main[['Total_Population']])
        self.df_main['Additional_Price'] = self.df_main['Scaled_Population'] * margin
        self.df_main['Subs_price_u'] = self.df_main['Subs_price_init'] + self.df_main['Additional_Price']

    def postprocess(self, result_dict):
        # 県ごとのデータを保存
        output_dir = os.path.join(self.setting_dict['output_dir'], self.setting_dict['id'], 'pref-wise')
        os.makedirs(output_dir, exist_ok=True)

        for p_code, (p_name, df) in zip(self.p_code_list, result_dict.items()):
            df.to_csv(os.path.join(output_dir, f'{p_code}_{p_name}.csv'), index=False)

        # ステップごとのデータを変換
        step_data = {}
        for p_code, (p_name, df) in zip(self.p_code_list, result_dict.items()):
            for _, row in df.iterrows():
                step = int(row['step'])
                if step not in step_data:
                    step_data[step] = []
                step_data[step].append({
                    'Prefecture_Code': p_code,
                    'Prefecture_Name': p_name,
                    'Price': row['p_values'],
                    'Demand': row['n_values'],
                    'Revenue': row['R_values'],
                    'f_values': row['f_values']
                })

        # ステップごとに CSV ファイルに保存
        output_dir = os.path.join(self.setting_dict['output_dir'], self.setting_dict['id'], 'month-wise')
        os.makedirs(output_dir, exist_ok=True)

        for step, data in step_data.items():
            print(step)
            df_step = pd.DataFrame(data)
            df_step.to_csv(os.path.join(output_dir, f'month_{step}.csv'), index=False)
    
    def simulate(self, alpha, P_min, P_max, N_min, N_max, n0, p0, num_steps):
        # GroundTruthDynamics2 インスタンスを作成
        f = GroundTruthDynamics2(P_min, P_max, N_min, N_max)
        
        # 初期値設定
        n_values = np.zeros(num_steps + 1)
        p_values = np.zeros(num_steps + 1)
        R_values = np.zeros(num_steps + 1)
        f_values = np.zeros(num_steps + 1)  # f(p) の値を保存するリストを追加
        n_values[0] = n0
        p_values[0] = p0
        R_values[0] = p0 * n0
        f_values[0] = f(p0)

        # シミュレーション実行
        for t in range(num_steps):
            p_t = p_values[t]
            n_t = n_values[t]
            p_t_plus_1 = p_t  # delta_p_t は 0 なので、p_t_plus_1 は常に p_t と同じ
            f_p_t_plus_1 = f(p_t_plus_1)
            n_t_plus_1 = n_t + alpha * (f_p_t_plus_1 - n_t)
            R_t_plus_1 = p_t_plus_1 * n_t_plus_1
            
            # 値を保存
            p_values[t + 1] = p_t_plus_1
            n_values[t + 1] = n_t_plus_1
            R_values[t + 1] = R_t_plus_1
            f_values[t + 1] = f_p_t_plus_1  # f(p) の値を保存
        
        # 結果を DataFrame にまとめる
        results = pd.DataFrame({
            "step": np.arange(num_steps + 1),
            "p_values": p_values,
            "n_values": n_values,
            "R_values": R_values,
            "f_values": f_values  # f(p) の値を追加
        })
        
        return results
        
    def main(self):
        print('Start Experiment! ------------------------------------------------\n')
        self.preprocess()

        result_dict = {}
        for p_name in self.p_name_list:
            print(f'Prefecture Name: {p_name}')

            df = self.df_main[self.df_main['Prefecture_JP'] == p_name]

            num_steps = self.timesteps
            alpha = 0.1
            N_min = df['Total_subs_l'].values[0]
            N_max = df['Total_subl_u'].values[0]
            P_min = df['Subs_price_l'].values[0]
            P_max = df['Subs_price_u'].values[0]

            n0 = df['Total_subs_init'].values[0]
            p0 = df['Subs_price_init'].values[0]

            result_dict[p_name] = self.simulate(alpha, P_min, P_max, N_min, N_max, n0, p0, num_steps)
        
        self.postprocess(result_dict)
        print('\nFinish Experiment! ------------------------------------------------')

if __name__ == '__main__':
    setting_dict = {
        'id': 'simulation_v4',
        'data_file': os.path.join(DATA_DIR, 'prefecture_data_with_pairs_info_v2.csv'),
        'output_dir': OUTPUT_DIR,
        'Timesteps': 100,
    }

    experiment = Experiment(setting_dict)
    experiment.main()