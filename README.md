# MCRF — Professional Scaffold (Part 1)


Quick start:


1. copy files into a folder `mcrf/` preserving structure
2. create virtualenv and install requirements: `pip install -r requirements.txt`
3. populate `data/universe_*.csv` or use provided samples
4. configure `config.py` (Discord webhook, environment)
5. test run: `python run_scanner.py` (manual run)
6. enable scheduler: set `ENABLE_SCHEDULER=true` in environment and run `python scheduler/apscheduler_job.py`


Notes:
- This scaffold separates concerns: core fetch/scoring, notify, scheduler.
- Part 2 will add batch fetcher, caching, rate-limit handling and more indicators.