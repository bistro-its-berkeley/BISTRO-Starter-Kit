import os
import sys


def rsync_results(hostname, host_ip, output_folder_name, dest_folder):
    return os.system('rsync -avz -e "ssh -i ~/.ssh/beam_competitions_key.pem" ubuntu@{host_ip}:/home/ubuntu//Uber-Prize-Starter-Kit/%s/ {dest_folder}/{output_folder_name}/{hostname} --exclude="*/ITERS/" --exclude="*/output*" --exclude="*/competition/viz/"'.format(hostname=hostname,host_ip=host_ip, output_folder_name=output_folder_name, dest_folder=dest_folder))


if __name__ == "__main__":
    # Args:
    #   - 1: Path of the output folder name to copy
    #   - 2: Destination folder to copy on local machine
    output_folder_name = sys.argv[1]
    dest_folder = sys.argv[2]

    hosts = ["52.13.145.44", "52.89.179.9", "54.191.161.231", "54.218.172.167", "54.218.29.151"]
    host_names = ["host{}".format(str(i+1)) for i in range(len(hosts)-1)]
    host_names.append('debug')

    res=[rsync_results(hostname, host_ip, output_folder_name, dest_folder) for hostname, host_ip in zip(host_names, hosts)]