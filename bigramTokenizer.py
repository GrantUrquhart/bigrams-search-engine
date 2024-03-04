from typing import List
import re
import abc
from abc import ABC


class Tokenizer(ABC):
    @abc.abstractmethod
    def tokenize(self, text: str) -> List[str]:
        pass


class BigramTokenizer(Tokenizer):
    def tokenize(self, text: str) -> List[str]:
        text = re.sub(r'[^\w\s\'$%]', '', text)
        initial = re.sub(r'(\W)', r' \1 ', text.lower())
        adjusted = re.sub(r'(\w) \' (\w)', r"\1'\2", initial)
        adjusted = re.sub(r'(\w) %', r"\1%", adjusted)
        adjusted = re.sub(r'\$ (\w)', r"$\1", adjusted)
        final = re.sub(r' \' ', '', adjusted)
        return final.split()
