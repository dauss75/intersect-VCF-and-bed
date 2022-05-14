#!/isilon/prodx/bcbio/anaconda/bin/python

import os, glob, subprocess
import pandas as pd
import shutil
import argparse
import time, datetime

def submit_multi_qsub(step_name, step_exe, step_args, step_nproc, step_runfolder, \
                      flag_dir, flags_exe, samples):

    job_list = []
    # static qsub variables
    args_prep=" ".join(step_args)
    resources = "nodes=1:ppn=" + step_nproc
    walltime = "walltime=24:00:00"

    for i in samples:
        step_args = args_prep + " -i " + i
        cmd = ["/usr/local/bin/qsub",
               "-l", resources,
               "-l", walltime,
               "-j oe",
               "-N", step_name,
               "-r y -d", step_runfolder,
               "-F '", step_args,"'",
                step_exe
               ]
        try:
            p = subprocess.check_output(" ".join(cmd), shell=True).decode('utf-8').rstrip()
            job_list.append(p)

        except subprocess.CalledProcessError:
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    flat_job_list = ':'.join(job_list)

    wait_job_list = "depend=afterok:" + flat_job_list
    wait_resources = "nodes=1:ppn=1"
    wait_job_name = "wait_" + step_name + "_jobs"

    flag_args = ["--flag_folder",flag_dir,
                 "--flag_file",step_name]

    make_flag_args = " ".join(flag_args)
    qsub_wait = ["/usr/local/bin/qsub",\
                 "-l",wait_resources,\
                 "-W",wait_job_list,\
                 "-d",step_runfolder,\
                 "-r y -j oe",\
                 "-o",flag_dir,\
                 "-N",wait_job_name,\
                 "-F '",make_flag_args,"'",\
                 flags_exe]
    qsub_wait_out = subprocess.check_output(" ".join(qsub_wait),shell=True).decode('utf-8').rstrip()
    batch_completed = 0
    while batch_completed == 0:
      if os.path.isfile(flag_dir + "/" + step_name + ".done"):
        batch_completed = 1
        return True
      else:
        time.sleep(1)

def __main__():

    parser = argparse.ArgumentParser(description='intersect BED with VCF')
    # Required arguments
    parser.add_argument('-i', '--vcf_dir', help='VCF directory', required=True)
    parser.add_argument('-b', '--bedF', help='bed file', required=True)
    parser.add_argument('-o', '--output_dir', help='output directory', required=True)
    args = parser.parse_args()

    vcf_dir = os.path.abspath(args.vcf_dir); bedF = os.path.abspath(args.bedF); output_dir = os.path.abspath(args.output_dir)

    tmp_dir = output_dir + '/tmp_dir'       # temp dir
    if not os.path.exists(output_dir) and not os.path.exists(tmp_dir):
        os.mkdir(output_dir); os.mkdir(tmp_dir)

    vcf_files = sorted(glob.glob('{}/*vcf'.format(vcf_dir)))
    if vcf_files:
        step_name = 'intersect'

        bedtools_path = "/isilon/RnD/tools/bedtools/2.25.0/bin/intersectBed"
        main_dir = '/isilon/RnD/tools/custom_script/bedtools'
        step_exe = main_dir + '/bedtools_cmd.py'
        flag_exe = main_dir + "/flagMaker.py"

        step_args =["-b", bedF,
                    "-is", bedtools_path,
                    "-t", tmp_dir,
                    "-o", output_dir,]
        step_nproc = '1'
        intersect_flag = submit_multi_qsub(step_name, step_exe, step_args, step_nproc, tmp_dir, tmp_dir, flag_exe, vcf_files)
        if intersect_flag:
            shutil.rmtree(tmp_dir)
if __name__=="__main__": __main__()
