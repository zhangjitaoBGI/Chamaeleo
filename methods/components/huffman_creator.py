"""
Name: Huffman creator

Coder: QianLong ZHUANG (BGI-Research)[V1],  HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): Customize Huffman tree based on the bit matrix
"""

import re


# noinspection PyTypeChecker
def get_map(bit_matrix, size=None, multiple=2):
    """
    introduction: Customize Huffman tree based on the bit matrix.

    :param bit_matrix: Bit matrix, containing only 0,1.
                        Type: Two-dimensional list(int)

    :param size: File size corresponding to the matrix.

    :param multiple: Number of branches constructed (decimal semi-octets).

    :return tree: Byte-based (256) Huffman tree.
    """

    if size is None:
        size = len(bit_matrix) * len(bit_matrix[0])

    # Replace the bit matrix with one-dimensional decimal byte list
    decimal_list = __get_decimal_list__(bit_matrix, size)

    # Store elements and their weights
    weight = {}
    # Store elements and their codes
    code = {}
    # Recorder, prepare for the following screening of valid keys
    _node = lambda i: "_" + str(i).zfill(3)
    for one_byte in decimal_list:
        # Create weight values for each element
        if _node(one_byte) in weight:
            weight[_node(one_byte)] += 1
        else:
            # Set the initial value of the code
            code[_node(one_byte)] = ""
            weight[_node(one_byte)] = 1

    for one_byte in range(1, multiple - 1):
        # Add impossible elements to ensure normal combination and close as one element
        if (len(weight) - 1) % (multiple - 1) == 0:
            break
        else:
            weight['_' * one_byte] = 0
    weight_list = list(weight.items())

    for index in range(0, (len(weight) - 1) // (multiple - 1)):
        weight_list = sorted(weight_list, key=lambda x: x[0])
        weight_list = sorted(weight_list, key=lambda x: x[1])
        # Combine the previous terms into one term
        item = str(index).zfill(3)
        weight = 0
        # Add Huffman coding and form new combinations
        for branch in range(0, multiple):
            item += weight_list[branch][0]
            weight += weight_list[branch][1]
            # Add headers to each item of the previous items.
            for index_item in re.findall(r"_\d{3}", weight_list[branch][0]):
                code[index_item] = str(multiple - branch - 1) + code[index_item]
        new = [(item, weight)]
        weight_list = weight_list[multiple:] + new

    dictionary = dict([int(key[1:]), value] for key, value in code.items())

    tree = []
    for index in range(256):
        tree.append(dictionary.get(index))

    return tree


# noinspection PyUnusedLocal
def __get_decimal_list__(bit_matrix, size):
    """
    introduction: Decimal list generated by the bit matrix.

    :param bit_matrix: Bit matrix, containing only 0,1.
                        Type: Two-dimensional list(int)

    :param size: File size corresponding to the matrix.

    :return decimal_list: Decimal list.
                           Type: One-dimensional list(int)
    """
    decimal_list = []

    bit_index = 0
    temp_byte = 0
    for row in range(len(bit_matrix)):
        for col in range(len(bit_matrix[0])):
            bit_index += 1
            temp_byte *= 2
            temp_byte += bit_matrix[row][col]
            if bit_index == 8:
                if size >= 0:
                    decimal_list.append(int(temp_byte))
                    size -= 1
                bit_index = 0
                temp_byte = 0

    return decimal_list