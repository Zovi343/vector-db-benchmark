#!/bin/bash
# LVD MODIFICATION START
python run.py --engines "weaviate-m-16-ef-128" --datasets "hnm_2k" --host "weaviate" --expname "hnm_2k_final" --kube
# LVD MODIFICATION END