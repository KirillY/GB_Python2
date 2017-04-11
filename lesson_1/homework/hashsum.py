import os
import hashlib
import csv
import unittest

from contextlib import contextmanager

CSVPATH = os.path.join(os.getcwd(), 'need_hashes.csv')
TXTPATH = os.path.join(os.getcwd(), 'need_hashes.txt')

# CSVPATH = os.CSVPATH.join(os.getcwd(), 'lesson_1', 'homework', 'need_hashes.csv') # path if we run in console
# https://raw.githubusercontent.com/pablorus/GB_Python2/master/lesson_1/homework/need_hashes.csv # csv source
'''
with open(CSVPATH, 'r', encoding='cp1251') as f: # by default csv file opens in cp1251??; equivalent to "open(CSVPATH) as f"
    lines = f.read().splitlines()
    print(lines[1]) # РЇ Р»СЋР±Р»СЋ РџРёС‚РѕРЅ;md5;
'''


@contextmanager
def error_handler(data):
    '''
    exception handler for get_hashsum()
    :param data: any value
    :return: if string, return bytes, encoded in utf-8; return unchanged data if already in bytes
    raise exception if object doesn't support .encode() method or wrong hash type use in get_hashsum()
    '''
    try:
        yield data  # exceptions below doesn't not work if error happened in this part!!!
    except AttributeError:  # exceptions for get_hashsum()
        print("ERROR. Cannot convert data into byte string, wrong data type")
    except ValueError:
        print('ERROR. Cannot recognize hash type from the string')


def get_hashsum(data, hash_type):
    '''
    convert data into bytes (if not yet) and returns its hash-sum
    :param data: 'string' type (utf-8 encoding string) or 'bytestring' type (any other encoding string, eg. ascii or cp1251)
    :param hash_type: string name of desired hash algorithm, eg. md5 or sha256
    :return: hash-sum
    doctests:
    >>> get_hashsum('I love Python', 'abra')
    ERROR. Cannot recognize hash type from the string
    >>> get_hashsum(['I love Python', 355], 'md5')
    ERROR. Cannot convert data into byte string, wrong data type
    '''
    with error_handler(data) as data: # using context manager for error handling
        if data is not bytes:
            data = data.encode('utf-8') # encode our string into bytes with utf-8
        h = hashlib.new(hash_type, data)  # create new hash object
        return h.hexdigest()  # return hex representation


def get_string_data(path, delimiter=';', file_encoding='utf-8'):
    '''
    :param path: path to the csv file
    :return:  nested lists of 2 first values in each line [[line[0], line[1]], ...]
    '''
    with open(path, 'r', encoding=file_encoding) as f: # !!! usually csv has cp1251 encoding but our csv is in utf-8
        reader = csv.reader(f, delimiter=delimiter)
        return [[line[0], line[1]] for line in reader if line] # put values into nested lists


def write_hashes(source_path, destination_path):
    '''
    open source_file
    take the 1-st value in a line, convert it to bytes
    take hash type from 2-nd value
    write hash-sum of 1-st value to the 3-d position
    :param CSVPATH: CSVPATH to the file
    :return: None
    '''
    data_lines = get_string_data(source_path)  # get data from source_path
    for line in data_lines:  # append a hashsum into the 3d place in each nested list(line)
        values, hash_name = line[0], line[1]
        line.append(get_hashsum(values, hash_name))
    with open(destination_path, 'w', encoding='UTF-8', newline='') as f:  # without newline='', it puts '\n' at the end
        if destination_path.endswith('.csv'):  # specific way of writing csv -> .writerow
            f = csv.writer(f, delimiter=';')
            for line in data_lines:
                f.writerow(line)
        elif destination_path.endswith('.txt'):  # join data inside lines with ';', join lines with '\n'
            f.write('\n'.join(';'.join(values) for values in data_lines))


### Assert test part ###

def test_get_hashsum_hashsum():
    assert get_hashsum('I love Python', 'md5') == '27eb2f69c24aa5f3503a6ae610f23a83', 'False: hashsum'


def test_write_hashes(tested_path=CSVPATH, sample_path=TXTPATH, delimiter=';', file_encoding='utf-8'):
    '''
    test if our string data in sample_path is equal to data in tested_path
    '''
    def get_line(path):
        with open(path, 'r', encoding=file_encoding) as file:
            if path.endswith('.csv'):
                file = csv.reader(file,
                                  delimiter=delimiter)  # Each row read from the csv file is returned as a LIST of strings!
            for line in file:
                yield ';'.join(line) if path.endswith('.csv') else line  # convert list to string if csv file

    for a, b in zip(get_line(tested_path), get_line(sample_path)):
        # print('"{}" AND "{}"'.format(a.strip(), b.strip())) # track trailing spaces and '\n'
        assert a.rstrip() == b.rstrip(), 'Lines {} AND {} are not equal'.format(a, b)


### Unittest part ###

class TestFile (unittest.TestCase):
    '''
    test if our string data in sample_path is equal to data in tested_path
    '''
    def test_write_hashes(self, tested_path=CSVPATH, sample_path=TXTPATH, delimiter=';', file_encoding='utf-8'):
        def get_line(path):
            with open(path, 'r', encoding=file_encoding) as file:
                if path.endswith('.csv'):
                    file = csv.reader(file,
                                      delimiter=delimiter)  # Each row read from the csv file is returned as a LIST of strings!
                for line in file:
                    yield ';'.join(line) if path.endswith('.csv') else line  # convert list to string if csv file

        for a, b in zip(get_line(tested_path), get_line(sample_path)):
            # print('"{}" AND "{}"'.format(a.strip(), b.strip())) # track trailing spaces and '\n'
            self.assertTrue (a.rstrip() == b.rstrip())


### RUN part ###

if __name__ == "__main__":
    write_hashes(CSVPATH, CSVPATH)
    ### TESTS ###
    test_get_hashsum_hashsum()
    test_write_hashes(tested_path=CSVPATH, sample_path=TXTPATH)

    import doctest

    doctest.testmod()

    unittest.main()



# lines = f.read().splitlines()
# # ba = bytearray(lines[1], 'cp1251')
# ba = lines[1].encode('cp1251')
# print(ba)
# # ba2 = bytearray(lines[1], 'utf-8')
# ba2 = lines[1].encode('utf-8')
# print(ba2)
# # print(ba.decode('utf-8')) # work
# print(ba2.decode('utf-8'))
# print(lines[1])

# s2 = lines[1]
# print(type(s2))
# print(s2)
# print(bytearray(s2, 'ascii'))
