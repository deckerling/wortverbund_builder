# wb_func.py
#
# Copyright 2019 E. Decker
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Miscellaneous functions needed for "wortverbund_builder.py" to work as
    intended."""

def mergesort(content_list, size):
    """Sorts the features and their positions in respect to the latter.

    A merge sort algorithm sorting the "content_list" from "smallest" position
    value to the "highest".

    Args:
        content_list: list with features of a wortverbund and their positions of
            occurrence.
        size:
        
    Returns the sorted content_list."""
    if size <= 1:
        return content_list
    else:
        half = int(size/2)
        left = []
        right = []
        for i in range(size):
            if i < half:
                left.append(content_list[i])
            else:
                right.append(content_list[i])
        if len(left) != 1:
            left = mergesort(left, half)
        if len(right) != 1:
            right = mergesort(right, size-half)
        j = 0
        for i in range(size):
            if j >= half:
                content_list[i] = right[i-j]
                continue
            if j <= i-(size-half):
                content_list[i] = left[j]
                j += 1
                continue
            if left[j][1] <= right[i-j][1]:
                content_list[i] = left[j]
                j += 1
            else:
                content_list[i] = right[i-j]
        return content_list


def find_extremes(content_list):
    """Calculates the smallest and highest values of every position's column of
        the positions of features of a wortverbund.
        
    Args:
        content_list: list with features of a wortverbund and their positions of
            occurrence.
            
    Returns:
        smallest_values: list containing the smallest values found for a
            position's column in a "content_list".
        highest_values: list containing the highest values found for a
            position's column in a "content_list"."""
    max_length = 0
    for i in range(len(content_list)):
        if max_length < len(content_list[i][1]):
            max_length = len(content_list[i][1])

    smallest_values = [9999999]*max_length
    highest_values = [0]*max_length
    try:
        for i in range(1, max_length):
            for j in range(len(content_list)):
                if smallest_values[i] > content_list[j][1][i]:
                    smallest_values[i] = content_list[j][1][i]
                if highest_values[i] < content_list[j][1][i]:
                    highest_values[i] = content_list[j][1][i]
    except IndexError:
        pass
    return smallest_values, highest_values


def calculate_position_values(content_list, smallest_values, highest_values):
    """Calculates the x-values needed to plot a wortverbund.

    Args:
        content_list: list with features of a wortverbund and their positions of
            occurrence.
        smallest_values: smallest value in a position's column (e.g. smallest
            number of lines of a page).
        highest_values: highest value in a position's column (e.g. highest
            number of lines of a page); will be used as "maximum" in order to
            calculate fractional parts of the values.
            
    Returns the x-values needed to plot a wortverbund."""
    values = [None]*len(content_list)
    max_length = 0
    for i in range(len(values)):
        if max_length < len(content_list[i][1]):
            max_length = len(content_list[i][1])
    for i in range(len(values)):
        values[i] = content_list[i][1][0]
        if max_length > 1:
            try:
                if smallest_values[1] != 0:
                    if (content_list[i][1][1]-1)/highest_values[1] > 1:
                        values[i] += 1
                    else:
                        values[i] += (content_list[i][1][1]-1)/highest_values[1]
                else:
                    if content_list[i][1][1]/highest_values[1] > 1:
                        values[i] += 1
                    else:
                         values[i] += content_list[i][1][1]/highest_values[1]
            except IndexError:
                pass
            try:
                values[i] = str(values[i]).split('.')
                values[i][1] = values[i][1][:3]
                values[i] = values[i][0]+'.'+values[i][1]
            except IndexError:
                pass
        if max_length > 2:
            for j in range(2, max_length):
                # Calculates the fractional part of the values by dividing by
                # "highest_values" and adding it as a string to the value
                # already calculated. This will generate values that enable the
                # program to work as intended - nevertheless those values cannot
                # be regarded as "exact".
                try:
                    if smallest_values[j] != 0:
                        values[i] += str((content_list[i][1][j]-1)/highest_values[j])[2:5]
                        if (content_list[i][1][j]-1)/highest_values[j] >= 1:
                            valTest =  values[i].split('.')
                            if len(valTest[1]) == 1:
                                values[i] = str(float(values[i])+0.1)
                            else:
                                string = ''
                                for k in range(len(valTest[1])-1):
                                    string += '0'
                                string += '1'
                                values[i] = str(float('0.'+string)+float(values[i]))
                    else:
                        values[i] += str(content_list[i][1][j]/highest_values[j])[2:5]
                        if content_list[i][1][j]/highest_values[j] >= 1:
                            valTest =  values[i].split('.')
                            if len(valTest[1]) == 1:
                                values[i] = str(float(values[i])+0.1)
                            else:
                                string = ''
                                for k in range(len(valTest[1])-1):
                                    string += '0'
                                string += '1'
                                values[i] = str(float('0.'+string)+float(values[i]))
                except IndexError:
                    pass
    for i in range(len(values)):
        if type(values[i]) == list:
            values[i] = values[i][0]
        values[i] = float(values[i])
    return values
