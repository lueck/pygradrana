#!/usr/bin/env python3

import sys,argparse
import xml.sax

from gradrana.tei import TeiP5Parser
from gradrana.gliederung import Gliederung
from gradrana.konfiguration import *
from gradrana.adjacencymatrix import *
from gradrana.network import *
from gradrana.graph import *

def __main__():

    # setup parser for command line arguments
    parser = argparse.ArgumentParser(
        description="Analyze a dramatic text.")
    subparsers = parser.add_subparsers(
        dest="command",
        help="Call 'gradrana SUBCOMMAND -h' for help on a subcommand.")

    matrix_parser = subparsers.add_parser(
        "configuration",
        help="Generate a configuration matrix of the analyzed play.",
        description="Generate a configuration matrix of the analyzed play.")
    matrix_parser.add_argument(
        "INFILE",
        help="The input file containing the dramatic text.")

    matrix_output = matrix_parser.add_mutually_exclusive_group()
    matrix_output.add_argument(
        "-m", "--html",
        help="Generate XHTML output.",
        action="store_const",
        dest="format",
        const=HtmlKonfigurationsmatrix,
        default=HtmlKonfigurationsmatrix) 
    matrix_output.add_argument(
        "-t", "--tex",
        help="Generate LaTeX output.",
        action="store_const",
        dest="format",
        const=LatexKonfigurationsmatrix)
    matrix_parser.add_argument(
        "-o", "--outfile",
        help="Outputfile. Defaults to stdout.")
    matrix_parser.add_argument(
        "-s", "--sums",
        help="Include sums in output.",
        action="store_true")
    matrix_parser.add_argument(
        "-z", "--zeros",
        help="Insert 0 (zero) where a value is missing.",
        action="store_const",
        dest="missing_value",
        const=0,
        default=" ")

    matrix_calculator = matrix_parser.add_mutually_exclusive_group()
    matrix_calculator.add_argument(
        "-p", "--presence",
        help="Evaluate presence on stage.",
        action="store_const",
        dest="calculator",
        const=praesenz,
        default=praesenz)
    matrix_calculator.add_argument(
        "-c", "--contributions",
        help="Evaluate count of contributions to talk on stage.",
        action="store_const",
        dest="calculator",
        const=beitragsanzahl)
    matrix_calculator.add_argument(
        "-l", "--letters",
        help="Evaluate length of utterances by counting letters (characters).",
        action="store_const",
        dest="calculator",
        const=beitragslaenge)
    matrix_calculator.add_argument(
        "-w", "--words",
        help="Evaluate length of utterances by counting words.",
        action="store_const",
        dest="calculator",
        const=beitragswoerter)

    gliederung_parser = subparsers.add_parser(
        "structuring",
        help="Inspect the structuring (acts, scenes) of a dramatic text.",
        description="Inspect the structuring (acts, scenes) of a dramatic text.")
    gliederung_parser.add_argument(
        "INFILE",
        help="The input file containing the dramatic text.")
    gliederung_parser.add_argument(
        "-i", "--indented",
        help="Output in indented form.",
        action="store_true")
    gliederung_parser.add_argument(
        "-f", "--first-speech",
        help="Include each scene's first speech. This may help to find annotation errors.",
        action="store_true")

    graph_parser = subparsers.add_parser(
        "graph",
        help="Generate a social network graph of the analyzed play.",
        description="Generate a social network graph of the analyzed play.")
    graph_parser.add_argument(
        "INFILE",
        help="The input file containing the dramatic text.")
    graph_parser.add_argument(
        "-z", "--zeros",
        help="Insert 0 (zero) where a value is missing.",
        action="store_const",
        dest="missing_value",
        const=0,
        default=" ")
    graph_parser.add_argument(
        "-o", "--outfile",
        help="Outputfile. Defaults to stdout.")
    graph_parser.add_argument(
        "-e", "--weighted-edges",
        help="Draw weighted edges (only for visualization).",
        action="store_true",
        dest="weighted_edges")

    graph_output = graph_parser.add_mutually_exclusive_group()
    graph_output.add_argument(
        "-m", "--html",
        help="Generate XHTML adjacency matrix.",
        action="store_const",
        dest="format",
        const=HtmlAdjacencyMatrix,
        default=HtmlAdjacencyMatrix) 
    graph_output.add_argument(
        "-t", "--tex",
        help="Generate LaTeX adjacency matrix.",
        action="store_const",
        dest="format",
        const=LatexAdjacencyMatrix) 
    graph_output.add_argument(
        "-v", "--visualization",
        help="Generate visualization of the social network graph.",
        action="store_const",
        dest="format",
        const=DramaVisualization) 

    graph_calculator = graph_parser.add_mutually_exclusive_group()
    graph_calculator.add_argument(
        "-p", "--presence",
        help="Evaluate presence on stage.",
        action="store_const",
        dest="calculator",
        const=praesenz,
        default=praesenz)
    graph_calculator.add_argument(
        "-c", "--contributions",
        help="Evaluate count of contributions to talk on stage.",
        action="store_const",
        dest="calculator",
        const=beitragsanzahl)
    graph_calculator.add_argument(
        "-l", "--letters",
        help="Evaluate length of utterances by counting letters (characters).",
        action="store_const",
        dest="calculator",
        const=beitragslaenge)
    graph_calculator.add_argument(
        "-w", "--words",
        help="Evaluate length of utterances by counting words.",
        action="store_const",
        dest="calculator",
        const=beitragswoerter)

    graph_edgeweight = graph_parser.add_mutually_exclusive_group()
    graph_edgeweight.add_argument(
        "-r", "--copresence",
        help="Evaluate edge weights: Results 1 if a pair of figures is on stage at the same time, and 0 otherwise. (Default)",
        action="store_const",
        dest="edgeweight",
        const=copresence,
        default=copresence)
    graph_edgeweight.add_argument(
        "-u", "--sum-weight",
        help="Evaluate edge weights: Sums up edge weights by adding the maximum of two persons contribution to the szene. This results in edge weights that are dominated by dominant figures.",
        action="store_const",
        dest="edgeweight",
        const=sum_edge_weight)
    graph_edgeweight.add_argument(
        "-i", "--minimum",
        help="Evaluate edge weights: Sums up edge weights by adding the minimum of two persons contribution to the szene. This results in lower weighted edges for margin figures.",
        action="store_const",
        dest="edgeweight",
        const=sum_min_edge_weight)
    graph_edgeweight.add_argument(
        "-a", "--maximum",
        help="Evaluate edge weights: Sums up edge weights by adding the maximum of two persons contribution to the szene. This results in edge weights that are dominated by dominant figures.",
        action="store_const",
        dest="edgeweight",
        const=sum_max_edge_weight)

    # actually parse command line arguments
    args = parser.parse_args()
    #print(args)

    # Parse input file
    xml_parser = xml.sax.make_parser()
    tei = TeiP5Parser()
    xml_parser.setContentHandler(tei)
    xml_parser.setFeature(xml.sax.handler.feature_namespaces, True)
    xml_parser.parse(args.INFILE)

    # Do what was said in the arguments
    if args.command == "configuration":
        processor = args.format(
            auswertfunktion=args.calculator,
            summen=args.sums,
            missing_value=args.missing_value,
            outfile=args.outfile)
    elif args.command == "structuring":
        processor = Gliederung(
            erste_rede=args.first_speech,
            treppe=args.indented)
    elif args.command == "graph":
        processor = args.format(
            auswertfunktion=args.calculator,
            missing_value=args.missing_value,
            outfile=args.outfile,
            weighted_edges=args.weighted_edges,
            sum_edge_weight=args.edgeweight)

    # call the processor with parsed scenes and dramatis personae
    processor(tei.szenen, {})

    #print(processor.personen, "\n\n", processor.kuerzel)
