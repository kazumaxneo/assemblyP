    
### Script to design outward specific primers at the end of the contig sequences.
under development



### Requirements

You must have the following installed on your system to use use this cript:  
* ubuntu  
* python3(>3.6)  
* primer3 (<https://github.com/primer3-org/primer3>)  
* primer3 masker (<https://github.com/bioinfo-ut/primer3_masker>)  
* bbmap (<https://github.com/BioInfoTools/BBMap>)  
* genometester4 (<https://github.com/bioinfo-ut/GenomeTester4>)  
* spades (<https://github.com/ablab/spades>)  
* biopython (<https://github.com/biopython/biopython>)  
optional  



### Install primerdesigner and doing test run
    #setup virtual enviroment using mamba
    mamba create -n PrimerDesign -y python=3.9
    #activate enviroment
    conda activate PrimerDesign
    #install dependancy
    mamba install -c bioconda primer3==2.5.0
    mamba install -c bioconda bbmap
    mamba install -c bioconda genometester4
    mamba install -c bioconda spades==3.15
        
    #clone this repository and install this package
    git clone git@github.com:kazumaxneo/asssemblyP.git && cd asssemblyP/
    pip install .
    
    #test run
    cd test_data/
    #perform de novo aassembly and make primers
    primerdesigner -f paired_1.fq.gz -r paired_2.fq.gz
    
    #make primers using preassembled sequences
    primerdesigner -f paired_1.fq.gz -r paired_2.fq.gz -f contigs.fasta


### Docker
    
    git clone git@github.com:kazumaxneo/genome_quest.git
    cd genome_quest
    docker build . -t genome_quest_docker
    docker run -itv $PWD:/data/ genome_quest_docker
    . ~/.profile
    genome_quest
　
　
### Licence
GPL v3.



    
        


