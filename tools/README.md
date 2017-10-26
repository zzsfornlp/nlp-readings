<!--- tools/README -->
## Generating Markdown files from csv files.
### Usage:
`python3 ../tools/gen_md.py -h`

	usage: gen_md.py [-h] -f PATH [-o PATH] [--list_fields LIST_FIELDS]
	                 [--filter FILTER] [--sort_fields SORT_FIELDS]
	                 [--sep_fields SEP_FIELDS] [--sum_fields SUM_FIELDS]
	                 [--show_fields SHOW_FIELDS]
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -f PATH, --file PATH  Input data file (csv file, fields separated by ",").
	  -o PATH, --output PATH
	                        Output file (default stdout).
	  --list_fields LIST_FIELDS
	                        List the values of fields (sep by ","; <empty> means
	                        all).
	  --filter FILTER       Filter like "(year==2016||year==2015)&&(proc==ACL)",
	                        currently only ==.
	  --sort_fields SORT_FIELDS
	                        Fields for sorting (sep by ",") (default:
	                        year,date,proc,link).
	  --sep_fields SEP_FIELDS
	                        Fields for separating (sep by ",") (default:
	                        year,proc).
	  --sum_fields SUM_FIELDS
	                        Fields for summary (sep by ",") (default:
	                        year,proc,title).
	  --show_fields SHOW_FIELDS
	                        Fields for printing (sep by ","; <empty> means all).
	                        (default: year,date,proc,title,link,tag)

### Examples:

	# [Default]: list them all
	python3 ../tool/gen_md.py -f "<csv-file>" > all.md

	# list by tag (the ones with tag "train")
	python3 ../tool/gen_md.py -f "<csv-file>" --filter "tag==train" > train.md

	# more complex filters (2016/2017-EMNLP-tag:"train" or )
	python3 ../tool/gen_md.py -f "<csv-file>" --filter "tag==train && (year==2016||year==2017) && proc==EMNLP" > train2.md

	# sorting and spearating by specific criterions (proc, year)
	python3 ../tool/gen_md.py -f "<csv-file>" --sort_fields "proc,year" --sep_fields "proc,year" > all2.md

	# displaying specific fields (only year,proc,title,link)
	python3 ../tool/gen_md.py -f "<csv-file>" --sort_fields "year,proc,title,link" > all3.md

