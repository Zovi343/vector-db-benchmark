#!/bin/bash
# LVD MODIFICATION START
python run.py --engines "qdrant-m-16-ef-128" --datasets "hnm_2k" --host "qdrant" --expname "hnm_2k_final" --kube
# LVD MODIFICATION END