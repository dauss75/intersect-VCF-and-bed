#!/isilon/prodx/bcbio/anaconda/bin/python3.6

import os
import argparse

#flag_folder = sys.argv[1]
#flag_file = sys.argv[2]
#os.system('touch ' + flag_folder + flag_file)

def submit_flag(flag_folder, flag_file):
    fname=flag_folder + "/" + flag_file + ".done"
    os.system('touch {}'.format(fname))

def __main__():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--flag_folder', dest="flag_folder", help="flag_folder", required=True)
    parser.add_argument('-ff', '--flag_file', dest="flag_file", help="flag_file", required=True)
    args = parser.parse_args()

    submit_flag(args.flag_folder, args.flag_file)

if __name__=="__main__": __main__()
