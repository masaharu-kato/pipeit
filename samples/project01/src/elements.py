#!env/bin/python
import argparse
import pipeit

from typing import List, Tuple


def elements(prefix:str, n:int) -> List[str]:
    return [prefix + str(i) for i in range(1, n+1)]

   
def main():
    argp = argparse.ArgumentParser(description='Create elements')
    argp.add_argument('prefix', type=str, help='Prefix of element name')
    argp.add_argument('number', type=int, help='Number of elements')
    args = argp.parse_args()

    def process(_):
        data = {}
        data['elements'] = elements(args.prefix, args.number)
        return data

    return pipeit.pipeit_with_json(args, process)


if __name__ == "__main__":
    main()
