import pandas as pd
import random
import os

last_names = pd.read_fwf('census-dist-all-last.txt.gz', compression='gzip', usecols=[0], header=None)
first_names = pd.read_csv('census-dist-female-first.csv.gz', compression='gzip', header=None)
first_names = first_names.append(pd.read_csv('census-dist-male-first.csv.gz', compression='gzip', header=None))


# Returns a pandas dataframe containing randomly generated first and last names from US census data
# n: number of samples to generate
# replacement: sampling with (True) or without (False) replacement
def generate_names(n=1000, replacement=True):
    df = pd.concat([last_names.sample(n, replace=replacement).reset_index(drop=True),
                    first_names.sample(n, replace=replacement).reset_index(drop=True)[0]],
                   axis=1)
    df.columns = ['last', 'first']
    df = pd.concat([df[col].astype(str).str.title() for col in df.columns], axis=1)
    return df


# Returns a list of randomly-generated US phone numbers
# n: number of samples to generate
def generate_phone_numbers(n=1000):
    numbers = []
    for i in range(n):
        area = chr(random.randint(50, 57)) + chr(random.randint(48, 57)) + chr(random.randint(48, 57))
        ex = chr(random.randint(50, 57)) + chr(random.randint(48, 57)) + chr(random.randint(48, 57))
        line = chr(random.randint(48, 57)) + chr(random.randint(48, 57)) + chr(random.randint(48, 57)) + chr(
            random.randint(48, 57))
        numbers.append(area+'-'+ex+'-'+line)
    return numbers


if __name__ == '__main__':
    chunk_size = 1000000
    n = remaining = 50000
    print_header = True
    mode = 'w'
    filename = os.path.join('output','randoms_' + str(n) + '.csv')
    while remaining > 0:
        names = generate_names(min(n, chunk_size))
        phones = pd.Series(generate_phone_numbers(min(n, chunk_size)))
        rands = pd.concat([names, phones], axis=1)
        rands.columns.values[2] = 'phone'
        rands.to_csv(filename, mode=mode, index=False, header=print_header)
        # rands.to_csv(filename, mode=mode, index=False, compression='gzip', header=print_header)
        remaining -= chunk_size
        print_header = False
        mode = 'a'
