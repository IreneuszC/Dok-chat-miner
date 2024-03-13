from rewarder import Rewarder
import os

"""
Class used for evaluation of the sammuries based on article.
"""
class Evaluator:
    """
    Initializing, creating the rewarder object.
    """
    def __init__(self) -> None:
        self.rewarder = Rewarder(os.path.join('trained_models','sample.model'))
        
    """
    Testing the functionality of the class.
    """
    def test(self):
        article = 'This is an example article. Article includes more information than the summary.'
        summary = 'This is an example summary.'
        score = self.rewarder(article, summary)
        return score
    
    """
    Doing the evaluation based on the summary and document.
    """
    def evaluate(self, document_data, summary_data, debug=False)->float:
        if debug:
            print(f"\nDocument data: {document_data}")
            print(f"Summary data: {summary_data}\n")
        return self.rewarder(document_data, summary_data)
    
    """
    Doing the evaluation based on the summary and document files.
    """
    def evaluate_files(self, path_to_document, path_to_summary, path_to_output_file, debug=False)->float:
        if os.path.exists(path_to_document):
            document_file = open(path_to_document, "r+")
        else:
            print(f"{path_to_document} doesn't exist!")
            return -100000000
        if os.path.exists(path_to_summary):
            summary_file = open(path_to_summary, "r+")
        else:
            print(f"{path_to_document} doesn't exist!")
            return -100000000
        output_file = open(path_to_output_file, "w+")
        
        document_data = document_file.read()
        summary_data = summary_file.read()
        
        score = self.evaluate(document_data, summary_data, debug)
        output_file.write(f"{score}")
        
        document_file.close()
        summary_file.close()
        output_file.close()
        return score
        
if __name__ == '__main__':
    """
    Testing...
    """
    evaluator = Evaluator()
    article = 'This is an example article. Article includes more information than the summary.'
    summary = 'This is an example summary.'
    score = evaluator.evaluate(article, summary)
    print(f"\n1. Score from strings: {score}")
    score = evaluator.evaluate_files("./testing_data/article.txt", "./testing_data/summary.txt", "./testing_data/output.txt", debug=True)
    print(f"\n2. Score from files: {score}")