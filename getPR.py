from github import Github
import time
from datetime import datetime
import sys
import getopt

g = Github("9517082cce9860b93b7117f40989b1a92de39de9")


def wait_limit_reset(remaining):
    rate_limit = g.get_rate_limit()
    if rate_limit.core.remaining < remaining:
        present = datetime.now()
        delta = present - rate_limit.core.reset
        print("waiting")
        time.sleep(3600 - int(delta.total_seconds()))
        print("rate limit reseted")


def is_build_fail(commit):
    status = commit.get_statuses()
    for s in status:
        if s.context == "continuous-integration/travis-ci/pr":
            if s.state == "failure":
                return True
            return False
    return False


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
    repo = g.get_repo(repo_name)
    pull_requests = repo.get_pulls(state='closed', base='master')

    merged_pull_requests = filter(lambda pr: pr.is_merged(), pull_requests)

    file = open(outputfile, "w")

    for pr in merged_pull_requests:
        commits = pr.get_commits()
        for c in commits:
            wait_limit_reset(100)
            if is_build_fail(c):
                print(pr.number)
                file.write(str(pr.number) + "\n")
                break

    file.close()
    print("end")


if __name__ == "__main__":
    main(sys.argv[1:])
