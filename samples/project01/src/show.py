#!/usr/bin/env python3
import pipeit


def show_elements(data):
    for group in data['groups']:
        print(', '.join(group))

    return data
   
   
def main():
    return pipeit.pipeit_with_json(None, show_elements, disable_cache=True, no_output=True)


if __name__ == "__main__":
    main()
