import numpy as np
import re


def swf_reader(file_name):
    with open(file_name,'r') as swf_file: # go to google what is the difference between 'r' and 'rb'
        data = []
        for ii,line in enumerate(swf_file):
            if ii == 0:
                k = line
                numerical_pattern = r'[\w]+= [-+]?[\d+|\d+\.\d+]+'  # this means:
                                                                    # find a pattern that looks like: some string followed by the equal sign
                                                                    # and a space, and then followed by some numbers that is positive or negative,
                                                                    # the number could be an integer -- \d+
                                                                    # or a float point number -- \d+\.\d+
                                                                    # "\" is called an escape command, it is to tell python whatever follows this is special
                text_pattern = r'[\w\.-]+= "[\w\.-]+"'
                header = {}
                for found_pattern in re.findall(numerical_pattern,k):
                    a,b = found_pattern.split('= ')
                    header[a] = float(b)
                for found_pattern in re.findall(text_pattern,k):
                    a,b = found_pattern.split('= ')
                    header[a] = b
            else:
                j = line
                temp = np.array(j.replace('\n','').split(' ')[5:], # first remove the last character that indicates switching line, and then we split the data by space
                                dtype = np.float32, # by directly defining the data type, we conver the strings to numerical values
                               )
                data.append(temp)
        header['Time'] = np.arange(header['TSB'],
                                   header['TSB']+(header['Npts'])*header['DI'],
                                   header['DI'])
        header['sampling_rate'] = 1000/header['DI']
    swf_file.close()
    return header,data
