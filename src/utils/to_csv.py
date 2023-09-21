from typing import List, Tuple
import os
import csv


def save_scores(config: object, scores: dict) -> None:
    """
    Saves computed score to scores.csv files

    :param config object
        Configuration object
    
    :param scores dict
        Dict of scores
    
    :return None
    """

    # Result root
    result_root = os.path.join(config['results']['root'])

    # Scores csv path
    scores_csv_path = os.path.join(result_root, config['results']['scores_csv'])

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
