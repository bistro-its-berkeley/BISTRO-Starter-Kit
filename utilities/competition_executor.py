import docker

class CompetitionDockerExecutor:
    def __init__(self, input_loc=None,
                 output_loc=None):
        self.input_loc = input_loc
        self.output_loc = output_loc
        self.client = docker.from_env()
        self.containers = {}

    def _verify_sim_name(self, sim_name):
        # TODO: implement as decorator: @verify_sim_name
        if sim_name not in self.containers:
            print("Container not executed using this interface.")

    def list_running_simulations(self):
        # TODO: Check if actually running somehow
        print([k for k in self.containers.keys()])

    def stop_all_simulations(self):
        [sim.stop() for sim in self.containers.values()]

    def output_simulation_logs(self, sim_name, filename=None):
        """Prints a specified simulation log or writes to file if filename is provided

        @param sim_name the requested simulation
        @param filename (optional) a path to which to save the logfile
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
        if self.output_loc is None:
            if sim_output_loc is not None:
                output_loc = sim_output_loc
            else:
                raise ValueError(
                    "No output location specified. One must be provided by default on object instantiation or supplied to this method as an argument.")

        if self.input_loc is None:
            if sim_input_loc is not None:
                input_loc = sim_input_loc
            else:
                raise ValueError(
                    "No input location specified. One must be provided by default on object instantiation or supplied to this method as an argument.")

        self.containers[sim_name] = self.client.containers.run('beammodel/beam-competition:0.0.1-SNAPSHOT',
                                                               command=r"--scenario {0} --sample-size {1} --iters {2}".format(
                                                                   scenario, sample_size, num_iterations),
                                                               detach=True,
                                                               volumes=
                                                               {output_loc: {"bind": "/output", "mode": "rw"},
                                                                input_loc: {"bind": "/submission-inputs",
                                                                            "mode": "ro"}})
