"""Module for splitting OPUS-100 corpora into small chunk\
and to save them in a csv file."""

# import standard python libraries
from pathlib import Path
from argparse import ArgumentParser, Namespace

# import installed packages
import pandas as pd

def raw_text_to_csv(corpora_folder: str,
                    out_folder: str) -> None:
    """Build CSV corpora from raw parallel corpora."""

    out_folder: Path = Path(out_folder)
    out_folder.mkdir(parents=True, exist_ok=True)
    # get english and french files with the help of the extension of the files
    english_files: list = sorted(Path(corpora_folder).glob("*.en"))
    french_files: list = sorted(Path(corpora_folder).glob("*.fr"))
    # will contain all couples of enlglish, french translations
    en_fr_translations: list = []
    for corpus_english, corpus_french in zip(english_files, french_files):
        for en_sentence, fr_sentence in zip(open(corpus_english), open(corpus_french)):
            en_sentence: str = en_sentence.strip()
            fr_sentence: str = fr_sentence.strip()
            en_fr_translations.append((en_sentence, fr_sentence))
    
    for idx, i in enumerate(range(0, len(en_fr_translations), 100_000)):
        pd.DataFrame(en_fr_translations[i:i + 100_000],
                    columns=["English", "French"]).to_csv(
                    out_folder / f"corpus_{idx + 1}.csv",
                    index=False)

def main(args: Namespace) -> None:
    """Call the CSV corpora builder from the given arguments."""
    raw_text_to_csv(args.corpora_folder, args.out_folder)

if __name__ == "__main__" :
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--corpora_folder",
        help="The directory containing the corpora.",
        type=str)
    parser.add_argument("--out_folder",
        help="The output folder.",
        type=str)
    main(parser.parse_args())