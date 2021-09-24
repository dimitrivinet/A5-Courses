import os
from typing import Any, List, Tuple
import torch
from torch.utils.data import Dataset
import torchtext


class HPBooks:
    """Harry Potter book for LSTM dataset."""

    book_paths: List[os.PathLike]
    texts: list
    tokenizer: Any

    def __init__(self, book_paths: List[os.PathLike]) -> None:
        self.book_paths = book_paths
        self.texts = []

        for book_path in book_paths:
            with open(book_path, "r", encoding="utf-8") as f:
                text = f.read()

            self.texts.append(text.strip("\\"))

        self.tokenizer = torchtext.data.utils.get_tokenizer(
            "basic_english", language="en"
        )

        self.tokens = []
        for book_index, _ in enumerate(self.book_paths):
            self.tokens.extend(self.tokenizer(self.texts[book_index]))

        self.vocab = torchtext.vocab.build_vocab_from_iterator(iter([self.tokens, ]), specials=["<unk>"])


class HPBooksDataset(Dataset):

    books: HPBooks
    train: bool
    sentence_size: int
    text: List[str]

    def __init__(self, books: HPBooks, train: bool, sentence_size: int = 10) -> None:
        super().__init__()

        self.books = books
        self.train = train
        self.sentence_size = sentence_size

        if self.train:
            self.tokens = self.books.tokenizer("".join(books.texts[:5]))
        else:
            self.tokens = self.books.tokenizer("".join(books.texts[5:]))

    def __len__(self) -> int:
        if len(self.tokens) < self.sentence_size + 1:
            return 0
        return len(self.tokens) - self.sentence_size - 1

    def __getitem__(self, index) -> Tuple[torch.Tensor, torch.Tensor]:
        return (
            torch.Tensor([self.books.vocab(self.tokens[index : index + 10]), ]),
            torch.Tensor(self.books.vocab([self.tokens[index + 10]])),
        )
