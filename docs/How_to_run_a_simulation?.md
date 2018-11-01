# How to run a simulation?

## Installing BEAM

Clone the following GitHub repository in your GitHub Desktop:
https://github.com/sfwatergit/BeamCompetitions

After you unzip the archive, you will see a directory that looks like this when partially expanded:

![Competition Repository](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/CompetitionRepository.png "Competition Repository")

***Figure 1: Competition Repository***

## Running a simulation

1. Open your Terminal.

2. Make sure you are located in the Competition GitHub repository by computing:

*cd* + the *absolute path of the competition repository* in the command line.

3. Download Gradle by running the following command: 

*./gradlew :run /PappArgs="['--config','fixed-inputs/siouxfalls/siouxfalls-1k.conf]"*

4. Launch a simulation by running the following command:

./gradlew run --args='--config fixed-data/siouxfalls/siouxfalls-1k.conf'

A progress bar is appearing in the terminal: Congratulations, you are running the simulation with BEAM! 




