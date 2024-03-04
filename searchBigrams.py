from indexing_process import run_inverted_index_indexing_process
from index import BigramIndexWithFrequencies



def main(index_filename: str):
    """
    Reads the index from the provided file and runs an interactive query search loop.
    :param index_filename: The file to read the index data from.
    """
    run_inverted_index_indexing_process("corpus.jsonl", "corpus.txt")
    index = BigramIndexWithFrequencies(index_filename)
    index.read()
    bigram = input("Please enter a bigram to search:")
    while bigram:
        result = index.search(bigram)
        for r in result.result_doc_ids:
            print(f'DOC_ID={r[0]} : FREQ={r[1]["freq"]} : TEXT={r[1]["text"]}')
        bigram = input("Please enter a bigram:")


if __name__ == "__main__":
    # sys.argv is a list of all the command-line arguments supplied to the script.
    # sys.argv[0] is the name of this script, so actual arguments start from position 1.
    main(index_filename='corpus.txt')
