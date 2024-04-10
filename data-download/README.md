# GNSS Data Retrieval Tool

## Overview

This command-line tool is designed to download GNSS (Global Navigation Satellite System) RINEX data from the EPN/Belgian RINEX repository using the [GNSS.be API](https://gnss.be/).

## Installation

### Prerequisites

- Python 3.x
- `pip` package manager

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ROB-GNSS/gnss.be-data-API-examples
    ```

2. **Navigate to the project directory:**

    ```bash
    cd gnss.be-data-API-examples/data-download
    ```

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command Line Arguments

The tool accepts the following command-line arguments:

- `repository`: Repository name (EPN or Belgium)
- `stationList`: List of nine-character station identifiers separated by comma or space (e.g. BRUX00BEL,DENT00BEL)
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format
- `rinex_version`: RINEX version (latest, 2, 3, 4)
- `output_directory`: Output directory path

#### Example Usage

```bash
python data-download.py EPN BRUX00BEL,DENT00BEL 2023-12-01 2023-12-31 latest C:\Temp\rinex_out