from tqdm import tqdm
from src.evaluation.eval import Evaluator
import csv
import os

from src.utils.to_csv import save_scores


def evaluate_corpus(config: object) -> None:
    """
    Evaluates all predicted subtitles given all source sentence

    :param config object
        Configuration object

    :return None
    """

    # all BLUE scores
    all_bleu = []

    # all CHRF scores
    all_chrf = []

    # all TER scores
    all_ter = []

    # Result root
    result_root = os.path.join(config['results']['root'])

    # Pairs csv path
    pairs_csv_path = os.path.join(result_root, config['results']['pairs_csv'])

    # open csv file read mode
    with open(pairs_csv_path, 'r') as csv_file:

        # csv reader
        csv_reader = csv.reader(csv_file, delimiter='\t')

        # skip the header row
        next(csv_reader)

        # go through csv rows
        for row in tqdm(csv_reader, desc=f"Evaluating", ncols=100):
            # if ever something is missing
            if len(row) != 3:

                # alerting
                print(f"Skipping invalid row: {row}, {len(row)}")

                # skipping
                continue
            
            # destructure fields
            _, target_sentence, predicted_sentence = row

            # evaluator
            evaluator = Evaluator(target_sentence, [predicted_sentence])

            # scores
            scores = evaluator.all_score()

            # BLEU score
            bleu_score = scores['BLEU']

            # Add current blue score
            all_bleu.append(bleu_score)

            # CHRF score
            chrf_score = scores['CHRF']

            # add current chrf score
            all_chrf.append(chrf_score)

            # TER score
            ter_score = scores['TER']

            # add current ter score
            all_ter.append(ter_score)

    
    # Mean of all bleu scores
    mean_bleu = sum(all_bleu) / len(all_bleu)

    # Mean of all chrf scores
    mean_chrf = sum(all_chrf) / len(all_chrf)

    # Mean of all ter scores
    mean_ter = sum(all_ter) / len(all_ter)

    # all scores
    all_scores = {"BLEU": mean_bleu, "CHRF": mean_chrf, "TER": mean_ter}

    # save all score to csv
    save_scores(config, all_scores)

