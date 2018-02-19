import itertools as it
import re
import numpy as np

def make_simulants(motifs, n_sim, output_file_name = None, retro = False, mono = False, no_duplicates = False, remove_stops = False, remove_existing = False, cap_runs = False, exclude = None, seed = None, concat = True):
    '''
    Given a set of motifs, generate n_sim sets of simulants with the same over-all dinucleotide frequencies.
    motifs: a list of strings (the motifs for which you want to generate simulants)
    n_sim: number of simulant sets required
    mono: use mono- rather than dinucleotide frequencies
    no_duplicates: don't allow duplicates within simulant sets
    remove_stops: don't allow simulants that contain stop codons
    remove_existing: don't allow simulants to coincide with motifs in the true set
    cap_runs: don't allow mononucleotide runs whose length exceeds that of the longst run of that base in the true motifs
    exclude: don't allow any of the motifs within this list
    seed: supply a seed for the PRNG
    concat: concatenate the true motifs before extracting dinucleotides
    '''

    print('running simulations')
    if cap_runs:
        longest_runs_numbers = get_longest_run(motifs)
        longest_runs_strings = ["".join([base for i in range(longest_runs_numbers[base] + 1)]) for base in longest_runs_numbers]
    motifs = [list(i) for i in motifs]
    nts = flatten(motifs)
    if mono:
        dints = flatten(motifs)
    else:
        if concat:
            dints = []
            #grab all the dinucleotides in the two reading frames
            for i in range(0, len(nts) - 1, 2):
                dints.append([nts[i], nts[i+1]])
            for i in range(1, len(nts) - 1, 2):
                dints.append([nts[i], nts[i+1]])
        else:
            dints = []
            for motif in motifs:
                for i in range(0, len(motif) - 1, 2):
                    dints.append([motif[i], motif[i+1]])
                for i in range(1, len(motif) - 1, 2):
                    dints.append([motif[i], motif[i+1]])
    # print(dints)
    # #right now you have a list of lists. Turn that into a list of strings where each string is one dinucleotide.
    dints = ["".join(i) for i in dints]
    print(dints)
    # simulants = [["" for j in motifs] for i in range(n_sim)]
    # for i, j in enumerate(motifs):
    #     if mono:
    #         dint_number = len(j)
    #     else:
    #         dint_number = len(j) // 2
    #     if len(j) % 2 == 0:
    #         even = True
    #     else:
    #         even = False
    #     for k in range(n_sim):
    #         found = False
    #         while not found:
    #             problem = False
    #             sim_motif = []
    #             for l in range(dint_number):
    #                 if seed:
    #                     random.seed(a = seed)
    #                     seed = seed + 1
    #                 sim_motif.append(random.choice(dints))
    #             #if the length of the motif is not an even number, add on a random mononucleotide from a bag made previously.
    #             if (not even) and (not mono):
    #                 sim_motif.append(random.choice(nts))
    #             sim_motif = "".join(sim_motif)
    #             if remove_stops:
    #                 if "TAA" in sim_motif or "TAG" in sim_motif or "TGA" in sim_motif:
    #                     problem = True
    #             if remove_existing:
    #                 if list(sim_motif) in motifs:
    #                     problem = True
    #             if cap_runs:
    #                 for run in longest_runs_strings:
    #                     if run in sim_motif:
    #                         problem = True
    #             if no_duplicates:
    #                 if sim_motif in simulants[k]:
    #                     problem = True
    #             if exclude:
    #                 if sim_motif in exclude:
    #                     problem = True
    #             if not problem:
    #                 found = True
    #                 simulants[k][i] = sim_motif
    # if output_file_name:
    #     if not retro:
    #         with open(output_file_name, "w") as file:
    #             for i in range(n_sim):
    #                 file.write("|".join(simulants[i]))
    #                 file.write("\n")
    #     else:
    #         for i in range(n_sim):
    #             with open("{0}/fake_ESEs_{1}.txt".format(output_file_name, i), "w") as file:
    #                 file.write("\n".join(simulants[i]))
    #                 file.write("\n")
    # return(simulants)



motifs = ['TCGCCG', 'GCAAGA', 'CGTCGA', 'CGTCGC', 'TCGACG', 'GACGGA', 'TCGGCG']

def get_dinucleotides(motifs, concat_motifs=None):

	print(motifs)

	dinucleotides = []

	if concat_motifs:
		#concat the motifs to a string
		motif_string = "".join([i for i in motifs])
		#compile the regex to find all instances of two characters
		dint_regex = re.compile(".{2}")
		#search for all dnts in the two reading frames
		dinucleotides.extend(re.findall(dint_regex, motif_string))
		dinucleotides.extend(re.findall(dint_regex, motif_string[1:]))
	else:
		motifs = [list(i) for i in motifs]
		for motif in motifs:
			#search for all dnts in the two reading frames
			for i in range(0, len(motif)-1, 2):
				dinucleotides.append([motif[i], motif[i+1]])
			for i in range(1, len(motif)-1, 2):
				dinucleotides.append([motif[i], motif[i+1]])
		#join the nts comprising a dint back together
		dinucleotides = ["".join(i) for i in dinucleotides]

	return(dinucleotides)

def generate_motifs(motifs, dinucleotides, seed):
	# simulants = [["" for j in motifs] for i in range(1)]
	# print(simulants)

	#set the randomisation seed
	if seed:
		np.random.seed(seed)
	else:
		rp.random.seed()

	created_simulants = []
	for i, motif in enumerate(motifs):
		#get the number of required dints to create simulant
		required_dinucleotides = len(motif) // 2
		created = False
		new_simulant = []
		while not created:
			#pick the number of required dinucleotides
			new_simulant.extend(np.random.choice(dinucleotides, required_dinucleotides))
			if new_simulant not in created_simulants:
				created = True
				created_simulants.append(new_simulant)

	simulants = ["".join(i) for i in created_simulants]
	return(simulants)

# create_simulated_motifs(motifs)
