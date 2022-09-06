import os

curPath = os.path.abspath(os.path.dirname(__file__))


class GlobalConfig:
    ENV = "uat"
    ROOT_DIR = os.path.split(curPath)[0]
    MAIN_ENV = False
    # default除入口主函数之外是无效key
    ENV_LIST = ["uat", "sim", "dev", "pro", "default"]
    RESULT_DICT = {}

