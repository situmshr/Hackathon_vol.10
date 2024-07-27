import os

# temp = __file__.rfind('/', 0, __file__.rfind('/'))
# prefix = __file__[:temp]
prefix = os.getcwd()
PROJECT_DIR = prefix
DATA_DIR = os.path.join(prefix, "data")
OUTPUT_DIR = os.path.join(prefix, "results")


# if __name__ == "__main__":
#     print(PROJECT_DIR)
#     print(DATA_DIR)
#     print(OUTPUT_DIR)