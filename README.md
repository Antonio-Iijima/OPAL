<p align=center><img src="https://github.com/Antonio-Iijima/OPAL/blob/main/logo.png?raw=true" width=75%></p>

---


# THE OPAL PROGRAMMING LANGUAGE


OPAL (Omni-Paradigm Programming Language) seeks to unify multiple diverse programming paradigms through a consistent syntax and an intuitive semantics.

OPAL is a continuation and expanded version of the [Alvin Programming Language](https://github.com/Antonio-Iijima/alvin), which inherits many of its design principles and features from Lisp.


## Table of Contents


- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Resources](#resources)
- [License](#license)


## Installation


Check if you have Python installed:

```
$ python3 --version
```

If not, install it from the [Python website](https://www.python.org/).

Once Python is installed, clone the repo:

```
$ git clone https://github.com/Antonio-Iijima/OPAL.git
$ cd OPAL
```

OPAL uses a virtual environment provided by Python's `venv` module. In order to run the setup script, execute the following:

```
$ chmod 755 opal
$ ./opal --build
```

You are now ready to start programming with OPAL. Run `./opal --help` for further information, or browse the documentation under [Resources](#resources).


## Usage


The OPAL interpreter can be run in many different ways. To start an interactive interpreter session, use the `-i` flag:

```
$ ./opal -i
OPAL v3.0, interactive
Enter 'help' to show further information
(Ω)
```

OPAL also includes a built-in, terminal-based IDE, which can be run using `./opal --ide`.

To run OPAL from any directory, add the following line to your `~/.bashrc` file, replacing `~/PATH/TO/OPAL` with the absolute path to the project, and restart the terminal:

```
opal() { . ~/PATH/TO/OPAL/opal $@; }
```

You should now be able to use `opal <flags>` directly as a command without needing to `cd` into the project directory.


## Contributing


If you have ideas for interesting features, find or fix a bug, or notice a typo, please feel free to contribute via a pull request.


## Resources


For a comprehensive deep dive into the features, usage, and implementation of OPAL, check out the [documentation](https://antonio-iijima.github.io/OPAL/).

OPAL is under active development; the following programming paradigms have varying degrees of functionality:

- Imperative
  - Procedural
- Declarative
  - Logic
- Functional
- Object-oriented
- Metaprogramming
  - Reflective

The following is a brief overview of OPAL's current language features:

- Cambridge Polish syntax and homoiconicity
- Applicative-order evaluation
- Side-effect
- Dynamic binding
- Dynamic and manual scoping
- Latent and optionally strict variable typing
- First-order functions and closures
- Objects
- Reflexive lambda functions and anonymous recursion
- Dynamic language extension


## License

OPAL is licensed under a [GNU General Public License](https://github.com/Antonio-Iijima/alvin/blob/main/LICENSE).
