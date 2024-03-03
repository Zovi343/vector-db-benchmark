#!/bin/bash
python run.py --engines "lvd-model-mlp4-ncat-20-epoch-200-lrs-001-nbuck-2-bthr-02-constw--1" --datasets "hnm_2k_no_filters" --host "lvd" --expname "hnm_2k" --kube
python run.py --engines "lvd-model-mlp4-ncat-20-epoch-200-lrs-001-nbuck-2-bthr-02-constw--1" --datasets "hnm_2k" --host "lvd" --expname "hnm_2k" --kube