#!/bin/bash
python run.py --engines "chroma-m-16-ef-100" --datasets "hnm_2k_no_filters" --host "chroma" --expname "hnm_2k" --kube
python run.py --engines "chroma-m-16-ef-100" --datasets "hnm_2k" --host "chroma" --expname "hnm_2k" --kube

python run.py --engines "weaviate-m-16-ef-128" --datasets "hnm_2k_no_filters" --host "weaviate" --expname "hnm_2k" --kube
python run.py --engines "weaviate-m-16-ef-128" --datasets "hnm_2k" --host "weaviate" --expname "hnm_2k" --kube

python run.py --engines "qdrant-m-16-ef-100" --datasets "hnm_2k_no_filters" --host "qdrant" --expname "hnm_2k" --kube
python run.py --engines "qdrant-m-16-ef-100" --datasets "hnm_2k" --host "qdrant" --expname "hnm_2k" --kube
