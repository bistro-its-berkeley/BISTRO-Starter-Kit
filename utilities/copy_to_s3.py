from os import path
import sys
import pandas as pd
from glob import glob
from shutil import rmtree
import os


def find_output_folder_name(path_submission, iteration=4):
    for i in range(iteration):
        path_submission = path.dirname(path_submission)
    return path_submission


if __name__ == "__main__":
    # Args:
    #   - 1: Name of the exploration to copy from

    output_folder_name = sys.argv[1]

    # Read the hosts from config file
    config = pd.read_table("~/.ssh/config")
    config = config["Host host1"].values
    hosts = [i.split(" ")[1] for i in config if "HostName" in i]

    host_names = ["host{}".format(str(i+1)) for i in range(len(hosts)-1)]
    host_names.append('debug')

    # Check if the output folder contains a submissionScores.csv file, i.e. of the simulation worked
    submissions = glob(r"Uber-Prize-Starter-Kit/search-output-{output_folder_name}/*/sioux_faux/sioux_faux-15k__*/"
                       r"competition/submissionScores.csv".format(output_folder_name=output_folder_name))
    right_output_folders = [find_output_folder_name(submissions[i], 4) for i in range(len(submissions))]
    all_output_folders = glob(r"Uber-Prize-Starter-Kit/search-output-{output_folder_name}/output_C*_RS*".format(
        output_folder_name=output_folder_name))

    for folder in all_output_folders:
        if folder not in right_output_folders:
            rmtree(folder)

    # Launching s3 sync
    os.chdir(f"../search-output-{output_folder_name}")
    os.system(f"aws s3 sync . s3://uber-prize-testing-output/search-output-{output_folder_name}")