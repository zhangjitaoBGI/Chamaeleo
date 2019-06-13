"""
Name: YYC (Yin-Yang DNA Storage Code)

Reference: None

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) DNA encoding by YYC.
             (2) DNA decoding by YYC.

Advantages: (1) High compressibility, maximum compressibility to 1/2 of the original data.
            (2) Prevent repetitive motifs, like ATCGATCG...
            (3) Increase the number of sequence changes (1,536 cases), increasing data security.
"""

import random
import sys
import numpy

import methods.components.inherent as inherent
import methods.components.motif_friendly as motif_friendly
import methods.components.index_data as index_data
import utils.log as log
import utils.monitor as monitor


# noinspection PyUnresolvedReferences,PyMethodMayBeStatic
# PyUnusedLocal,PyProtectedMember,PyBroadException, PyArgumentList
# noinspection PyProtectedMember
class YYC:
    def __init__(self, base_reference=None, current_code_matrix=None, support_bases=None, support_spacing=0,
                 max_ratio=0.8, search_count=1):
        """
        introduction: The initialization method of YYC.

        :param base_reference: Correspondence between base and binary data (RULE 1).
                                Make sure that the first and third, and the second and fourth are equal, so there are only two cases:
                                [0, 0, 1, 1] or [1, 1, 0, 0].

        :param current_code_matrix: Conversion rule between base and binary data based on support base and current base (RULE 2).
                                     Label row is the support base, label col is the current base.
                                         A   T   C   G
                                     A   X1  Y1  X2  Y2
                                     T   X3  Y3  X4  Y4
                                     C   X5  Y5  X6  Y6
                                     G   X7  Y7  X8  Y8
                                     Make sure that Xn + Yn = 1 and Xn * Yn = 0, n is in [1, 8].

        :param support_bases: Base replenishment before official data.
                               Make sure that the count of support base must more than support spacing.
                               Make sure that the number range of each position is {0, 1, 2, 3}, reference base index.

        :param support_spacing: Spacing between support base and current base.
                                 When the support base is the front of the current base, the spacing is 0.

        :param max_ratio: The max ratio of 0 or 1.
                           When the (count/length) >= this parameter, we decide that this binary sequence is not good.

        """

        # Set default values for Rules 1 and 2
        if not base_reference:
            base_reference = [0, 0, 1, 1]
        if not current_code_matrix:
            current_code_matrix = [[1, 0, 1, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 0, 1]]
        if not support_bases:
            support_bases = [inherent.index_base.get(0)]

        # Detect parameters correctness
        self.__init_check__(support_bases, support_spacing, base_reference, current_code_matrix, max_ratio)

        # Assign input data to class variables
        self.base_reference = base_reference
        self.current_code_matrix = current_code_matrix
        self.support_bases = support_bases
        self.support_spacing = support_spacing
        self.max_ratio = max_ratio
        self.index_binary_length = 0
        self.file_size = 0
        self.search_count = search_count
        self.monitor = monitor.Monitor()

    def __init_check__(self, support_bases, support_spacing, base_reference, current_code_matrix, max_ratio):
        """
        introduction: The verification of initialization parameters.

        :param base_reference: Correspondence between base and binary data (RULE 1).
                                Make sure that the first and third, and the second and fourth are equal, so there are only 6 cases:
                                Make sure that Two of the bases are 1 and the other two are 0..

        :param current_code_matrix: Conversion rule between base and binary data based on support base and current base (RULE 2).
                                     Label row is the support base, label col is the current base.
                                         A   T   C   G
                                     A   X1  Y1  X2  Y2
                                     T   X3  Y3  X4  Y4
                                     C   X5  Y5  X6  Y6
                                     G   X7  Y7  X8  Y8
                                     Make sure that Xn + Yn = 1 and Xn * Yn = 0, n is in [1, 8].

        :param support_bases: Base replenishment before official data.
                               Make sure that the count of support base must more than support spacing.
                               Make sure that the number range of each position is {0, 1, 2, 3}, reference base index

        :param support_spacing: Spacing between support base and current base.
                                 Make sure that support_spacing must less than the length of support_bases

        :param max_ratio: The max ratio of 0 or 1.
                           Make sure that max ratio must more than 50% and less than 100%..

        """
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Create the YYC method.")

        # Check support bases
        for index in range(len(support_bases)):
            if support_bases[index] != 'A' and support_bases[index] != 'T' and support_bases[index] != 'C' and \
                            support_bases[index] != 'G':
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Only A, T, C, and G can be included in the support bases, "
                           "and the support bases[" + str(index) + "] has entered " + str(support_bases[index] + "!"))
        if len(support_bases) < support_spacing + 1:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The count of support base needs more than support spacing!")

        # Check base reference (rule 1)
        for index in range(len(base_reference)):
            if base_reference[index] != 0 and base_reference[index] != 1:
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Only 0 and 1 can be included in the base reference, "
                           "and base_reference[" + str(index) + "] has entered " + str(base_reference[index] + "!"))
        if sum(base_reference) != 2:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "Wrong correspondence between base and binary data!")

        # Check current code matrix (rule 2)
        for row in range(len(current_code_matrix)):
            for col in range(len(current_code_matrix[row])):
                if current_code_matrix[row][col] != 0 and current_code_matrix[row][col] != 1:
                    log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                               "Only 0 and 1 can be included in the current code matrix, "
                               "and the current code matrix [" + str(index) + "] has entered " + str(
                                   base_reference[index] + "!"))
        for row in range(len(current_code_matrix)):
            for col in range(0, len(current_code_matrix[row]) - 1, 2):
                if current_code_matrix[row][col] + current_code_matrix[row][col + 1] == 1 \
                        and current_code_matrix[row][col] * current_code_matrix[row][col + 1] == 0:
                    continue
                else:
                    log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                               "Wrong current code matrix, "
                               "the error locations are [" + str(row) + ", " + str(col) + "] and [" + str(
                                   row) + ", " + str(col) + "]! "
                                                           "Rules are that they add up to 1 and multiply by 0.")

        # Check max ratio
        if max_ratio <= 0.5 or max_ratio >= 1:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "Wrong max ratio (" + str(max_ratio) + ")!")

# ================================================= encode part ========================================================

    def encode(self, matrix, file_size, need_index):
        """
        introduction: Encode DNA motifs from the data of binary file.

        :param matrix: Generated binary two-dimensional matrix.
                        The data of this matrix contains only 0 or 1 (non-char).
                        Type: int or bit.

        :param file_size: The size of the file corresponds to this matrix.

        :param need_index: Declare whether the binary sequence indexes are required in the DNA motifs.
                            Type: bool.

        :return dna_motifs: The DNA motif of len(matrix) rows.
                             Type: list(list(char)).
        """

        self.file_size = file_size
        self.index_binary_length = int(len(str(bin(len(matrix)))) - 2)

        self.monitor.restore()
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Separate good data from bad data.")
        good_datas, bad_datas = self.__divide_library__(matrix, need_index)

        self.monitor.restore()
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Random pairing and friendly testing.")
        datas = self.__pairing__(good_datas, bad_datas)

        self.monitor.restore()
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Convert to DNA motif string set.")
        dna_motifs = self.__synthesis_motifs__(datas)

        return dna_motifs

    def __divide_library__(self, matrix, need_index):
        """
        introduction: Separate good and bad data from total data, and splice index and data as a list

        :param matrix: Generated binary two-dimensional matrix
                       The data of this matrix contains only 0 or 1 (non-char).
                       Type: int or bit

        :returns good_datas, bad datas: good and bad data from total data
                                        Type: list(int)
        """

        bad_indexs = []
        for row in range(len(matrix)):
            if numpy.sum(matrix[row]) > len(matrix[row]) * self.max_ratio or numpy.sum(matrix[row]) < len(
                    matrix[row]) * (1 - self.max_ratio):
                bad_indexs.append(row)

        if len(matrix) < len(bad_indexs) * 5:
            log.output(log.WARN, str(__name__), str(sys._getframe().f_code.co_name),
                       "There may be a large number of motifs that are difficult to use. "
                       "We recommend stopping and modifying the rules.")

        if len(bad_indexs) == 0 and len(matrix) == 0:
            return None, None
        elif len(bad_indexs) == 0:
            good_datas = []
            for row in range(len(good_datas)):
                self.monitor.output(row, len(good_datas))
                if need_index:
                    good_datas.append(index_data.connect(row, matrix[row], self.index_binary_length))
                else:
                    good_datas.append(matrix[row])
            return good_datas, None
        elif len(bad_indexs) == len(matrix):
            bad_datas = []
            for row in range(len(bad_datas)):
                self.monitor.output(row, len(bad_datas))
                if need_index:
                    bad_datas.append(index_data.connect(row, matrix[row], self.index_binary_length))
                else:
                    bad_datas.append(matrix[row])
            return None, bad_datas
        else:
            good_datas = []
            bad_datas = []
            for row in range(len(matrix)):
                self.monitor.output(row, len(matrix))
                if row in bad_indexs:
                    if need_index:
                        bad_datas.append(index_data.connect(row, matrix[row], self.index_binary_length))
                    else:
                        bad_datas.append(matrix[row])
                else:
                    if need_index:
                        good_datas.append(index_data.connect(row, matrix[row], self.index_binary_length))
                    else:
                        good_datas.append(matrix[row])

            return good_datas, bad_datas

    def __pairing__(self, good_datas, bad_datas):
        """
        introduction: Match good data with bad data, to ensure that the overall data is better.
                      If there are only good or bad data left, they will pair themselves up.

        :param good_datas: Generated binary two-dimensional matrix, the repetition rate of 0 or 1 is related low.
                            Type: Two-dimensional list(int)

        :param bad_datas: Generated binary two-dimensional matrix, the repetition rate of 0 or 1 is related high.
                           Type: Two-dimensional list(int)

        :returns datas: Matched results
                         Type: Two-dimensional list(int)
        """

        datas = []
        good_indexs = None
        bad_indexs = None
        if good_datas is not None and bad_datas is not None:
            good_indexs = set(str(i) for i in range(len(good_datas)))
            bad_indexs = set(str(i) for i in range(len(bad_datas)))
        elif good_datas is None and bad_datas is not None:
            good_indexs = set(str(i) for i in range(0))
            bad_indexs = set(str(i) for i in range(len(bad_datas)))
        elif good_datas is not None and bad_datas is None:
            good_indexs = set(str(i) for i in range(len(good_datas)))
            bad_indexs = set(str(i) for i in range(0))
        else:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "YYC did not receive matrix data!")

        for index in range(0, len(good_datas) + len(bad_datas), 2):
            self.monitor.output(index, len(good_datas) + len(bad_datas))
            if index < len(good_datas) + len(bad_datas) - 1:
                if len(good_indexs) != 0 and len(bad_indexs) != 0:
                    for search_index in range(self.search_count):
                        good_index = int(good_indexs.pop())
                        bad_index = int(bad_indexs.pop())
                        if motif_friendly.friendly_check(
                                self.__list_to_motif__(good_datas[good_index], bad_datas[bad_index])) \
                                or search_index == self.search_count - 1:
                            datas.append(good_datas[good_index])
                            datas.append(bad_datas[bad_index])
                            break
                        else:
                            good_indexs.add(str(good_index))
                            bad_indexs.add(str(bad_index))
                            index -= 1
                elif len(bad_indexs) == 0:
                    for search_index in range(self.search_count):
                        good_index1 = int(good_indexs.pop())
                        good_index2 = int(good_indexs.pop())
                        if motif_friendly.friendly_check(
                                self.__list_to_motif__(good_datas[good_index1], good_datas[good_index2])) \
                                or search_index == self.search_count - 1:
                            datas.append(good_datas[good_index1])
                            datas.append(good_datas[good_index2])
                            break
                        else:
                            good_indexs.add(str(good_index1))
                            good_indexs.add(str(good_index2))
                            index -= 1
                elif len(good_indexs) == 0:
                    for search_index in range(self.search_count):
                        bad_index1 = int(bad_indexs.pop())
                        bad_index2 = int(bad_indexs.pop())
                        if motif_friendly.friendly_check(
                                self.__list_to_motif__(bad_datas[bad_index1], bad_datas[bad_index2])) \
                                or search_index == self.search_count - 1:
                            datas.append(bad_datas[bad_index1])
                            datas.append(bad_datas[bad_index2])
                        else:
                            bad_indexs.add(str(bad_index1))
                            bad_indexs.add(str(bad_index2))
                            index -= 1
                else:
                    log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                               "Pairing wrong in YYC pairing!")
            else:
                datas.append(
                    good_datas[int(good_indexs.pop())] if len(good_indexs) != 0 else bad_datas[int(bad_indexs.pop())])

        del good_indexs, good_datas, bad_indexs, bad_datas

        return datas

    def __synthesis_motifs__(self, datas):
        """
        introduction: Synthesis motifs by two-dimensional data set.

        :param datas: Original data from file.
                       Type: Two-dimensional list(int).

        :return dna_motifs: The DNA motifs from the original data set
                             Type: One-dimensional list(string).
        """

        dna_motifs = []
        for row in range(0, len(datas), 2):
            self.monitor.output(row, len(datas))
            if row < len(datas) - 1:
                dna_motifs.append(self.__list_to_motif__(datas[row], datas[row + 1]))
            else:
                dna_motifs.append(self.__list_to_motif__(datas[row], None))

        del datas

        return dna_motifs

    def __list_to_motif__(self, upper_list, lower_list):
        """
        introduction: from two binary list to DNA motif

        :param upper_list: The upper binary list
                            Type: List(byte)

        :param lower_list: The lower binary list
                            Type: List(byte)

        :return: a DNA motif
                  Type: List(char)
        """

        dna_motif = []

        for col in range(len(upper_list)):
            if lower_list is not None:
                if col > self.support_spacing:
                    dna_motif.append(self.__binary_to_base__(upper_list[col], lower_list[col],
                                                             dna_motif[col - (self.support_spacing + 1)]))
                else:
                    dna_motif.append(self.__binary_to_base__(upper_list[col], lower_list[col],
                                                             self.support_bases[col]))
            else:
                if col > self.support_spacing:
                    dna_motif.append(self.__binary_to_base__(upper_list[col], random.randint(0, 1),
                                                             dna_motif[col - (self.support_spacing + 1)]))
                else:
                    dna_motif.append(self.__binary_to_base__(upper_list[col], random.randint(0, 1),
                                                             self.support_bases[col]))
        return dna_motif

    def __binary_to_base__(self, upper_bit, lower_bit, support_base):
        """
        introduction: Get one base from two binary, based on the rules of YYC.

        :param upper_bit: The upper bit, used to identify two of the four bases by RULE 1.

        :param lower_bit: The lower bit, one of the parameters,
                           used to identify one of the two bases by RULE 2, after RULE 1.

        :param support_base: The base for support to get base in current position, one of the parameters,
                              used to identify one of the two bases by RULE 2, after RULE 1.

        :return one_base: The base in current position.
                           Type: int
        """

        current_options = []
        for index in range(len(self.base_reference)):
            if self.base_reference[index] == int(upper_bit):
                current_options.append(index)

        one_base = None
        if self.current_code_matrix[inherent.base_index.get(support_base)][current_options[0]] == int(lower_bit):
            one_base = inherent.index_base[current_options[0]]
        else:
            one_base = inherent.index_base[current_options[1]]

        return one_base

# ================================================= decode part ========================================================

    def decode(self, dna_motifs, has_index):
        """
        introduction: Decode DNA motifs to the data of binary file.

        :param dna_motifs: The DNA motif of len(matrix) rows.
                            Type: One-dimensional list(string).

        :param has_index: Declare whether the DNA motifs contain binary sequence indexes.
                           Type: bool.

        :return matrix: The binary matrix corresponding to the dna motifs.
                         Type: Two-dimensional list(int).
        """

        if not dna_motifs:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "DNA motif string set is None")

        self.monitor.restore()
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Convert DNA motifs to binary matrix.")
        temp_matrix = self.__convert_binaries__(dna_motifs)

        if has_index:
            self.monitor.restore()
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Divide index and data from binary matrix.")
            indexs, datas = index_data.divide_all(temp_matrix, self.index_binary_length)

            self.monitor.restore()
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Restore the disrupted data order.")
            matrix = index_data.sort_order(indexs, datas)
        else:
            matrix = temp_matrix

        self.monitor.restore()
        return matrix

    def __convert_binaries__(self, dna_motifs):
        """
        introduction: Convert DNA motifs to binary matrix.
                      One DNA motif <-> two-line binaries.

        :param dna_motifs: The DNA motif of len(matrix) rows.
                            Type: One-dimensional list(string).

        :return matrix: The binary matrix corresponding to the dna motifs.
                         Type: Two-dimensional list(int).
        """

        matrix = []

        for row in range(len(dna_motifs)):
            self.monitor.output(row, len(dna_motifs))
            upper_row_datas, lower_row_datas = self.__dna_motif_to_binaries__(dna_motifs[row])
            matrix.append(upper_row_datas)
            matrix.append(lower_row_datas)

        del dna_motifs

        return matrix

    def __dna_motif_to_binaries__(self, dna_motif):
        """
        introduction: Convert one DNA motif to two-line binary list.

        :param dna_motifs: The DNA motif of len(matrix) rows.
                            Type: One-dimensional list(string).

        :returns upper_row_list, lower_row_list: The binary list corresponding to the dna motif.
                                                Type: One-dimensional list(int).
        """

        upper_row_list = []
        lower_row_list = []

        for col in range(len(dna_motif)):
            if col > self.support_spacing:
                upper_binary, lower_binary = self.__base_to_binary__(dna_motif[col],
                                                                     dna_motif[col - (self.support_spacing + 1)])
                upper_row_list.append(upper_binary)
                lower_row_list.append(lower_binary)
            else:
                upper_binary, lower_binary = self.__base_to_binary__(dna_motif[col], self.support_bases[col])
                upper_row_list.append(upper_binary)
                lower_row_list.append(lower_binary)

        return upper_row_list, lower_row_list

    def __base_to_binary__(self, current_base, support_base):
        """
        introduction: Get two bit from current base and support base, based on the rules of YYC.

        :param current_base: The upper bit, used to identify the upper bit by RULE 1.

        :param support_base: The base for support to get base in current position, one of the parameters (with current base),
                              used to identify the lower bit by RULE 2.

        :returns upper_bit lower_bit: The upper bit and lower bit.
                                       Type: int, int
        """
        upper_bit = self.base_reference[inherent.base_index[current_base]]
        lower_bit = self.current_code_matrix[inherent.base_index[support_base]][inherent.base_index[current_base]]
        return upper_bit, lower_bit
