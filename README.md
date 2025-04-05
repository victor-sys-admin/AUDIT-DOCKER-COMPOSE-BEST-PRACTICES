# AUDIT-DOCKER-COMPOSE-BEST-PRACTICES

# Summary

[Introduction](#introduction)<br>
[I - Run the program](#i---run-the-program)<br>
-- [A - Create a virtual environment (optional)](#a---create-a-virtual-environment-optional)<br>
-- [B - Install dependencies](#b---install-dependencies)<br>
-- [C - Run the program](#c---run-the-program)<br>
[II - Good to know](#ii---good-to-know)<br>
-- [A - Exit codes](#a---exit-codes)<br>
---- [1 - Exit as expected (code 0)](#1---exit-as-expected-code-0)<br>
---- [2 - Compliance issue(s) (code 1)](#2---compliance-issues-code-1)<br>
---- [3 - File(s) not found (code 2)](#3---files-not-found-code-2)<br>
---- [4 - File(s) couldn't be audited (code 3)](#4---files-couldnt-be-audited-code-3)<br>
<!-- -- [B - Put in CI/CD]()<br>
-- [C - Sequence Diagram]()<br> -->
[III - Development](#iii---development)<br>
-- [A - General testing](#a---general-testing)<br>
---- [1 - Testing linting (Quality)](#1---testing-linting-quality)<br>
---- [2 - Security testing](#2---security-testing)<br>

# Introduction

This repository hosts a Python program to audit Docker Compose compliance 
with best practices.

# I - Run the program

## A - Create a virtual environment (optional)

To create a virtual environment using `venv` you can use:
```sh
python3 -m venv .venv
```

Then you need to activate it, using the following command on Linux/MacOS:
```sh
. .venv/bin/activate
```

## B - Install dependencies

To install dependencies, you will use `pip` like this:
```sh
pip install -r requirements.txt
```

## C - Run the program

If you are at the root of this repository, you can run the program like this:
```sh
python3 src/main.py
```

# II - Good to know

## A - Exit codes

### 1 - Exit as expected (code 0)

The program stops as designed, with no error. All the audited Docker 
Compose files are compliant with the best practices checked by the program.

### 2 - Compliance issue(s) (code 1)

The program stops as designed, with no error. However, the program found 
compliance issue(s).

### 3 - File(s) not found (code 2)

The program stops because it could not find any `.yaml` or `.yml` files.

### 4 - File(s) couldn't be audited (code 3)

The program stops because it could not audit the YAML file(s) found in the 
current directory.

# III - Development

## A - General testing

### 1 - Testing linting (Quality)

You can test code quality with `pylint` (same check as in the CI/CD).

To do so, move to the `src` folder, then:
```sh
pylint ./*.py
```

### 2 - Security testing

You can test code security with `bandit` (same check as in the CI/CD).

To do so, move to the `src` folder, then:
```sh
bandit . -r
```

If you store your `venv` in `src` you should use the following command:
```sh
bandit . -r --exclude "./.venv"
```
