#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 22:46:11 2018

@author: shanghungshih
"""

import os
import time
import requests
import pandas as pd
import argparse
import logging
from textwrap import dedent
from multiprocessing import Pool


logger_stderr = logging.getLogger(__name__+'stderr')
logger_stderr.setLevel(logging.INFO)
stderr_handler = logging.StreamHandler()
stderr_handler.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
logger_stderr.addHandler(stderr_handler)
logger_null = logging.getLogger(__name__+'null')
null_handler = logging.NullHandler()
logger_null.addHandler(null_handler)

VERSION = (1, 0, 0)
__version__ = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])

class autoOncotator:
    
    def __init__(self, num, project, input_dir, output_dir, tsv, maf):
        self.num = num
        self.project = project
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.tsv = tsv
        self.maf = maf
        
    def remove_snp(self, project, input_dir, output_dir):
        in_file = os.path.join(input_dir, project)
        out_file = os.path.join(output_dir, project.replace('.vcf', '.filter.vcf'))
        out = open(out_file, 'w+') 
        with open(in_file, 'r') as f:
            for i in f.readlines():
                if i.count('#') == 0:
                    if i.split(sep='\t')[0].split(sep='chr')[1].isnumeric() == True or i.split(sep='\t')[0].split(sep='chr')[1].endswith('X') == True or i.split(sep='\t')[0].split(sep='chr')[1].endswith('Y') == True:
                        if i.split(sep='\t')[2].startswith('rs') == False:
                            out.writelines(i)
        out.close()
        
    def vcf2oncotator(self, project, output_dir, tsv):
        in_file = os.path.join(output_dir, project.replace('.vcf', '.filter.vcf'))
        out_file = os.path.join(os.getcwd(), project.replace('.vcf', '.'+tsv))
        out = open(out_file, 'w+')
        with open(in_file, 'r') as f:
            for l in f.readlines():
                if l.count('#') == 0:
                    if l.split(sep='\t')[0].split(sep='chr')[1].isnumeric() == True or l.split(sep='\t')[0].split(sep='chr')[1].endswith('X') == True or l.split(sep='\t')[0].split(sep='chr')[1].endswith('Y') == True:
                        if l.split(sep='\t')[2].startswith('rs') == False:
                            # SNV
                            if len(l.split(sep='\t')[3]) == 1 and len(l.split(sep='\t')[4]) == 1:
                                line = str(l.split(sep='\t')[0].split(sep='chr')[1])+'\t'+str(l.split(sep='\t')[1])+'\t'+str(l.split(sep='\t')[1])+'\t'+str(l.split(sep='\t')[3])+'\t'+str(l.split(sep='\t')[4])+'\n'
                                out.writelines(line)
                            # deletion
                            if len(l.split(sep='\t')[3]) != 1 and len(l.split(sep='\t')[4]) == 1:
                                line = str(l.split(sep='\t')[0].split(sep='chr')[1])+'\t'+str(int(l.split(sep='\t')[1])+1)+'\t'+str(int(l.split(sep='\t')[1])+len(l.split(sep='\t')[3][1:]))+'\t'+str(l.split(sep='\t')[3][1:])+'\t'+'-'+'\n'
                                out.writelines(line)
                            # insertion
                            if len(l.split(sep='\t')[3]) == 1 and len(l.split(sep='\t')[4]) != 1:
                                line = str(l.split(sep='\t')[0].split(sep='chr')[1])+'\t'+str(int(l.split(sep='\t')[1]))+'\t'+str(int(l.split(sep='\t')[1])+len(l.split(sep='\t')[4])-1)+'\t'+'-'+'\t'+str(l.split(sep='\t')[4][1:])+'\n'
                                out.writelines(line)
        out.close()
        
    def oncotator_api(self, project, output_dir, tsv, maf):
        in_file = os.path.join(output_dir, project.replace('filter.vcf', tsv))
        out_file = os.path.join(os.getcwd(), in_file.replace('.'+tsv, '.'+maf+'.json'))
        
        #col = ['Hugo_Symbol', 'Entrez_Gene_Id', 'Center', 'NCBI_Build', 'Chromosome', 'Start_position', 'End_position', 'Strand', 'Variant_Classification', 'Variant_Type', 'Reference_Allele', 'Tumor_Seq_Allele1', 'Tumor_Seq_Allele2', 'dbSNP_RS', 'dbSNP_Val_Status', 'Tumor_Sample_Barcode', 'Matched_Norm_Sample_Barcode', 'Match_Norm_Seq_Allele1', 'Match_Norm_Seq_Allele2', 'Tumor_Validation_Allele1', 'Tumor_Validation_Allele2', 'Match_Norm_Validation_Allele1', 'Match_Norm_Validation_Allele2', 'Verification_Status', 'Validation_Status', 'Mutation_Status', 'Sequencing_Phase', 'Sequence_Source', 'Validation_Method', 'Score', 'BAM_file', 'Sequencer', 'Tumor_Sample_UUID', 'Matched_Norm_Sample_UUID', 'Genome_Change', 'Annotation_Transcript', 'Transcript_Strand', 'Transcript_Exon', 'Transcript_Position', 'cDNA_Change', 'Codon_Change', 'Protein_Change', 'Other_Transcripts', 'Refseq_mRNA_Id', 'Refseq_prot_Id', 'SwissProt_acc_Id', 'SwissProt_entry_Id', 'Description', 'UniProt_AApos', 'UniProt_Region', 'UniProt_Site', 'UniProt_Natural_Variations', 'UniProt_Experimental_Info', 'GO_Biological_Process', 'GO_Cellular_Component', 'GO_Molecular_Function', 'COSMIC_overlapping_mutations', 'COSMIC_fusion_genes', 'COSMIC_tissue_types_affected', 'COSMIC_total_alterations_in_gene', 'Tumorscape_Amplification_Peaks', 'Tumorscape_Deletion_Peaks', 'TCGAscape_Amplification_Peaks', 'TCGAscape_Deletion_Peaks', 'DrugBank', 'ref_context', 'gc_content', 'CCLE_ONCOMAP_overlapping_mutations', 'CCLE_ONCOMAP_total_mutations_in_gene', 'CGC_Mutation_Type', 'CGC_Translocation_Partner', 'CGC_Tumor_Types_Somatic', 'CGC_Tumor_Types_Germline', 'CGC_Other_Diseases', 'DNARepairGenes_Role', 'FamilialCancerDatabase_Syndromes', 'MUTSIG_Published_Results', 'OREGANNO_ID', 'OREGANNO_Values', '1000Genome_AA', '1000Genome_AC', '1000Genome_AF', '1000Genome_AFR_AF', '1000Genome_AMR_AF', '1000Genome_AN', '1000Genome_CIEND', '1000Genome_CIPOS', '1000Genome_CS', '1000Genome_DP', '1000Genome_EAS_AF', '1000Genome_END', '1000Genome_EUR_AF', '1000Genome_IMPRECISE', '1000Genome_MC', '1000Genome_MEINFO', '1000Genome_MEND', '1000Genome_MLEN', '1000Genome_MSTART', '1000Genome_NS', '1000Genome_SAS_AF', '1000Genome_SVLEN', '1000Genome_SVTYPE', '1000Genome_TSD', 'ACHILLES_Lineage_Results_Top_Genes', 'CGC_Cancer', 'Germline', 'Mut', 'CGC_Cancer', 'Molecular', 'Genetics', 'CGC_Cancer', 'Somatic', 'Mut', 'CGC_Cancer', 'Syndrome', 'CGC_Chr', 'CGC_Chr', 'Band', 'CGC_GeneID', 'CGC_Name', 'CGC_Other', 'Germline', 'Mut', 'CGC_Tissue', 'Type', 'COSMIC_n_overlapping_mutations', 'COSMIC_overlapping_mutation_descriptions', 'COSMIC_overlapping_primary_sites', 'ClinVar_ASSEMBLY', 'ClinVar_HGMD_ID', 'ClinVar_SYM', 'ClinVar_TYPE', 'ClinVar_rs', 'ESP_AA', 'ESP_AAC', 'ESP_AA_AC', 'ESP_AA_AGE', 'ESP_AA_GTC', 'ESP_AvgAAsampleReadDepth', 'ESP_AvgEAsampleReadDepth', 'ESP_AvgSampleReadDepth', 'ESP_CA', 'ESP_CDP', 'ESP_CG', 'ESP_CP', 'ESP_Chromosome', 'ESP_DBSNP', 'ESP_DP', 'ESP_EA_AC', 'ESP_EA_AGE', 'ESP_EA_GTC', 'ESP_EXOME_CHIP', 'ESP_FG', 'ESP_GL', 'ESP_GM', 'ESP_GS', 'ESP_GTC', 'ESP_GTS', 'ESP_GWAS_PUBMED', 'ESP_MAF', 'ESP_PH', 'ESP_PP', 'ESP_Position', 'ESP_TAC', 'ESP_TotalAAsamplesCovered', 'ESP_TotalEAsamplesCovered', 'ESP_TotalSamplesCovered', 'Ensembl_so_accession', 'Ensembl_so_term', 'Familial_Cancer_Genes_Reference', 'Familial_Cancer_Genes_Synonym', 'HGNC_Accession', 'Numbers', 'HGNC_CCDS', 'IDs', 'HGNC_Chromosome', 'HGNC_Date', 'Modified', 'HGNC_Date', 'Name', 'Changed', 'HGNC_Date', 'Symbol', 'Changed', 'HGNC_Ensembl', 'Gene', 'ID', 'HGNC_Ensembl', 'ID(supplied', 'by', 'Ensembl)', 'HGNC_Entrez', 'Gene', 'ID(supplied', 'by', 'NCBI)', 'HGNC_Enzyme', 'IDs', 'HGNC_Gene', 'family', 'description', 'HGNC_HGNC', 'ID', 'HGNC_Locus', 'Group', 'HGNC_Locus', 'Type', 'HGNC_Name', 'Synonyms', 'HGNC_OMIM', 'ID(supplied', 'by', 'NCBI)', 'HGNC_Previous', 'Names', 'HGNC_Previous', 'Symbols', 'HGNC_Primary', 'IDs', 'HGNC_Pubmed', 'IDs', 'HGNC_Record', 'Type', 'HGNC_RefSeq', 'IDs', 'HGNC_RefSeq(supplied', 'by', 'NCBI)', 'HGNC_Secondary', 'IDs', 'HGNC_Status', 'HGNC_Synonyms', 'HGNC_UCSC', 'ID(supplied', 'by', 'UCSC)', 'HGNC_UniProt', 'ID(supplied', 'by', 'UniProt)', 'HGNC_VEGA', 'IDs', 'HGVS_coding_DNA_change', 'HGVS_genomic_change', 'HGVS_protein_change', 'ORegAnno_bin', 'UniProt_alt_uniprot_accessions', 'build', 'ccds_id', 'dbNSFP_1000Gp1_AC', 'dbNSFP_1000Gp1_AF', 'dbNSFP_1000Gp1_AFR_AC', 'dbNSFP_1000Gp1_AFR_AF', 'dbNSFP_1000Gp1_AMR_AC', 'dbNSFP_1000Gp1_AMR_AF', 'dbNSFP_1000Gp1_ASN_AC', 'dbNSFP_1000Gp1_ASN_AF', 'dbNSFP_1000Gp1_EUR_AC', 'dbNSFP_1000Gp1_EUR_AF', 'dbNSFP_Ancestral_allele', 'dbNSFP_CADD_phred', 'dbNSFP_CADD_raw', 'dbNSFP_CADD_raw_rankscore', 'dbNSFP_ESP6500_AA_AF', 'dbNSFP_ESP6500_EA_AF', 'dbNSFP_Ensembl_geneid', 'dbNSFP_Ensembl_transcriptid', 'dbNSFP_FATHMM_pred', 'dbNSFP_FATHMM_rankscore', 'dbNSFP_FATHMM_score', 'dbNSFP_GERP++_NR', 'dbNSFP_GERP++_RS', 'dbNSFP_GERP++_RS_rankscore', 'dbNSFP_Interpro_domain', 'dbNSFP_LRT_Omega', 'dbNSFP_LRT_converted_rankscore', 'dbNSFP_LRT_pred', 'dbNSFP_LRT_score', 'dbNSFP_LR_pred', 'dbNSFP_LR_rankscore', 'dbNSFP_LR_score', 'dbNSFP_MutationAssessor_pred', 'dbNSFP_MutationAssessor_rankscore', 'dbNSFP_MutationAssessor_score', 'dbNSFP_MutationTaster_converted_rankscore', 'dbNSFP_MutationTaster_pred', 'dbNSFP_MutationTaster_score', 'dbNSFP_Polyphen2_HDIV_pred', 'dbNSFP_Polyphen2_HDIV_rankscore', 'dbNSFP_Polyphen2_HDIV_score', 'dbNSFP_Polyphen2_HVAR_pred', 'dbNSFP_Polyphen2_HVAR_rankscore', 'dbNSFP_Polyphen2_HVAR_score', 'dbNSFP_RadialSVM_pred', 'dbNSFP_RadialSVM_rankscore', 'dbNSFP_RadialSVM_score', 'dbNSFP_Reliability_index', 'dbNSFP_SIFT_converted_rankscore', 'dbNSFP_SIFT_pred', 'dbNSFP_SIFT_score', 'dbNSFP_SLR_test_statistic', 'dbNSFP_SiPhy_29way_logOdds', 'dbNSFP_SiPhy_29way_logOdds_rankscore', 'dbNSFP_SiPhy_29way_pi', 'dbNSFP_UniSNP_ids', 'dbNSFP_Uniprot_aapos', 'dbNSFP_Uniprot_acc', 'dbNSFP_Uniprot_id', 'dbNSFP_aaalt', 'dbNSFP_aapos', 'dbNSFP_aapos_FATHMM', 'dbNSFP_aapos_SIFT', 'dbNSFP_aaref', 'dbNSFP_cds_strand', 'dbNSFP_codonpos', 'dbNSFP_fold-degenerate', 'dbNSFP_genename', 'dbNSFP_hg18_pos(1-coor)', 'dbNSFP_phastCons100way_vertebrate', 'dbNSFP_phastCons100way_vertebrate_rankscore', 'dbNSFP_phastCons46way_placental', 'dbNSFP_phastCons46way_placental_rankscore', 'dbNSFP_phastCons46way_primate', 'dbNSFP_phastCons46way_primate_rankscore', 'dbNSFP_phyloP100way_vertebrate', 'dbNSFP_phyloP100way_vertebrate_rankscore', 'dbNSFP_phyloP46way_placental', 'dbNSFP_phyloP46way_placental_rankscore', 'dbNSFP_phyloP46way_primate', 'dbNSFP_phyloP46way_primate_rankscore', 'dbNSFP_refcodon', 'gencode_transcript_name', 'gencode_transcript_status', 'gencode_transcript_tags', 'gencode_transcript_type', 'gene_id', 'gene_type', 'havana_transcript', 'secondary_variant_classification', 'strand', 'transcript_id']

        out = open(out_file, 'w+')
        ct = 1
        out.writelines('{"data": [')
        with open(in_file, 'r') as f:
            for i in f.readlines():
                url = 'http://www.broadinstitute.org/oncotator/mutation/{}_{}_{}_{}_{}/'.format(i.split()[0], i.split()[1], i.split()[2], i.split()[3], i.split()[4])
                res = requests.get(url)
                out.writelines(res.text)
                if ct != len(f.readlines()):
                    out.writelines(',')
                ct+=1
        out.writelines(']}')
        out.close()

        df = pd.read_json(out_file)
        print(df['data'])

def work_log(work_data):
    startTime = time.time()
    p1 = autoOncotator(work_data[0], work_data[1], args.input_dir, args.output_dir, args.tsv, args.maf)
    
    #p1.remove_snp(p1.project, p1.input_dir, p1.output_dir)
    #p1.vcf2oncotator(p1.project, p1.output_dir, p1.tsv)
    p1.oncotator_api(p1.project, p1.output_dir, p1.tsv, p1.maf)
    
    
    endTime = time.time()
    print('>>> Done for vcf [%s] : %.2f min.' %(work_data[1], (endTime-startTime)/60))

def pool_handler():
    p = Pool(args.pool_size)
    p.map(work_log, work)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=dedent("""\
Testing environment: Python 3.6

Inputs:
1. vcf file: Specify the file name with the -v or --vcf argument.

Outputs:
1. filter.vcf file: Remove SNP from the specified vcf file.
2. tsv file: Generate the input format file for Oncotator.
3. maf file: Annotated variants by Oncotator(http://portals.broadinstitute.org/oncotator/) using API.
    * Variants_num: Numbers of the variants in the input vcf file.
    * non-SNP Variants_num: Numbers of the non-SNP variants in the input vcf file.

Usage:
1. List all vcfs in specified directory (e.g. current working directory)
python3 autoOncotator.py -l .
2. One vcf file
python3 autoOncotator.py -v test123.mutect2.vcf
3. Parallel annotate vcf files
python3 autoOncotator.py -p -v test123.mutect2.vcf
"""))
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-v', '--vcf', type=str, help='Variant call file, vcf format.')
    optional.add_argument('-i', '--input_dir', type=str, default=os.getcwd(), help='input directory (default: current working directory)')
    optional.add_argument('-o', '--output_dir', type=str, default=os.getcwd(), help='output directory (default: current working directory)')
    optional.add_argument('-t', '--tsv', type=str, default='tsv', help='Generate the input format file for Oncotator, you can defined the name of the file (default: tsv)')
    optional.add_argument('-m', '--maf', type=str, default='oncotator.maf.txt', help='output file name (default: oncotator.maf.txt)')
    optional.add_argument('-l', '--list_id', type=str, help='list all vcf files in specified directory')
    optional.add_argument('-p', '--pool_size', type=int, default=1, help='Pool size of multi-thread for parallel computing (default: 15)')
    optional.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)
    parser._action_groups.append(optional)
    args = parser.parse_args()
    
    if args.vcf is None and args.list_id is None:
        parser.print_help()
        
    if args.vcf:
        vcfs = str(args.vcf).split(',')
        logger_stderr.info('Loading %s...' %(vcfs))
        
        if args.input_dir:
            logger_stderr.info('Input directory: [%s]' %(args.input_dir))
            
        if args.output_dir:
            logger_stderr.info('Output directory: [%s]' %(args.output_dir))
            
        if args.tsv:
            logger_stderr.info('Name of input file for Oncotator: [%s]' %(args.tsv))
            
        if args.maf:
            logger_stderr.info('Output file name: [%s]' %(args.maf))
        
        if args.pool_size:
            logger_stderr.info('Pool size of multi-thread for parallel computing: [%s]' %(args.pool_size))
            
        work = []
        for i, j in enumerate(vcfs):
            work.append([i, j.strip()])
        work = tuple(work)
        #print(work)
        pool_handler()
    
    if args.list_id is not None:
        test = [i for i in os.listdir(args.list_id) if '.vcf' in i]
        txt = str()
        for i in test:
            txt += i+','
        logger_stderr.info('list all vcfs in [%s]...\n>>> Num. of list: [%s]\n>>> list: [%s]' %(os.getcwd(), len(test), txt[:-1]))
    

