trap 'exit' SIGINT SIGTERM SIGHUP SIGQUIT

for step in 10 20
do
    for usage in 0.1 0.3 0.5 0.9
    do
        for adherence in 0.1 0.3 0.5 0.9
        do
          export step &&
          export usage &&
          export adherence &&
          mldev run -f ./experiment.yml --no-commit run_experiment
        done
    done
done