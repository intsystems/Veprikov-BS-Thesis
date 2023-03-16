trap 'exit' SIGINT SIGTERM SIGHUP SIGQUIT

for step in 10
do
    for usage in 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.95
    do
        for adherence in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
        do
          export step &&
          export usage &&
          export adherence &&
          mldev run -f ./experiment.yml --no-commit run_experiment
        done
    done
done