
import os
import sys
from .path_info import path_parser
# , PROJECT_DIR, DATA_DIR, OUTPUT_DIR
# sys.path.append(".")

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import optuna

from .utils_simulation import GroundTruthDynamics1, GroundTruthDynamics2




class MatchPriceOptimizer:
    def __init__(self, setting_dict):
        """
        Initialize the MatchPriceOptimizer with the given settings.

        Parameters:
        setting_dict (dict): A dictionary containing settings for the optimizer.
            - 'trainsteps' (int): The number of timesteps to consider for the optimization.
                                 Defaults to 100 if not provided.
            - 'data_file' (str): Path to the CSV file containing the main data.
                                 Defaults to 'default_data.csv' if not provided.

        Attributes:
        trainsteps (int): The number of timesteps for the optimization.
        train_steps (int): The number of training steps, calculated as timesteps - 50 + 1.
        df_main (pd.DataFrame): The main data loaded from the provided CSV file.
        p_code_list (np.ndarray): Unique list of prefecture codes from the data.
        p_name_list (np.ndarray): Unique list of prefecture names from the data.
        """

        # Ground truth の 価格-需要 dynamics の設定
        # self.setting_dict = setting_dict
        self.train_steps = setting_dict['trainsteps']
        # self.data_dir = setting_dict.get(os.path.join(DATA_DIR, setting_dict['data_dir']))
        # self.output_dir = os.path.join(OUTPUT_DIR, setting_dict['output_dir'])
        self.data_dir, self.output_dir = path_parser(setting_dict['data_dir'],setting_dict['output_dir'],setting_dict.get('project_dir',os.getcwd()))
        self.dynamics_type = setting_dict.get('dynamics_type', 'Non-Linear')

        self.df_main = pd.read_csv(os.path.join(os.path.dirname(__file__), 'prefecture_data_with_pairs_info_v2.csv'), index_col=0)
        self.p_code_list = self.df_main['Prefecture_Code'].unique()
        self.p_name_list = self.df_main['Prefecture_JP'].unique()

    def parameter_setting(self):
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
        output_dir = os.path.join(self.output_dir, 'pref-wise')
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
        output_dir = os.path.join(self.output_dir, 'month-wise')
        os.makedirs(output_dir, exist_ok=True)

        for step, data in step_data.items():
            print(step)
            df_step = pd.DataFrame(data)
            df_step.to_csv(os.path.join(output_dir, f'month_{step}.csv'), index=False)


    def find_delta_p(self, f_gt, P_min, P_max, p_values, f_values):
        def objective(trial):
            p = trial.suggest_uniform('p', P_min, P_max)
            return p * f_gt(p)

        sampler = optuna.samplers.TPESampler()
        study = optuna.create_study(direction='maximize', sampler=sampler)
        
        # 既に観測された p_values と f_values を追加
        for p, f in zip(p_values, f_values):
            if P_min <= p <= P_max:
                trial = optuna.trial.create_trial(
                    params={'p': p},
                    distributions={'p': optuna.distributions.UniformDistribution(P_min, P_max)},
                    value=p * f
                )
                study.add_trial(trial)
        
        # 新しい1つの試行を実行
        study.optimize(objective, n_trials=1)

        # 最適化された p の値を返す
        best_p = study.best_params['p']
        delta_p = best_p - p_values[-1]
        return delta_p

    def inputdata_process(self, df_train, f_gt):
        df_train['R_values'] = df_train['p_values'] * df_train['n_values']
        df_train['f_values'] = df_train['p_values'].map(f_gt)
        # return df_train

    def simulate(self, df_train, alpha, P_min, P_max, N_min, N_max, train_data_num):
        # f_gt = None
        if self.dynamics_type == 'Linear':
            f_gt = GroundTruthDynamics1(P_min, P_max, N_min, N_max)
        elif self.dynamics_type == 'Non-Linear':
            f_gt = GroundTruthDynamics2(P_min, P_max, N_min, N_max)
        
        self.inputdata_process(df_train, f_gt)
        
        num_steps = train_data_num + self.train_steps
        # 初期値設定
        n_values = np.zeros(num_steps)
        p_values = np.zeros(num_steps)
        R_values = np.zeros(num_steps)
        f_values = np.zeros(num_steps)
        n_values[:train_data_num] = df_train['n_values'].values
        p_values[:train_data_num] = df_train['p_values'].values
        R_values[:train_data_num] = df_train['R_values'].values
        f_values[:train_data_num] = df_train['f_values'].values

        # print(n_values)

        # シミュレーション実行
        for t in range(train_data_num-1 , num_steps-1):
            p_t = p_values[t]
            n_t = n_values[t]

            delta_p = self.find_delta_p(f_gt, P_min, P_max, p_values[:t], f_values[:t])

            p_t_plus_1 = p_t + delta_p
            f_p_t_plus_1 = f_gt(p_t_plus_1)
            n_t_plus_1 = n_t + alpha * (f_p_t_plus_1 - n_t)
            R_t_plus_1 = p_t_plus_1 * n_t_plus_1
            
            # 値を保存
            p_values[t + 1] = p_t_plus_1
            n_values[t + 1] = n_t_plus_1
            R_values[t + 1] = R_t_plus_1
            f_values[t + 1] = f_p_t_plus_1

        # 結果を DataFrame にまとめる
        results = pd.DataFrame({
            "step": np.arange(num_steps ),
            "p_values": p_values,
            "n_values": n_values,
            "R_values": R_values,
            "f_values": f_values
        })
        
        return results
        
    def main(self):
        print('Start Experiment! ------------------------------------------------\n')
        self.parameter_setting()

        train_data_file_name_list = sorted(os.listdir(self.data_dir))

        result_dict = {}
        for p_name, train_data_file_name in zip(self.p_name_list, train_data_file_name_list):
            print(f'Prefecture Name: {p_name}')

            df = self.df_main[self.df_main['Prefecture_JP'] == p_name]

            # num_steps = self.train_steps
            alpha = 0.1
            N_min = df['Total_subs_l'].values[0]
            N_max = df['Total_subl_u'].values[0]
            P_min = df['Subs_price_l'].values[0]
            P_max = df['Subs_price_u'].values[0]

            n0 = df['Total_subs_init'].values[0]
            p0 = df['Subs_price_init'].values[0]

            df_train = pd.read_csv(os.path.join(self.data_dir, train_data_file_name))
            # df_train = df_train[df_train['step'] < self.train_steps]
            train_data_num = len(df_train)
            result_dict[p_name] = self.simulate(df_train, alpha, P_min, P_max, N_min, N_max, train_data_num)

        self.postprocess(result_dict)
        print('\nFinish Experiment! ------------------------------------------------')



if __name__ == '__main__':
    # data_dir : 分析を開始するデータ置き場。./data/${data_dir}となるように設定
    # output_dir : 出力結果を保存するディレクトリ。./results/${out_dir}/となるように設定。
    # trainsteps : 何ヶ月分予測したいか
    # 
    setting_dict = {
        'project_dir': os.getcwd(),
        'data_dir': 'data1',
        'output_dir': 'moduletest_4',
        'trainsteps': 10,
        'dynamics_type': 'Non-Linear'
    }

    experiment = MatchPriceOptimizer(setting_dict)
    experiment.main()



