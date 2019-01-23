import boto3
import sys
import os
from os import path
from multiprocessing.pool import ThreadPool
from datetime import datetime

bucketName = "uber-prize-testing-output"
s3 = boto3.client('s3')


def upload(filename):
    s3.upload_file(filename, bucketName, filename)

def main(name_of_exploration):
    ## Setting working directory to Uber Prize starter kit root
    os.chdir("..")

    # search-output-all_randomrandom
    ## Finding all relevant files
    output_dir = f"search-output-{name_of_exploration}"

    files_to_copy = []
    for root, dirs, files in os.walk(output_dir, topdown=False):
        # print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            # print(len(path) * '---', file)
            files_to_copy.append(path.join(root, file))

    n_files = len(files_to_copy)
    for idx, f_i in enumerate(files_to_copy):
        if idx % 50 == 0:
            print(f"Copying {idx + 1} out of {n_files}")
        s3.upload_file(f_i, bucketName, f_i)

    # First attempt at parallelization
    # Raises an error because joblib does not want to parallelize a function with arguments
    # that cannot be pickled
    # Parallel(n_jobs=-2)(delayed(s3.upload_file)(f_i, bucketName, f_i) for f_i in files_to_copy)

    # with multi-processing
    # Seems to upload something but not sure if faste
    # pool = ThreadPool(processes=2)
    # pool.map(upload, files_to_copy)


if __name__ == "__main__":
    name_of_exploration = sys.argv[1]
    main(name_of_exploration)


