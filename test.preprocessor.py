from src.preprocess.preprocessor import TMXPreprocessor
from pathlib import Path


if __name__ == "__main__":
    tmux_file_path = Path("/netscratch/mhannani/data_preparation/TED2020/de-en.tmx")
    output_json_file = Path("./output_ted_2020_de_en.json")

    # TMX preprocessor
    tmx_preprocessor = TMXPreprocessor(tmux_file_path, output_json_file)

    tmx_preprocessor.fire()