mock_download_gff3_result = """##gff-version 3
#!gff-spec-version 1.21
#!processor NCBI annotwriter
##sequence-region NC_072680.1 1 15417
##species https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=213953
NC_072680.1	RefSeq	region	1	15417	.	+	.	ID=NC_072680.1:1..15417;Dbxref=taxon:213953;Is_circular=true;Name=MT;gbkey=Src;genome=mitochondrion;isolate=par015;mol_type=genomic DNA
NC_072680.1	RefSeq	gene	1	806	.	+	.	ID=gene-P6G87_mgr01;Dbxref=GeneID:79505109;Name=rrn12;gbkey=Gene;gene=rrn12;gene_biotype=rRNA;locus_tag=P6G87_mgr01
NC_072680.1	RefSeq	rRNA	1	806	.	+	.	ID=rna-P6G87_mgr01;Parent=gene-P6G87_mgr01;Dbxref=GeneID:79505109;gbkey=rRNA;gene=rrn12;locus_tag=P6G87_mgr01;product=12S ribosomal RNA
NC_072680.1	RefSeq	exon	1	806	.	+	.	ID=exon-P6G87_mgr01-1;Parent=rna-P6G87_mgr01;Dbxref=GeneID:79505109;gbkey=rRNA;gene=rrn12;locus_tag=P6G87_mgr01;product=12S ribosomal RNA
NC_072680.1	RefSeq	gene	807	870	.	+	.	ID=gene-P6G87_mgt01;Dbxref=GeneID:79505110;Name=trnV(uac);gbkey=Gene;gene=trnV(uac);gene_biotype=tRNA;locus_tag=P6G87_mgt01
NC_072680.1	RefSeq	tRNA	807	870	.	+	.	ID=rna-P6G87_mgt01;Parent=gene-P6G87_mgt01;Dbxref=GeneID:79505110;gbkey=tRNA;gene=trnV(uac);locus_tag=P6G87_mgt01;product=tRNA-Val
NC_072680.1	RefSeq	exon	807	870	.	+	.	ID=exon-P6G87_mgt01-1;Parent=rna-P6G87_mgt01;Dbxref=GeneID:79505110;gbkey=tRNA;gene=trnV(uac);locus_tag=P6G87_mgt01;product=tRNA-Val
NC_072680.1	RefSeq	gene	871	2232	.	+	.	ID=gene-P6G87_mgr02;Dbxref=GeneID:79505088;Name=rrn16;gbkey=Gene;gene=rrn16;gene_biotype=rRNA;locus_tag=P6G87_mgr02
NC_072680.1	RefSeq	rRNA	871	2232	.	+	.	ID=rna-P6G87_mgr02;Parent=gene-P6G87_mgr02;Dbxref=GeneID:79505088;gbkey=rRNA;gene=rrn16;locus_tag=P6G87_mgr02;product=16S ribosomal RNA
NC_072680.1	RefSeq	exon	871	2232	.	+	.	ID=exon-P6G87_mgr02-1;Parent=rna-P6G87_mgr02;Dbxref=GeneID:79505088;gbkey=rRNA;gene=rrn16;locus_tag=P6G87_mgr02;product=16S ribosomal RNA
NC_072680.1	RefSeq	gene	2233	2301	.	+	.	ID=gene-P6G87_mgt02;Dbxref=GeneID:79505111;Name=trnL(uag);gbkey=Gene;gene=trnL(uag);gene_biotype=tRNA;locus_tag=P6G87_mgt02
NC_072680.1	RefSeq	tRNA	2233	2301	.	+	.	ID=rna-P6G87_mgt02;Parent=gene-P6G87_mgt02;Dbxref=GeneID:79505111;gbkey=tRNA;gene=trnL(uag);locus_tag=P6G87_mgt02;product=tRNA-Leu
NC_072680.1	RefSeq	exon	2233	2301	.	+	.	ID=exon-P6G87_mgt02-1;Parent=rna-P6G87_mgt02;Dbxref=GeneID:79505111;gbkey=tRNA;gene=trnL(uag);locus_tag=P6G87_mgt02;product=tRNA-Leu
NC_072680.1	RefSeq	gene	2303	3241	.	+	.	ID=gene-P6G87_mgp13;Dbxref=GeneID:79505089;Name=ND1;gbkey=Gene;gene=ND1;gene_biotype=protein_coding;locus_tag=P6G87_mgp13
NC_072680.1	RefSeq	CDS	2303	3241	.	+	0	ID=cds-YP_010729870.1;Parent=gene-P6G87_mgp13;Dbxref=GenBank:YP_010729870.1,GeneID:79505089;Name=YP_010729870.1;gbkey=CDS;gene=ND1;locus_tag=P6G87_mgp13;product=NADH dehydrogenase subunit 1;protein_id=YP_010729870.1;transl_table=5
NC_072680.1	RefSeq	gene	3258	3322	.	-	.	ID=gene-P6G87_mgt03;Dbxref=GeneID:79505075;Name=trnS(uga);gbkey=Gene;gene=trnS(uga);gene_biotype=tRNA;locus_tag=P6G87_mgt03
NC_072680.1	RefSeq	tRNA	3258	3322	.	-	.	ID=rna-P6G87_mgt03;Parent=gene-P6G87_mgt03;Dbxref=GeneID:79505075;gbkey=tRNA;gene=trnS(uga);locus_tag=P6G87_mgt03;product=tRNA-Ser
NC_072680.1	RefSeq	exon	3258	3322	.	-	.	ID=exon-P6G87_mgt03-1;Parent=rna-P6G87_mgt03;Dbxref=GeneID:79505075;gbkey=tRNA;gene=trnS(uga);locus_tag=P6G87_mgt03;product=tRNA-Ser
NC_072680.1	RefSeq	gene	3323	4474	.	-	.	ID=gene-P6G87_mgp12;Dbxref=GeneID:79505090;Name=CYTB;gbkey=Gene;gene=CYTB;gene_biotype=protein_coding;locus_tag=P6G87_mgp12
NC_072680.1	RefSeq	CDS	3323	4474	.	-	0	ID=cds-YP_010729871.1;Parent=gene-P6G87_mgp12;Dbxref=GenBank:YP_010729871.1,GeneID:79505090;Name=YP_010729871.1;gbkey=CDS;gene=CYTB;locus_tag=P6G87_mgp12;product=cytochrome b;protein_id=YP_010729871.1;transl_table=5
NC_072680.1	RefSeq	gene	4488	5018	.	-	.	ID=gene-P6G87_mgp11;Dbxref=GeneID:79505076;Name=ND6;gbkey=Gene;gene=ND6;gene_biotype=protein_coding;locus_tag=P6G87_mgp11
NC_072680.1	RefSeq	CDS	4488	5018	.	-	0	ID=cds-YP_010729872.1;Parent=gene-P6G87_mgp11;Dbxref=GenBank:YP_010729872.1,GeneID:79505076;Name=YP_010729872.1;gbkey=CDS;gene=ND6;locus_tag=P6G87_mgp11;product=NADH dehydrogenase subunit 6;protein_id=YP_010729872.1;transl_table=5
NC_072680.1	RefSeq	gene	5021	5085	.	+	.	ID=gene-P6G87_mgt04;Dbxref=GeneID:79505077;Name=trnP(ugg);gbkey=Gene;gene=trnP(ugg);gene_biotype=tRNA;locus_tag=P6G87_mgt04
NC_072680.1	RefSeq	tRNA	5021	5085	.	+	.	ID=rna-P6G87_mgt04;Parent=gene-P6G87_mgt04;Dbxref=GeneID:79505077;gbkey=tRNA;gene=trnP(ugg);locus_tag=P6G87_mgt04;product=tRNA-Pro
NC_072680.1	RefSeq	exon	5021	5085	.	+	.	ID=exon-P6G87_mgt04-1;Parent=rna-P6G87_mgt04;Dbxref=GeneID:79505077;gbkey=tRNA;gene=trnP(ugg);locus_tag=P6G87_mgt04;product=tRNA-Pro
NC_072680.1	RefSeq	gene	5086	5151	.	-	.	ID=gene-P6G87_mgt05;Dbxref=GeneID:79505091;Name=trnT(ugu);gbkey=Gene;gene=trnT(ugu);gene_biotype=tRNA;locus_tag=P6G87_mgt05
NC_072680.1	RefSeq	tRNA	5086	5151	.	-	.	ID=rna-P6G87_mgt05;Parent=gene-P6G87_mgt05;Dbxref=GeneID:79505091;gbkey=tRNA;gene=trnT(ugu);locus_tag=P6G87_mgt05;product=tRNA-Thr
NC_072680.1	RefSeq	exon	5086	5151	.	-	.	ID=exon-P6G87_mgt05-1;Parent=rna-P6G87_mgt05;Dbxref=GeneID:79505091;gbkey=tRNA;gene=trnT(ugu);locus_tag=P6G87_mgt05;product=tRNA-Thr
NC_072680.1	RefSeq	gene	5154	5444	.	+	.	ID=gene-P6G87_mgp10;Dbxref=GeneID:79505092;Name=ND4L;gbkey=Gene;gene=ND4L;gene_biotype=protein_coding;locus_tag=P6G87_mgp10
NC_072680.1	RefSeq	CDS	5154	5444	.	+	0	ID=cds-YP_010729873.1;Parent=gene-P6G87_mgp10;Dbxref=GenBank:YP_010729873.1,GeneID:79505092;Name=YP_010729873.1;gbkey=CDS;gene=ND4L;locus_tag=P6G87_mgp10;product=NADH dehydrogenase subunit 4L;protein_id=YP_010729873.1;transl_table=5
NC_072680.1	RefSeq	gene	5445	6785	.	+	.	ID=gene-P6G87_mgp09;Dbxref=GeneID:79505078;Name=ND4;gbkey=Gene;gene=ND4;gene_biotype=protein_coding;locus_tag=P6G87_mgp09
NC_072680.1	RefSeq	CDS	5445	6785	.	+	0	ID=cds-YP_010729874.1;Parent=gene-P6G87_mgp09;Dbxref=GenBank:YP_010729874.1,GeneID:79505078;Name=YP_010729874.1;gbkey=CDS;gene=ND4;locus_tag=P6G87_mgp09;product=NADH dehydrogenase subunit 4;protein_id=YP_010729874.1;transl_table=5
NC_072680.1	RefSeq	gene	6786	6846	.	+	.	ID=gene-P6G87_mgt06;Dbxref=GeneID:79505079;Name=trnH(gug);gbkey=Gene;gene=trnH(gug);gene_biotype=tRNA;locus_tag=P6G87_mgt06
NC_072680.1	RefSeq	tRNA	6786	6846	.	+	.	ID=rna-P6G87_mgt06;Parent=gene-P6G87_mgt06;Dbxref=GeneID:79505079;gbkey=tRNA;gene=trnH(gug);locus_tag=P6G87_mgt06;product=tRNA-His
NC_072680.1	RefSeq	exon	6786	6846	.	+	.	ID=exon-P6G87_mgt06-1;Parent=rna-P6G87_mgt06;Dbxref=GeneID:79505079;gbkey=tRNA;gene=trnH(gug);locus_tag=P6G87_mgt06;product=tRNA-His
NC_072680.1	RefSeq	gene	6847	8583	.	+	.	ID=gene-P6G87_mgp08;Dbxref=GeneID:79505093;Name=ND5;gbkey=Gene;gene=ND5;gene_biotype=protein_coding;locus_tag=P6G87_mgp08
NC_072680.1	RefSeq	CDS	6847	8583	.	+	0	ID=cds-YP_010729875.1;Parent=gene-P6G87_mgp08;Dbxref=GenBank:YP_010729875.1,GeneID:79505093;Name=YP_010729875.1;gbkey=CDS;gene=ND5;locus_tag=P6G87_mgp08;product=NADH dehydrogenase subunit 5;protein_id=YP_010729875.1;transl_table=5
NC_072680.1	RefSeq	gene	8585	8648	.	+	.	ID=gene-P6G87_mgt07;Dbxref=GeneID:79505080;Name=trnF(gaa);gbkey=Gene;gene=trnF(gaa);gene_biotype=tRNA;locus_tag=P6G87_mgt07
NC_072680.1	RefSeq	tRNA	8585	8648	.	+	.	ID=rna-P6G87_mgt07;Parent=gene-P6G87_mgt07;Dbxref=GeneID:79505080;gbkey=tRNA;gene=trnF(gaa);locus_tag=P6G87_mgt07;product=tRNA-Phe
NC_072680.1	RefSeq	exon	8585	8648	.	+	.	ID=exon-P6G87_mgt07-1;Parent=rna-P6G87_mgt07;Dbxref=GeneID:79505080;gbkey=tRNA;gene=trnF(gaa);locus_tag=P6G87_mgt07;product=tRNA-Phe
NC_072680.1	RefSeq	gene	8647	8711	.	-	.	ID=gene-P6G87_mgt08;Dbxref=GeneID:79505094;Name=trnE(uuc);gbkey=Gene;gene=trnE(uuc);gene_biotype=tRNA;locus_tag=P6G87_mgt08
NC_072680.1	RefSeq	tRNA	8647	8711	.	-	.	ID=rna-P6G87_mgt08;Parent=gene-P6G87_mgt08;Dbxref=GeneID:79505094;gbkey=tRNA;gene=trnE(uuc);locus_tag=P6G87_mgt08;product=tRNA-Glu
NC_072680.1	RefSeq	exon	8647	8711	.	-	.	ID=exon-P6G87_mgt08-1;Parent=rna-P6G87_mgt08;Dbxref=GeneID:79505094;gbkey=tRNA;gene=trnE(uuc);locus_tag=P6G87_mgt08;product=tRNA-Glu
NC_072680.1	RefSeq	gene	8777	8837	.	-	.	ID=gene-P6G87_mgt09;Dbxref=GeneID:79505095;Name=trnS(gcu);gbkey=Gene;gene=trnS(gcu);gene_biotype=tRNA;locus_tag=P6G87_mgt09
NC_072680.1	RefSeq	tRNA	8777	8837	.	-	.	ID=rna-P6G87_mgt09;Parent=gene-P6G87_mgt09;Dbxref=GeneID:79505095;gbkey=tRNA;gene=trnS(gcu);locus_tag=P6G87_mgt09;product=tRNA-Ser
NC_072680.1	RefSeq	exon	8777	8837	.	-	.	ID=exon-P6G87_mgt09-1;Parent=rna-P6G87_mgt09;Dbxref=GeneID:79505095;gbkey=tRNA;gene=trnS(gcu);locus_tag=P6G87_mgt09;product=tRNA-Ser
NC_072680.1	RefSeq	gene	8841	8906	.	-	.	ID=gene-P6G87_mgt10;Dbxref=GeneID:79505096;Name=trnN(guu);gbkey=Gene;gene=trnN(guu);gene_biotype=tRNA;locus_tag=P6G87_mgt10
NC_072680.1	RefSeq	tRNA	8841	8906	.	-	.	ID=rna-P6G87_mgt10;Parent=gene-P6G87_mgt10;Dbxref=GeneID:79505096;gbkey=tRNA;gene=trnN(guu);locus_tag=P6G87_mgt10;product=tRNA-Asn
NC_072680.1	RefSeq	exon	8841	8906	.	-	.	ID=exon-P6G87_mgt10-1;Parent=rna-P6G87_mgt10;Dbxref=GeneID:79505096;gbkey=tRNA;gene=trnN(guu);locus_tag=P6G87_mgt10;product=tRNA-Asn
NC_072680.1	RefSeq	gene	8909	8974	.	-	.	ID=gene-P6G87_mgt11;Dbxref=GeneID:79505097;Name=trnR(ucg);gbkey=Gene;gene=trnR(ucg);gene_biotype=tRNA;locus_tag=P6G87_mgt11
NC_072680.1	RefSeq	tRNA	8909	8974	.	-	.	ID=rna-P6G87_mgt11;Parent=gene-P6G87_mgt11;Dbxref=GeneID:79505097;gbkey=tRNA;gene=trnR(ucg);locus_tag=P6G87_mgt11;product=tRNA-Arg
NC_072680.1	RefSeq	exon	8909	8974	.	-	.	ID=exon-P6G87_mgt11-1;Parent=rna-P6G87_mgt11;Dbxref=GeneID:79505097;gbkey=tRNA;gene=trnR(ucg);locus_tag=P6G87_mgt11;product=tRNA-Arg
NC_072680.1	RefSeq	gene	8975	9039	.	-	.	ID=gene-P6G87_mgt12;Dbxref=GeneID:79505098;Name=trnA(ugc);gbkey=Gene;gene=trnA(ugc);gene_biotype=tRNA;locus_tag=P6G87_mgt12
NC_072680.1	RefSeq	tRNA	8975	9039	.	-	.	ID=rna-P6G87_mgt12;Parent=gene-P6G87_mgt12;Dbxref=GeneID:79505098;gbkey=tRNA;gene=trnA(ugc);locus_tag=P6G87_mgt12;product=tRNA-Ala
NC_072680.1	RefSeq	exon	8975	9039	.	-	.	ID=exon-P6G87_mgt12-1;Parent=rna-P6G87_mgt12;Dbxref=GeneID:79505098;gbkey=tRNA;gene=trnA(ugc);locus_tag=P6G87_mgt12;product=tRNA-Ala
NC_072680.1	RefSeq	gene	9040	9393	.	-	.	ID=gene-P6G87_mgp07;Dbxref=GeneID:79505099;Name=ND3;gbkey=Gene;gene=ND3;gene_biotype=protein_coding;locus_tag=P6G87_mgp07
NC_072680.1	RefSeq	CDS	9040	9393	.	-	0	ID=cds-YP_010729876.1;Parent=gene-P6G87_mgp07;Dbxref=GenBank:YP_010729876.1,GeneID:79505099;Name=YP_010729876.1;gbkey=CDS;gene=ND3;locus_tag=P6G87_mgp07;product=NADH dehydrogenase subunit 3;protein_id=YP_010729876.1;transl_table=5
NC_072680.1	RefSeq	gene	9394	9460	.	-	.	ID=gene-P6G87_mgt13;Dbxref=GeneID:79505081;Name=trnG(ucc);gbkey=Gene;gene=trnG(ucc);gene_biotype=tRNA;locus_tag=P6G87_mgt13
NC_072680.1	RefSeq	tRNA	9394	9460	.	-	.	ID=rna-P6G87_mgt13;Parent=gene-P6G87_mgt13;Dbxref=GeneID:79505081;gbkey=tRNA;gene=trnG(ucc);locus_tag=P6G87_mgt13;product=tRNA-Gly
NC_072680.1	RefSeq	exon	9394	9460	.	-	.	ID=exon-P6G87_mgt13-1;Parent=rna-P6G87_mgt13;Dbxref=GeneID:79505081;gbkey=tRNA;gene=trnG(ucc);locus_tag=P6G87_mgt13;product=tRNA-Gly
NC_072680.1	RefSeq	gene	9464	10252	.	-	.	ID=gene-P6G87_mgp06;Dbxref=GeneID:79505100;Name=COX3;gbkey=Gene;gene=COX3;gene_biotype=protein_coding;locus_tag=P6G87_mgp06
NC_072680.1	RefSeq	CDS	9464	10252	.	-	0	ID=cds-YP_010729877.1;Parent=gene-P6G87_mgp06;Dbxref=GenBank:YP_010729877.1,GeneID:79505100;Name=YP_010729877.1;gbkey=CDS;gene=COX3;locus_tag=P6G87_mgp06;product=cytochrome c oxidase subunit III;protein_id=YP_010729877.1;transl_table=5
NC_072680.1	RefSeq	gene	10252	10929	.	-	.	ID=gene-P6G87_mgp05;Dbxref=GeneID:79505082;Name=ATP6;gbkey=Gene;gene=ATP6;gene_biotype=protein_coding;locus_tag=P6G87_mgp05
NC_072680.1	RefSeq	CDS	10252	10929	.	-	0	ID=cds-YP_010729878.1;Parent=gene-P6G87_mgp05;Dbxref=GenBank:YP_010729878.1,GeneID:79505082;Name=YP_010729878.1;gbkey=CDS;gene=ATP6;locus_tag=P6G87_mgp05;product=ATP synthase F0 subunit 6;protein_id=YP_010729878.1;transl_table=5
NC_072680.1	RefSeq	gene	10923	11087	.	-	.	ID=gene-P6G87_mgp04;Dbxref=GeneID:79505083;Name=ATP8;gbkey=Gene;gene=ATP8;gene_biotype=protein_coding;locus_tag=P6G87_mgp04
NC_072680.1	RefSeq	CDS	10923	11087	.	-	0	ID=cds-YP_010729879.1;Parent=gene-P6G87_mgp04;Dbxref=GenBank:YP_010729879.1,GeneID:79505083;Name=YP_010729879.1;gbkey=CDS;gene=ATP8;locus_tag=P6G87_mgp04;product=ATP synthase F0 subunit 8;protein_id=YP_010729879.1;transl_table=5
NC_072680.1	RefSeq	gene	11088	11155	.	-	.	ID=gene-P6G87_mgt14;Dbxref=GeneID:79505084;Name=trnD(guc);gbkey=Gene;gene=trnD(guc);gene_biotype=tRNA;locus_tag=P6G87_mgt14
NC_072680.1	RefSeq	tRNA	11088	11155	.	-	.	ID=rna-P6G87_mgt14;Parent=gene-P6G87_mgt14;Dbxref=GeneID:79505084;gbkey=tRNA;gene=trnD(guc);locus_tag=P6G87_mgt14;product=tRNA-Asp
NC_072680.1	RefSeq	exon	11088	11155	.	-	.	ID=exon-P6G87_mgt14-1;Parent=rna-P6G87_mgt14;Dbxref=GeneID:79505084;gbkey=tRNA;gene=trnD(guc);locus_tag=P6G87_mgt14;product=tRNA-Asp
NC_072680.1	RefSeq	gene	11156	11225	.	-	.	ID=gene-P6G87_mgt15;Dbxref=GeneID:79505101;Name=trnK(cuu);gbkey=Gene;gene=trnK(cuu);gene_biotype=tRNA;locus_tag=P6G87_mgt15
NC_072680.1	RefSeq	tRNA	11156	11225	.	-	.	ID=rna-P6G87_mgt15;Parent=gene-P6G87_mgt15;Dbxref=GeneID:79505101;gbkey=tRNA;gene=trnK(cuu);locus_tag=P6G87_mgt15;product=tRNA-Lys
NC_072680.1	RefSeq	exon	11156	11225	.	-	.	ID=exon-P6G87_mgt15-1;Parent=rna-P6G87_mgt15;Dbxref=GeneID:79505101;gbkey=tRNA;gene=trnK(cuu);locus_tag=P6G87_mgt15;product=tRNA-Lys
NC_072680.1	RefSeq	gene	11226	11907	.	-	.	ID=gene-P6G87_mgp03;Dbxref=GeneID:79505102;Name=COX2;gbkey=Gene;gene=COX2;gene_biotype=protein_coding;locus_tag=P6G87_mgp03
NC_072680.1	RefSeq	CDS	11226	11907	.	-	0	ID=cds-YP_010729880.1;Parent=gene-P6G87_mgp03;Dbxref=GenBank:YP_010729880.1,GeneID:79505102;Name=YP_010729880.1;Note=TAA stop codon is completed by the addition of 3' A residues to the mRNA;gbkey=CDS;gene=COX2;locus_tag=P6G87_mgp03;product=cytochrome c oxidase subunit II;protein_id=YP_010729880.1;transl_except=(pos:complement(11226..11226)%2Caa:TERM);transl_table=5
NC_072680.1	RefSeq	gene	11908	11969	.	-	.	ID=gene-P6G87_mgt16;Dbxref=GeneID:79505085;Name=trnL(uaa);gbkey=Gene;gene=trnL(uaa);gene_biotype=tRNA;locus_tag=P6G87_mgt16
NC_072680.1	RefSeq	tRNA	11908	11969	.	-	.	ID=rna-P6G87_mgt16;Parent=gene-P6G87_mgt16;Dbxref=GeneID:79505085;gbkey=tRNA;gene=trnL(uaa);locus_tag=P6G87_mgt16;product=tRNA-Leu
NC_072680.1	RefSeq	exon	11908	11969	.	-	.	ID=exon-P6G87_mgt16-1;Parent=rna-P6G87_mgt16;Dbxref=GeneID:79505085;gbkey=tRNA;gene=trnL(uaa);locus_tag=P6G87_mgt16;product=tRNA-Leu
NC_072680.1	RefSeq	gene	11970	13505	.	-	.	ID=gene-P6G87_mgp02;Dbxref=GeneID:79505103;Name=COX1;end_range=13505,.;gbkey=Gene;gene=COX1;gene_biotype=protein_coding;locus_tag=P6G87_mgp02;partial=true
NC_072680.1	RefSeq	CDS	11970	13505	.	-	0	ID=cds-YP_010729881.1;Parent=gene-P6G87_mgp02;Dbxref=GenBank:YP_010729881.1,GeneID:79505103;Name=YP_010729881.1;Note=can not determine the start codon;end_range=13505,.;gbkey=CDS;gene=COX1;locus_tag=P6G87_mgp02;partial=true;product=cytochrome c oxidase subunit I;protein_id=YP_010729881.1;transl_table=5
NC_072680.1	RefSeq	gene	13509	13572	.	+	.	ID=gene-P6G87_mgt17;Dbxref=GeneID:79505086;Name=trnY(gua);gbkey=Gene;gene=trnY(gua);gene_biotype=tRNA;locus_tag=P6G87_mgt17
NC_072680.1	RefSeq	tRNA	13509	13572	.	+	.	ID=rna-P6G87_mgt17;Parent=gene-P6G87_mgt17;Dbxref=GeneID:79505086;gbkey=tRNA;gene=trnY(gua);locus_tag=P6G87_mgt17;product=tRNA-Tyr
NC_072680.1	RefSeq	exon	13509	13572	.	+	.	ID=exon-P6G87_mgt17-1;Parent=rna-P6G87_mgt17;Dbxref=GeneID:79505086;gbkey=tRNA;gene=trnY(gua);locus_tag=P6G87_mgt17;product=tRNA-Tyr
NC_072680.1	RefSeq	gene	13577	13643	.	+	.	ID=gene-P6G87_mgt18;Dbxref=GeneID:79505104;Name=trnC(gca);gbkey=Gene;gene=trnC(gca);gene_biotype=tRNA;locus_tag=P6G87_mgt18
NC_072680.1	RefSeq	tRNA	13577	13643	.	+	.	ID=rna-P6G87_mgt18;Parent=gene-P6G87_mgt18;Dbxref=GeneID:79505104;gbkey=tRNA;gene=trnC(gca);locus_tag=P6G87_mgt18;product=tRNA-Cys
NC_072680.1	RefSeq	exon	13577	13643	.	+	.	ID=exon-P6G87_mgt18-1;Parent=rna-P6G87_mgt18;Dbxref=GeneID:79505104;gbkey=tRNA;gene=trnC(gca);locus_tag=P6G87_mgt18;product=tRNA-Cys
NC_072680.1	RefSeq	gene	13636	13700	.	-	.	ID=gene-P6G87_mgt19;Dbxref=GeneID:79505105;Name=trnW(uca);gbkey=Gene;gene=trnW(uca);gene_biotype=tRNA;locus_tag=P6G87_mgt19
NC_072680.1	RefSeq	tRNA	13636	13700	.	-	.	ID=rna-P6G87_mgt19;Parent=gene-P6G87_mgt19;Dbxref=GeneID:79505105;gbkey=tRNA;gene=trnW(uca);locus_tag=P6G87_mgt19;product=tRNA-Trp
NC_072680.1	RefSeq	exon	13636	13700	.	-	.	ID=exon-P6G87_mgt19-1;Parent=rna-P6G87_mgt19;Dbxref=GeneID:79505105;gbkey=tRNA;gene=trnW(uca);locus_tag=P6G87_mgt19;product=tRNA-Trp
NC_072680.1	RefSeq	gene	13701	14714	.	-	.	ID=gene-P6G87_mgp01;Dbxref=GeneID:79505106;Name=ND2;gbkey=Gene;gene=ND2;gene_biotype=protein_coding;locus_tag=P6G87_mgp01
NC_072680.1	RefSeq	CDS	13701	14714	.	-	0	ID=cds-YP_010729882.1;Parent=gene-P6G87_mgp01;Dbxref=GenBank:YP_010729882.1,GeneID:79505106;Name=YP_010729882.1;gbkey=CDS;gene=ND2;locus_tag=P6G87_mgp01;product=NADH dehydrogenase subunit 2;protein_id=YP_010729882.1;transl_table=5
NC_072680.1	RefSeq	gene	14757	14825	.	+	.	ID=gene-P6G87_mgt20;Dbxref=GeneID:79505087;Name=trnQ(uug);gbkey=Gene;gene=trnQ(uug);gene_biotype=tRNA;locus_tag=P6G87_mgt20
NC_072680.1	RefSeq	tRNA	14757	14825	.	+	.	ID=rna-P6G87_mgt20;Parent=gene-P6G87_mgt20;Dbxref=GeneID:79505087;gbkey=tRNA;gene=trnQ(uug);locus_tag=P6G87_mgt20;product=tRNA-Gln
NC_072680.1	RefSeq	exon	14757	14825	.	+	.	ID=exon-P6G87_mgt20-1;Parent=rna-P6G87_mgt20;Dbxref=GeneID:79505087;gbkey=tRNA;gene=trnQ(uug);locus_tag=P6G87_mgt20;product=tRNA-Gln
NC_072680.1	RefSeq	gene	14823	14886	.	-	.	ID=gene-P6G87_mgt21;Dbxref=GeneID:79505107;Name=trnI(gau);gbkey=Gene;gene=trnI(gau);gene_biotype=tRNA;locus_tag=P6G87_mgt21
NC_072680.1	RefSeq	tRNA	14823	14886	.	-	.	ID=rna-P6G87_mgt21;Parent=gene-P6G87_mgt21;Dbxref=GeneID:79505107;gbkey=tRNA;gene=trnI(gau);locus_tag=P6G87_mgt21;product=tRNA-Ile
NC_072680.1	RefSeq	exon	14823	14886	.	-	.	ID=exon-P6G87_mgt21-1;Parent=rna-P6G87_mgt21;Dbxref=GeneID:79505107;gbkey=tRNA;gene=trnI(gau);locus_tag=P6G87_mgt21;product=tRNA-Ile
NC_072680.1	RefSeq	gene	14888	14956	.	-	.	ID=gene-P6G87_mgt22;Dbxref=GeneID:79505108;Name=trnM(cau);gbkey=Gene;gene=trnM(cau);gene_biotype=tRNA;locus_tag=P6G87_mgt22
NC_072680.1	RefSeq	tRNA	14888	14956	.	-	.	ID=rna-P6G87_mgt22;Parent=gene-P6G87_mgt22;Dbxref=GeneID:79505108;gbkey=tRNA;gene=trnM(cau);locus_tag=P6G87_mgt22;product=tRNA-Met
NC_072680.1	RefSeq	exon	14888	14956	.	-	.	ID=exon-P6G87_mgt22-1;Parent=rna-P6G87_mgt22;Dbxref=GeneID:79505108;gbkey=tRNA;gene=trnM(cau);locus_tag=P6G87_mgt22;product=tRNA-Met
NC_072680.1	RefSeq	D_loop	14957	15417	.	+	.	ID=id-NC_072680.1:14957..15417;Note=A+T rich region containing origin of replication;gbkey=D-loop

##sequence-region OP953390.1 1 15417
##species https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=213953
OP953390.1	Genbank	region	1	15417	.	+	.	ID=OP953390.1:1..15417;Dbxref=taxon:213953;Is_circular=true;Name=MT;gbkey=Src;genome=mitochondrion;isolate=par015;mol_type=genomic DNA
OP953390.1	Genbank	gene	1	806	.	+	.	ID=gene-rrn12;Name=rrn12;gbkey=Gene;gene=rrn12;gene_biotype=rRNA
OP953390.1	Genbank	rRNA	1	806	.	+	.	ID=rna-rrn12;Parent=gene-rrn12;gbkey=rRNA;gene=rrn12;product=12S ribosomal RNA
OP953390.1	Genbank	exon	1	806	.	+	.	ID=exon-rrn12-1;Parent=rna-rrn12;gbkey=rRNA;gene=rrn12;product=12S ribosomal RNA
OP953390.1	Genbank	gene	807	870	.	+	.	ID=gene-trnV(uac);Name=trnV(uac);gbkey=Gene;gene=trnV(uac);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	807	870	.	+	.	ID=rna-trnV(uac);Parent=gene-trnV(uac);gbkey=tRNA;gene=trnV(uac);product=tRNA-Val
OP953390.1	Genbank	exon	807	870	.	+	.	ID=exon-trnV(uac)-1;Parent=rna-trnV(uac);gbkey=tRNA;gene=trnV(uac);product=tRNA-Val
OP953390.1	Genbank	gene	871	2232	.	+	.	ID=gene-rrn16;Name=rrn16;gbkey=Gene;gene=rrn16;gene_biotype=rRNA
OP953390.1	Genbank	rRNA	871	2232	.	+	.	ID=rna-rrn16;Parent=gene-rrn16;gbkey=rRNA;gene=rrn16;product=16S ribosomal RNA
OP953390.1	Genbank	exon	871	2232	.	+	.	ID=exon-rrn16-1;Parent=rna-rrn16;gbkey=rRNA;gene=rrn16;product=16S ribosomal RNA
OP953390.1	Genbank	gene	2233	2301	.	+	.	ID=gene-trnL(uag);Name=trnL(uag);gbkey=Gene;gene=trnL(uag);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	2233	2301	.	+	.	ID=rna-trnL(uag);Parent=gene-trnL(uag);gbkey=tRNA;gene=trnL(uag);product=tRNA-Leu
OP953390.1	Genbank	exon	2233	2301	.	+	.	ID=exon-trnL(uag)-1;Parent=rna-trnL(uag);gbkey=tRNA;gene=trnL(uag);product=tRNA-Leu
OP953390.1	Genbank	gene	2303	3241	.	+	.	ID=gene-ND1;Name=ND1;gbkey=Gene;gene=ND1;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	2303	3241	.	+	0	ID=cds-WEF74741.1;Parent=gene-ND1;Dbxref=NCBI_GP:WEF74741.1;Name=WEF74741.1;gbkey=CDS;gene=ND1;product=NADH dehydrogenase subunit 1;protein_id=WEF74741.1;transl_table=5
OP953390.1	Genbank	gene	3258	3322	.	-	.	ID=gene-trnS(uga);Name=trnS(uga);gbkey=Gene;gene=trnS(uga);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	3258	3322	.	-	.	ID=rna-trnS(uga);Parent=gene-trnS(uga);gbkey=tRNA;gene=trnS(uga);product=tRNA-Ser
OP953390.1	Genbank	exon	3258	3322	.	-	.	ID=exon-trnS(uga)-1;Parent=rna-trnS(uga);gbkey=tRNA;gene=trnS(uga);product=tRNA-Ser
OP953390.1	Genbank	gene	3323	4474	.	-	.	ID=gene-CYTB;Name=CYTB;gbkey=Gene;gene=CYTB;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	3323	4474	.	-	0	ID=cds-WEF74742.1;Parent=gene-CYTB;Dbxref=NCBI_GP:WEF74742.1;Name=WEF74742.1;gbkey=CDS;gene=CYTB;product=cytochrome b;protein_id=WEF74742.1;transl_table=5
OP953390.1	Genbank	gene	4488	5018	.	-	.	ID=gene-ND6;Name=ND6;gbkey=Gene;gene=ND6;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	4488	5018	.	-	0	ID=cds-WEF74743.1;Parent=gene-ND6;Dbxref=NCBI_GP:WEF74743.1;Name=WEF74743.1;gbkey=CDS;gene=ND6;product=NADH dehydrogenase subunit 6;protein_id=WEF74743.1;transl_table=5
OP953390.1	Genbank	gene	5021	5085	.	+	.	ID=gene-trnP(ugg);Name=trnP(ugg);gbkey=Gene;gene=trnP(ugg);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	5021	5085	.	+	.	ID=rna-trnP(ugg);Parent=gene-trnP(ugg);gbkey=tRNA;gene=trnP(ugg);product=tRNA-Pro
OP953390.1	Genbank	exon	5021	5085	.	+	.	ID=exon-trnP(ugg)-1;Parent=rna-trnP(ugg);gbkey=tRNA;gene=trnP(ugg);product=tRNA-Pro
OP953390.1	Genbank	gene	5086	5151	.	-	.	ID=gene-trnT(ugu);Name=trnT(ugu);gbkey=Gene;gene=trnT(ugu);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	5086	5151	.	-	.	ID=rna-trnT(ugu);Parent=gene-trnT(ugu);gbkey=tRNA;gene=trnT(ugu);product=tRNA-Thr
OP953390.1	Genbank	exon	5086	5151	.	-	.	ID=exon-trnT(ugu)-1;Parent=rna-trnT(ugu);gbkey=tRNA;gene=trnT(ugu);product=tRNA-Thr
OP953390.1	Genbank	gene	5154	5444	.	+	.	ID=gene-ND4L;Name=ND4L;gbkey=Gene;gene=ND4L;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	5154	5444	.	+	0	ID=cds-WEF74744.1;Parent=gene-ND4L;Dbxref=NCBI_GP:WEF74744.1;Name=WEF74744.1;gbkey=CDS;gene=ND4L;product=NADH dehydrogenase subunit 4L;protein_id=WEF74744.1;transl_table=5
OP953390.1	Genbank	gene	5445	6785	.	+	.	ID=gene-ND4;Name=ND4;gbkey=Gene;gene=ND4;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	5445	6785	.	+	0	ID=cds-WEF74745.1;Parent=gene-ND4;Dbxref=NCBI_GP:WEF74745.1;Name=WEF74745.1;gbkey=CDS;gene=ND4;product=NADH dehydrogenase subunit 4;protein_id=WEF74745.1;transl_table=5
OP953390.1	Genbank	gene	6786	6846	.	+	.	ID=gene-trnH(gug);Name=trnH(gug);gbkey=Gene;gene=trnH(gug);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	6786	6846	.	+	.	ID=rna-trnH(gug);Parent=gene-trnH(gug);gbkey=tRNA;gene=trnH(gug);product=tRNA-His
OP953390.1	Genbank	exon	6786	6846	.	+	.	ID=exon-trnH(gug)-1;Parent=rna-trnH(gug);gbkey=tRNA;gene=trnH(gug);product=tRNA-His
OP953390.1	Genbank	gene	6847	8583	.	+	.	ID=gene-ND5;Name=ND5;gbkey=Gene;gene=ND5;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	6847	8583	.	+	0	ID=cds-WEF74746.1;Parent=gene-ND5;Dbxref=NCBI_GP:WEF74746.1;Name=WEF74746.1;gbkey=CDS;gene=ND5;product=NADH dehydrogenase subunit 5;protein_id=WEF74746.1;transl_table=5
OP953390.1	Genbank	gene	8585	8648	.	+	.	ID=gene-trnF(gaa);Name=trnF(gaa);gbkey=Gene;gene=trnF(gaa);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	8585	8648	.	+	.	ID=rna-trnF(gaa);Parent=gene-trnF(gaa);gbkey=tRNA;gene=trnF(gaa);product=tRNA-Phe
OP953390.1	Genbank	exon	8585	8648	.	+	.	ID=exon-trnF(gaa)-1;Parent=rna-trnF(gaa);gbkey=tRNA;gene=trnF(gaa);product=tRNA-Phe
OP953390.1	Genbank	gene	8647	8711	.	-	.	ID=gene-trnE(uuc);Name=trnE(uuc);gbkey=Gene;gene=trnE(uuc);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	8647	8711	.	-	.	ID=rna-trnE(uuc);Parent=gene-trnE(uuc);gbkey=tRNA;gene=trnE(uuc);product=tRNA-Glu
OP953390.1	Genbank	exon	8647	8711	.	-	.	ID=exon-trnE(uuc)-1;Parent=rna-trnE(uuc);gbkey=tRNA;gene=trnE(uuc);product=tRNA-Glu
OP953390.1	Genbank	gene	8777	8837	.	-	.	ID=gene-trnS(gcu);Name=trnS(gcu);gbkey=Gene;gene=trnS(gcu);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	8777	8837	.	-	.	ID=rna-trnS(gcu);Parent=gene-trnS(gcu);gbkey=tRNA;gene=trnS(gcu);product=tRNA-Ser
OP953390.1	Genbank	exon	8777	8837	.	-	.	ID=exon-trnS(gcu)-1;Parent=rna-trnS(gcu);gbkey=tRNA;gene=trnS(gcu);product=tRNA-Ser
OP953390.1	Genbank	gene	8841	8906	.	-	.	ID=gene-trnN(guu);Name=trnN(guu);gbkey=Gene;gene=trnN(guu);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	8841	8906	.	-	.	ID=rna-trnN(guu);Parent=gene-trnN(guu);gbkey=tRNA;gene=trnN(guu);product=tRNA-Asn
OP953390.1	Genbank	exon	8841	8906	.	-	.	ID=exon-trnN(guu)-1;Parent=rna-trnN(guu);gbkey=tRNA;gene=trnN(guu);product=tRNA-Asn
OP953390.1	Genbank	gene	8909	8974	.	-	.	ID=gene-trnR(ucg);Name=trnR(ucg);gbkey=Gene;gene=trnR(ucg);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	8909	8974	.	-	.	ID=rna-trnR(ucg);Parent=gene-trnR(ucg);gbkey=tRNA;gene=trnR(ucg);product=tRNA-Arg
OP953390.1	Genbank	exon	8909	8974	.	-	.	ID=exon-trnR(ucg)-1;Parent=rna-trnR(ucg);gbkey=tRNA;gene=trnR(ucg);product=tRNA-Arg
OP953390.1	Genbank	gene	8975	9039	.	-	.	ID=gene-trnA(ugc);Name=trnA(ugc);gbkey=Gene;gene=trnA(ugc);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	8975	9039	.	-	.	ID=rna-trnA(ugc);Parent=gene-trnA(ugc);gbkey=tRNA;gene=trnA(ugc);product=tRNA-Ala
OP953390.1	Genbank	exon	8975	9039	.	-	.	ID=exon-trnA(ugc)-1;Parent=rna-trnA(ugc);gbkey=tRNA;gene=trnA(ugc);product=tRNA-Ala
OP953390.1	Genbank	gene	9040	9393	.	-	.	ID=gene-ND3;Name=ND3;gbkey=Gene;gene=ND3;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	9040	9393	.	-	0	ID=cds-WEF74747.1;Parent=gene-ND3;Dbxref=NCBI_GP:WEF74747.1;Name=WEF74747.1;gbkey=CDS;gene=ND3;product=NADH dehydrogenase subunit 3;protein_id=WEF74747.1;transl_table=5
OP953390.1	Genbank	gene	9394	9460	.	-	.	ID=gene-trnG(ucc);Name=trnG(ucc);gbkey=Gene;gene=trnG(ucc);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	9394	9460	.	-	.	ID=rna-trnG(ucc);Parent=gene-trnG(ucc);gbkey=tRNA;gene=trnG(ucc);product=tRNA-Gly
OP953390.1	Genbank	exon	9394	9460	.	-	.	ID=exon-trnG(ucc)-1;Parent=rna-trnG(ucc);gbkey=tRNA;gene=trnG(ucc);product=tRNA-Gly
OP953390.1	Genbank	gene	9464	10252	.	-	.	ID=gene-COX3;Name=COX3;gbkey=Gene;gene=COX3;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	9464	10252	.	-	0	ID=cds-WEF74748.1;Parent=gene-COX3;Dbxref=NCBI_GP:WEF74748.1;Name=WEF74748.1;gbkey=CDS;gene=COX3;product=cytochrome c oxidase subunit III;protein_id=WEF74748.1;transl_table=5
OP953390.1	Genbank	gene	10252	10929	.	-	.	ID=gene-ATP6;Name=ATP6;gbkey=Gene;gene=ATP6;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	10252	10929	.	-	0	ID=cds-WEF74749.1;Parent=gene-ATP6;Dbxref=NCBI_GP:WEF74749.1;Name=WEF74749.1;gbkey=CDS;gene=ATP6;product=ATP synthase F0 subunit 6;protein_id=WEF74749.1;transl_table=5
OP953390.1	Genbank	gene	10923	11087	.	-	.	ID=gene-ATP8;Name=ATP8;gbkey=Gene;gene=ATP8;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	10923	11087	.	-	0	ID=cds-WEF74750.1;Parent=gene-ATP8;Dbxref=NCBI_GP:WEF74750.1;Name=WEF74750.1;gbkey=CDS;gene=ATP8;product=ATP synthase F0 subunit 8;protein_id=WEF74750.1;transl_table=5
OP953390.1	Genbank	gene	11088	11155	.	-	.	ID=gene-trnD(guc);Name=trnD(guc);gbkey=Gene;gene=trnD(guc);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	11088	11155	.	-	.	ID=rna-trnD(guc);Parent=gene-trnD(guc);gbkey=tRNA;gene=trnD(guc);product=tRNA-Asp
OP953390.1	Genbank	exon	11088	11155	.	-	.	ID=exon-trnD(guc)-1;Parent=rna-trnD(guc);gbkey=tRNA;gene=trnD(guc);product=tRNA-Asp
OP953390.1	Genbank	gene	11156	11225	.	-	.	ID=gene-trnK(cuu);Name=trnK(cuu);gbkey=Gene;gene=trnK(cuu);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	11156	11225	.	-	.	ID=rna-trnK(cuu);Parent=gene-trnK(cuu);gbkey=tRNA;gene=trnK(cuu);product=tRNA-Lys
OP953390.1	Genbank	exon	11156	11225	.	-	.	ID=exon-trnK(cuu)-1;Parent=rna-trnK(cuu);gbkey=tRNA;gene=trnK(cuu);product=tRNA-Lys
OP953390.1	Genbank	gene	11226	11907	.	-	.	ID=gene-COX2;Name=COX2;gbkey=Gene;gene=COX2;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	11226	11907	.	-	0	ID=cds-WEF74751.1;Parent=gene-COX2;Dbxref=NCBI_GP:WEF74751.1;Name=WEF74751.1;Note=TAA stop codon is completed by the addition of 3' A residues to the mRNA;gbkey=CDS;gene=COX2;product=cytochrome c oxidase subunit II;protein_id=WEF74751.1;transl_except=(pos:complement(11226..11226)%2Caa:TERM);transl_table=5
OP953390.1	Genbank	gene	11908	11969	.	-	.	ID=gene-trnL(uaa);Name=trnL(uaa);gbkey=Gene;gene=trnL(uaa);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	11908	11969	.	-	.	ID=rna-trnL(uaa);Parent=gene-trnL(uaa);gbkey=tRNA;gene=trnL(uaa);product=tRNA-Leu
OP953390.1	Genbank	exon	11908	11969	.	-	.	ID=exon-trnL(uaa)-1;Parent=rna-trnL(uaa);gbkey=tRNA;gene=trnL(uaa);product=tRNA-Leu
OP953390.1	Genbank	gene	11970	13505	.	-	.	ID=gene-COX1;Name=COX1;end_range=13505,.;gbkey=Gene;gene=COX1;gene_biotype=protein_coding;partial=true
OP953390.1	Genbank	CDS	11970	13505	.	-	0	ID=cds-WEF74752.1;Parent=gene-COX1;Dbxref=NCBI_GP:WEF74752.1;Name=WEF74752.1;Note=can not determine the start codon;end_range=13505,.;gbkey=CDS;gene=COX1;partial=true;product=cytochrome c oxidase subunit I;protein_id=WEF74752.1;transl_table=5
OP953390.1	Genbank	gene	13509	13572	.	+	.	ID=gene-trnY(gua);Name=trnY(gua);gbkey=Gene;gene=trnY(gua);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	13509	13572	.	+	.	ID=rna-trnY(gua);Parent=gene-trnY(gua);gbkey=tRNA;gene=trnY(gua);product=tRNA-Tyr
OP953390.1	Genbank	exon	13509	13572	.	+	.	ID=exon-trnY(gua)-1;Parent=rna-trnY(gua);gbkey=tRNA;gene=trnY(gua);product=tRNA-Tyr
OP953390.1	Genbank	gene	13577	13643	.	+	.	ID=gene-trnC(gca);Name=trnC(gca);gbkey=Gene;gene=trnC(gca);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	13577	13643	.	+	.	ID=rna-trnC(gca);Parent=gene-trnC(gca);gbkey=tRNA;gene=trnC(gca);product=tRNA-Cys
OP953390.1	Genbank	exon	13577	13643	.	+	.	ID=exon-trnC(gca)-1;Parent=rna-trnC(gca);gbkey=tRNA;gene=trnC(gca);product=tRNA-Cys
OP953390.1	Genbank	gene	13636	13700	.	-	.	ID=gene-trnW(uca);Name=trnW(uca);gbkey=Gene;gene=trnW(uca);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	13636	13700	.	-	.	ID=rna-trnW(uca);Parent=gene-trnW(uca);gbkey=tRNA;gene=trnW(uca);product=tRNA-Trp
OP953390.1	Genbank	exon	13636	13700	.	-	.	ID=exon-trnW(uca)-1;Parent=rna-trnW(uca);gbkey=tRNA;gene=trnW(uca);product=tRNA-Trp
OP953390.1	Genbank	gene	13701	14714	.	-	.	ID=gene-ND2;Name=ND2;gbkey=Gene;gene=ND2;gene_biotype=protein_coding
OP953390.1	Genbank	CDS	13701	14714	.	-	0	ID=cds-WEF74753.1;Parent=gene-ND2;Dbxref=NCBI_GP:WEF74753.1;Name=WEF74753.1;gbkey=CDS;gene=ND2;product=NADH dehydrogenase subunit 2;protein_id=WEF74753.1;transl_table=5
OP953390.1	Genbank	gene	14757	14825	.	+	.	ID=gene-trnQ(uug);Name=trnQ(uug);gbkey=Gene;gene=trnQ(uug);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	14757	14825	.	+	.	ID=rna-trnQ(uug);Parent=gene-trnQ(uug);gbkey=tRNA;gene=trnQ(uug);product=tRNA-Gln
OP953390.1	Genbank	exon	14757	14825	.	+	.	ID=exon-trnQ(uug)-1;Parent=rna-trnQ(uug);gbkey=tRNA;gene=trnQ(uug);product=tRNA-Gln
OP953390.1	Genbank	gene	14823	14886	.	-	.	ID=gene-trnI(gau);Name=trnI(gau);gbkey=Gene;gene=trnI(gau);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	14823	14886	.	-	.	ID=rna-trnI(gau);Parent=gene-trnI(gau);gbkey=tRNA;gene=trnI(gau);product=tRNA-Ile
OP953390.1	Genbank	exon	14823	14886	.	-	.	ID=exon-trnI(gau)-1;Parent=rna-trnI(gau);gbkey=tRNA;gene=trnI(gau);product=tRNA-Ile
OP953390.1	Genbank	gene	14888	14956	.	-	.	ID=gene-trnM(cau);Name=trnM(cau);gbkey=Gene;gene=trnM(cau);gene_biotype=tRNA
OP953390.1	Genbank	tRNA	14888	14956	.	-	.	ID=rna-trnM(cau);Parent=gene-trnM(cau);gbkey=tRNA;gene=trnM(cau);product=tRNA-Met
OP953390.1	Genbank	exon	14888	14956	.	-	.	ID=exon-trnM(cau)-1;Parent=rna-trnM(cau);gbkey=tRNA;gene=trnM(cau);product=tRNA-Met
OP953390.1	Genbank	D_loop	14957	15417	.	+	.	ID=id-OP953390.1:14957..15417;Note=A+T rich region containing origin of replication;gbkey=D-loop

##sequence-region OQ164359.1 1 387
##species https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=213953
OQ164359.1	Genbank	region	1	387	.	+	.	ID=OQ164359.1:1..387;Dbxref=taxon:213953;gbkey=Src;genome=genomic;mol_type=mRNA;specimen-voucher=par015
OQ164359.1	Genbank	gene	1	387	.	+	.	ID=gene-hyp24;Name=hyp24;end_range=387,.;gbkey=Gene;gene=hyp24;partial=true;start_range=.,1
OQ164359.1	Genbank	CDS	1	387	.	+	0	ID=cds-WDS95887.1;Parent=gene-hyp24;Dbxref=NCBI_GP:WDS95887.1;Name=WDS95887.1;end_range=387,.;gbkey=CDS;gene=hyp24;partial=true;product=hypothetical protein;protein_id=WDS95887.1;start_range=.,1

##sequence-region OQ164309.1 1 765
##species https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=213953
OQ164309.1	Genbank	region	1	765	.	+	.	ID=OQ164309.1:1..765;Dbxref=taxon:213953;gbkey=Src;genome=genomic;mol_type=mRNA;specimen-voucher=par015
OQ164309.1	Genbank	gene	1	765	.	+	.	ID=gene-hyp22;Name=hyp22;end_range=765,.;gbkey=Gene;gene=hyp22;partial=true;start_range=.,1
OQ164309.1	Genbank	CDS	1	765	.	+	0	ID=cds-WDS95837.1;Parent=gene-hyp22;Dbxref=NCBI_GP:WDS95837.1;Name=WDS95837.1;end_range=765,.;gbkey=CDS;gene=hyp22;partial=true;product=hypothetical protein;protein_id=WDS95837.1;start_range=.,1

##sequence-region OQ164244.1 1 1433
##species https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=213953
OQ164244.1	Genbank	region	1	1433	.	+	.	ID=OQ164244.1:1..1433;Dbxref=taxon:213953;gbkey=Src;genome=genomic;mol_type=mRNA;specimen-voucher=par015
OQ164244.1	Genbank	gene	1	1433	.	+	.	ID=gene-hyp21;Name=hyp21;end_range=1433,.;gbkey=Gene;gene=hyp21;partial=true;start_range=.,1
OQ164244.1	Genbank	CDS	1	1433	.	+	0	ID=cds-WDS95772.1;Parent=gene-hyp21;Dbxref=NCBI_GP:WDS95772.1;Name=WDS95772.1;end_range=1433,.;gbkey=CDS;gene=hyp21;partial=true;product=hypothetical protein;protein_id=WDS95772.1;start_range=.,1

##sequence-region OQ163616.1 1 846
"""
