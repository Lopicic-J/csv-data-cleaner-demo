from pathlib import Path
import sys
import pandas as pd

INPUT_FILE = Path("sample_dirty_data.csv")
OUTPUT_FILE = Path("cleaned_output.csv")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Strip whitespace from string values
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].astype(str).str.strip()

    # Replace empty-like strings with proper missing values
    df = df.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

    # Drop completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing values with placeholders
    fill_values = {
        "name": "Unknown",
        "email": "missing@example.com",
        "city": "Unknown",
        "age": 0,
    }

    for column, default_value in fill_values.items():
        if column in df.columns:
            df[column] = df[column].fillna(default_value)

    return df


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else INPUT_FILE
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else OUTPUT_FILE

    try:
        print(f"Loading file: {input_path}")
        df = pd.read_csv(input_path)

        print(f"Original rows: {len(df)}")
        cleaned_df = clean_dataframe(df)
        print(f"Cleaned rows: {len(cleaned_df)}")

        cleaned_df.to_csv(output_path, index=False)

        print(f"Saved cleaned file to: {output_path}")
        print("Done.")

    except FileNotFoundError:
        print(f"File not found: {input_path}")
        sys.exit(1)
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
