import glob
import os

import pandas as pd
from tqdm import tqdm
from kystdatahuset_api_radio2mmsi import resolve_radio
import argparse


def get_callsigns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keeps only unique radio callsigns in the dataframe
    """
    df = df.loc[:, ["Radiokallesignal (ERS)"]]
    df = df.dropna()
    df = df.drop_duplicates()
    return df


def radio2mmsi(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resolve the MMSI of a vessel based on the radio callsign
    """
    df["mmsi"] = 0
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Resolving MMSIs"):
        df.loc[idx, "mmsi"] = resolve_radio(row["Radiokallesignal (ERS)"])
    df = df.dropna()
    df["mmsi"] = df["mmsi"].astype(int)
    return df


def find_por_files(root_dir: str) -> list[str]:
    """
    Recursively find all CSV files under root_dir whose filename ends with
    "por.csv" (case-insensitive).
    """
    pattern = os.path.join(root_dir, "**", "*.csv")
    all_csv_files = glob.glob(pattern, recursive=True)

    por_files = sorted(
        f for f in all_csv_files if os.path.basename(f).lower().endswith("por.csv")
    )
    return por_files


def load_por_files(por_files: list[str]) -> pd.DataFrame:
    """
    Load and concatenate a list of POR CSV files into a single dataframe
    """
    dfs = []
    for csv_file in por_files:
        print(f"Loading {csv_file}")
        try:
            df = pd.read_csv(csv_file, sep=";", decimal=",", low_memory=False)
        except Exception as e:
            print(f"  Skipping {csv_file}: could not read file ({e})")
            continue
        dfs.append(df)

    if not dfs:
        raise ValueError("No POR CSV files could be read successfully")

    combined = pd.concat(dfs, ignore_index=True)
    return combined


def main(root_dir: str) -> None:
    """
    Create mapping between the radio callsign and MMSI of a vessel,
    using every "*por.csv" file found anywhere under root_dir
    """
    output_file = "radio2mmsi.csv"

    # Find all POR csv files in root_dir and its subdirectories
    por_files = find_por_files(root_dir)
    if not por_files:
        raise FileNotFoundError(f'No "*por.csv" files found under {root_dir}')
    print(f'Found {len(por_files)} "*por.csv" file(s) under {root_dir}')

    # Load and combine new data from all found POR CSV files
    por_df = load_por_files(por_files)
    por_radio = get_callsigns(por_df)
    new_df = radio2mmsi(por_radio)

    # Load existing data if file exists
    if os.path.exists(output_file):
        print(f"Loading existing mappings from {output_file}")
        existing_df = pd.read_csv(output_file, sep=";")

        # Combine old and new data
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)

        # Remove duplicates, keeping the first occurrence
        combined_df = combined_df.drop_duplicates(subset=["Radiokallesignal (ERS)"], keep="first")

        print(f"Added {len(new_df)} new entries, total: {len(combined_df)} unique callsigns")
    else:
        print(f"Creating new file {output_file}")
        combined_df = new_df

    # Save combined data
    combined_df.to_csv(output_file, index=False, sep=";")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create a mapping from radio callsign to MMSI, recursively finding all "*por.csv" '
        "files under a given directory"
    )
    parser.add_argument(
        "root_dir", type=str, help='Root directory to search recursively for "*por.csv" files'
    )
    args = parser.parse_args()
    main(args.root_dir)
