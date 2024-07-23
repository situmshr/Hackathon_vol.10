# src 外のディレクトリ（notebooks/, experiments/, etc）のファイル内で src のプログラムを呼び出す


例）experiments/simulation_v1.py
```
import sys
from path_info import PROJECT_DIR, DATA_DIR, OUTPUT_DIR
sys.path.append(PROJECT_DIR)

from src.utils_simulation import GroundTruthDynamics, PriceOptimizationEnv
```
