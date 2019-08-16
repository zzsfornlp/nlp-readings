<!--- tools/README -->
## Generating Markdown file from the json data file.
### Usage:
`python3 ../tools/json2md.py -h`

	usage: json2md.py [-h] [-i PATH] [-o PATH] [-e PATH] [--filter FILTER]
					  [--summary SUMMARY] [--sort SORT] [--sep SEP] [--show SHOW]

	optional arguments:
	  -h, --help            show this help message and exit
	  -i PATH, --input PATH
							Input data json-file (default stdin).
	  -o PATH, --output PATH
							Output md-file (default stdout).
	  -e PATH, --extra PATH
							Extra output file (default stderr).
	  --filter FILTER       Filter code, eg.: d.year==2018 and d.proc=="ACL"
	  --summary SUMMARY     Summary/Counting code, eg.: (d.year, d.proc).
	  --sort SORT           Sorting code, eg.: (d.year, d.idx)
	  --sep SEP             Fields for separating (sep by ",").
	  --show SHOW           Fields for showing (sep by ",")

### Examples:

	# [Default]: list them all
	python3 ../tool/json2md.py -i ../data/data.json -o output.md

	# filter by tag (the ones with tag "train")
	python3 ../tool/json2md.py -i ../data/data.json --filter "'train' in d.tag" -o train.md

	# more complex filters (2016/2017-EMNLP-tag=="train")
	python3 ../tool/json2md.py -i ../data/data.json --filter "'train' in d.tag and (d.year==2016 or d.year==2017) and d.proc=='EMNLP'" -o train2.md

	# sorting and spearating by specific criterions (proc, year)
	python3 ../tool/json2md.py -i ../data/data.json --sort "(d.proc, d.year)" --show "proc,year,title" --sep "proc,year" -o all2.md

	# displaying specific fields (only year,proc,title,link)
	python3 ../tool/json2md.py -i ../data/data.json --show "year,proc,title,link" -o all3.md

### Note:

Surely, the json data itself can be utilized to print in other formats, I think its field names are easy to understand.
