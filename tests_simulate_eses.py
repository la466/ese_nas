import unittest
import simulate_eses as se
import generic as gen

class Test_simulate_eses(unittest.TestCase):

    def test_get_dinucleotides_reg(self):
        motif_set = gen.read_many_fields("test_data/test_get_dinucleotides_reg/motif_set.txt", ",")
        motif_set = [i[0] for i in motif_set]
        expected = gen.read_many_fields("test_data/test_get_dinucleotides_reg/expected_dinucleotides.txt", ",")
        expected = [i[0] for i in expected]
        observed = se.get_dinucleotides(motif_set)
        self.assertEqual(observed, expected)

    def test_get_dinucleotides_contact(self):
        motif_set = gen.read_many_fields("test_data/test_get_dinucleotides_concat/motif_set.txt", ",")
        motif_set = [i[0] for i in motif_set]
        expected = gen.read_many_fields("test_data/test_get_dinucleotides_concat/expected_dinucleotides.txt", ",")
        expected = [i[0] for i in expected]
        observed = se.get_dinucleotides(motif_set, concat_motifs=True)
        self.assertEqual(observed, expected)

    def test_generate_motifs(self):
        motif_set = gen.read_many_fields("test_data/test_generate_motifs/motif_set.txt", ",")
        motif_set = [i[0] for i in motif_set]
        dinucleotides = gen.read_many_fields("test_data/test_generate_motifs/dinucleotides.txt", ",")
        dinucleotides = [i[0] for i in dinucleotides]
        expected = gen.read_many_fields("test_data/test_generate_motifs/expected_simulated_motifs.txt", ",")
        expected = [i[0] for i in expected]
        observed = se.generate_motifs(motif_set, dinucleotides, seed=5)
        self.assertEqual(observed, expected)
