from setuptools import setup

# requirements.txtの内容を読み込む関数
def parse_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()

# print(parse_requirements('constraints.txt'))
setup(
    install_requires=parse_requirements('constraints.txt')
)
