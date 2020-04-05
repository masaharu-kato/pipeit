import pipeit


def show_elements(data):
    for group in data.groups:
        print(', '.join(group))

    return data
   
   
def main():
    return pipeit.pipeit(None, show_elements)


if __name__ == "__main__":
    main()
