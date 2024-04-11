import requests
import wget
import argparse
import re
import os
from datetime import datetime



def validate_repository(repository):
    if repository not in ["EPN", "Belgium"]:
        raise argparse.ArgumentTypeError("Invalid repository name. Choose from EPN or Belgium.")
    return repository

def validate_station_list(station_list):
    identifiers = re.split(r',|\s', station_list)
    if len(identifiers) < 1:
        raise argparse.ArgumentTypeError("Invalid station list. Provide at least one 9 char identifier separated by comma or space.")
    for identifier in identifiers:
        if len(identifier) != 9:
            raise argparse.ArgumentTypeError("Invalid station 9-char identifier length. Each station 9-char identifier should be nine characters long.")
    return identifiers

def validate_date(date):
    try:
        return datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Use YYYY-MM-DD format.")

def validate_rinex_version(rinex_version):
    if rinex_version not in ["latest", "2", "3", "4"]:
        raise argparse.ArgumentTypeError("Invalid RINEX version. Choose from latest, 2, 3, or 4.")
    return rinex_version

def validate_output_directory(output_directory):
    if not os.path.exists(output_directory):
        raise argparse.ArgumentTypeError(f"Output directory '{output_directory}' does not exist.")
    return output_directory



def check_params():
    parser = argparse.ArgumentParser(description="Command line tool to download RINEX data from EPN or from Belgium repository.")
    
    # Add arguments
    parser.add_argument("repository", type=validate_repository, help="Repository name. Available values: EPN, Belgium (e.g. EPN)")
    parser.add_argument("station_list", type=validate_station_list, help="List of nine char identifiers separated by comma(e.g. BRUX00BEL,DENT00BEL or \"BRUX00BEL DENT00BEL\")")
    parser.add_argument("start_date", type=validate_date, help="Start date in YYYY-MM-DD format (e.g. 2023-12-29)")
    parser.add_argument("end_date", type=validate_date, help="End date in YYYY-MM-DD format (e.g. 2023-12-30)")
    parser.add_argument("rinex_version", type=validate_rinex_version, help="RINEX version (latest, 2, 3, 4) (e.g. latest)")
    parser.add_argument("output_directory", type=validate_output_directory, help="Output directory path")
    
    # Parse arguments
    args = parser.parse_args()

    # Return parsed arguments as a dictionary
    return {
        "repository": args.repository,
        "station_list": args.station_list,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "rinex_version": args.rinex_version,
        "output_directory": args.output_directory
    }

def make_api_request(repository, station_id, rinex_version, start_date, end_date):
    repository = repository.lower()
    station_id = station_id.upper()
    start = start_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")
    url = f"https://gnss.be/api/v1/{repository}/station-data/{station_id}?rinexVersion={rinex_version}&startDate={start}&endDate={end}&changeDate=1996-01-01"
    headers = {'accept': 'application/json'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    args = check_params()
    for station_id in args['station_list']:
        data_list = make_api_request(args['repository'], station_id, args['rinex_version'], args['start_date'], args['end_date'])
        for file in data_list:
            wget.download(file['url'], out=args['output_directory'])

