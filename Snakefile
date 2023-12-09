ASSEMBLE_GENOME_URL = "ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/949/185/GCA_001949185.1_Rvar_4.0/GCA_001949185.1_Rvar_4.0_genomic.fna.gz"
AUGUSTUS_PROTEIN_FASTA = "https://drive.google.com/u/0/uc?id=1hCEywBlqNzTrIpQsZTVuZk1S9qKzqQAq&export=download"
AUGUSTUS_GFF = "https://drive.google.com/u/0/uc?id=12ShwrgLkvJIYQV2p1UlXklmxSOOxyxj4&export=download"


# downloads assembled genome from ncbi
rule assembled_genome_download:
	output:
		'data/assembled_genome.fna.gz'
	shell:
		"""
		wget -O {output} {ASSEMBLE_GENOME_URL}
		"""


# downloads precomputed AUGUSTUS results
rule augustus_results_download:
	output:
		file_fasta = 'data/augustus_whole.fasta',
		file_gff = 'data/augustus_whole.gff'
	run:
		shell("wget -O {output.file_fasta} {AUGUSTUS_PROTEIN_FASTA}")
		shell("wget -O {output.file_gff} {AUGUSTUS_GFF}")


# creates a local database for following blast alignment
rule blast_create_database:
	input:
		'results/augustus_whole_parsed.fasta'
	output:
		'results/blast/local_database.pdb',
		'results/blast/local_database.phr',
		'results/blast/local_database.pin',
		'results/blast/local_database.pjs',
		'results/blast/local_database.pot',
		'results/blast/local_database.psq',
		'results/blast/local_database.ptf',
		'results/blast/local_database.pto'
	shell:
		"""
		makeblastdb \
		-in {input} \
		-dbtype prot \
		-out results/blast/local_database
		"""


# performing blast alignment with created database and found peptides
rule blast_perform_the_search:
	input:
		query = 'data/peptides.fa'
	output:
		'results/blast/aligned_blast'
	shell:
		"""
		blastp \
		-db results/blast/local_database \
		-query {input.query} \
		-outfmt "6 qseqid sseqid evalue qcovs pident" \
		-out {output}
		"""


# finds unique proteins from the result of perfomed blast
rule save_unique_proteins:
	input:
		'results/blast/aligned_blast'
	output:
		'results/unique_proteins.txt'
	run:
		shell("echo '\n'$(cat {input} | cut -f 2 | sort | uniq | wc -l) 'unique proteins detected\n'")
		shell("cat {input} | cut -f 2 | sort | uniq > {output}")


# creates indexes for following parsing
rule samtools_faidx_extract_proteins:
	input:
		'results/{sample}.fasta'
	output:
		'results/{sample}.fasta.fai'
	shell:
		"samtools faidx results/{wildcards.sample}.fasta"


# extracts found proteins using created indexes
rule extract_proteins:
	input:
		'results/augustus_whole_parsed.fasta.fai',
		fasta = 'results/augustus_whole_parsed.fasta',
		unique_prot = 'results/unique_proteins.txt'
	output:
		'results/extracted_proteins.fasta'
	shell:
		"""
		xargs samtools faidx \
		{input.fasta} \
		< {input.unique_prot} \
		> {output}
		"""
		

# extracts found filtered proteins using the same created indexes
rule extract_filtered_proteins:
	input:
		'results/augustus_whole_parsed.fasta.fai',
		fasta = 'results/augustus_whole_parsed.fasta',
		filter_prot = 'results/filtered_proteins.txt'
	output:
		'results/extracted_filtered_proteins.fasta'
	shell:
		"""
		xargs samtools faidx \
		{input.fasta} \
		< {input.filter_prot} \
		> {output}
		"""
