#!/usr/bin/env python
#Segun Jung

import os, argparse, subprocess, shutil

def run_intersect(vcf, bed, tmp_dir, out_dir, bedtools):
    sn=os.path.basename(vcf).split('.vcf')[0]
    header='{}/{}_header.vcf'.format(tmp_dir, sn)
    with open(vcf,'r') as f, open(header,'w') as o:
        for line in f:
            # line=line.strip()
            if line.startswith('#'):
                o.write(line)
    intersectF = '{}/{}.intersect_tmp.vcf'.format(tmp_dir, sn)
    cmd = '{} -a {} -b {} > {}'.format(bedtools, vcf, bed, intersectF)
    out, error = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=tmp_dir).communicate()
    if error:
        print("An error occured: {error}".format(error=error))
    finalF = '{}/{}.intersect.vcf'.format(tmp_dir, sn)
    finaloutF = '{}/{}.intersect.vcf'.format(out_dir, sn)
    if os.path.exists(header) and os.path.exists(intersectF):
        filenames = [header, intersectF]
        with open(finalF, 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())
    shutil.copy(finalF, finaloutF)


def __main__():

    parser = argparse.ArgumentParser(description='intersect BED with VCF')
    # Required arguments
    parser.add_argument('-i', '--vcf', help='VCF directory', required=True)
    parser.add_argument('-b', '--bedF', help='bed file', required=True)
    parser.add_argument('-is', '--bedtools', help='bed file', required=True)
    parser.add_argument('-t', '--tmp_dir', help='output directory', required=True)
    parser.add_argument('-o', '--output_dir', help='output directory', required=True)
    args = parser.parse_args()

    run_intersect(args.vcf, args.bedF, args.tmp_dir, args.output_dir, args.bedtools)

if __name__=="__main__": __main__()
