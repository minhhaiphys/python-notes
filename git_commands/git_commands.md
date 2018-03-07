# Tutorial: Git Common Commands

### SET UP GIT

Configure identity
```shell
git config --global user.name "minhhaiphys"
git config --global user.email "mn455@cornell.edu"
```

Set default editor to Atom
```shell
git config --global core.editor "atom --wait"
```

Set default editor to Sublime Text
```shell
git config --global core.editor subl
```

Check the settings
```shell
git config --list
```

See the local config file
```shell
cat .git/config
```

### WORKING WITH REPO

Clone an existing repo online
```shell
git clone https://github.com/minhhaiphys/xyz.git <new directory name>
```

List remote repos
```shell
git remote -v
```

Add a remote repo
```shell
git remote add <name> <url>
```

Get data from remote
```shell
git fetch <remote-name>
```

Get data and merge into local repo
```shell
git pull
```

Push back to server repo
```shell
git push <server> <branch>
```

Remove a remote repo
```shell
git remote rm <repo>
```

### BRANCHES

List all branches
```shell
git branch
[-r]: remote branches
```

Make branch
```shell
git branch <branch name> <start-point>
```

Delete branch
```shell
git branch -d <branch>
[-D]: Force delete
```

Switch to branch
```shell
git checkout <branch>
```

Create new branch and switch to it
```shell
git checkout -b <new> <start-point>
```

Merge branchA into the current branch
```shell
git merge <branchA>
```

### COMMIT

Check status
```shell
git status [-s]
```

Stage or add files
```shell
git add <files>
```

Remove a file out of staged area
```shell
git rm --cached <filename>
```

** Commit **

_[-a]: add all tracked files _

_[-m]: add a message_

_[-v]: choose commits on the go_
```shell
git commit [-v] [-a]
```

See the differences
```shell
git diff [--staged]
```

Rename a file
```shell
git mv <oldname> <newname>
```

Show the last commit
```shell
git show
```

See history

_[-p] [-num]: See details_

_[--stat]: short report_

_[--pretty]: format_

_[--since = 2.weeks]: see recent changes_
```shell
git log
```

Discard changes (not yet staged)
```shell
git checkout -- <filename>
```
