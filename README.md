# Istiophoridae

Istiophoridae is a Genetic Algorithm based parameter tuning system for chess engines.
It was developed for the [Black Marlin chess engine](https://github.com/jnlt3/blackmarlin).
The name of the tuner originates from the family of the fish: Istiophoridae.

# Installation

- Istiophoridae doesn't have any dependencies, git cloning the repository is sufficient to get it working
- Inside the repository root
  - Create a books directory and place the relevant .epd files.
  - Create a cutechess directory and place cutechess-cli in the directory.
  - Create an engines directory where the executable to be tuned will take place.

# Usage

- Make a config file based on the templates in the config directory.
- Running multiple cutechess instances in parallel is not currently supported, make sure to adjust cutechess threads option accordingly to compensate.
- There is no support for tuning config files as of yet, you will have to modify `params.py`. 
- The format is as follows: `params.append(Param("NAME", MIN, MAX, True))`
- Place engine executable in the engines directory, the opening book in the books directory and cutechess configuration in the config directory. 
- Run with `python3 main.py --engine Engine --book Book.epd --cutechess config.json`

# Missing Features

- Tuning results of non-ordinal parameters are currently broken.
- There aren't any ways to impose constraints on parameters.
- Tuner will always perform a global search, it is not possible to have a starting point.  


# Contributing

- Make sure to use `black` as formatter
- Make sure to use `pylance` on strict mode   