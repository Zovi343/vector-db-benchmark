#!/bin/bash
# LVD MODIFICATION START
python run.py --engines "milvus-m-16-ef-128" --datasets "hnm_2k" --host "milvus" --expname "hnm_2k_final" --kube

python run.py --engines "milvus-m-16-ef-128" --datasets "hnm_2k_no_filters" --host "milvus" --expname "hnm_2k_final" --kube
# LVD MODIFICATION END