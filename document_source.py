import abc
import json
from abc import ABC

from documents import DocumentCollection, DictDocumentCollection, InputDocument


class DocumentSource(ABC):
    """
    Text Acquisition component of the Indexing Process.

    This can be a feed or a crawled source, though the current interface reads all documents
    at the same time.
    """
    @abc.abstractmethod
    def read(self) -> DocumentCollection:
        """
        Get documents from this source.
        :return: The DocumentCollection of all documents from this source.
        """
        pass

class BigramJsonlSource(DocumentSource):
    def __init__(self, name: str):
        self.name = name

    def read(self) -> DocumentCollection:
        with open(self.name) as fp:
            collections = DictDocumentCollection.create_empty()
            for line in fp:
                record = json.loads(line)
                collections.insert(InputDocument(doc_id=record['_id'], text=record['text']))
        return collections