from github import Github
import time

def wait_limit_reset(github, remaining):
    rate_limit = github.get_rate_limit()
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