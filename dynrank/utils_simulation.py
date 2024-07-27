import numpy as np
import matplotlib.pyplot as plt
import gym
# from stable_baselines3 import PPO


class GroundTruthDynamics1:
    def __init__(self, P_min: float, P_max: float, \
                 N_min: int, N_max: int, k: float = 0.0025):
        self.P_min = P_min
        self.P_max = P_max
        self.N_min = N_min
        self.N_max = N_max
        self.k = k
        self.x0 = (P_max + P_min) / 2  # シグモイド関数の中央位置

    def __call__(self, p: float) -> float:
        value = self.N_min + (self.N_max - self.N_min) / (1 + np.exp(self.k * (p - self.x0)))
        return np.clip(value, self.N_min, self.N_max)
    

class GroundTruthDynamics2:
    def __init__(self, P_min: float, P_max: float, \
                 N_min: int, N_max: int):
        self.P_min = P_min
        self.P_max = P_max
        self.N_min = N_min
        self.N_max = N_max

    def __call__(self, p: float) -> float:
        # 線形補間
        value = self.N_max - (self.N_max - self.N_min) * (p - self.P_min) / (self.P_max - self.P_min)
        return np.clip(value, self.N_min, self.N_max)


def plot_functions(N_func, P_min, P_max, num_points=500):
    """
    Plots N(p) and p * N(p) for a given N_func over the range [P_min, P_max].

    Parameters:
    N_func (callable): The function N(p) to plot.
    P_min (float): The minimum value of P.
    P_max (float): The maximum value of P.
    num_points (int): The number of points to use for plotting (default is 500).
    """
    P_values = np.linspace(P_min, P_max, num_points)
    N_values = [N_func(P) for P in P_values]
    PN_values = [P * N_func(P) for P in P_values]

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Plot N(p)
    axs[0].plot(P_values, N_values, label='N(p)')
    axs[0].set_xlabel('P')
    axs[0].set_ylabel('N')
    axs[0].set_title('Function: N(p)')
    axs[0].legend()
    axs[0].grid(True)

    # Plot p * N(p)
    axs[1].plot(P_values, PN_values, label='p * N(p)', color='orange')
    axs[1].set_xlabel('P')
    axs[1].set_ylabel('p * N(p)')
    axs[1].set_title('Function: p * N(p)')
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()


class PriceOptimizationEnv(gym.Env):
    def __init__(self, dynamics, P_min, P_max, N_min, N_max):
        super(PriceOptimizationEnv, self).__init__()
        self.dynamics = dynamics
        self.P_min = P_min
        self.P_max = P_max
        self.N_min = N_min
        self.N_max = N_max

        # Action and observation space
        self.action_space = gym.spaces.Box(low=self.P_min, high=self.P_max, shape=(1,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=np.array([self.P_min, self.N_min]), 
                                                high=np.array([self.P_max, self.N_max]), dtype=np.float32)

        self.current_price = np.random.uniform(self.P_min, self.P_max)
        self.current_demand = self.dynamics(self.current_price)
        self.current_revenue = self.current_price * self.current_demand

    def reset(self):
        self.current_price = np.random.uniform(self.P_min, self.P_max)
        self.current_demand = self.dynamics(self.current_price)
        self.current_revenue = self.current_price * self.current_demand
        return np.array([self.current_price, self.current_demand])

    def step(self, action):
        new_price = action[0]
        new_demand = self.dynamics(new_price)
        new_revenue = new_price * new_demand

        reward = new_revenue - self.current_revenue

        self.current_price = new_price
        self.current_demand = new_demand
        self.current_revenue = new_revenue

        done = False

        return np.array([self.current_price, self.current_demand]), reward, done, {}

    def render(self, mode='human'):
        pass



# if __name__ == "__main__":
#     P_min, P_max = 0, 5000
#     N_min, N_max = 0, 2000

#     # dynamics = GroundTruthDynamics1(P_min, P_max, N_min, N_max)
#     dynamics = GroundTruthDynamics2(P_min, P_max, N_min, N_max)

#     # General function N(p) = GroundTruthDynamics instance
#     plot_functions(dynamics, P_min, P_max)


# if __name__ == "__main__":
#     P_min, P_max = 0, 5000
#     N_min, N_max = 0, 2000
#     k = 0.0025

#     dynamics_gt = GroundTruthDynamics1(P_min, P_max, N_min, N_max, k)

#     env = PriceOptimizationEnv(dynamics_gt, P_min, P_max, N_min, N_max)

#     model = PPO("MlpPolicy", env, verbose=1)
#     model.learn(total_timesteps=10000)

#     obs = env.reset()
#     for i in range(100):
#         action, _states = model.predict(obs)
#         obs, rewards, dones, info = env.step(action)
#         print(f'Step {i + 1}: Price = {obs[0]}, Demand = {obs[1]}, Reward = {rewards}')

    