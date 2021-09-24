#!/usr/bin/env python3
"""
Remove page numbers from Harry Potter books.
"""

import os

def main():
    files = list(os.walk("."))[0][2]
    files = [file for file in files if "harry_potter" in file]
    print(files)

    for file in files:
        count = 0
        with open(file, "r") as f:
            book_lines = f.readlines()
            for line_index, line in enumerate(book_lines):
                if "Page" in line:
                    count += 1
                    book_lines[line_index] = ""

        with open(file, "w") as f:
            for line in book_lines:
                f.write(line)

        print(f"Changed {count} lines in {file}.")

if __name__ == "__main__":
    main()
