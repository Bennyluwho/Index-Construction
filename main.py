from indexer import Indexer
from index_merger import IndexMerger
from stats_printer import StatsPrinter
from pathlib import Path

def clean_old_partials(folder="."):
    folder = Path(folder)
    for f in folder.glob("partial_index_*.json"):
        f.unlink()
    for f in folder.glob("partial_docids_*.json"):
        f.unlink()
    print("Old partial JSON files deleted.")



if __name__ == "__main__":

    clean_old_partials(".")

    indexer = Indexer(root_folder="DEV", batch_size=60000)
    indexer.build()
  
