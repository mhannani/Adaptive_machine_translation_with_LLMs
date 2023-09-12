import sacrebleu


class Evaluator:
    """
    Evaluation utilities
    """

    def __init__(self, reference_sentence: str, predicted_sentence: str) -> None:
        """
        Class constructor for evaluating MT

        :param reference_sentence str
            The reference sentence

        :param predicted_sentence str
            The predicted sentence
        
        :return None
        """

        # Ground truth sentence
        self.reference_sentence: str = reference_sentence

        # Predicted sentence
        self.predicted_sentence: str = predicted_sentence
    
    def _bleu_score(self) -> float:
        """
        BLEU score
        """

    def bleu_score(self) -> float:
        """
        Calculates the BLEU score for the given sentences

        :Return float
            The BLEU score value
        """

        # Calculate the BLEU score
        blue_score = sacrebleu.corpus_bleu(self.predicted_sentence, [[self.reference_sentence]])

        return blue_score.score
    
    def chrf_score(self) -> float:
        """
        Calculates the CHRF score for the given sentences

        :Return float
            The CHRT score value
        """

        # Calculate the BLEU score
        chrf_score = sacrebleu.corpus_chrf(self.predicted_sentence, [[self.reference_sentence]])

        return chrf_score.score

    def ter_score(self) -> float:
        """
        Calculates the TER score for the given sentences

        :Return float
            The TER score value
        """

        # Calculate the BLEU score
        ter_score = sacrebleu.corpus_ter(self.predicted_sentence, [[self.reference_sentence]])

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
