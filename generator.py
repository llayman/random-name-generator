import os
import random
import string

import pandas as pd


# Returns a pandas dataframe containing randomly generated first and last names from US census data
# n: number of samples to generate
# replacement: sampling with (True) or without (False) replacement
def generate_names(n, replacement=True):
    """
    Returns a pandas dataframe containing randomly generated first and last names from US census data
    :param n: number of samples to generate
    :param replacement: sampling with (True) or without (False) replacement
    :return:
    """
    last_names = pd.read_fwf('census-dist-all-last.txt.gz', compression='gzip', usecols=[0], header=None)
    first_names = pd.read_csv('census-dist-female-first.csv.gz', compression='gzip', header=None)
    first_names = first_names.append(pd.read_csv('census-dist-male-first.csv.gz', compression='gzip', header=None))

    df = pd.concat([last_names.sample(n, replace=replacement).reset_index(drop=True),
                    first_names.sample(n, replace=replacement).reset_index(drop=True)[0]],
                   axis=1)
    df.columns = ['last', 'first']
    df = pd.concat([df[col].astype(str).str.title() for col in df.columns], axis=1)
    return df


def generate_phone_numbers(n):
    """
    Returns a list of randomly-generated US phone numbers
    :param n: number of samples to generate
    :return:
    """
    numbers = []
    for i in range(n):
        area = chr(random.randint(50, 57)) + chr(random.randint(48, 57)) + chr(random.randint(48, 57))
        ex = chr(random.randint(50, 57)) + chr(random.randint(48, 57)) + chr(random.randint(48, 57))
        line = chr(random.randint(48, 57)) + chr(random.randint(48, 57)) + chr(random.randint(48, 57)) + chr(
            random.randint(48, 57))
        numbers.append(area + '-' + ex + '-' + line)
    return numbers


def generate_license_plates(n, k=7):
    chars = string.ascii_uppercase + string.digits
    licenses = []
    for i in range(n):
        licenses.append(''.join(random.choices(chars, k=k)))
    return licenses


if __name__ == '__main__':
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    chunk_size = 1000000
    n = remaining = 50000
    print_header = True
    mode = 'w+'
    if not os.path.isdir('output'):
        os.mkdir('output')
    filename = os.path.join('output', 'randoms_' + str(n) + '.csv')
    while remaining > 0:
        names = generate_names(min(n, chunk_size))
        phones = pd.Series(generate_phone_numbers(min(n, chunk_size)))
        ages = pd.Series(random.choices(range(18, 100 + 1), k=min(n, chunk_size)))
        states = pd.Series(random.choices(states, k=min(n, chunk_size)))
        license_plates = pd.Series(generate_license_plates(min(n, chunk_size)))

        rands = pd.concat([names, phones, ages, states, license_plates], axis=1)
        rands.columns.values[2] = 'phone'
        rands.columns.values[3] = 'age'
        rands.columns.values[4] = 'state'
        rands.columns.values[5] = 'license plate'

        rands.to_csv(filename, mode=mode, index=False, header=print_header)
        # rands.to_csv(filename, mode=mode, index=False, compression='gzip', header=print_header)
        remaining -= chunk_size
        print_header = False
        mode = 'a'
