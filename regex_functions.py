"""
# Copyright Nick Cheng, Brian Harrington, Danny Heap, Yitong Hu
# 2013, 2014, 2015
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2015
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.


def is_regex(s):
    ''' (str) -> bool
    Given a string s check if the string is a correct/valid regular expression
    string, if it's valid return True else return False
    >>> is_regex('((1|0*).5)')
    True
    >>> is_regex('(5.*)')
    False
    >>> is_regex([])
    False
    >>> is_regex('')
    False
    >>> is_regex('((2.1).(2.1))')
    True
    >>> is_regex(((0|2)**))
    False
    >>> is_regex('((0**.2))')
    False
    >>> is_regex('((2**).0)')
    False
    >>> is_regex('(0|2)**')
    True
    >>> is_regex('((0|2)**)')
    False
    >>> is_regex('(1.|2)')
    False
    >>> is_regex('((1.2)*.2)')
    True
    '''
    # boolean checker
    checker = (symbol_finder(s) and star_property(s) and bar_dot_property(s)
               and num_property(s) and parenthises_property(s)
               and extra_exceptions(s) and end_star)
    # check the checker first
    if checker is False:
        return False
    # empty string is invalid
    elif len(s) == 0:
        return False
    # check for any other simple regex
    elif len(s) <= 4:
        # can't have either '(',')'
        if s[0] == '(' or s[len(s) - 1] == ')':
            return False
        # can't have '(' and ')'
        elif s[0] == '(' and s[len(s) - 1] == ')':
            return False
        # can't have a star at the end
        elif s[len(s) - 1] == '*':
            return False
        # otherwise use checker
        else:
            return checker
    # when there is more than 2 letters
    else:
        # check for start with '(' and end with ')'
        if (s[0] == '(' and s[len(s) - 1] == ')'):
            # when there is extra bracket
            if (s[1] == '('and s[len(s) - 2] == ')'):
                # third element is a '(' and second last is not a number
                # or a star
                if (s[2] == '(' and s[len(s) - 3] in '012e*'):
                    return False
                # any other possibility check the checker
                else:
                    return checker
            # when more than string length of greater than 5 check second
            # value and second last value are not numbers
            elif (s[1] in '012e' and s[len(s) - 2] in '012e' and len(s) > 5):
                return False
            # extra bracket for ending with star
            elif (s[1] == '(' and s[len(s) - 2] == '*'
                  and s[len(s) - 3] not in '012e'):
                return False
            # anything else check with the checker boolean
            else:
                return checker
        # when it starts with '(' and ends with '*'
        elif (s[0] == '(' and s[len(s) - 1] == '*'):
            # when not a propre element is in front of the last star
            if s[len(s) - 2] not in ')*012e':
                return False
            # second last element is a number
            elif s[len(s) - 2] in '012e':
                return False
            # anything else check with boolean checker
            else:
                return checker
        # it's false if it starts and ends with other symbols
        else:
            return False


def symbol_finder(s):
    ''' (str) -> bool
    Take a string and veriffy if it has the correct symbols
    >>> symbol_helper('(1.2)')
    True
    >>> symbol_helper('((1.2*)|e*)')
    True
    >>> symbol_helper('(1,2)')
    False
    >>> symbol_helper('(1.3)')
    False
    >>> symbol_helper('(1>?!2)')
    False
    '''
    # a list of possible symbols
    symbols = '(012e*.|)'
    # set a counter for comparison
    prop_sym = 0
    # loop every element of the string
    for rep in s:
        # when it's a proper symbol
        if rep in symbols:
            # add 1 to the counter
            prop_sym += 1
    # return a boolean comparison to check is all elements are valid symbols
    return prop_sym == len(s)


def star_property(s):
    ''' (str) -> bool
    Check if the star symbol has the right properties
    >>> star_property('(1.2*)')
    True
    star_property('(1.2*)*********')
    True
    star_property('(1.*2*)')
    False
    star_property('((1.2*)*)')
    False
    star_property('*(1.2*)')
    False
    '''
    # create possible value from elements in front and back
    front = '012e)*'
    back = ').|*'
    # set a counter to count the index
    counter = 0
    # have a boolean comparison
    output = 0
    # loop the string
    for letter in s:
        # when element is a star
        if (letter == '*'):
            # when the star is the first element
            if (counter == 0):
                # is an invalid regex add one to output
                output += 1
            # when the star is not the last element
            elif (counter < len(s) - 1):
                # just check the previous element
                output += s[counter - 1] not in front
                output += s[counter + 1] not in back
            # when the star is the last element
            elif (counter == len(s) - 1):
                # check previous and next element are valid
                output += s[counter - 1] not in front
        # add one to the counter
        counter += 1
    return output == 0


def bar_dot_property(s):
    ''' (str) -> bool
    Check if the bar and the dot symbol has the right properties
    >>> bar_dot_property('((1|2).0)')
    True
    bar_dot_property('((1|2).0).')
    False
    bar_dot_property('((1|2).0)|')
    False
    bar_dot_property('.((1|2).0))
    False
    bar_dot_property('|((1|2).0))
    False
    bar_dot_property('((1|.2).0))
    False
    '''
    # create possible value from elements in front and back
    front = '012e)*'
    back = '(012e'
    # set a counter to count the index
    counter = 0
    # have a boolean comparison
    output = 0
    # loop the string
    for letter in s:
        # when element is a bar or dot
        if (letter in '|.'):
            # when the bar/dot is the first element
            if (counter == 0):
                # add one to the output because it can't be the first element
                output += 1
            # when the bar/dot is not the last element of the string
            elif (counter < len(s) - 1):
                # just check the previous element
                output += s[counter - 1] not in front
                output += s[counter + 1] not in back
            # when the bar/dot is the last element
            elif (counter == len(s) - 1):
                # invalid form of regex add one to output
                output += 1
        # add one to the counter
        counter += 1
    return output == 0


def num_property(s):
    ''' (str) -> bool
    Check if numbers has the right properties
    >>> num_property('(1|2*)')
    True
    >>> num_property('(11|2*)')
    False
    >>> num_property('(1|2*)2')
    False
    >>> num_property('1(1|2*)')
    False
    '''
    # create possible value from elements in front and back
    front = '(.|'
    back = ').|*'
    # set a counter to count the index
    counter = 0
    # have a boolean comparison
    output = 0
    # loop the string
    for letter in s:
        # when element is a number
        if (letter in '012e'):
            # when the number is the first element
            if (counter == 0):
                # when length is just one
                if len(s) == 1:
                    # is a valid regex
                    output += 0
                # when length is greater than 1
                else:
                    # check the element in the back
                    output += s[counter + 1] not in back
            # when the number is not the last element of the string
            elif (counter < len(s) - 1):
                # just check the previous element
                output += s[counter - 1] not in front
                output += s[counter + 1] not in back
            # when the number is the last element
            elif (counter == len(s) - 1):
                # cannot be the last element
                output += 1
        # add one to the counter
        counter += 1
    return output == 0


def extra_exceptions(s):
    ''' (str) -> bool
    Make sure that when a there is a parenthises it closes at least 4 from
    the last open parenthesis
    >>> extra_exceptions('((2**).0)')
    False
    >>> extra_exceptions('((2*).0)')
    False
    >>> extra_exceptions('((2*.1).0)')
    True
    >>> extra_exceptions('((1.1).2)')
    True
    '''
    # create variable to be zero for the loop and output
    counter = 0
    output = 0
    # loop to check for letters
    for letter in s:
        # when it find the right letter at the right place
        if letter == '(' and counter < len(s) - 3:
            # second letter from it can't be ')'
            if s[counter + 2] == ')':
                output += 1
            # third letter from it can't be ')'
            if s[counter + 2] == ')':
                output += 1
            # fourth letter from it can't be ')'
            if s[counter + 3] == ')':
                output += 1
            # fourth letter from it can't be '*'
            if s[counter + 3] == '*':
                output += 1
        # index counter add one
        counter += 1
    return output == 0
# check if ( follows are equal to ) follows


def end_star(s):
    ''' (str) -> bool
    When a regex ends with star make sure it doesn't have double ')' infront
    for as many star in the back

    >>> end_star('(1.2)*****')
    True
    >>> end_star('((1.2)*)****')
    True
    >>> end_star('((1.2))*****')
    False
    '''
    # start at zero
    output = 0
    # lowest regex with star
    if len(s) == 1:
        output += 0
    # when s has more than 1 letter
    else:
        print(s)
        # check for the last element to be a star
        if s[len(s) - 1] == '*':
            # check 2 other elements infront to ')'
            if s[len(s) - 2] == ')' and s[len(s) - 3] == ')':
                # add one because is invalid regex
                output += 1
            else:
                # add nothing
                output += 0
        # when there is not star add nothing
        else:
            output += 0
        # recurse by removing last element
    end_star(s[:-1])
    return output == 0


def parenthises_property(s):
    ''' (str) -> bool
    Check if the parenthises are properly used
    >>> parenthises_property('(1.2)')
    True
    >>> parenthises_property('((1.2))')
    False
    >>> parenthises_property('((1.2)(')
    False
    >>> parenthises_property(')(1.2))')
    False
    '''
    # create possible value from elements in front and back
    open_front = '.|('
    open_back = '012e('
    close_front = '012e*)'
    close_back = '.|*)'
    # set a counter to count the index
    counter = 0
    # have a boolean comparison
    output = 0
    # loop the string
    for letter in s:
        # when element is a '('
        if (letter == '('):
            # when the '(' is the first element
            if (counter == 0):
                output += s[counter + 1] not in open_back
            # when the '(' is not the last element of the string
            elif (counter < len(s) - 1):
                # just check the previous element
                output += s[counter - 1] not in open_front
                output += s[counter + 1] not in open_back
            # when the '(' is the last element
            elif (counter == len(s) - 1):
                # impossible case
                output += 1
        # when element is a ')'
        elif (letter == ')'):
            # when the ')' is the first element
            if (counter == 0):
                # impossible case
                output += 1
            # when the ')' is not the last element of the string
            elif (counter < len(s) - 1):
                # just check the previous element
                output += s[counter - 1] not in close_front
                output += s[counter + 1] not in close_back
            # when the ')' is the last element
            elif (counter == len(s) - 1):
                # check previous and next element are valid
                output += s[counter - 1] not in close_front
        # add one to the counter
        counter += 1
    return output == 0


def all_regex_permutations(s):
    ''' (str) -> set
    Given a string s return a set of all possible permuation of the string
    regex(must be valid expressions)
    >>> all_regex_permutations('(1.2)')
    {(2.1), (1.2)}
    >>> all_regex_permutations('1*')
    {1*}
    >>> all_regex_permutations('2')
    {2}
    >>> all_regex_permutations('(1.2)*')
    {(2.1)*, (1.2)*, (2.1*), (1.2*), (2*.1), (1*.2)}
    '''
    # create an empty set
    perm_set = set()
    # have a list of all possible permutations
    perm_list = permutations_helper(s)
    # when s is not a regex
    if is_regex(s) is False:
        return perm_set
    # when s is a regex
    else:
        # loop throught list of permutations
        for perm in perm_list:
            # when the permutaion is a regex
            if is_regex(perm) is True:
                # add it to the new set
                perm_set.add(perm)
        return perm_set


def permutations_helper(s):
    ''' (str) -> list
    Given a string find all the possible permutaiton of the string and put
    them in a list
    >>> permutation_helper('(1)')
    {'1()', '1)(', '()1', '(1)', ')(1', ')1('}
    >>> permutation_helper('1*')
    {'1*','*1'}
    '''
    # create an empty list
    result = []
    # start a if statement to stop recursion
    if len(s) == 1:
        # return the element when length is 1
        result = [s]
    # when there is more than 1 element
    else:
        # have a loop to every index of the input and keep track of it
        for index, count in enumerate(s):
            # create an loop to check every letter in the string
            for perm in permutations_helper(s[:index] + s[index + 1:]):
                # add the permutation into the list
                result += [count + perm]
    return result


def regex_match(r, s):
    ''' (object, str) -> bool
    Verify if the string s contains the root r
    >>> regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '111110')
    True
    '''
    # when the root is for single length string
    if r == Leaf('0') or r == Leaf('1') or r == Leaf('2') or r == Leaf('e'):
        # check if the string is a number
        return s in '012e'
    else:
        pass
    # start with the root
    # check right elements of the root
    # check the left elements of the root


def build_regex_tree(regex):
    ''' (object) -> object
    Given a regex string expression, builds the corresponding expression tree
    and return the root
    >>> build_regex_tree('(1.2)')
    DotTree(Leaf('1'), Leaf('2'))
    >>> build_regex_tree('1')
    Leaf('1')
    >>> build_regex_tree('(1.2)*')
    StarTree(DotTree(Leaf('1'), Leaf('2')))
    '''
    # when there is only a number
    if len(regex) == 1:
        # return the leaf
        return Leaf(regex)
    # when there is 2 element in the string
    elif len(regex) == 2:
        # return a star tree with the first element as a leaf
        return StarTree(Leaf(regex[0]))
    # a more complex regex including dot or bar
    elif len(regex) == 5:
        # when is a dot
        if regex[2] == '.':
            # build the dot tree
            return DotTree(Leaf(regex[1]), Leaf(regex[3]))
        # when is a bar
        elif regex[2] == '|':
            # build a bar tree
            return BarTree(Leaf(regex[1]), Leaf(regex[3]))
    # a star as a root
    elif len(regex) == 6:
            # when is a dot
            if regex[2] == '.':
                # build the dot tree
                return StarTree(DotTree(Leaf(regex[1]), Leaf(regex[3])))
            # when is a bar
            elif regex[2] == '|':
                # build a bar tree
                return StarTree(BarTree(Leaf(regex[1]), Leaf(regex[3])))
    else:
        pass
    # for more than 6 of length check for root
    # check for the root bar
    # add the leafs on the right and the leafs of the left
    # check for the root dot
    # add the leafs on the right and the leafs of the left
    # check for the root star
    # since is a star is only takes one leaf
