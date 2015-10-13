#!/usr/bin/env python

import argparse
import os

import allensdk.core.json_utilities as json_utilities
from allensdk.core.nwb_data_set import NwbDataSet

import lims_utils

import run_passive_fit

import fit_stage_1
import fit_stage_2

def start_specimen(specimen_id, output_directory):
    #parser = argparse.ArgumentParser(description='Set up DEAP-style fit')
    #parser.add_argument('--output_dir', required=True)
    #parser.add_argument('specimen_id', type=int)
    #args = parser.parse_args()

    data = lims_utils.get_specimen_info(specimen_id)
    #output_directory = os.path.join(output_dir, 'specimen_%d' % specimen_id)

    is_spiny = data['dendrite type'] != 'aspiny'

    data_set = NwbDataSet(data['nwb_path'])

    passive_fit_data = run_passive_fit.run_passive_fit(data['id'], data_set, is_spiny, data['sweeps'], data['swc_path'], output_directory)
    json_utilities.write(os.path.join(output_directory, 'passive_fit_data.json'), passive_fit_data)

    stage_1_jobs = fit_stage_1.prepare_stage_1(data_set, data['sweeps'], data['swc_path'], passive_fit_data, is_spiny, output_directory)
    json_utilities.write(os.path.join(output_directory, 'stage_1_jobs.json'), stage_1_jobs)
    
    fit_stage_1.run_stage_1(stage_1_jobs)

    stage_2_jobs = fit_stage_2.prepare_stage_2(output_directory)
    fit_stage_2.run_stage_2(stage_2_jobs)

if __name__ == "__main__": main()
