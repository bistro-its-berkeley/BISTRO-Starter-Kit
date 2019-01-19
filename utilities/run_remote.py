from fabric import ThreadingGroup, Connection
from invoke.exceptions import UnexpectedExit


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

    # globals
    # TODO[vgv]: read these from config file

    hosts = ["52.13.145.44", "52.89.179.9", "54.191.161.231", "54.218.172.167", "54.218.29.151"]
    key_file_loc = sys.argv[1]
    host_num = int(sys.argv[2]) - 1

    host1_conn = connect_single(hosts[0], key_file_loc)
    host2_conn = connect_single(hosts[1], key_file_loc)
    host3_conn = connect_single(hosts[2], key_file_loc)
    host4_conn = connect_single(hosts[3], key_file_loc)
    debug_conn = connect_single(hosts[4], key_file_loc)

    connections = [host1_conn, host2_conn, host3_conn, host4_conn, debug_conn]
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

    # Activate venv and run exploratory analysis on target server
    run('cd /home/ubuntu/venv/beam_competitions/bin && \
         source activate && \
         cd /home/ubuntu/Uber-Prize-Starter-Kit && \
         sudo rm -rf search-* && \
         cd /home/ubuntu/Uber-Prize-Starter-Kit/utilities && \
         python exploratory_analysis.py {}'.format(str(host_num - 1)), connection)
