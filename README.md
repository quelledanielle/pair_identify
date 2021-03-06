pair_identify
=============
Study of transcription factor cooperativity

---

# Table of contents

[**Understanding the data**](https://github.com/quelledanielle/pair_identify#understanding-the-data)  

* [**Input files**](https://github.com/quelledanielle/pair_identify#input-files)
	* tf1_list.txt
	* tf2_list.txt
	* rmsk.txt : RepeatMasker data
	* chip_seq_[tf1 code].txt : ChIP-seq data
	* M\*.txt : TFBS data
* [**Output files**](https://github.com/quelledanielle/pair_identify#output-files)
	* d_TTT_[tf2 code].csv : TFBS pairs and distances inside tf1 ChIP-seq regions
	* d_FTT_[tf2 code].csv : TFBS pairs and distances outside tf1 ChIP-seq regions
	* f_[tf2 code].csv : distance frequencies
	* s_[tf2 code].txt : number of sites and cases
	* z.csv : pairs with z-scores greater or equal to Z_THRESHOLD
	
[**Usage**](https://github.com/quelledanielle/pair_identify#usage)  

* [**Overview**](https://github.com/quelledanielle/pair_identify#overview)
	* File descriptions
* [**Running analyze.py**](https://github.com/quelledanielle/pair_identify#running-analyzepy)
	* One pair
	* All pairs
	* Using screen
* [**Setting up additional input files**](https://github.com/quelledanielle/pair_identify#setting-up-additional-input-files)
	* One pair
	* All pairs

[**TODO**](https://github.com/quelledanielle/pair_identify#todo)  
[**Contact**](https://github.com/quelledanielle/pair_identify#contact)  

---

# Understanding the data

The files used and generated by *analyze.py* can be accessed through the **koksoak.cs.mcgill.ca** server in the **/scratch/dpham4/PI/data** directory.

## Input files

### tf1_list.txt
**Path:** /scratch/dpham4/PI/data/tf1_list.txt  
**Format:** [tf1 code] [tf1 name]\\n  
**Example:** M00008 SP1  

**Description:**  
This file is a list of tf1s (transcription factors with available ChIP-seq data). M\* indicates the forward strand, whereas M\*\_r indicates the reverse strand. This list was compiled from filenames matching M\*_\*.bed in **/home/mcb/blanchem/wgEncodeRegTfbsClustered**. Some tf1s were removed that contained noPhastCons in the filename, or due to empty TFBS files.  

When running *analyze.py*, lines beginning with the \# symbol will be ignored.

### tf2_list.txt

**Path:** /scratch/dpham4/PI/data/[chromosome]/tf2_list.txt  
**Format:** [tf2 code]\\n  
**Example:** M00001  

**Description:**  
This file is a list of tf2s (all transcription factors being tested as candidate partners for tf1s). M\* indicates the forward strand, whereas M\*\_r indicates the reverse strand. This list was compiled from filenames matching sites.M\*.gz in **/scratch/blanchem/[chromsome]/sites**. Some tf2s were removed from the list due to empty TFBS files.

### rmsk.txt : RepeatMasker data

**Path:** /scratch/dpham4/PI/data/[chromosome]/rmsk.txt  
**Format:** [start position],[end position]\\n  
**Example:** 10000 10469  

**Description:**  
This file contains the positions of RepeatMasker regions in a particular chromosome. RepeatMasker data provides regions of known transposable elements in the genome. Extracted from the RepeatMasker data for all chromosomes at **/scratch/dpham4/PI/data/rmsk.txt.gz**.  

### chip_seq_[tf1 code].txt : ChIP-seq data

**Path:** /scratch/dpham4/PI/data/[chromosome]/chip_seq_[tf1 code].txt  
**Format:** [chromosome] [start position] [end position] [tf1 name]\\n  
**Example:** chr1	713863	714256	SP1  

**Description:**  
This file contains the positions of ChIP-seq regions for a particular tf1 in a particular chromosome. These are experimentally verified regions that have been sequenced after being 'fished out' using the given tf1. The tf1 may not be directly bound to the region. Extracted from **/home/mcb/blanchem/wgEncodeRegTfbsClustered/[tf1 code]_[tf1 name].bed**.

### M\*.txt : TFBS data

**Path:** /scratch/dpham4/PI/data/[chromosome]/[tf1 or tf2 code].txt  
**Format:** [genome] [site position] [score] [sequence]\\n  
**Example:** 0	10974	-9.58	GAGGCGTGGC  

**Description:**  
This file contains TFBS positions for either a tf1 or tf2. The 0 in the first column indicates that the sites are found in the human genome (hg19). The site position in the second column is used in *analyze.py*, but the remaining columns are unused. Extracted from **/scratch/blanchem/[chromsome]/sites/sites.[tf1 or tf2 code].gz**

## Output files  

### d_TTT_[tf2 code].csv : TFBS pairs and distances
#### Inside tf1 ChIP-seq regions

**Path:** /scratch/dpham4/PI/data/[chromosome]/[tf1 code]/d_TTT_[tf2 code].csv  
**Format:** [tf1 site position],[tf2 site position],[distance]\\n  
**Example:** 23181478,23181471,7  

**Description:**  
This file reports the positions of pairs with predicted sites that are found in tf1 ChIP-seq regions, and the absolute value between them, if the distance between pairs is less than MAX_TFBS_DIST. The positions may be useful for searching the [UCSC Genome Browser](http://genome.ucsc.edu/cgi-bin/hgGateway) or the [Bejerano GREAT tool](http://bejerano.stanford.edu/great/public/html/).

### d_FTT_[tf2 code].csv : TFBS pairs and distances
#### Outside tf1 ChIP-seq regions

**Path:** /scratch/dpham4/PI/data/[chromosome]/[tf1 code]/d_FTT_[tf2 code].csv  
**Format:** [tf1 site position],[tf2 site position],[distance]\\n  
**Example:** 58313,58217,96  

**Description:**  
This file reports the positions of pairs predicted sites that are not found in tf1 ChIP-seq regions, and the absolute value between them, if the distance between pairs is less than MAX_TFBS_DIST. The positions may be useful for searching the [UCSC Genome Browser](http://genome.ucsc.edu/cgi-bin/hgGateway) or the [Bejerano GREAT tool](http://bejerano.stanford.edu/great/public/html/).

### f_[tf2 code].csv : distance frequencies

**Path:** /scratch/dpham4/PI/data/[chromosome]/[tf1 code]/f_[tf2 code].csv  
**Format:** [distance],[frequency],[z-score]\\n  
**Example:** 7,929,155.999906228  

**Description:**  
This file reports (regardless of TTT or FTT categorization) the distance between pairs of binding sites, the number of times that distance was found, and a z-score. The z-score is calculated as (frequency - mean) / (standard deviation), where the mean and standard deviation have been calculated for distances greater than or equal to MIN_MEAN_CUTOFF.  

The purpose of MIN_MEAN_CUTOFF is to determine a 'background level' frequency. The first few distances are ignored as they may have large frequencies from similar PWMs (Position Weight Matrices). See Professor Blanchette for an explanation of the similar PWMs issue.

### s_[tf2 code].txt : number of sites and cases

**Path:** /scratch/dpham4/PI/data/[chromosome]/[tf1 code]/s_[tf2 code].txt  
**Format:**  
\<tf1 code\> \<number of tf1 sites\>\\n  
\<tf2 code\> \<number of tf2 sites\>\\n  
TTT \<number of TTT cases\>\\n  
FTT \<number of FTT cases\>\\n  
**Example:**  
M00795_r 36683  
M00059_r 84099  
TTT 7  
FTT 4349  

**Description:**  
This file reports counts of the number of predicted tf1 and tf2 sites, as well as the number of pairs categorized as TTT or FTT.

### z.csv : pairs with z-scores greater or equal to Z_THRESHOLD

**Path:** /scratch/dpham4/PI/data/z.csv  
**Format:** [args],[highest z-score]\\n  
**Example:** chr1 POU2F2 M00795_r M00059_r,155.999906228  

**Description:**  
A line is appended to this file if the pair's frequency data contains a z-score greater or equal to Z_THRESHOLD. The line contains args (chromosome, tf1 name, tf1 code, tf2 code), and the highest z-score found.

---

# Usage

Accessed through **koksoak.cs.mcgill.ca**, the files required to run *analyze.py* are located in the **/scratch/dpham4/PI/pair_identify** directory. They have the same contents as the files in this GitHub repository.

## Overview

**Python:** 2.7.3 on **koksoak** server

### File descriptions

#### Logistics

**.gitignore:** Files listed in the .gitignore will not be tracked by git  
**README.md:** This documentation  
**__init__.py:** Enables Python to treat pair_identify as a package  

#### Setup

**setup.sh:** Sets up rmsk, chip_seq_M\*, M\* files required for one set of args if they don't exist  
**min_rmsk.py:** Removes unnecessary columns from *rmsk.txt*, automatically run in *setup.sh*  
**tf2_list.py:** Sets up *tf2_list.txt* if it doesn't exist, automatically run with *analyze.py* --all  

#### Analysis

**analyze.py:** Main program, uses previously setup input files and generates output files  
**casedata.py:** Module containing **study()**, which generates data for TTT/FTT cases and frequencies  
**stats.py:** Module containing **z_scores()**, **mean()**, **std()** for calculating z-scores

#### Data classes

**rmsk.py:** Module containing RMSK class, which loads and stores RepeatMasker data  
**chipseq.py:** Module containing ChipSeq class, which loads and stores ChIP-seq data  
**tfbs.py:** Module containing TFBS class, which loads and stores TFBS data for tf1 or tf2

#### Log

**log:** Processing and Completed args with the local time, appended to *log* while *analyze.py* is running  
*Note:* log *is cleared at the beginning of running all args in* analyze.py 

## Running analyze.py

Either one pair of TFs or all pairs of TFs can be run by *analyze.py*. Any input files for this pair must be setup before before running *analyze.py*.  

For chr1: RepeatMasker, 45 ChIP-seq, 1243 TFBS files have already been prepared.

### One pair

**Usage:** `python analyze.py [chromosome] [tf1 name] [tf1 code] [tf2 code]`  
**Example:** `python analyze.py chr1 POU2F2 M00795_r M00059_r`

### All pairs

**Usage:** `python analyze.py --all [chromosome]`  
**Example:** `python analyze.py --all chr1`

#### Using screen

It is very useful to run `python analyze.py --all chr1` using a detached screen so the program continues running even after logging out of the server. You may find a [screen user manual](http://www.delorie.com/gnu/docs/screen/screen_toc.html) useful, but here are some basic commands:  

* To invoke a new screen, run the `screen` command
* Run the desired commands within the new screen
* To detach from the screen, press `ctrl + a`, then `d`
* To reattach the screen, run `screen -d -r`
* If several screens are running, reattach one via `screen -d -r [identifier]`  
*e.g. screen -d -r 11189.pts-5.koksoak*
* For a list of invoked screens, run `screen -ls`
* To kill a screen, run `screen -X -S [identifier] kill`
* To exit a screen, reattach it and run `exit`

## Setting up additional input files

### One pair

*setup.sh* requires the following original input files:  

* **RepeatMasker:** /scratch/dpham4/PI/data/rmsk.txt.gz
* **ChIP-seq:** /home/mcb/blanchem/wgEncodeRegTfbsClustered/[tf1 code (0:6)]\_[tf1 name].bed  
*Note: same ChIP-seq file used for forward and reverse strands, so tf1 code without _r is used*
* **TFBS (tf1):** /scratch/blanchem/[chromosome]/sites/sites.[tf1 code].gz
* **TFBS (tf2):** /scratch/blanchem/[chromosome]/sites/sites.[tf2 code].gz

If the original input files are all present, run *setup.sh*:  

**Usage:** `./setup.sh [chromosome] [tf1 name] [tf1 code] [tf2 code]`  
**Example:** `./setup.sh chr1 POU2F2 M00795_r M00059_r`

If `grep` fails, or does not find any matches, it will return 0. In turn, *setup.sh* will return an exit code corresponding to the file it was unable to prepare: {1: RepeatMasker, 2: ChIP-seq, 3: tf1 TFBS, 4: tf2 TFBS}.

### All pairs

There is no script for setting up files for all pairs, since *analyze.py* was modified to do the task only once. It is straightforward to run *setup.sh* using your own list of args.  

To call *setup.sh* in a Python script:

* `from subprocess import call`
* `call('./setup.sh %s' % args, shell=True)`  
where args has the format '[chromosome] [tf1 name] [tf1 code] [tf2 code]'

To include the new tf1 or tf2 when running all pairs in *analyze.py*:  

* Manually add them to *tf1_list.txt* or *tf2_list.txt* using the format described in  
[Understanding the data > Input files > tf1_list.txt or tf2_list.txt](https://github.com/quelledanielle/pair_identify#input-files)

*Note: for any chromosome other than chr1, you may need to remove TFs from tf2_list if the original TFBS files are empty (the tf2_list for chr1 has already been cleaned up manually)*

---

## TODO

* Further filtering of the args in *z.csv*
* Check positions of interesting distances for proximity to genes ([GREAT](http://bejerano.stanford.edu/great/public/html/))
* Data analysis to find supporting evidence of transcription factor cooperation
* Apply approach to extant mammalian genomes and inferred ancestral mammalian genomes  
*Note: current TFBS data provides positions relative to the human genome, but the TFBS positions required are from the original genomes*

---

## Contact

Feel free to use or modify any part of the existing code to suit the needs of your project.

For questions or clarification, email **danielle.pham@mail.mcgill.ca**.