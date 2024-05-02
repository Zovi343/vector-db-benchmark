#!/bin/bash
# LVD MODIFICATION START
python run.py --engines "chroma-m-16-ef-128" --datasets "hnm_2k_no_filters" --host "chroma" --expname "hnm_2k_final" --kube
# LVD MODIFICATION END