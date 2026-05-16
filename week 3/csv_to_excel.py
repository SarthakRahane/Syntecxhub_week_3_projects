import pandas as pd
import argparse
import logging
import os
import sys


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def process_csv(input_file, output_file):
    try:
        # Check file exists
        if not os.path.exists(input_file):
            logging.error(f"File not found: {input_file}")
            return

        logging.info("Reading CSV file...")

        # Read csv
        df = pd.read_csv(input_file)

        if df.empty:
            logging.error("CSV file is empty.")
            return

        # Remove extra spaces from column names
        df.columns = df.columns.str.strip()

        # Rename columns (optional normalization)
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        # Fill missing values
        df.fillna("N/A", inplace=True)

        # Try date conversion
        for column in df.columns:
            if "date" in column:
                try:
                    df[column] = pd.to_datetime(
                        df[column],
                        errors="coerce"
                    )
                except:
                    pass

        # Export to excel
        logging.info("Writing Excel file...")

        df.to_excel(
            output_file,
            index=False,
            engine="openpyxl"
        )

        logging.info(f"Success! File saved as: {output_file}")

    except pd.errors.EmptyDataError:
        logging.error("CSV file contains no data.")

    except pd.errors.ParserError:
        logging.error("Invalid CSV format.")

    except PermissionError:
        logging.error("Permission denied. Close the Excel file if open.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="CSV to Excel Converter"
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path of input CSV file"
    )

    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path of output Excel file"
    )

    args = parser.parse_args()

    process_csv(
        args.input,
        args.output
    )


if __name__ == "__main__":
    main()