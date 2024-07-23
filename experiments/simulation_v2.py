import os
import sys
from path_info import PROJECT_DIR, DATA_DIR, OUTPUT_DIR
sys.path.append(PROJECT_DIR)

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from stable_baselines3 import PPO
from src.utils_simulation import GroundTruthDynamics, PriceOptimizationEnv




class Experiment:
    def __init__(self, setting_dict):
        # Ground truth の 価格-需要 dynamics の設定
        self.setting_dict = setting_dict

        self.df_main = pd.read_csv(setting_dict['data_file'], index_col=0)
        self.p_code_list = self.df_main['Prefecture_Code'].unique()

    def preprocess(self):
        margin = self.setting_dict['P_max'] - self.setting_dict['P_min']
        scaler = MinMaxScaler()
        self.df_main['Scaled_Population'] = scaler.fit_transform(self.df_main[['Total_Population']])
        self.df_main['Additional_Price'] = self.df_main['Scaled_Population'] * margin

    def postprocess(self, result_dict):
        # ステップごとのデータを変換
        step_data = {}
        for p_code, results in result_dict.items():
            for result in results:
                step = result['Step']
                if step not in step_data:
                    step_data[step] = []
                step_data[step].append({
                    'Prefecture_Code': p_code,
                    'Price': result['Price'],
                    'Demand': result['Demand']
                })

        output_dir = os.path.join(self.setting_dict['output_dir'], self.setting_dict['id'])
        os.makedirs(output_dir, exist_ok=True)

        # ステップごとに CSV ファイルに保存
        for step, data in step_data.items():
            df = pd.DataFrame(data)
            df.to_csv(os.path.join(output_dir, f'month_{step}.csv'), index=False)

    def simulate(self, P_min, P_max, N_min, N_max):
        result_list = []

        dynamics_gt = GroundTruthDynamics(P_min, P_max, N_min, N_max, k=0.0025)
        env = PriceOptimizationEnv(dynamics_gt, P_min, P_max, N_min, N_max)
        model = PPO("MlpPolicy", env, verbose=1)
        model.learn(total_timesteps=10000)

        obs = env.reset()
        for i in range(100):
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env.step(action)
            print(f'Step {i + 1}: Price = {obs[0]}, Demand = {obs[1]}, Reward = {rewards}')

            result_list.append({
                'Step': i + 1,
                'Price': obs[0],
                'Demand': obs[1],
            })
        
        return result_list
        
    def main(self):
        print('Start Experiment! ------------------------------------------------\n')
        self.preprocess()

        result_dict = {}
        for p_code in self.p_code_list:
            print(f'Prefecture Code: {p_code}')

            df = self.df_main[self.df_main['Prefecture_Code'] == p_code]
            P_min = self.setting_dict['P_min']
            P_max = self.setting_dict['P_base'] + df['Additional_Price'].values[0]
            N_min = 0
            N_max = df['Total_Population'].values[0]

            result_dict[p_code] = self.simulate(P_min, P_max, N_min, N_max)
        
        self.postprocess(result_dict)
        print('\nFinish Experiment! ------------------------------------------------')




if __name__ == "__main__":
    # Ground truth の 価格-需要 dynamics の設定
    setting_dict = {
        'id': 'simulation_v2',
        'data_file': os.path.join(DATA_DIR, 'prefecture_data.csv'),
        'output_dir': os.path.join(OUTPUT_DIR),
        'P_base': 3000,
        'P_min': 1000,
        'P_max': 5000,
        'k': 0.0025,
    }

    experiment = Experiment(setting_dict)
    experiment.main()
