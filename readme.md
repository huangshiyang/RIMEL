# RIMEL project

## Get pull request from a github repository

```sh
getPR.py -r <github/repo> -o <outputfile>

#example
getPR.py -r SonarSource/sonarqube -o pull_requests_sonarqube.txt
```

## Analyse pull request

```sh
getCommitesofPR.py -r <github/repo> -i <inputfile>

#example
getCommitesofPR.py -r SonarSource/sonarqube -i pull_requests_sonarqube.txt
```