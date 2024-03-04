from document_source import DocumentSource, BigramJsonlSource
from document_transformer import DocumentTransformer, BigramSearchDocumentTransformer
from index import Index, Indexer, NaiveIndexer
from bigramTokenizer import BigramTokenizer
from collections import Counter
from typing import Dict, List

class CounterBasedTextCounter():
    def count_words(self, text: str) -> Dict[str, int]:
        counts = Counter()
        counts.update(BigramTokenizer().tokenize(text))
        return counts

class DefaultIndexingProcess:
    """
    Simple implementation of the indexing prorocess.

    This class runs components of the indexing process supplied to it either in the constructor
    or in the arguments to the |run| function below.
    """
    def __init__(self, document_transformer: DocumentTransformer, indexer: Indexer):
        self.document_transformer = document_transformer
        self.indexer = indexer

    def count_total_words(self, texts_list: List[str]) -> Counter:
        counts = Counter()
        counter = CounterBasedTextCounter()
        for text in texts_list:
            counts.update(counter.count_words(text))
        return counts

    def compute_stopwords(self, words: [str]) -> [str]:
        counts = self.count_total_words(words)
        stopwords = set()
        for count in counts.most_common(20):
            counter = 0
            for word in words:
                if count[0] in word:
                    counter += 1
            if counter >= 9:
                stopwords.add(count[0])
        return stopwords

    def run(self, source: DocumentSource) -> Index:
        """
        Runs the Indexing Process using the supplied components.
        :param source: Source of documents to index.
        :return: An index used to search documents from the given source.
        """
        # Run the aquisition stage, or just load the results of that stage. Enable iteration over
        # all documents from the given source.

        document_collection = source.read()
        # Create an empty index. Documents will be added one at a time.
        index = self.indexer.create_index()
        everything = [doc.text for doc in document_collection]
        stopwords = self.compute_stopwords(everything)
        for doc in document_collection:
            # Transform and index the document.
            transformed_doc = self.document_transformer.transform_document(doc=doc, stopwords=stopwords)
            index.add_document(transformed_doc)
        return index


def create_naive_indexing_process(index_filename: str) -> DefaultIndexingProcess:
    return DefaultIndexingProcess(
        document_transformer=BigramSearchDocumentTransformer(tokenizer=BigramTokenizer()),
        indexer=NaiveIndexer(index_filename))


def create_inverted_index_indexing_process(index_filename: str) -> DefaultIndexingProcess:
    return DefaultIndexingProcess(
        document_transformer=BigramSearchDocumentTransformer(tokenizer=BigramTokenizer()),
        indexer=NaiveIndexer(index_filename))


def run_inverted_index_indexing_process(input_filename: str, output_filename: str):
    ip = create_naive_indexing_process(output_filename)
    index = ip.run(BigramJsonlSource(input_filename))
    index.write()


