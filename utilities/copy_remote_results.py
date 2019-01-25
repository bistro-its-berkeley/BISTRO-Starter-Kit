import os
import sys
from os import path
import pandas as pd


def rsync_results(hostname, host_ip, output_folder_name, dest_folder):
    return os.system('rsync -avz -e "ssh -i ~/.ssh/beam_competitions_key.pem" ubuntu@{host_ip}:/home/ubuntu/'
                     'Uber-Prize-Starter-Kit/search-output-{output_folder_name}/ {dest_folder}/'
                     '{output_folder_name}/{hostname} --exclude="*/ITERS/" --exclude="*/output*" --exclude="*'
                     '/competition/viz/"'.format(hostname=hostname,host_ip=host_ip,
                                                 output_folder_name=output_folder_name,
                                                 dest_folder=dest_folder))


def find_output_folder_name(path_submission, iteration=4):
    for i in range(iteration):
        path_submission = path.dirname(path_submission)
    return path_submission


if __name__ == "__main__":
    # Args:
    #   - 1: Name of the exploration to copy from
    #   - 2: Path of the destination folder to copy on local machine (a folder named after the exploration will be
    #        created in it)

    output_folder_name = sys.argv[1]
    dest_folder = sys.argv[2]

    # Read the hosts from config file
    config = pd.read_table("~/.ssh/config")
    config = config["Host host1"].values
    hosts = [i.split(" ")[1] for i in config if "HostName" in i]

    host_names = ["host{}".format(str(i+1)) for i in range(len(hosts)-1)]
    host_names.append('debug')

    _ = [os.makedirs(path.join(dest_folder, output_folder_name, h)) for h in host_names
         if not os.path.exists(path.join(dest_folder, output_folder_name, h))]
    res = [rsync_results(hostname, host_ip, output_folder_name, dest_folder) for hostname, host_ip in zip(host_names, hosts)]