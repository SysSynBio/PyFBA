import argparse
import copy
import os
import sys

from fba import run_fba
from metabolism import biomass_equation, Compound
from parse import SBML, read_media_file

__author__ = 'Rob Edwards'

parser = argparse.ArgumentParser(description="Print the equations of reactions in an sbml file")
parser.add_argument('-s', help='sbml file', required=True)
parser.add_argument('-m', help='media file', required=True)
parser.add_argument('-v', help='verbose output', action='store_true')
args = parser.parse_args()

if not os.path.exists(args.s):
    sys.exit("SBML file {} was not found".format(args.s))

sbml = SBML.parse(args.s, False)

# get the reactions from the SBML file. This is a dict of metabolite.Reaction objects
rxn = sbml.reactions
if args.v:
    sys.stderr.write("List of 'rxns' list: {}\n".format(len(rxn)))

# filter out reactions where one of the components is an uptake/secretion reaction (aka boundary reaction)
reactions_to_run  = set()
uptake_secretion_reactions = {}
biomass_equation = None
for r in rxn:
    if 'biomass_equation' in rxn[r].name.lower():
        biomass_equation = rxn[r]
        continue
    is_boundary = False
    for c in rxn[r].all_compounds():
        if c.uptake_secretion:
            is_boundary = True
    if is_boundary:
        rxn[r].is_uptake_secretion = True
        uptake_secretion_reactions[r] = rxn[r]
    else:
        reactions_to_run.add(r)


# get all the compounds fromt the SBML file. This is a dict of metabolite.Compound objects
cps = sbml.compounds
# filter for compounds that are boundary compounds
cpds = {}
for c in cps:
    if not cps[c].uptake_secretion:
        cpds[c]  = cps[c]

if args.v:
    sys.stderr.write("List of 'cpds' list: {}\n".format(len(cpds)))

# read the media file
media = read_media_file(args.m)

# correct some of the media names so that they match the compounds in the
# SBML file. This is why we should use compound IDs and not names!
newmedia = set()
for m in media:
    intracellular_m = copy.copy(m)
    intracellular_m.location = 'c'
    if str(intracellular_m) in cpds:
        newmedia.add(m)
    else:
        testname = str(intracellular_m).replace('-', '_')
        if testname in cpds:
            newname = m.name.replace('-', '_')
            newloc = m.location
            newmedia.add(Compound(newname, newloc))
        else:
            testname = str(intracellular_m).replace('+', '')
            if testname in cpds:
                newname = m.name.replace('+', '')
                newloc = m.location
                newmedia.add(Compound(newname, newloc))
            else:
                newmedia.add(m)

media = newmedia


# adjust the lower bounds of uptake secretion reactions for things that are not in the media
for u in uptake_secretion_reactions:
    is_media_component = False
    for c in uptake_secretion_reactions[u].all_compounds():
        if c in media:
            is_media_component = True
    if not is_media_component:
        rxn[u].lower_bound = 0.0
        uptake_secretion_reactions[u].lower_bound = 0.0


# run the fba
status, value, growth = run_fba(cpds, rxn, reactions_to_run, media, biomass_equation, uptake_secretion_reactions, args.v)
sys.stdout.write("The FBA completed with value; {} and growth: {}\n".format(value, growth))