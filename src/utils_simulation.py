import numpy as np


class GroundTruthDynamics:
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





# if __name__ == "__main__":
#     import numpy as np
#     import matplotlib.pyplot as plt

#     P_min, P_max = 0, 5000
#     N_min, N_max = 200, 200000

#     dynamics_gt = GroundTruthDynamics(P_min, P_max, N_min, N_max, k=0.0025)
#     P = np.linspace(P_min, P_max, 100)
#     N = dynamics_gt(P)
#     plt.plot(P, N)
#     plt.xlabel("P")
#     plt.ylabel("N")
#     plt.show()