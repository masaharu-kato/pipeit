import argparse
import itertools
import pipeit

from typing import List, Tuple


def group_elements(elements:List[str], _type:str, r:int) -> List[Tuple[str, ...]]:
    if _type == 'prod':
        return list(itertools.product(elements, r))
    if _type == 'comb':
        return list(itertools.combinations(elements, r=r))
    if _type == 'comb_rep':
        return list(itertools.combinations_with_replacement(elements, r=r))

   
def main():
    argp = argparse.ArgumentParser(description='Group elements')
    argp.add_argument('-t', '--type'      , type=str, required=True, choices=['prod', 'comb', 'comb_rep'], help='Grouping method')
    argp.add_argument('-n', '--n_in_group', type=int, required=True, help='Number of elements in each group')
    args = argp.parse_args()

    def process(data):
        data.groups = group_elements(data.elements, args.type, args.n_in_group)
        return data

    return pipeit.pipeit(args, process)


if __name__ == "__main__":
    main()
