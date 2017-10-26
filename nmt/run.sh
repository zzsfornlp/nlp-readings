#!/bin/bash

PYFILE="../tools/gen_md.py"
echo "Generate them to 'all.md'."
python3 ${PYFILE}  -f nmt-summary.csv  > all.md
echo "Generate the tag files."
python ${PYFILE} -f nmt-summary.csv --list_fields "tag"
for i in analysis attention domain model multi phrase prac search semi smt syntax train vocab;
do
python ${PYFILE} -f nmt-summary.csv  --filter "tag==$i" > $i.md
done
echo "done"
