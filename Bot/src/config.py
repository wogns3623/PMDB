import os
import yaml

# TODO: config를 singleton으로 만들기
def get_config(key: str = None):
    PROJECT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    SOURCE_DIR = os.path.join(PROJECT_DIR, "src")

    with open(os.path.join(PROJECT_DIR, "config.yml")) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)["config"]
        config["project_dir"] = PROJECT_DIR
        config["source_dir"] = SOURCE_DIR

        if key is not None:
            return config[key]
        return config
