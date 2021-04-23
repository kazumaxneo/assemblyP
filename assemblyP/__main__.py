#!/usr/bin/env python3
import subprocess
import sys
from Bio import SeqIO
import codecs
import subprocess,shlex
from subprocess import PIPE
import statistics
import os
import argparse


parser = argparse.ArgumentParser(description='Script to design outward specific primers at the end of the contig sequences (v0.1)')
##parser.add_argument("reference", metavar="<reference.fasta>", type=str, help="reference fasta file (gzipped allowed)")
parser.add_argument("-c", metavar="<contigs.fasta>", type=str, default="", help="contig fasta file")
parser.add_argument("-f", metavar="<forward reads>", type=str, default="", help="paired read 1")
parser.add_argument("-r", metavar="<reverse reads>", type=str, default="", help="paired read 2")
parser.add_argument("-o", metavar="PATH", type=str, default="output/spades", help="output directory name")
parser.add_argument("-k", metavar="16", type=int, default=16, help="K-mer size for rpeat masking.")
parser.add_argument("-g", metavar="PATH", type=str, default="output/temp/contigs.fasta", help="spades contig name")
parser.add_argument("-l", metavar="PATH", type=str, default="out_16.list", help="glistmaker output file")
parser.add_argument("-m", metavar="PATH", type=str, default="output/temp/masked", help="repeat masked file")
parser.add_argument("-n", metavar="PATH", type=str, default="output/temp/NNN_masked_border1000bps.fasta", help="border sequences")

## 引数を解析
args = parser.parse_args()    
contigs = args.c
fq1 = args.f
fq2 = args.r
output_path = args.o
kmersize = args.k
contig = args.g
glistmakerlist = args.l
maskseq = args.m
borders = args.n

#usage
print("\nDe novo mode:")
print("usage: python part1-change.py -f paired_1.fq.gz -r paired_2.fq.gz\n")
print("Primer mode:")
print("usage: python part1-change.py -f paired_1.fq.gz -r paired_2.fq.gz -c contigs.fasta\n")

#error message
if fq1 == "":
    print ('paired-end fastq1 is necessary.')
    sys.exit()
if fq2 == "":
    print ('paired-end fastq2 is necessary.')
    sys.exit()

# ディレクトリが存在しない場合、ディレクトリを作成
DIR1 = "output/spades"
DIR2 = "output/log"
DIR3 = "output/primer"
DIR4 = "output/temp"
if contigs == "":
    if not os.path.exists(DIR1):
        os.makedirs(DIR1)
if not os.path.exists(DIR2):
    os.makedirs(DIR2)
if not os.path.exists(DIR3):
    os.makedirs(DIR3)
if not os.path.exists(DIR4):
    os.makedirs(DIR4)

#def
#Assembly
def assembly():
    args1 = ['spades.py', '-1', fq1, '-2', fq2, '-k', '67', '--careful', '-o', output_path]
    spades_filename = 'output/log/spades_stderr'
    spades_log = 'output/log/spades.log'
    with open(spades_filename, 'wt') as stdout, open(spades_log, 'w') as stderr:
        subprocess.call(args1, stdout=stdout, stderr=stderr)	  

#K-mer count
def kmercount():
    args2 = ['glistmaker', contig]
    glistmaker_filename = 'output/log/glistmaker_stderr'
    glistmaker_log = 'output/log/glistmaker.log'
    with open(glistmaker_filename, 'wt') as stdout, open(glistmaker_log, 'w') as stderr:
        subprocess.call(args2, stdout=stdout, stderr=stderr)
#Masking
def masking():
    command = 'primer3_masker -a 2 -l out_16.list output/temp/contigs.fasta'
    output = open('./output/temp/masked', 'w')
    devnull = open('/dev/null', 'w')
    subprocess.Popen(shlex.split(command), stdout=output, stderr=devnull)

#Read coverage
def coverage():
    cmd1 = 'bbmap.sh ref=output/temp/contigs.fasta nodisk in1={} in2={} covstats=mapping.txt' \
        ' 2> output/log/bbmap.log'.format(fq1, fq2)
    result = subprocess.run(cmd1, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    for line in result.stdout.splitlines():
        print(line)

#Assembly
if contigs == "":
    print("De novo assembly starts. It'll take a while.")
    assembly()
    print("De novo assembly finished")
    command1 = subprocess.run('cp output/spades/contigs.fasta output/temp/contigs.fasta', shell=True, check=True, stdout=PIPE, universal_newlines=True)
else:
    for record in SeqIO.parse(contigs, 'fasta'):
        id_part = record.id
        seq = record.seq
        print(">", record.id, "\n", seq, file=codecs.open('output/temp/contigs.fasta', 'a', 'utf-8'), sep='')

kmercount()
print("K-mer count finished")
masking()
print("Repeat mask finished")
coverage()
print("Read count finished")


#カバレッジを辞書”dict”に追加
row_no = 0
top5 = ""
l = list(range(0))
dict = {}
fileopen = open("mapping.txt", "r", encoding="utf_8")
while True:
    line = fileopen.readline()
    array = line.split('\t')
    if line:
        newdict = {row_no:array[1]}
        dict.update(newdict)
        row_no += 1
        #print(row_no, array[1])
        if (row_no > 1 and row_no < 7): #top5の長さのcontigのカバレッジを取得
            l.append(array[1])
    else:
        break
med = statistics.median(l)
maxc = (2 * float(med))
minc = (float(med) / 2)
print('Max coverage = ',maxc, '\nMinimum coverage = ', minc)

seq_no = 0
for record in SeqIO.parse(maskseq, 'fasta'):
    id_part = record.id
    seq = record.seq
    seq_no += 1
    
    #2000bp以下のcontigは除外しつつ末端配列を抽出
    if len(seq) > 2000:
        #比較前にfloat型に変換
        cov = float(dict[seq_no])
        #カバレッジ判定
        if cov >= minc and cov <= maxc:
            print('contig', len(seq), '(bp) is the length within the threshould range.', 'Coverage', cov, '(average read depth) is within the specified range.')
            print(">", record.id, "_L\n", seq[127:1127], file=codecs.open('output/temp/NNN_masked_border1000bps.fasta', 'a', 'utf-8'), sep='')
            print(">", record.id, "_R\n", seq[-1127:-127], file=codecs.open('output/temp/NNN_masked_border1000bps.fasta', 'a', 'utf-8'), sep='')
            #ヒアドキュメント
            configL = """SEQUENCE_ID=example
SEQUENCE_TEMPLATE={seql}
PRIMER_TASK=pick_right_only
PRIMER_PICK_LEFT_PRIMER=0
PRIMER_PICK_INTERNAL_OLIGO=0
PRIMER_PICK_RIGHT_PRIMER=1
PRIMER_OPT_SIZE=26
PRIMER_MIN_SIZE=22
PRIMER_MAX_SIZE=30
PRIMER_PRODUCT_SIZE_RANGE=75-150
PRIMER_EXPLAIN_FLAG=1
PRIMER_NUM_RETURN=1
PRIMER_MAX_GC=60
PRIMER_MAX_END_GC=3
PRIMER_MIN_TM=55
PRIMER_OPT_TM=60
PRIMER_MAX_TM=63
PRIMER_MUST_MATCH_THREE_PRIME=nnnns
PRIMER_MUST_MATCH_FIVE_PRIME=wnnnn
=""".format(seql = seq[127:1127])

            configR = """SEQUENCE_ID=example
SEQUENCE_TEMPLATE={seqr}
PRIMER_TASK=pick_left_only
PRIMER_PICK_LEFT_PRIMER=1
PRIMER_PICK_INTERNAL_OLIGO=0
PRIMER_PICK_RIGHT_PRIMER=0
PRIMER_OPT_SIZE=26
PRIMER_MIN_SIZE=22
PRIMER_MAX_SIZE=30
PRIMER_PRODUCT_SIZE_RANGE=75-150
PRIMER_EXPLAIN_FLAG=1
PRIMER_NUM_RETURN=1
PRIMER_MAX_GC=60
PRIMER_MAX_END_GC=3
PRIMER_MIN_TM=55
PRIMER_OPT_TM=60
PRIMER_MAX_TM=63
PRIMER_MUST_MATCH_THREE_PRIME=nnnns
PRIMER_MUST_MATCH_FIVE_PRIME=wnnnn
=""".format(seqr = seq[-1127:-127])

            #保存
            with open('output/temp/configL', 'w') as fl:
                print(configL, file=fl)
            with open('output/temp/configR', 'w') as fr:
                print(configR, file=fr)
            
            #primer抽出
            with open('output/primer/primers', 'a') as f2:
                primer3commnadL = subprocess.run('primer3_core output/temp/configL', shell=True, check=True, stdout=PIPE, universal_newlines=True)
                for line in primer3commnadL.stdout.splitlines():
                    separateL = line.split('=')
                    if separateL[0] == "PRIMER_RIGHT_0_SEQUENCE":
                        print(">", id_part, "_primerL\n", separateL[1], file=f2, sep='')
            
                primer3commnadR = subprocess.run('primer3_core output/temp/configR', shell=True, check=True, stdout=PIPE, universal_newlines=True)
                for line in primer3commnadR.stdout.splitlines():
                    separateR = line.split('=')
                    if separateR[0] == "PRIMER_LEFT_0_SEQUENCE":
                        print(">", id_part, "_primerR\n", separateR[1], file=f2, sep='')
            print('Primer created')
    else:
        print('contig', len(seq), '(bp) is smaller than threshould')
print("PCR primers were created")

command2 = subprocess.run('mv out_16.list output/temp/', shell=True, check=True, stdout=PIPE, universal_newlines=True)
command3 = subprocess.run('mv mapping.txt output/primer/', shell=True, check=True, stdout=PIPE, universal_newlines=True)
print("Job ffinished")
