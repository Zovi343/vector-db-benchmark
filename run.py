import fnmatch
import traceback
from typing import List
from benchmark import DATASETS_DIR, KUBE_DIR, copy_directory
from engine.base_client.client import RESULTS_DIR
from datetime import datetime
import stopit
import typer

from benchmark.config_read import read_dataset_config, read_engine_configs
from benchmark.dataset import Dataset
from engine.base_client import IncompatibilityError
from engine.clients.client_factory import ClientFactory

app = typer.Typer()


@app.command()
def run(
    engines: List[str] = typer.Option(["*"]),
    datasets: List[str] = typer.Option(["*"]),
    host: str = "localhost",
    skip_upload: bool = False,
    skip_search: bool = False,
    skip_if_exists: bool = True,
    exit_on_error: bool = True,
    timeout: float = 86400.0,
    exp_name: str = "",
    # If run on kubernetes, the datasets files need to be taken from volume
    kube: bool = False,
):
    """
    Example:
        python3 run.py --engines *-m-16-* --engines qdrant-* --datasets glove-*
    """
    if kube:
        copy_directory(KUBE_DIR + "/data", DATASETS_DIR)

    all_engines = read_engine_configs()
    all_datasets = read_dataset_config()

    selected_engines = {
        name: config
        for name, config in all_engines.items()
        if any(fnmatch.fnmatch(name, engine) for engine in engines)
    }
    selected_datasets = {
        name: config
        for name, config in all_datasets.items()
        if any(fnmatch.fnmatch(name, dataset) for dataset in datasets)
    }

    for engine_name, engine_config in selected_engines.items():
        for dataset_name, dataset_config in selected_datasets.items():
            print(f"Running experiment: {engine_name} - {dataset_name}")
            client = ClientFactory(host).build_client(engine_config)
            dataset = Dataset(dataset_config)
            dataset.download()
            try:
                with stopit.ThreadingTimeout(timeout) as tt:
                    client.run_experiment(
                        dataset, skip_upload, skip_search, skip_if_exists
                    )
                client.delete_client()

                # If the timeout is reached, the server might be still in the
                # middle of some background processing, like creating the index.
                # Next experiment should not be launched. It's better to reset
                # the server state manually.
                if tt.state != stopit.ThreadingTimeout.EXECUTED:
                    print(
                        f"Timed out {engine_name} - {dataset_name}, "
                        f"exceeded {timeout} seconds"
                    )
                    exit(2)
            except IncompatibilityError as e:
                print(f"Skipping {engine_name} - {dataset_name}, incompatible params")
                continue
            except KeyboardInterrupt as e:
                traceback.print_exc()
                exit(1)
            except Exception as e:
                print(f"Experiment {engine_name} - {dataset_name} interrupted")
                traceback.print_exc()
                if exit_on_error:
                    raise e
                continue

    now = datetime.now()
    experiment_timestamp = f"{now.second}_{now.minute}_{now.hour}_{now.day}_{now.month}_{now.year}"

    if len(exp_name):
        experiment_timestamp = exp_name

    if kube:
        copy_directory(RESULTS_DIR, KUBE_DIR + f"/results_{experiment_timestamp}")


if __name__ == "__main__":
    app()
