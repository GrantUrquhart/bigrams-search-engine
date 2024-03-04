import abc
from abc import ABC
from documents import InputDocument, TransformedDocument

class DocumentTransformer(ABC):
    """
    Text Transformation component of the Index Process.

    Text normalization and tokenization is expected to be part of this component.
    """
    @abc.abstractmethod
    def transform_document(self, doc: InputDocument, stopwords: [str]) -> TransformedDocument:
        pass


class BigramSearchDocumentTransformer(DocumentTransformer):
    """
    An DocumentTransformer implementation that runs the supplied tokenizer.
    """
    def __init__(self, tokenizer):
        """
        :param tokenizer: A tokenizer instance that will be used in document transformation.
        """
        self.tokenizer = tokenizer

    def transform_document(self, doc: InputDocument, stopwords: [str]) -> TransformedDocument:
        """
        Creates TransformedDocument from the given InputDocument by tokenizing its text.

        Uses the tokenizer instance supplied in the constructor.
        :param doc: The InputDocument to be transformed.
        :return: The transformed document
        """
        tokens = self.tokenizer.tokenize(doc.text)
        digrams = list()
        if len(tokens) > 0:
            i = 0
            while tokens[i] in stopwords: i+=1
            while i < len(tokens)-1:
                preWord = tokens[i];
                i+=1
                if tokens[i] in stopwords: i+=1
                else: digrams.append(preWord + ' ' + tokens[i])
        return TransformedDocument(doc_id=doc.doc_id, tokens=digrams, text=doc.text)
