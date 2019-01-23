import boto3
import sys
import os
from os import path


def main(name_of_exploration):
    ## Setting working directory to Uber Prize starter kit root
    os.chdir("..")

    s3 = boto3.client('s3')

    # search-output-all_randomrandom
    ## Finding all relevant files
    output_dir = f"search-output-{name_of_exploration}"
    bucketName = "uber-prize-testing-output"

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
    # Parallel(n_jobs=-2)(delayed(s3.upload_file)(f_i, bucketName, f_i) for f_i in files_to_copy)


if __name__ == "__main__":
    name_of_exploration = sys.argv[1]
    main(name_of_exploration)



