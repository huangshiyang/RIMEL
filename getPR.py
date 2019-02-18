from github import Github
import time
from datetime import datetime
import sys
import getopt
from utils import *


def main(argv):
    repo_name = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hr:o:", ["repo=", "ofile="])
    except getopt.GetoptError:
        print("test.py -r <github/repo> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("test.py -r <github/repo> -o <outputfile>")
            sys.exit()
        elif opt in ("-r", "--repo"):
            repo_name = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if repo_name == '' or outputfile == '':
        print("test.py -r <github/repo> -o <outputfile>")
        sys.exit(2)

    print("start")
    g = Github("9517082cce9860b93b7117f40989b1a92de39de9")
    repo = g.get_repo(repo_name)
    pull_requests = repo.get_pulls(state='closed', base='master')

    merged_pull_requests = filter(lambda pr: pr.is_merged(), pull_requests)

    file = open(outputfile, "w")

    for pr in merged_pull_requests:
        commits = pr.get_commits()
        for c in commits:
            wait_limit_reset(g, 100)
            if is_build_fail(c):
                print(pr.number)
                file.write(str(pr.number) + "\n")
                break

    file.close()
    print("end")


if __name__ == "__main__":
    main(sys.argv[1:])
