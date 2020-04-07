#!env/bin/python
import pipeit


def show_elements(data):
    for group in data['groups']:
        print(', '.join(group))

    return data
   
   
def main():
    return pipeit.pipeit_with_json(None, show_elements, disable_cache=True)


if __name__ == "__main__":
    main()
