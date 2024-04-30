from pathlib import Path
import sys
from src.helpers.get import parse_toml
from src.utils.corpus_eval import evaluate_corpus
import click

@click.command(context_settings=dict(help_option_names=['-h', '--help'], max_content_width=120))
@click.argument('dataset_name', type=str)
@click.argument('lang', type=str)
# @click.argument('model_name', type=str)
@click.argument('tsv_filename', type=str)

def main(dataset_name: str, lang: str, tsv_filename: str):
    """
    Evaluate experiments

    :param dataset_name str
        Dataset name
    :param lang str
        Target Language
    :param tsv_filename str
        The TSV filename

    :param k_fm int
        The Fuzzy matches to use for the experiment
    """

    print(f'!@@ Dataset: {dataset_name}, Language: {lang}, tsv_filename: {tsv_filename} @@!')

    # toml path
    toml_path: str = Path(f"./configs/{lang}/{dataset_name}.toml")
    
    # Ensure the toml file exists
    if not toml_path.exists():
        print(f"Config file '{dataset_name}.toml' not found at ./configs/, path: {toml_path}")

        # quit
        sys.exit(1)

    # parsing toml
    config = parse_toml(toml_path)

    print(config)
    # evaluate
    evaluate_corpus(config, tsv_filename)


if __name__ == "__main__":
    main()  
