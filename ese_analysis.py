import simulate_eses as se
import generic as gen

ese_sets = {
	# "ESR": "./data/ESR.txt",
	# "Ke400_ESEs": "./data/Ke400_ESEs.txt",
	# "PESE": "./data/PESE.txt",
	# "RESCUE": "./data/RESCUE.txt",
	# "INT3": "./data/CaceresHurstESEs_INT3.txt"
	"RBP_motifs": "./data/RBP_motifs.txt"
}

for ese_set in ese_sets:
	print('Starting {0} set.'.format(ese_set))
	#create output files
	simulated_set_output = "output_data/{0}_simulants.txt".format(ese_set)
	output_file = "output_data/{0}_stop_counts.csv".format(ese_set)
	#get motifs
	motifs = gen.read_many_fields(ese_sets[ese_set], ",")
	motifs = [i[0] for i in motifs[1:]]
	#get the number of stop codons found in the real set
	real_count = se.get_stop_codon_count(motifs)
	#generate simulated motifs using motif set
	print('Simulating {0} set.'.format(ese_set))
	se.generate_motifs_sets(motifs, 10000, output_file=simulated_set_output)
	simulated_motif_sets = gen.read_many_fields(simulated_set_output, "|")
	with open(output_file, "w") as output:
		output.write('id,stop_count\n')
		output.write('real,{0}\n'.format(real_count))
		for i, simulated_set in enumerate(simulated_motif_sets):
			stop_count = se.get_stop_codon_count(simulated_set)
			output.write('{0},{1}\n'.format(i+1, stop_count))
