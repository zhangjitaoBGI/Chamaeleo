"""
Name: Functional testing for YYC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The reliability of Yin-Yang code transformation
"""

import random
import unittest

from Chamaeleo.methods import yyc


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.tool = yyc.YYC()
        # Rule 495
        self.tool.base_reference = [0, 1, 0, 1]
        self.tool.current_code_matrix = [[1, 1, 0, 0], [1, 0, 0, 1], [1, 1, 0, 0], [1, 1, 0, 0]]
        self.tool.support_bases = ["A"]
        self.tool.support_spacing = 0
        self.tool.max_ratio = 0.8
        self.tool.search_count = 1

        self.test_upper_list = [random.randint(0, 1) for _ in range(120)]
        self.test_lower_list = [random.randint(0, 1) for _ in range(120)]

    def test_list_to_motif(self):
        dna_motif = self.tool.__list_to_motif__(
            self.test_upper_list, self.test_lower_list
        )
        self.assertEqual(
            dna_motif,
            [
                "T",
                "G",
                "A",
                "C",
                "A",
                "T",
                "T",
                "G",
                "A",
                "T",
                "G",
                "A",
                "G",
                "G",
                "G",
                "C",
                "C",
                "G",
                "C",
                "A",
                "G",
                "C",
                "C",
                "G",
                "T",
                "G",
                "T",
                "C",
                "G",
                "T",
                "C",
                "C",
                "G",
                "G",
                "A",
                "C",
                "G",
                "A",
                "T",
                "C",
                "A",
                "G",
                "C",
                "T",
                "T",
                "C",
                "T",
                "G",
                "A",
                "A",
                "T",
                "C",
                "C",
                "C",
                "C",
                "T",
                "G",
                "G",
                "G",
                "T",
                "C",
                "A",
                "G",
                "T",
                "C",
                "C",
                "T",
                "C",
                "T",
                "C",
                "T",
                "T",
                "T",
                "G",
                "G",
                "T",
                "T",
                "G",
                "G",
                "A",
                "T",
                "A",
                "T",
                "C",
                "A",
                "C",
                "G",
                "G",
                "T",
                "T",
                "C",
                "T",
                "A",
                "G",
                "C",
                "G",
                "C",
                "G",
                "G",
                "C",
                "T",
                "G",
                "A",
                "C",
                "A",
                "T",
                "G",
                "T",
                "C",
                "G",
                "C",
                "C",
                "A",
                "C",
                "T",
                "G",
                "T",
                "C",
                "C",
                "A"
            ],
        )

    def test_motif_to_list(self):
        upper_row_list, lower_row_list = self.tool.__dna_motif_to_binaries__(
            [
                "T",
                "G",
                "A",
                "C",
                "A",
                "T",
                "T",
                "G",
                "A",
                "T",
                "G",
                "A",
                "G",
                "G",
                "G",
                "C",
                "C",
                "G",
                "C",
                "A",
                "G",
                "C",
                "C",
                "G",
                "T",
                "G",
                "T",
                "C",
                "G",
                "T",
                "C",
                "C",
                "G",
                "G",
                "A",
                "C",
                "G",
                "A",
                "T",
                "C",
                "A",
                "G",
                "C",
                "T",
                "T",
                "C",
                "T",
                "G",
                "A",
                "A",
                "T",
                "C",
                "C",
                "C",
                "C",
                "T",
                "G",
                "G",
                "G",
                "T",
                "C",
                "A",
                "G",
                "T",
                "C",
                "C",
                "T",
                "C",
                "T",
                "C",
                "T",
                "T",
                "T",
                "G",
                "G",
                "T",
                "T",
                "G",
                "G",
                "A",
                "T",
                "A",
                "T",
                "C",
                "A",
                "C",
                "G",
                "G",
                "T",
                "T",
                "C",
                "T",
                "A",
                "G",
                "C",
                "G",
                "C",
                "G",
                "G",
                "C",
                "T",
                "G",
                "A",
                "C",
                "A",
                "T",
                "G",
                "T",
                "C",
                "G",
                "C",
                "C",
                "A",
                "C",
                "T",
                "G",
                "T",
                "C",
                "C",
                "A",
            ]
        )
        self.assertEqual(upper_row_list, self.test_upper_list)
        self.assertEqual(lower_row_list, self.test_lower_list)
