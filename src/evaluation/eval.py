from typing import List
import sacrebleu


class Evaluator:
    """
    Evaluation utilities
    """

    def __init__(self, reference_sentence: List, predicted_sentence: List) -> None:
        """
        Class constructor for evaluating MT

        :param reference_sentence List
            The reference sentence

        :param predicted_sentence List
            The predicted sentence
        
        :return None
        """

        # Ground truth sentence
        self.reference_sentence: List = reference_sentence

        # Predicted sentence
        self.predicted_sentence: List = predicted_sentence

    def bleu_score(self) -> float:
        """
        Calculates the BLEU score for the given sentences

        :Return float
            The BLEU score value
        """

        # Calculate the BLEU score
        blue_score = sacrebleu.corpus_bleu(self.predicted_sentence, [self.reference_sentence], tokenize='flores200')

        return blue_score.score
    
    def chrf_score(self) -> float:
        """
        Calculates the CHRF score for the given sentences

        :Return float
            The CHRT score value
        """

        # Calculate the BLEU score
        chrf_score = sacrebleu.corpus_chrf(self.predicted_sentence, [self.reference_sentence])

        return chrf_score.score

    def ter_score(self) -> float:
        """
        Calculates the TER score for the given sentences

        :Return float
            The TER score value
        """

        # Calculate the BLEU score
        ter_score = sacrebleu.corpus_ter(self.predicted_sentence, [self.reference_sentence])

        return ter_score.score
    
    def all_score(self) -> dict:
        """
        Computes all score and return dict of their values
        """

        # BLEU score
        blue_score = self.bleu_score()

        # CHRF score
        chrf_score = self.chrf_score()

        # TER score
        ter_score = self.ter_score()

        return {
            'BLEU': round(blue_score, 2),
            'CHRF': round(chrf_score, 2),
            'TER': round(ter_score, 2)
        }

