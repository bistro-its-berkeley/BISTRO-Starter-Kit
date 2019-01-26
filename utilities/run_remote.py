from fabric import ThreadingGroup, Connection
from invoke.exceptions import UnexpectedExit
import pandas as pd


def connect_parallel(hosts, key_file_loc):
    return ThreadingGroup(*hosts, user='ubuntu', connect_kwargs={"key_filename": [key_file_loc]})


def connect_single(host, key_file_loc):
    return Connection(host, user='ubuntu', connect_kwargs={"key_filename": [key_file_loc]})


def run(cmd, connection):
    return connection.run(cmd)


def run_n(cmd, connections):
    return [run(cmd, connection) for connection in connections]


if __name__ == '__main__':
    import sys

    # Args:
    #   - 1: path to key file
    #   - 2: number of host (1-5) below
    #   - 3: Name of output folder

    # globals

    # Read the hosts from config file
    config = pd.read_table("~/.ssh/config")
    config = config["Host host1"].values
    hosts = [i.split(" ")[1] for i in config if "HostName" in i]

    key_file_loc = sys.argv[1]
    host_num = int(sys.argv[2]) - 1
    output_folder = sys.argv[3]
    input_mode = sys.argv[4]

    connections = [connect_single(hosts[i], key_file_loc) for i in range(len(hosts))]
    connection = connections[host_num]

    ###############################
    # Begin remote commands here:
    ###############################

    # Pull latest docker image
    run('docker pull beammodel/beam-competition:0.0.1-SNAPSHOT', connection)

    # Update git for starter kit (optionally comment out if run since previous update, but error catching will
    # save us in this case)
    try:
        run('cd /home/ubuntu/Uber-Prize-Starter-Kit/utilities &&  \
            git pull origin vgv/#55-adapt_ramdom_search', connection)
    except UnexpectedExit:
        print("Already pulled in latest!")

    # TODO[vgv]: Check if venv exists and if not, create!
    # Kill all containers before running simulation
    # run('sudo pkill java', connection)
    try:
        run('sudo docker stop $(docker ps -aq) -t 0', connection)
    except Exception as e:
        print("No Docker containers to delete.")
        pass

    # Commands to delete all search folders
    # cd / home / ubuntu / Uber - Prize - Starter - Kit & & \
    # sudo rm - rf search - * & & \

            # Activate venv and run exploratory analysis on target server
    run('cd /home/ubuntu/venv/beam_competitions/bin && \
         source activate && \
         cd /home/ubuntu/Uber-Prize-Starter-Kit/utilities && \
         python3 exploratory_analysis.py {0} {1} {2}'.format(str(host_num), output_folder, input_mode), connection)
