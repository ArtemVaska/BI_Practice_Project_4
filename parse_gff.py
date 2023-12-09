import os


def select_genes_from_gff_to_fasta(input_gff: str, output_fasta: str = None):
    """
    Extracts the gene name and protein sequences from the gff file and creates a FASTA file containing 
    the gene names and protein sequences flanking the specified genes 

    Args:
    - input_gff (str): path to the gff file.
    - output_fasta (str, optional): path to the output FASTA file. If not provided, a default name is generated.

    Returns:
    - None: The function writes the selected gene and protein sequences to the output FASTA file.
    """

    if output_fasta is None:
        name = os.path.basename(input_gff).split('.')[0]
        output_fasta = name + '.fasta'
    protein_list = []
    current_sequence = []
    gene_name = ''
    with open(input_gff, mode='r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if line.startswith('# start gene'):
                gene_name = line.split()[3]
            elif gene_name and line.startswith('# protein sequence ='):
                if not line.endswith(']'):
                    protein = line.split('[')[1]
                    current_sequence.append(protein)
                else:
                    protein = line.split('[')[1][:-1]
                    current_sequence.append(protein)
                    current_protein = ''.join(current_sequence)
                    protein_list.append([gene_name, current_protein])
                    gene_name = ''
                    current_sequence = []
            elif gene_name and current_sequence and line.startswith('#') and not line.endswith(']'):
                protein = line.split()[1]
                current_sequence.append(protein)
            elif gene_name and current_sequence and line.endswith(']'):
                protein = line.split()[1][:-1]
                current_sequence.append(protein)
                current_protein = ''.join(current_sequence)
                protein_list.append([gene_name, current_protein])
                gene_name = ''
                current_sequence = []
            line = file.readline()

    with open(output_fasta, mode='w') as outfile:
        for gene_name, current_protein in protein_list:
            outfile.write(f'>{gene_name}\n{current_protein}\n')


if __name__ == '__main__':
    input_gff = input('Enter the path to the .gff file: ')
    enter_output_fasta = input('Do you want to specify the name of output file? (y/n): ')
    if enter_output_fasta.lower() == 'y':
        output_fasta = input('Enter the name of output file: ')
    else:
        output_fasta = None
    select_genes_from_gff_to_fasta(input_gff, output_fasta)
    print('Your job is done!')
