#!/bin/bash
python run.py --engines "qdrant-m-16-ef-128" --datasets "hnm_2k" --host "qdrant" --expname "hnm_2k_final" --kube

python run.py --engines "qdrant-m-16-ef-128" --datasets "hnm_2k_no_filters" --host "qdrant" --expname "hnm_2k_final" --kube