    
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



### Install assemblyP and doing test run
    #setup virtual enviroment using mamba
    mamba create -n assemblyP -y python=3.9
    #activate enviroment
    conda activate assemblyP
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
    assemblyP -f paired_1.fq.gz -r paired_2.fq.gz
    
    #make primers using preassembled sequences
    assemblyP -f paired_1.fq.gz -r paired_2.fq.gz -f contigs.fasta


### Docker
    

　
　
### Licence
GPL v3.



    
        


