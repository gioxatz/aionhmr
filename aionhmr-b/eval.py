import argparse
import os
from pathlib import Path
import traceback
from typing import Optional

import pandas as pd
import torch
from filelock import FileLock
from src.configs import dataset_eval_config
from src.datasets import create_dataset
from src.utils import Evaluator, recursive_to
from tqdm import tqdm

from src.configs import CACHE_DIR_AIONHMR
from src.models import AionHMRb, download_models, load_aionhmr, DEFAULT_CHECKPOINT

def main():
    parser = argparse.ArgumentParser(description='Evaluate trained models')
    parser.add_argument('--checkpoint', type=str, default=DEFAULT_CHECKPOINT, help='Path to pretrained model checkpoint')
    parser.add_argument('--results_file', type=str, default='results/eval_regression.csv', help='Path to results file.')
    parser.add_argument('--dataset', type=str, default='COCO-VAL,SYRIP,RH,CHILDPLAY', help='Dataset to evaluate') # choices=['H36M-VAL-P2', '3DPW-TEST', 'MPI-INF-TEST']
    parser.add_argument('--task', type=str, default='2D', choices=['2D', '3D', 'height'], help='Target attribute for evaluation')
    parser.add_argument('--batch_size', type=int, default=16, help='Batch size for inference')
    parser.add_argument('--num_samples', type=int, default=1, help='Number of test samples to draw')
    parser.add_argument('--num_workers', type=int, default=8, help='Number of workers used for data loading')
    parser.add_argument('--log_freq', type=int, default=10, help='How often to log results')
    parser.add_argument('--shuffle', dest='shuffle', action='store_true', default=False, help='Shuffle the dataset during evaluation')
    parser.add_argument('--exp_name', type=str, default=None, help='Experiment name')

    args = parser.parse_args()

    # Download and load checkpoints
    download_models(CACHE_DIR_AIONHMR)
    model, model_cfg = load_aionhmr(args.checkpoint)

    # Setup AionHMR-b model
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = model.to(device)
    model.eval()

    # Load config and run eval, one dataset at a time
    print('Evaluating on datasets: {}'.format(args.dataset), flush=True)
    for dataset in args.dataset.split(','):
        dataset_cfg = dataset_eval_config()[dataset]
        args.dataset = dataset
        run_eval(model, model_cfg, dataset_cfg, device, args)

def run_eval(model, model_cfg, dataset_cfg, device, args):
    # Create dataset and data loader
    dataset = create_dataset(model_cfg, dataset_cfg, train=False)
    dataloader = torch.utils.data.DataLoader(dataset, args.batch_size, shuffle=args.shuffle, num_workers=args.num_workers)

    # List of metrics to log
    if args.dataset in ['3DPW-TEST']:
        metrics = ['mode_re', 'mode_mpjpe']
        pck_thresholds = None
    if args.dataset in ['COCO-VAL']:
        metrics = ['mode_kpl2']
        pck_thresholds = [0.05, 0.1]
    if args.dataset in ['SYRIP', 'RH', 'CHILDPLAY', 'BABYROBOT']:
        if args.task == '2D':   
            metrics = ['mode_kpl2']
            pck_thresholds = [0.05, 0.1]
        elif args.task == '3D':
            metrics = ['mode_re', 'mode_mpjpe']
            pck_thresholds = None
        elif args.task == 'height':
            metrics = ['avg_height_diff', 'avg_height_perc_diff', 'avg_height']
            pck_thresholds = None
        else:
            print("Select what you want to evaluate: 2D, 3D, height")
            exit(0)

    # Setup evaluator object
    evaluator = Evaluator(
        dataset_length=int(1e8), 
        keypoint_list=dataset_cfg.KEYPOINT_LIST, 
        pelvis_ind=model_cfg.EXTRA.PELVIS_IND, 
        metrics=metrics,
        pck_thresholds=pck_thresholds,
    )

    # Go over the images in the dataset.
    try:
        for i, batch in enumerate(tqdm(dataloader)):
            batch = recursive_to(batch, device)
            with torch.no_grad():
                out = model(batch)
            evaluator(out, batch)
            if i % args.log_freq == args.log_freq - 1:
                evaluator.log()
        evaluator.log()
        error = None
    except (Exception, KeyboardInterrupt) as e:
        traceback.print_exc()
        error = repr(e)
        i = 0

    # Append results to file
    metrics_dict = evaluator.get_metrics_dict()
    save_eval_result(args.results_file, metrics_dict, args.checkpoint, args.dataset, error=error, iters_done=i, exp_name=args.exp_name)


def save_eval_result(
    csv_path: str,
    metric_dict: float,
    checkpoint_path: str,
    dataset_name: str,
    # start_time: pd.Timestamp,
    error: Optional[str] = None,
    iters_done=None,
    exp_name=None,
) -> None:
    """Save evaluation results for a single scene file to a common CSV file."""

    timestamp = pd.Timestamp.now()
    exists: bool = os.path.exists(csv_path)
    exp_name = exp_name or Path(checkpoint_path).parent.parent.name

    # save each metric as different row to the csv path
    metric_names = list(metric_dict.keys())
    metric_values = list(metric_dict.values())
    N = len(metric_names)
    df = pd.DataFrame(
        dict(
            timestamp=[timestamp] * N,
            checkpoint_path=[checkpoint_path] * N,
            exp_name=[exp_name] * N,
            dataset=[dataset_name] * N,
            metric_name=metric_names,
            metric_value=metric_values,
            error=[error] * N,
            iters_done=[iters_done] * N,
        ),
        index=list(range(N)),
    )

    # Lock the file to prevent multiple processes from writing to it at the same time.
    lock = FileLock(f"{csv_path}.lock", timeout=10)
    with lock:
        df.to_csv(csv_path, mode="a", header=not exists, index=False)

if __name__ == '__main__':
    main()
