
import json
from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "records.json"


def explore_records():
    """Print three facts about the ChalanCheck legal records."""

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)

        df = pd.DataFrame(records)

        required_columns = {
            "section",
            "max_fine_first",
            "max_fine_repeat",
        }

        if not required_columns.issubset(df.columns):
            raise ValueError("Required record columns are missing.")

        print("\nChalanCheck - Data Exploration")
        print("-----------------------------")

        # Fact 1: Number of unique legal sections
        print(f"Fact 1 - Unique sections: {df['section'].nunique()}")

        # Fact 2: Highest recorded first-offence fine
        highest_first_fine = df["max_fine_first"].max()
        print(f"Fact 2 - Highest first-offence fine: Rs. {highest_first_fine:,.0f}")

        # Fact 3: Records with a separate repeat-offence fine
        repeat_count = df["max_fine_repeat"].notna().sum()
        print(f"Fact 3 - Records with repeat-offence fine: {repeat_count}")

    except (OSError, json.JSONDecodeError, ValueError, KeyError) as error:
        print(f"Data exploration failed: {error}")


if __name__ == "__main__":
    explore_records()
