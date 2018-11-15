import docker


class CompetitionContainerExecutor:
    """Utility to run (potentially many) instances of the simulation.

    Pointers to docker-py container objects executed by this utility are cached on the field
    self.containers under the name specified in the self.run(...) method. Convenience methods on this object can be
    used to simplify interaction with one or many of these containers.

    :param input_loc: a permanent input file directory, i.e., /submission-inputs (if you expect not to feed
                      this in manually; see run method below).
    :param output_loc: a permanent output file directory (it's a good idea to set this,
                        else you will need to do so for every container you create).
    """
    def __init__(self, input_loc=None,
                 output_loc=None):
        self.input_loc = input_loc
        self.output_loc = output_loc
        self.client = docker.from_env()
        self.containers = {}

    def _verify_sim_name(self, sim_name):
        # TODO: implement as decorator: @verify_sim_name
        if sim_name not in self.containers:
            raise ValueError("Container not executed using this interface.")

    def list_running_simulations(self):
        """Queries the run status for executed containers cached on this object in turn
        (updating their status as appropriate).

        :return: a list of running containers
        """
        running = []
        for name, container in self.containers.items():
            container.reload()
            if container.status == 'running':
                running.append(name)
        return running

    def get_submission_stats(self, sim_name):
        # TODO: Parse and return the output stats for this simulation from the <output_dir>/siouxfalls-${sz}__<timestamp>/competition/submissionScore.txt file.
        # Output Format should be pandas DataFrame
        return NotImplementedError()


    def stop_all_simulations(self, remove=True):
        """Stop and all simulations. Containers are removed (both from this object and the docker daemon by default).

        Removal frees the names that were used to execute containers previously, so it's generally a good idea to
        remove if you will be planning reusing names.

        :param remove: whether to remove the containers cached on this object.
        """
        for container in self.containers.values():
            container.stop()
            if remove:
                container.remove()
        self.containers.clear()

    def output_simulation_logs(self, sim_name, filename=None):
        """Prints a specified simulation log or writes to file if filename is provided

        :param sim_name the requested simulation
        :param filename (optional) a path to which to save the logfile
        """
        self._verify_sim_name(sim_name)
        logs = self.containers[sim_name].logs().decode('utf-8')
        if filename is None:
            print(logs)
        else:
            with open(filename, 'w') as f:
                f.write(logs)


    def run_simulation(self,
                       sim_name,
                       sim_output_loc=None,
                       sim_input_loc=None,
                       scenario='siouxfalls',
                       sample_size='1k',
                       num_iterations=10):
        """Creates a new container running a Uber Prize competition simulation on a specified set of inputs.

        Containers are run in a background process, so several containers can be run in parallel
        (though this is a loose and uncoordinated parallelism... future updates may scale execution out over
        compute nodes).

        This utility adds the container to the list of containers managed by this object.

        :param sim_name: name of the simulation instance (will become the container name)
        :param sim_output_loc: the (absolute) path to locate simulation outputs
        :param sim_input_loc: (absolute) path where simulation inputs are located
        :param scenario: which of the available scenarios will be run in the container
        :param sample_size: available samples size (scenario dependent, see documentation).
        :param num_iterations: number of iterations to run BEAM simulation engine.
        """
        output_loc = self.output_loc
        input_loc = self.input_loc
        if output_loc is None:
            if sim_output_loc is not None:
                output_loc = sim_output_loc
            else:
                raise ValueError(
                    "No output location specified. One must be provided by default on object instantiation or supplied to this method as an argument.")

        if input_loc is None:
            if sim_input_loc is not None:
                input_loc = sim_input_loc
            else:
                raise ValueError(
                    "No input location specified. One must be provided by default on object instantiation or supplied to this method as an argument.")

        self.containers[sim_name] = self.client.containers.run('beammodel/beam-competition:0.0.1-SNAPSHOT',
                                                               name=sim_name,
                                                               command=r"--scenario {0} --sample-size {1} --iters {2}".format(
                                                                   scenario, sample_size, num_iterations),
                                                               detach=True,
                                                               volumes=
                                                               {output_loc: {"bind": "/output", "mode": "rw"},
                                                                input_loc: {"bind": "/submission-inputs",
                                                                            "mode": "ro"}})


if __name__ == '__main__':
    # Example to demonstrate/test usage. Not a production script.
    import time
    import sys

    # Must use absolute paths here
    ex = CompetitionContainerExecutor(input_loc=sys.argv[1],
                                   output_loc=sys.argv[2])

    print("Running Container")

    try:
        uber = ex.client.containers.get('uber')
        uber.stop()
        uber.remove()
        print("Found container from previous run, removing and creating new sim container...")
    except docker.errors.NotFound:
        print("Creating new simulation container...")


    ex.run_simulation('uber')

    # Let it roll for a bit (hopefully at least one or two iterations!)
    if len(sys.argv) < 4:
        print("Running simulation for 40 seconds...")
        time.sleep(40)
    else:
        run_time = int(sys.argv[3])
        print("Running simulation for {} seconds...".format(str(run_time)))
        time.sleep(int(run_time))

    ex.output_simulation_logs('uber')

    # Good idea to call this at the end of any run to clean up containers (particularly if you want to reuse names)!
    ex.stop_all_simulations()
