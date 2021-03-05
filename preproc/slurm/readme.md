# TMO preprocessing
Contributors: Elio Champenois, Taran Driver, Matt Ware

## Required libraries
You'll need to source the newest psana2 libraries. Run `source /cds/sw/ds/ana/conda2/manage/bin/psconda.sh` on the terminal.

## Mandatory updates
* Batch submission is currently using the old LSF (bsub) interface. This has now been taken down and will no longer work.

## Suggested updates
* Experiment is hard coded into `preproc.py`. This should be handed to the script from the command line.
* Output folder should also be a command line prompt.
* Updated keyword args in the readme

## Preprocessing flow
1) Automated job submission

	* Controlled by `autopreproc.py`, which calls `slurmJob.sh`.
	* Run via `python autopreproc.py --keyword-args=...`

2) Single job submission
	* Controlled by `preproc.py`

## File descriptions

### autopreproc.py
Automates the batch submission, calls slurmJob.sh

### slurmJob.sh
Submits SLURM jobs. Try running first with psdebugq.

### preproc.py
Run a single or multi-cored analysis of the data.
Run as `mpirun python -u preproc.py --keyword-args=...`

### input.py
Specifies the command line input structure that is read in by preproc.py

Try running,
```bash
python input.py --nodes=1 --directory=.
```

## Batch analysis info from LCLS
Info on the available batch system and how to submit batch jobs can be found on the [LCLS confluence page](https://confluence.slac.stanford.edu/display/PCDS/Batch+System+Analysis+Jobs?src=sidebar).

