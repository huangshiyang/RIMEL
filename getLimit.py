from github import Github
g = Github("9517082cce9860b93b7117f40989b1a92de39de9")
rate_limit = g.get_rate_limit()
print(rate_limit)
print(rate_limit.core.reset)
