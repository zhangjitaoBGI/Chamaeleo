# Read Before You Want to Make a Contribution
**Chamaeleo** is currently the only library focused on the coding and decoding methods for DNA storage.
We hope to provide a readable, robust and high-performance learning and use framework for researchers and engineers.
We very much welcome your participation and dedicate our strength to this community.

## Language in USE
We use **Python3.5** to develop the entire kit currently.

## Package in USE
The packages we are calling now is as follows:

- [x] sys
- [x] os
- [x] random
- [x] math
- [x] struct
- [x] datetime
- [x] numpy
- [x] pickle


If you have other packages, Please add them here.

When choosing the external package you need, you need to consider the problems caused by different systems and focus on the reliability of the source of the package.
For example, the Windows version of Python has no "termios" module.
We do not want situations where we cannot develop or use this kit because of the external packages.
In addition, some non-robust external packages may lead to instability or even collapse of the kit.

## Coding Specification
### Document Header Annotation Specification
The beginning of the file needs to contain several information:
(1) Name, (2) Coder, (3) Current Version, and (4) Function(s).

A macro overview of a document is necessary, which helps us to know what tasks this document has accomplished.
Among them, the "Name" section can contain the papers we quoted or other references.
This operation will help people with learning needs to trace back to the principles of methods.


A simple example is shown below:

```python
"""
Name: YYC(Ying-Yang DNA Storage Code)

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) DNA encoding by YYC.
             (2) DNA decoding by YYC.

Advantages: (1) high compressibility, maximum compressibility to 1/2 of the original data.
            (2) preventing repetitive motifs, like ATCGATCG...
            (3) increase the number of sequence changes (1,536 cases), increasing data security.
"""
```

### Function Header Annotation Specification
Unless the construction and reading of the function is very simple, we need to complete the annotation of the function header.
This is very important for cooperative development.
Usually, the annotation includes the purpose of the function, the interpretation and constraints of the input parameters, and the necessary information of the return production.


Two simple example is shown below:
```python
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
```

and another is:

```python
"""
introduction: Separate good and bad data from total data, and splice index and data as a list

:param matrix: Generated binary two-dimensional matrix
               The data of this matrix contains only 0 or 1 (non-char).
               Type: int or bit

:returns good_datas, bad datas: good and bad data from total data
                                Type: list(int)
"""
```

### Process Output Specification
Part of the process may require a long loading time.
We recommend that you be able to monitor the completion time using **monitor.py** objects under folder **utils**.

The specific usage is as follows:

```python
import utils.monitor as monitor

monitor = monitor.Monitor()
# do something
length = 1000000000000
for index in range(length):
    monitor.output(index, length)
    # do something
```

### Log Output Specification
We want you to print each core step to the console through **log.py**  in folder **utils**.
This helps us understand what steps a macro approach takes.

The specific usage is as follows:

```python
import sys
import utils.log as log

log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
           "Restore the disrupted data order.")

log.output(log.WARN, str(__name__), str(sys._getframe().f_code.co_name),
           "There may be a large number of motifs that are difficult to use. "
           "We recommend stopping and modifying the rules.")

log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
           "The file selection operation was not performed correctly. Please complete the operation again!")
```
We have declared three types available now: NORMAL, WARN, and ERROR.
If the type is ERROR, we will end this program immediately.
- If the type is NORMAL, print normal.
- If the type is WARN, print yellow and high light.
- If the type is ERROR, print red and high light.