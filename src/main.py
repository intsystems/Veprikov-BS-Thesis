import argparse
import json
import os
from tqdm import tqdm

from experiment import *

parser = None
folder = None
run_times = None
random_seed = None
data_type = None
noise = None


def create_model(model_params):
    if 'gbr_model' in model_params:
        model_name = 'gbr'
        model = lambda : gbr_model(**model_params['gbr_model'])
        print(f"Using model: {model_name}")
        yield model, model_name
    if 'ridge_model' in model_params:
        model_name = 'ridge'
        model = lambda : ridge_model(**model_params['ridge_model'])
        print(f"Using model: {model_name}")
        yield model, model_name


def single_model(model_params, params):
    print(f"Running single-model experiment with data type %s" % data_type)
    if data_type == 'boston':
        X, y, _ = get_boston_dataset()
    elif data_type == 'synthetic':
        X, y = get_synthetic_dataset()
    else:
        raise ValueError('Wrong data type!' + data_type)
    for model, model_name in create_model(model_params):
        for trial in tqdm(range(0, run_times)):
            os.makedirs(f"{folder}/{trial}", exist_ok=True)
            single_model_experiment(X, y, model, model_name=f"{folder}/{trial}/{model_name}", **params)


def hidden_loop(model_params, params, noise):
    print(f"Running hidden-loop experiment with data type %s" % data_type)
    print(f"adherence = {params['adherence']}, usage = {params['usage']}, noise = {noise}")
    if data_type == 'boston':
        X, y, _ = get_boston_dataset()
    elif data_type == 'synthetic':
        X, y = get_synthetic_dataset(noise)
    else:
        raise ValueError('Wrong data type!' + data_type)

    for model, model_name in create_model(model_params):
        results = MultipleResults(model_name, **HiddenLoopExperiment.default_state)

        for trial in tqdm(range(0, run_times)):
            hle = HiddenLoopExperiment(X, y, model, model_name, path=folder, step_hist=step_hist)
            prepare_params = {k: params[k] for k in params.keys() & {'train_size'}}
            hle.prepare_data(**prepare_params)

            loop_params = {k: params[k] for k in params.keys() & {'adherence', 'usage', 'step'}}
            hle.hidden_loop_experiment(**loop_params)

            results.add_results(**vars(hle))

        results.plot_multiple_results(folder)

def hidden_sample(model_params, params, noise):
    print(f"Running hidden-sample experiment with data type %s" % data_type)
    print(f"adherence = {params['adherence']}, usage = {params['usage']}, noise = {noise}")
    if data_type == 'boston':
        X, y, _ = get_boston_dataset()
    elif data_type == 'synthetic':
        X, y = get_synthetic_dataset(noise)
    else:
        raise ValueError('Wrong data type!' + data_type)

    for model, model_name in create_model(model_params):
        #results = MultipleResults(model_name, **HiddenLoopExperiment.default_state)

        for trial in tqdm(range(0, run_times)):
            hle = HiddenLoopExperiment(X, y, model, model_name, path=folder, step_hist=step_hist, N=N)
            prepare_params = {k: params[k] for k in params.keys() & {'train_size'}}
            hle.prepare_data(**prepare_params)

            loop_params = {k: params[k] for k in params.keys() & {'adherence', 'usage', 'step'}}
            hle.hidden_sampling_experiment(**loop_params)

            #results.add_results(**vars(hle))

        #results.plot_multiple_results(folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", type=str,
                        help="Kind of experiment: single-model, hidden-loop or hidden-sample")
    parser.add_argument("--params", type=str,
                        help="A json string with experiment parameters")
    parser.add_argument("--model_params", type=str,
                        help="A json string with model name and parameters")
    parser.add_argument("--folder", type=str,
                        help="Save results to this folder", default="./results")
    parser.add_argument("--random_seed", type=int,
                        help="Use the provided value to init the random state", default=42)
    parser.add_argument("--run_times", type=int,
                        help="How many time to repeat the trial", default=1)
    parser.add_argument("--data", type=str, help="What data to use", default='synthetic')
    parser.add_argument("--step_hist", type=int,
                        help="After how many steps make a histogram", default=100)
    parser.add_argument("--noise", type=float,
                        help="noise in original data", default=1.0)
    parser.add_argument("--N", type=int,
                        help="how many times do sampling experiment", default=10**6)
    args = parser.parse_args()
    model_str = args.model_params
    params_str = args.params
    kind = args.kind
    folder = args.folder
    random_seed = args.random_seed
    run_times = args.run_times
    data_type = args.data
    step_hist = args.step_hist
    noise = args.noise
    N = args.N
    os.makedirs(folder, exist_ok=True)

    model_dict = json.loads(model_str)
    params_dict = json.loads(params_str)

    init_random_state(random_seed)

    if kind == "single-model":
        single_model(model_dict, params_dict)
    elif kind == "hidden-loop":
        os.makedirs(folder+"/hists", exist_ok=True)
        os.makedirs(folder+"/deviations", exist_ok=True)
        hidden_loop(model_dict, params_dict, noise)
    elif kind == "hidden-sample":
        os.makedirs(folder + "/hists", exist_ok=True)
        os.makedirs(folder + "/deviations", exist_ok=True)
        hidden_sample(model_dict, params_dict, noise)
    else:
        parser.error("Unknown experiment kind: " + kind)