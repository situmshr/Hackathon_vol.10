import os

# temp = __file__.rfind('/', 0, __file__.rfind('/'))
# prefix = __file__[:temp]
# prefix = os.getcwd()
# PROJECT_DIR = prefix
# DATA_DIR = os.path.join(prefix, "data")
# OUTPUT_DIR = os.path.join(prefix, "results")
def path_parser(data_dir,output_dir,project_dir):
    data_abs_dir = os.path.join(project_dir,'data',data_dir)
    output_abs_dir = os.path.join(project_dir,'results',output_dir)
    return data_abs_dir, output_abs_dir


# if __name__ == "__main__":
#     print(PROJECT_DIR)
#     print(DATA_DIR)
#     print(OUTPUT_DIR)