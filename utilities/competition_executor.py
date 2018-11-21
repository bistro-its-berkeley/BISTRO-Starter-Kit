import multiprocessing
from os import path

import docker
import pandas as pd

from functools import wraps


def _get_submission_timestamp_from_log(log):
    """Parses the logs of a container to find the precise time at which the output directory was
    created."""

    lines = log.decode('utf-8').split('\n')
    for line in lines:
        if 'Beam output directory is' in line:
            words = line.split(' ')
            output_dir = words[-1]
            timestamp = output_dir.split('/')[-1].split('__')[-1]
            return timestamp
    else:
        raise ValueError("No timestamp found for submission. Error running submission!")


class Submission(object):
    """Points to the simulation as the submission is executing and thus permits the querying of the simulation state
    as it executes within the container.

    Additionally this class summarizes the submission results of a specific simulation run.

    Parameters
    ----------
        submission_id : string
            Identifier of the simulation instance (will become the container name)
        scenario_name : string
            Which of the available scenarios will be run in the container (i.e SiouxFalls)
        input_directory : string
            Location of the input files for the simulation
        output_root :string:
            Location of the output directory for the simulation
        sample_size : string:
            Available samples size (scenario dependent, see documentation, i.e 1k)
        num_iterations: float:
            Number of iterations to run BEAM simulation engine

    """

    def __init__(self,
                 submission_id,
                 scenario_name,
                 input_directory,
                 output_root,
                 sample_size,
                 num_iterations,
                 container):
        # Delay initialization in order to get timestamp
        time.sleep(10)
        log = container.logs()
        self._submission_id = submission_id
        self._timestamp = _get_submission_timestamp_from_log(log)
        self.n_iters = num_iterations
        self.sample_size = sample_size
        self.scenario_name = scenario_name
        self.input_directory = input_directory
        self._container = container

        self.output_directory = self._format_out_dir(output_root)

    def logs(self):
        return self._container.logs()

    def stop(self):
        self._container.stop()

    def remove(self):
        self._container.remove()

    def status(self):
        self._container.update()
        return self._container.status

    def reload(self):
        self._container.reload()

    def _format_out_dir(self, output_root):
        """Creates the path to the output directory of the simulation.
        """
        return path.join(output_root, self.scenario_name,
                         "{}-{}__{}".format(self.scenario_name, self.sample_size, self._timestamp))

    def score(self):
        """ Extracts the submission scores from the simulation outputs and creates a pandas DataFrame from it.

        Parses the submissionScores.txt output file containing the raw and weighted subscores,
        as well as the general score of the simulation run. Stores the result in a pandas DataFrame

        Returns
        -------
        all_scores : pd.DataFrame
            summary of the raw and weighted subscores, as well as the total score of the simulation run.

        """

        with open(path.join(self.output_directory, "competition", "submissionScores.txt"), "r") as f:
            lines = f.readlines()

            data = []
            for idx, l in enumerate(lines):
                if idx == 0:
                    columns = l.rstrip('\n').split("|")
                    columns = [i.strip() for i in columns]
                    continue
                elif idx == 1:
                    continue
                values = l.rstrip('\n').split("|")
                values = [i.strip() for i in values]
                values = [i if len(i) > 0 else "0" for i in values]
                data.append(values)

        df = pd.DataFrame(data, columns=columns)

        all_scores = []

        for score_type in ["Weight", "Raw Score", "Weighted Score"]:
            pivoted = pd.pivot_table(df, values=score_type, columns="Component Name", aggfunc="first").reset_index(
                drop=True)
            pivoted.columns = ["%s_%s" % (i, score_type) for i in pivoted.columns]
            all_scores.append(pivoted)
        all_scores = pd.concat(all_scores, 1).astype(float)
        return all_scores

    def summary_stats(self):
        """ Extracts the submission statistics from the simulation outputs and creates a pandas DataFrame from it.

        Reads the summaryStats.csv output file containing many of the raw output statistics of the simulation
        (see "Understanding the outputs and the scoring function" page of the Starter Kit).

        Returns
        -------
         DataFrame:
            Summary of the output stats of the submission

        """

        summary_file = path.join(self.output_directory, "summaryStats.csv")
        return pd.read_csv(summary_file)

    def is_complete(self):
        """ Checks if the submission is complete.

        Returns
        -------
        bool
            True if the simulation is complete, False otherwise.

        """

        path_submission_scores = path.join(self.output_directory, "competition", "submissionScores.txt")
        return path.exists(path_submission_scores)

    def __str__(self):
        return "Submission_id: {}\n\t Scenario name: {}\n\t # iters: {}\n\t sample size: {}".format(self._submission_id,
                                                                                                    self.scenario_name,
                                                                                                    self.n_iters,
                                                                                                    self.sample_size)


def verify_submission_id(func):
    """Checks that the container id exists in the CompetitionContainerExecutor object."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        self, submission_id = args
        if submission_id not in self.containers:
            raise ValueError("Container not executed using this interface.")
        else:
            return func(*args, **kwargs)

    return wrapper


class CompetitionContainerExecutor:
    """Utility to run (potentially many) instances of the simulation.

    Pointers to docker-py container objects executed by this utility are cached on the field
    self.containers under the name specified in the self.run(...) method. Convenience methods on this object can be
    used to simplify interaction with one or many of these containers.

    Args:
        input_root (string): a permanent input file directory, i.e., /submission-inputs (if you expect not to feed
                      this in manually; see run method below).
        output_root (string): a permanent output file directory (it's a good idea to set this,
                        else you will need to do so for every container you create)

    """

    def __init__(self, input_root=None,
                 output_root=None):
        self.input_root = input_root
        self.output_root = output_root
        self.client = docker.from_env()
        self.containers = {}

    def list_running_simulations(self):
        """Queries the run status for executed containers cached on this object in turn
        (updating their statuses as appropriate).

        Returns: a list of running containers

        """
        running = []
        for name, container in self.containers.items():
            container.reload()
            if container.status == 'running':
                running.append(name)
        return running

    @verify_submission_id
    def get_submission_scores_and_stats(self, submission_id):
        """ Returns two of the simulation outputs (as pandas DataFrames) for a specific submission ID:
        the scores and the statistics.


        Parameters
        ----------
        submission_id : str
            The unique identifier for the submission

        Returns
        -------
        Tuple(DataFrame,DataFrame)
            [0] Summary of the raw and weighted sub-scores as well as the final score of the
            submission, and;
            [1] summary of the output stats of the submission. (see "Understanding the outputs
            and the scoring function" page of the Starter Kit for the full list of stats)

        Raises
        ------
        ValueError
            The scores do not exist yet i.e the simulation is still running.

        """
        submission = self.containers[submission_id]

        if submission.is_complete():
            scores = submission.score()
            stats = submission.summary_stats()

            return scores, stats
        else:
            raise NameError("Simulation {0} is still running.".format(submission_id))

    def stop_all_simulations(self, remove=True):
        """Stops all simulations. Containers are removed (both from this object and the docker daemon by default).

        Removal frees the names that were used to execute containers previously, so it's generally a good idea to
        remove if you plan to reuse names.

        Parameters
        ----------
        remove : bool
            Whether to remove the containers cached on this object.

        """
        for container in self.containers.values():
            container.stop()
            if remove:
                container.remove()
        self.containers.clear()

    @verify_submission_id
    def output_simulation_logs(self, sim_name, filename=None):
        """Prints a specified simulation log or writes to file if filename is provided.


        Parameters
        ----------
        sim_name : str
            Name of the the requested simulation
        filename : str, optional
            A path to which to save the logfile

        Returns
        -------
        str
            Log output as bytestring

        """

        logs = self.containers[sim_name].logs().decode('utf-8')
        if filename is None:
            print(logs)
        else:
            with open(filename, 'w') as f:
                f.write(logs)
        return logs

    @verify_submission_id
    def check_if_submission_complete(self, sim_name):
        """ Checks if a given submission is complete.

        Parameters
        ----------
        sim_name : (string)
            identifier of the simulation instance

        Returns
        -------
        bool :
            True if the given simulation is complete, False otherwise


        """
        return self.containers[sim_name].is_complete()


    def run_simulation(self,
                       submission_id,
                       submission_output_root=None,
                       submission_input_root=None,
                       scenario_name='siouxfalls',
                       sample_size='1k',
                       num_iterations=10,
                       num_cpus=multiprocessing.cpu_count() - 1,
                       mem_limit="4g"):
        """Creates a new container running an Uber Prize competition simulation on a specified set of inputs.

        Containers are run in a background process, so several containers can be run in parallel
        (though this is a loose and uncoordinated parallelism... future updates may scale execution out over
        compute nodes).

        This utility adds the container to the list of containers managed by this object.


        Parameters
        ----------
        submission_id : str
            Identifier of the simulation instance (will become the container name)
        submission_output_root : str
            The (absolute) path to locate simulation outputs
        submission_input_root : str
            The (absolute) path where simulation inputs are located
        scenario_name : str
        sample_size : str
             The available sample size (scenario dependent, see documentation).
        num_iterations : int
            Number of iterations for which to run the BEAM simulation engine.
        num_cpus : str
            Number of cpus to allocate to container (0.01 - Runtime.getRuntime().availableProcessors())
        mem_limit : int

        """
        output_root = self.output_root
        input_root = self.input_root

        if output_root is None:
            if submission_output_root is not None:
                output_root = submission_output_root
            else:
                raise ValueError(
                    "No output location specified. One must be provided by default "
                    "on object instantiation or supplied to this method as an argument.")

        if input_root is None:
            if submission_input_root is not None:
                input_root = submission_input_root
            else:
                raise ValueError(
                    "No input location specified. One must be provided by default "
                    "on object instantiation or supplied to this method as an argument.")

        container = self.client.containers.run('beammodel/beam-competition:0.0.1-SNAPSHOT',
                                               name=submission_id,
                                               command=r"--scenario {0} --sample-size {1} --iters {2}".format(
                                                   scenario_name, sample_size, num_iterations),
                                               detach=True,
                                               volumes=
                                               {output_root: {"bind": "/output", "mode": "rw"},
                                                input_root: {"bind": "/submission-inputs",
                                                             "mode": "ro"}})

        self.containers[submission_id] = Submission(submission_id,
                                                    scenario_name,
                                                    input_root,
                                                    output_root,
                                                    sample_size,
                                                    num_iterations,
                                                    container)


if __name__ == '__main__':
    # Example to demonstrate/test usage. Not a production script. For more detailed explanations, read the API-tutorial
    # Jupyter Notebook in the Starter-Kit repository.

    import time
    import sys

    CONTAINER_ID = 'uber1'

    # Must use absolute paths here
    ex = CompetitionContainerExecutor(input_root=sys.argv[1],
                                      output_root=sys.argv[2])

    print("Running Container")

    try:
        uber = ex.client.containers.get(CONTAINER_ID)
        uber.stop()
        uber.remove()
        print("Found container from previous run, removing and creating new sim container...")
    except docker.errors.NotFound:
        print("Creating new simulation container...")

    ex.run_simulation(CONTAINER_ID, num_iterations=1, num_cpus=10)

    # Let it roll for a bit (hopefully at least one or two iterations!)
    if len(sys.argv) < 4:
        print("Running simulation for 40 seconds...")
        time.sleep(40)
    else:
        run_time = int(sys.argv[3])
        print("Running simulation for {} seconds...".format(str(run_time)))
        time.sleep(int(run_time))

    ex.output_simulation_logs(CONTAINER_ID)

    # Good idea to call this at the end of any run to clean up containers (particularly if you want to reuse names)!
    ex.stop_all_simulations()
