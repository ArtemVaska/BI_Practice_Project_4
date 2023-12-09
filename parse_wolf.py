import re


def transform_results_from_wolf(results_wolf: str, output_txt: str = None):
    """
    Transforms copied result from WoLF PSORT tool to .txt file.

    Args:
    - results_wolf (str): copied results from WoLF PSORT tool.
    - output_txt (str, optional): name of new .txt file.

    Returns:
    - None: The function writes the results to .txt file with specified name.
    """
    
    if output_txt is None:
        output_txt = 'results_wolf'

    results_wolf_list = ' '.join(results_wolf)
    results_list = results_wolf_list.split(' ')
    results_dict = {}

    for word in results_list:
        if re.match(r'g\d+', word):
            id = word
            results_dict[id] = {}
        elif word != 'details':
            if word.find(':') != -1:
                pos = word.strip(':')
            else:
                results_dict[id][pos] = word.strip(',')

    with open(output_txt + '.txt', mode='w') as outfile:

        for id, pos in results_dict.items():
            outfile.write(f'{id}:\n')
            for name, value in pos.items():
                outfile.write(f'\t{name}: {value}\n')


if __name__ == '__main__':
    results_wolf = []
    print('Enter the results of WoLF PSORT (press Enter, if you are done): ')
    while True:  # False - empty string
        seq = input()
        if seq:
            results_wolf.append(seq)
        else:
            break

    enter_output_txt = input('Do you want to specify the name of output file? (y/n): ')
    if enter_output_txt.lower() == 'y':
        output_txt = input('Enter the name of output file without extension: ')
    else:
        output_txt = None
    transform_results_from_wolf(results_wolf, output_txt)
    print('Your job is done!')
