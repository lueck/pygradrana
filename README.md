A Tool for Analyzing Dramatic Texts
===================================

`pygradrana` is a library and tool for analyzing dramatic texts. It's
written for the Digital Humanities community. It's has a parser for
TEI-encoded plays and offers functions for generating configuration
matrices of plays like described by Solomon Marcus[1],
social network graphs and some inspections useful for evaluating a
plays text encoding.


## Installation

Requirements:

- Python 3.x (tested on Python 3.5 on Debian stretch)
- networkx
- Matplotlib
- LaTeX (only if you want to create nice PDFs with matrices)

Clone this repository, `cd` into the base directory of the clone and
run

	pip3 install .

This will install `pygradrana` and the required python packages
`networkx` and `Matplotlib`.


## Usage

`pygradrana` comes with a command line program called
`gradrana`. This program has subcommands. To get help on the
subcommands run

	gradrana SUBCOMMAND -h

on the commandline. The subcommands are

configuration
: Generate a configuration matrix of the analyzed play. This is a
table where the columns represent the scenes of a play and the rows
represent the persons (figures). If a person is present on a scene,
the table cell has a non-zero value. This value is calculated by an
evaluation function. You can choose from several evaluation function:
for the plain presence on the scene, for the count of contributions to
the scene's talk, for the length of utterance in words or characters.

graph
: Generate a social network graph of the analyzed play. You can choose
to either generate an adjacency matrix of the graph or a visual
representation of it. For calculating the edges' weights there are the
same evaluation functions again.

structuring
: Inspect the structuring (acts, scenes) of a dramatic text. This may
help to find annotation errors.


## History

`pygradrana` was written in 2019 for a digital humanities course at
[FernUniversität in Hagen](http://www.fernuni-hagen.de).


## Examples

Checkout the [configuration matrix](doc/dantons-tod_config.pdf) and
the
[social network graph's adjacency matrix](doc/dantons-tod_adjacency.pdf)
of Georg Büchners dramatic play *Dantons Tod*. The TEI-document came
from [gerdracor](https://github.com/dracor-org/gerdracor). `gradrana`
was called with the `--words` option, i.e. the words a dramatic person
contributed to each scene's talk was evaluated. Checkout the
visualization of the social network graph of that same play below.

![Visualization of the social network graph](doc/dantons-tod.png)


## License

This project is licensed under the terms of the MIT license.


## Reference(s):

[1] Solomon Marcus: Mathematische Poetik, Bukarest/Frankfurt
a.M. 1973, 278-370
