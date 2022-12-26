# Add Repository

## Description

A simple Python script to save save different Github repositories in a file. Useful when, for some reason, you are migrating your system and you want to downloads all the repositories previously downloaded in your old system.

## Getting Started

### Dependencies

Asumming you have `Python3` and `pip` installed, use:
```
pip install beautifulsoup4
```
which is the only non built-in library this script uses.

### Installing
Run:
```
git clone https://github.com/p4nchit0z/addRepo.git
```
### Executing program

* Once downloaded/cloned, just run:
```
python3 addRepo.py -w https://SOMEGITHUBPAGEHERE.com/USER_HERE/REPO_HERE
```

Using this repository as an example:

```
python3 addRepo.py -w https://github.com/p4nchit0z/addRepo
```

by default, this will create a file `repositories.txt` in the directory the script is being run (not where the script is located) with two columns: first one with the repository name and the second one with the repository description. If `repositories.txt` already exists, it will just add a new line. Additionaly, it checks if the repository you are passing has been previously added. To save/read a different file (not called `repositories.txt`), just use the `-f` flag, for example, `-f someDifferentName.txt`.


* Now, installing the repositories saved in `repositories.txt` using Bash:

```
while read line; do git clone $(echo $line | awk -F '--' '{printf $1}'); done < repositories.txt
```


## Help

To check some extra features, just type:
```
python3 addRepo.py --help
```

## Authors

[@p4nchit0z](https://github.com/p4nchit0z)

## License

This project is licensed under the MIT License - see the LICENSE file for details
