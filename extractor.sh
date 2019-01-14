#!/bin/bash
# Indique au système que l'argument qui suit est le programme utilisé pour exécuter ce fichier
# En règle générale, les "#" servent à mettre en commentaire le texte qui suit comme ici
echo "Es que l’erreur vient du code implanté ?"
cd sonarqube
git log >> ../allCommits.txt
git log --merges >> ../onlyMerges.txt
git log --pretty=format:'%h : %s' --graph > ../logError.log
