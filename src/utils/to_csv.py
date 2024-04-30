from typing import List, Tuple
import os
import csv
from pathlib import Path


def save_scores(config: object, scores: dict, tsv_filename: str) -> None:
    """
    Saves computed score to scores.csv files

    :param config object
        Configuration object
    
    :param scores dict
        Dict of scores
    
    :param tsv_filename str
        The TSV filename

    :return None
    """

    # Result root
    result_root = Path(config['results']['root'])

    out_csv = f"scores_{Path(tsv_filename).stem}.csv"

    # Scores csv path
    scores_csv_path = result_root / out_csv

    # open csv file read mode
    with open(scores_csv_path, 'w') as csv_file:

        # csv writer
        csv_writer = csv.writer(csv_file)

        # write header
        csv_writer.writerow(['Metric', 'Mean Score'])

        # write bleu score value
        csv_writer.writerow(['BLEU', scores['BLEU']])

        # write chrf score value
        csv_writer.writerow(['CHRF', scores['CHRF']])

        # write ter score value
        csv_writer.writerow(['TER', scores['TER']])
