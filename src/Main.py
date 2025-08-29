import os
import argparse
import logging

from filesystem import filesystem
from entities import file, criterion
from datetime import datetime

def __init_log(base_path, debug):
    log_name = f"execution_{datetime.now().strftime("%Y%m%d%H%M%S")}.log"
    log_level = logging.INFO
    if debug == "true":
        log_level = logging.DEBUG
    logging.basicConfig(filename=os.path.join(base_path, ".log", log_name), level=log_level)
    logging.info("LOGGING SYSTEM STARTED")
    logging.debug("Debug level activated! ")

# Create parser
parser = argparse.ArgumentParser(description="Add destination base path. [optional: classifcation mode data by default]")

# Add arguments
parser.add_argument("-o", "--origin", type=str, default="./", help="Origin base path (optional)")
parser.add_argument("-d", "--destination", default="../out", type=str, help="Destination base path (optional)")
parser.add_argument("-c","--criteria", type=str, default="date", help="Classification criteria. The criterion can ve piped with |. Valid criteria: <date, type, path=key_word> (optional)")
parser.add_argument("-dl","--debuglevel", type=str, default="false", help="Debug level (optional)")

# Parse arguments
args = parser.parse_args()
base_folder = args.origin
destiny_folder = args.destination
criteria = args.criteria
__init_log(base_folder, args.debuglevel)
all_files = []
for path, folders, files in os.walk(base_folder):
    for name in files:
        if ".log" not in path:
            all_files.append(file.File(name, path))
destinationCriteria = criterion.CriterionFactory.get_criteria(criteria)
print(destinationCriteria)
for fileToClassify in all_files:
    destination = destiny_folder
    for criterion in destinationCriteria:
        destination = criterion.calculate_destination(fileToClassify, destination)

    print(f"Classification: File {fileToClassify.file_name()} - Destination {destination}")
