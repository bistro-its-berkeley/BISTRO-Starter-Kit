import docker


class CompetitionContainerExecutor:
    """Utility to run (potentially many) instances of the simulation.

    :param input_loc: a permanent input file directory (if you expect not to feed
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
        # TODO: Check if actually running somehow
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
        for container in self.containers.values():
            container.stop()
            if remove:
                container.remove()

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

        Adds the container to the list of containers managed by this object.

        :param sim_name: name of the simulation instance (will become the container name)
        :param sim_output_loc: the path to locate simulation outputs
        :param sim_input_loc: where simulation inputs will be located
        :param scenario: which of the available scenarios will be run in the container?
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
    ex = CompetitionDockerExecutor(input_loc=sys.argv[1],
                                   output_loc=sys.argv[2])

    ex.run_simulation('uber')

    # Let it roll for a bit (hopefully at least one or two iterations!)
    time.sleep(40)

    ex.output_simulation_logs('uber')

    # Good idea to call this at the end of any run to clean up containers (particularly if you want to reuse names)!
    ex.stop_all_simulations()
