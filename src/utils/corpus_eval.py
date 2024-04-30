from pathlib import Path
from tqdm import tqdm
from src.evaluation.eval import Evaluator
import csv

from src.utils.to_csv import save_scores


def evaluate_corpus(config: object, tsv_filename: str) -> None:
    """
    Evaluates all predicted subtitles given all source sentence

    :param config object
        Configuration object
    
    :param tsv_filename str
        The TSV filename

    :return None
    """

    # Result root
    result_root = Path(config['results']['root'])

    # Pairs csv path
    pairs_tsv_path = result_root / config['data']['target_language'] / tsv_filename

    # target sentences
    target_sentences = []
    
    # predicted sentences
    predicted_sentences =[]

    # open csv file read mode
    with open(pairs_tsv_path.as_posix(), 'r') as csv_file:

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

            # append target sentence
            target_sentences.append(target_sentence)

            # append predicted sentence
            predicted_sentences.append(predicted_sentence)

    # evaluator
    evaluator = Evaluator(target_sentences, predicted_sentences)

    # scores
    scores = evaluator.all_score()

    # all scores
    all_scores = {"BLEU": scores['BLEU'], "CHRF": scores['CHRF'], "TER": scores['TER']}

    print(all_scores)

    # save all score to csv
    save_scores(config, all_scores, tsv_filename)

