import tomli
from pathlib import Path


def parse_toml(toml_path: Path) -> dict:
    """
    Parses toml configuration file

    :param toml_path Path
        Toml file Path
    
    :return dict
        Returned dictionary of key-value pairs
    """

    # Load and parse the specified TOML configuration file
    try:
        with open(toml_path.as_posix(), 'rb') as config_file:
            return tomli.load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"TOML file '{toml_path}' not found.")
    except tomli.TOMLDecodeError as e:
        raise ValueError(f"Error parsing TOML file '{toml_path}': {e}")
    

if __name__ == "__main__":
    toml_path = Path("../../config/config.toml")

    # parse toml file
    config = parse_toml(toml_path)

    # print config
    print(config)