# QOSsimulation

## Installation
run the command `pip install -r /path/to/requirements.txt`
to install the required python packages for this simulator.

Check that the python environment uses the 'src' folder as working directory
(This should be the case when using VS Code)

## Setting up the simulation
To run a single simulation use 'main.py' as the start-up file.

To run batch simulations with variable Latency Spike Configurations use 'repeatMain.py' as the start-up file.

To run batch simulation with variable MBP Counts use 'userMain.py' as the start-up file.

## Configuring the simulation
Most configurations can be set in the 'SimConfig.py' file.
Currently only two resource allocation approaches are supported, which can be set using the SIMULATE_MODE field in 'SimConfig.py:
- PRIORITY_FIRST (Baseline)
- SCHEDULING (Delay-Tolerant Scheduling)

To adjust MBP Counts set change the 'COMPANIES' field in 'SimConfig.py'

The standard QoS requirements for MBPs can is set in 'ServiceConfig.py'

The remaining Configurations show the default configurations used throughout all simulations scenarios.

The batch simulations (in 'repeatMain' and 'userMain') contain the code to adjust Configurations dynamically for batch jobs.

Warning!: Running batch simulations takes a lot of time and generates a lot of data
From experience running the Baseline 1600 times takes several hours, the Delay-tolerant scheduling takes more 40+ hours for 1600 simulations.
Several GBs of data a generated in the process.
