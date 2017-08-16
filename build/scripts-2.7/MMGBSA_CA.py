#!/usr/bin/python

"""
Created on Tue Oct 25 15:19:00 2016

@author: noel
"""
import os
import sys
import em.energy.MMGBSA_CA_L as MCL
import optparse

def main():
    usage = "usage: %prog [options] arg"
    d = "This program reads a CRD and PSF file that have been generated by CHARMM and generates a Supper Structure.\It \
then generates energies from the coordinates and parameters. The CSV file will take the namen of the CRD file without t\
he suffix.\n NOTE: The term Raw-MMGBSA refers to self and pair free energies for individual amino acid components. The \
term delta-MMGBSA refers to free energy diferences between the bound and the unbound states for each component."
    opt_parser = optparse.OptionParser(usage,description=d)

    group = optparse.OptionGroup(opt_parser, "Generates de delta_MMGBSA between the bound and unbound state.")
    group.add_option("--deltabind", action="store_true", help="Generates a file with delta (bound -unbound) MMGBSA CA o\
#f binding.")
    group.add_option("--self1",type="str",help="Path to MMGBSA self-electrostatics file.")
    group.add_option("--pair1",type="str",help="Path to MMGBSA pair electrostatics file.")
    opt_parser.add_option_group(group)

    group = optparse.OptionGroup(opt_parser, "Raw Binding MMGBSA Option","This calculates MMGBSA energies from self and\
 pair-wise component contributions. It is 'RAW' because it only gives self and pair energies for the component and not \
an actual delta-MMGBSA binding energy.")
    group.add_option("--CAbind", action="store_true", help="Calculate binding-MMGBSA CA group.")
    group.add_option("--crd", type="str",help="Enter CRD file generated by CHARMM. Filename will is used as output suffix.")
    group.add_option("--psf", type="str",help="Enter PSF file generated by CHARMM in XPLOR format.")
    group.add_option("--gb", type="str",help="Enter GB Radii file generated by CHARMM.")
    group.add_option("--gbz", type="str",help="Enter GB Radii file generated by CHARMM, tranlated 500A in z-direction.")
    group.add_option("--sa", type="str",help="Enter Surface Area file generated by CHARMM.")
    group.add_option("--saz", type="str",help="Enter Surface Area file generated by CHARMM, tranlated 500A in z-direction.")
    group.add_option("--ver", action="store_true", default=False, help="Verbose output for debugging.")
    group.add_option("--mov", type="str",help="Chain to move for binding energy calcualtions. Enter one or more, \
                                               chain identifiers that will be displaced from the CRD file. \
                                               Ex: \"A\", or \"A,B\" separated by comas and in hard quotes.")
    group.add_option("--dis", type="str",help="Distance chain is move for binding energy calcualtions in Angstroms.")
    opt_parser.add_option_group(group)

    group = optparse.OptionGroup(opt_parser, "Initial Raw Sumamry Option","This histograms self and pair MMGBSA energie\
s as an initial overview of the values. It histograms contributions from GB, SA, EE, VDW.The default number of bins for\
 the histograms is that given by the max and min energies found divided by the cutoff. A cutoff is needed because most \
components' contributions to the energy are close to zero and can be discarted for further analysis. This summary will \
help find an appropriate cutoff. The cutoff is entered as a positive number, but it applies to both positive and negati\
ve energies, keeping energies grater thant a positive cutoff and lower thatn a negative cutoff.It generates other basic\
statistics. It also generates a plot of number of components vs. cutoff to guide the search for an optimal cutoff. The \
SUMMMARY IS OUTPUT TO THE TERMINAL, and to a TXT file.")
    group.add_option("--rawsum", action="store_true", help="Generates a raw summary from raw MMGBSA CA of binding.")
    group.add_option("--self2",type="str",help="Path to MMGBSA self-electrostatics file.")
    group.add_option("--pair2",type="str",help="Path to MMGBSA pair electrostatics file.")
    group.add_option("--cut",type="float",help="A cutoff value in kCal/mols.")
    group.add_option("--range",type="str",default="(-10,10,200):(-5,5,300)",help="RANge is a string with TWO tuples sep\
arated by a column ':'. The tuples have three elements (min,max,bins) for the min and max values for the histogram, and\
 the number of bins for the histogram. Ex: '(-10,10,200):(-5,5,300)' is the default. This gives flexibility to the user\
 to visualize the components' energy distributions for self and pair wise energies and select and appropriate cutoff. I\
f the labels cover the histogram, play with min and max until the histogram shows properly. Four histograms are output.\
 The first two are always output and cannot be modified. They correspond to distributions within the full range of ener\
gies, and distributions for the components' energies within the selected cutoff. The other two are '(-10,10,200):(-5,5,\
300)' by default or any specified values by the user. This option is not required.")
    opt_parser.add_option_group(group)
    options, args = opt_parser.parse_args()
############################################  Options Entered ##########################################################
    if options.deltabind:
        if options.CAbind:
            if options.rawsum:
                opt_parser.error("Two options can't be selected at the same time. Enter -h for help.")
    if options.CAbind:
        if options.rawsum:
            opt_parser.error("Two options can't be selected at the same time. Enter -h for help.")
############################################  Options Checked ##########################################################
    analysis = MCL.mmgbsa_ca_analysis(os.getcwd())
    if options.deltabind:
        if not os.path.exists(options.self1):
            opt_parser.error("Error: MMGBSA SELF file not found.\n Type --help for description and options.")
        if not os.path.exists(options.pair1):
            opt_parser.error("Error: MMGBSA PAIR file not found.\n Type --help for description and options.")
        analysis.mmgbsa_binding(options)
    if options.CAbind:
        if not os.path.exists(options.crd):
            opt_parser.error("Error: File path to CRD file does not exist.\n Type --help for description and options.")
        if not os.path.exists(options.psf):
            opt_parser.error("Error: File path to PSF file does not exist.\n Type --help for description and options.")
        if not os.path.exists(options.gb):
            opt_parser.error("Error: File path to gb file does not exist.\n Type --help for description and options.")
        if not os.path.exists(options.gbz):
            opt_parser.error("Error: File path to gbZ file does not exist.\n Type --help for description and options.")
        if not os.path.exists(options.sa):
            opt_parser.error("Error: File path to sa file does not exist.\n Type --help for description and options.")
        if not os.path.exists(options.saz):
            opt_parser.error("Error: File path to saZ file does not exist.\n Type --help for description and options.")
        if not options.mov:
            opt_parser.error("Error: Chain(s) to move not specified.\n Type --help for description and options.")
        if not options.dis:
            opt_parser.error("Error: Distance to move chains not specified.\n Type --help for description and options.")
        #print(options)
        analysis.mmgbsa_CA_bindingMatrix(options)
    if options.rawsum:
        if not os.path.exists(options.self2):
            opt_parser.error("Error: MMGBSA SELF file not found.\n Type --help for description and options.")
        if not os.path.exists(options.pair2):
            opt_parser.error("Error: MMGBSA PAIR file not found.\n Type --help for description and options.")
        if not options.cut:
            opt_parser.error("Error: Cutoff for energies not specified.\n Type --help for description and options.")
        analysis.mmgbsa_raw_summary(options)

if __name__ == '__main__':
    main()
