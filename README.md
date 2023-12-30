# A mathematical model of the hidden feedback loop effects in machine learning systems

Widespread deployment of societal-scale machine learning systems necessitates a thorough understanding of the resulting long-term effects these systems have on their environment, including trustworthiness, presence of bias, and violation of safety requirements.
We introduce a repeated learning process to jointly describe feedback loops, error amplification, induced concept drift, and other related phenomena. he process comprises the entire cycle of obtaining the data, training the predictive model, and delivering predictions to end-users within a single mathematical model.
A distinctive feature of such repeated learning setting is that the state of the environment becomes causally dependent on the learner itself over time, thus violating the usual assumptions about the data distribution.
We conduct a series of computational experiments using an exemplary supervised learning problem on a synthetic data set. The results of the experiments correspond to the theoretical predictions derived from the model. 

## Problem statement

We running the experiments as show at the figures below 

<img src=".figures/Hidden_loop.png" alt="Sliding window setup" width="300"/>
<img src=".figures/Hidden_sample.png" alt="Sample update setup" width="350"/>

## How to run with mldev 

Running the same experiment with [mldev](https://gitlab.com/mlrep/mldev) involves the following steps.

Install the ``mldev`` by executing

```bash
$ git clone https://github.com/prog-autom/hidden-demo.git
$ curl https://gitlab.com/mlrep/mldev/-/raw/develop/install_mldev.sh -o install_mldev.sh
$ chmod +x install_mldev.sh
$ yes n | install_mldev.sh
``` 
Then initialize the experiment, this will install required dependencies

```bash
$ mldev --config ./hidden-demo/.mldev/config.yaml init --no-commit -r ./hidden-demo
```

Detailed description of the experiment can be found in ``./experiment.yml``. See docs for ``mldev`` for details.

## Complete experiment with mldev

There is a script ``./run_experiment.sh`` that runs the experiment
for a grid of parameters, usage from 0.1 to 0.9, adherenec from 0.1 to 0.9 
and step size 10 or 20.

The script relies on mldev to run trials for a fixed set of parameters.

## Source code

Source code can be found in ``./src`` folder. The [main.py](./src/main.py) file contains glue code to run experiments.
The [experiment.py](./src/experiment.py) contains experiment implementation and utility procedures.
