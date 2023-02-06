# OrderYourRepos

## Description

How many times has happened to you that you clone and clone repositories but with time you forget what they suppose to do?
So you have to revisit the site, check what it does, forget again with the time what it does and so on...

For this reason I decided to create a couple of simple features to put order in your (and mine) chaos for the repositories we use.

## Getting Started

### Dependencies

Asumming you have `Python3` and `pip`/`pip3` installed, use:
```
pip3 install beautifulsoup4
pip3 install tabulate
```
### Installing
Run:
```
git clone https://github.com/p4nchit0z/addRepo.git
```
### Usage - addRepo.py

* Once downloaded/cloned, just run:
```
python3 addRepo.py -w https://SOMEGITHUBPAGEHERE.com/USER_HERE/REPO_HERE
```

Using this repository as an example:

```
python3 addRepo.py -w https://github.com/p4nchit0z/OrderMyRepos
```

by default, this will create a file `repositories.txt` in the directory the script is being run (not where the script is located) with multiple columns: 

   1. Save the original Github's weblink.
   2. Extract the title/main header of the Github's repository.
   3. Select for which Operating System (OS) is the repository scoped for (default: `Any`).
   4. Selects the (main) programming language, as indicated by Github's language bar.
   5. Extracts the description for the repository

However, I know this is a lot of stuff to our eyes if we open the file `repositories.txt` (or whatever the file you have saved your repos). For that reason I also created an additional featured called `showRepo.py`


### Usage - showRepo.py

```
python3 showRepo.py
```

this will print in a pretty table all the repositories you have added to `repositories.txt` (or whatever the file you have saved your repos using `-f` flag)

* Now, installing the repositories saved in `repositories.txt` using Bash:

```
while read line; do git clone $(echo $line | awk -F '--' '{printf $1}'); done < repositories.txt
```


## Help

To check more features, just type:
```
python3 addRepo.py --help
```

and

```
python3 showRepo.py
```

## Authors

[@p4nchit0z](https://github.com/p4nchit0z)

## License

This project is licensed under the MIT License - see the LICENSE file for details
