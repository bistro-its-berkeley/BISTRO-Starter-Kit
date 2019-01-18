key_file_loc = r"/Users/vgolfi/.ssh/beam_competitions_key.pem"
username = "ubuntu"
from fabric import ThreadingGroup

hosts = ["52.13.145.44", "52.89.179.9", "54.191.161.231", "54.218.172.167", "54.218.29.151"]

# The commands set the correct working directory (needs to be run in utilities folder
# We also need to have activated the appropriate environment
commands = ["cd /home/ubuntu/Uber-Prize-Starter-Kit/utilities; python exploratory_analysis.py %s"%i for i in range(5)]
result = []

for command, host in zip(commands, hosts):
    # Activating the correct environment
    ThreadingGroup(*[host],user=username,
                   connect_kwargs={"key_filename":[key_file_loc]}).run("source activate /home/ubuntu/venv/beam_competitions/bin/activate")

    # Running the exploratory analysis command.
    ThreadingGroup(*[host], user=username,connect_kwargs={"key_filename":[key_file_loc]}).run(command)