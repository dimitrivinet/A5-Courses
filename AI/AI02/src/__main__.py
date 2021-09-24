from torch.utils.data import DataLoader
import torch

from src.data import HPBooks, HPBooksDataset
from src.utils import TrainingConfig
from src import training

SENTENCE_SIZE = 10
BATCH_SIZE = 16

hp_book_paths = [
    "/home/dimitri/Documents/A5-Courses/AI/AI02/harry_potter_books/txts/harry_potter_1.txt",
    "/home/dimitri/Documents/A5-Courses/AI/AI02/harry_potter_books/txts/harry_potter_2.txt",
    "/home/dimitri/Documents/A5-Courses/AI/AI02/harry_potter_books/txts/harry_potter_3.txt",
    "/home/dimitri/Documents/A5-Courses/AI/AI02/harry_potter_books/txts/harry_potter_4.txt",
    "/home/dimitri/Documents/A5-Courses/AI/AI02/harry_potter_books/txts/harry_potter_5.txt",
    "/home/dimitri/Documents/A5-Courses/AI/AI02/harry_potter_books/txts/harry_potter_6.txt",
    "/home/dimitri/Documents/A5-Courses/AI/AI02/harry_potter_books/txts/harry_potter_7.txt",
]


def main():
    hp_books = HPBooks(hp_book_paths)

    hp_trainset = HPBooksDataset(hp_books, train=True, sentence_size=SENTENCE_SIZE)
    hp_validset = HPBooksDataset(hp_books, train=False, sentence_size=SENTENCE_SIZE)
    hp_trainloader = DataLoader(hp_trainset, batch_size=BATCH_SIZE)
    hp_validloader = DataLoader(hp_validset, batch_size=BATCH_SIZE)

    cfg = TrainingConfig(num_epochs=100, save_dir="./output", save_all=False)

    print("creating model.")

    model = torch.nn.RNN(
        input_size=SENTENCE_SIZE, hidden_size=len(hp_books.vocab), num_layers=4, batch_first=True
    )

    print("starting training!")

    training.train(hp_trainloader, hp_validloader, model, cfg)


if __name__ == "__main__":
    main()
