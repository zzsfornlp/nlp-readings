#!/bin/python3

# read csv file and generate specific easy-to-read files (currently Markdown)
import argparse, sys
from collections import Iterable

class Header(object):
    def __init__(self, heads):
        self.heads = heads
        self._idx = dict([(h, i) for i, h in enumerate(heads)])

    def index(self, f):
        assert f in self._idx, "Unknown name %s." % f
        return self._idx[f]

    def _parse(self, filter, idx):
        # ! && || name () <space>
        def _tok(filter, idx):
            while idx<len(filter) and filter[idx]==' ':
                idx += 1
            if idx>=len(filter):
                return "", idx
            s = filter[idx]
            if s in "()!":
                return s, idx+1
            elif s in "&|":
                assert idx+1<len(filter), "Unexpected EOS."
                assert filter[idx+1]==s, "Unexpected token at %s, expecting %s." % (idx+1, s)
                return s+s, idx+2
            else:
                idx += 1
                while idx<len(filter) and filter[idx] not in "()!&|":
                    s += filter[idx]
                    idx += 1
                return s, idx
        def _par_one(filter, idx):
            one, idx = _tok(filter, idx)
            if one == '(':
                f1, idx = _par_or(filter, idx)
                one2, idx = _tok(filter, idx)
                assert one2==")", "Unmatched () detected at %s" % (idx,)
                return f1, idx
            elif one == "": #EOS
                return lambda x: True, idx
            else:
                # todo(warn): only "=" currently
                fs = one.split("==")
                assert len(fs)==2, "Unsupported filter %s." % "<SEP>".join(fs)
                which, target = self.index(fs[0]), fs[1]
                def _ff(x):
                    ones = x[which]
                    if not isinstance(ones, Iterable):
                        ones = [ones]
                    return any(one==target for one in ones)
                return _ff, idx
        def _par_not(filter, idx):
            idx_old = idx
            one, idx = _tok(filter, idx)
            if one != "!":
                idx = idx_old
                return _par_one(filter, idx)
            else:
                f1, idx = _par_one(filter, idx)
                return lambda x: not f1(x), idx
        def _par_and(filter, idx):
            f1, idx = _par_not(filter, idx)
            fs = [f1]
            while idx<len(filter):
                idx_old = idx
                one, idx = _tok(filter, idx)
                if one != "&&":   # not "&&" as expected
                    idx = idx_old
                    break
                f2, idx = _par_not(filter, idx)
                fs.append(f2)
            def _ff(x):
                for _f in fs:
                    if not _f(x):
                        return False
                return True
            return _ff, idx
        def _par_or(filter, idx):
            f1, idx = _par_and(filter, idx)
            fs = [f1]
            while idx<len(filter):
                idx_old = idx
                one, idx = _tok(filter, idx)
                if one != "||":   # not "||" as expected
                    idx = idx_old
                    break
                f2, idx = _par_and(filter, idx)
                fs.append(f2)
            def _ff(x):
                for _f in fs:
                    if _f(x):
                        return True
                return False
            return _ff, idx
        ff, idx = _par_or(filter, idx)
        one, idx = _tok(filter, idx)
        assert one=="", "Unexpected token %s at %s" % (one, idx)
        return ff

    # check
    @staticmethod
    def _test_parser():
        hh = Header(["year", "date", "proc", "link"])
        print(hh.select([(1,2,3,4), (3,-1,2,2), (1,2,2,9), (2,2,2,9), (2,2,2,8)], "(year==1)|| (!link==9)&&(proc==2)"))

    # helpers #
    def all_heads(self):
        return self.heads

    def get_values(self, one, fields):
        return [one[self.index(f)] for f in fields]

    def list(self, contents, whats=None):
        ret = {}
        if whats is None:
            whats = [k for k in self.all_heads()]
        for one in whats:
            ii = self.index(one)
            ss = set()
            for c in contents:
                for tok in c[ii]:
                    ss.add(tok)
            ret[one] = sorted(list(ss))
        return ret

    def select(self, contents, filter):
        ff = self._parse(filter, 0)
        return [one for one in contents if ff(one)]

    def sort(self, contents, fields):
        ll = [self.index(name) for name in fields]
        if len(ll)==0:
            return contents
        else:
            return sorted(contents, key=lambda x: ["|".join(x[i]) for i in ll])

    def render(self, contents, sep_fields, sum_fields, show_fields):
        # separate if different (after sorting)
        rr = MarkdownRender()
        s = ""
        prev_sep = "NEVER"
        if len(show_fields)==0:
            show_fields = self.heads
        s += rr.render_start()
        for one in contents:
            this_sep = rr.render_sep(sep_fields, self.get_values(one, sep_fields))
            if this_sep != prev_sep:
                s += this_sep
                prev_sep = this_sep
            s += rr.render_sum(sum_fields, self.get_values(one, sum_fields))
            s += rr.render_ins(show_fields, self.get_values(one, show_fields))
        return s

# data presented as heads([f1, f2, f3, ..., fn])/contents([{f1:?, f2:?, ..., fn:?}, {...}, ...])
def read_csv(fname, split=",", split2="|"):
    with open(fname) as file:
        lines = [l.strip().split(split) for l in file]
    assert len(lines) > 1, "Too few data"
    heads = lines[0]
    contents = []
    for l2 in lines[1:]:
        assert len(l2) == len(heads), "Unmatched data"
        one = [c.split(split2) for c in l2]
        contents.append(one)
    return heads, contents

class MarkdownRender(object):
    def __init__(self):
        self.count = 0

    def render_start(self):
        return "==========<br>\n\# auto-generated by *'python3 %s'*<br>==========\n" % " ".join(sys.argv)

    def render_one(self, f, o, keep_f):
        # todo: special ones
        if f == "date":
            o = o[0]
            oo = "%s%s-%s" % ("19" if o[0:2]>"50" else "20", o[0:2], o[2:4])
        elif f == "link":
            o = o[0]
            oo = "[[paper]](%s), [[bib]](%s)" % (o, o+".bib")
        elif f == "tag":
            oo = ", ".join(["[[%s]](%s.md)" % (z, z) for z in sorted(o)])
        else:
            oo = ", ".join(o)
        if keep_f:
            return "%s: %s" % (f, oo)
        else:
            return oo

    def render_sep(self, fields, ones):
        s = "-----\n### "
        s += ", ".join(self.render_one(f,o,True) for f,o in zip(fields, ones))
        s += "\n\n"
        return s

    def render_sum(self, fields, ones):
        self.count += 1
        s = "##### (%s) "%self.count + ", ".join(self.render_one(f,o,False) for f,o in zip(fields, ones))+"\n\n"
        return s

    def render_ins(self, fields, ones):
        s = ""
        # s = "(%s)" % self.count
        for f,o in zip(fields, ones):
            s += "* "+self.render_one(f,o,True)+"\n"
        s += "\n\n"
        return s

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, metavar='PATH', help='Input data file (csv file, fields separated by ",").')
    parser.add_argument("-o", "--output", type=str, default=None, metavar='PATH', help='Output file (default stdout).')
    # parser.add_argument("--in_type", type=str, default="csv", choices=["csv"], help='Input file type.')
    # parser.add_argument("--out_type", type=str, default="markdown", choices=["markdown"], help='Output file type.')
    # step0: list
    parser.add_argument("--list_fields", type=str, default=None, help='List the values of fields (sep by ","; <empty> means all).')
    # step1: filter
    parser.add_argument("--filter", type=str, default=None, help='Filter like "(year==2016||year==2015)&&(proc==ACL)", currently only ==.')
    # step2: sort
    parser.add_argument("--sort_fields", type=str, default="year,date,proc,link", help='Fields for sorting (sep by ",") (default: %(default)s).')
    # step3: separate / summary / show
    parser.add_argument("--sep_fields", type=str, default="year,proc", help='Fields for separating (sep by ",") (default: %(default)s).')
    parser.add_argument("--sum_fields", type=str, default="year,proc,title", help='Fields for summary (sep by ",") (default: %(default)s).')
    parser.add_argument("--show_fields", type=str, default="year,date,proc,title,link,tag", help='Fields for printing (sep by ","; <empty> means all). (default: %(default)s)')
    a = parser.parse_args()
    # deal with them
    args = vars(a)
    for n in ["sort_fields", "sep_fields", "sum_fields", "show_fields", "list_fields"]:
        if args[n] is not None:
            if args[n] == "":
                args[n] = []
            else:
                args[n] = args[n].split(",")
    return args

def main():
    args = init()
    # read
    heads, contents = read_csv(args["file"])
    hh = Header(heads)
    # list ?
    to_list = args["list_fields"]
    if to_list is not None:
        if len(to_list) == 0:
            to_list = None
        ret = hh.list(contents, to_list)
        for k in sorted(ret.keys()):
            print("%s: %s" % (k, " ".join(ret[k])))
    else:
        contents0 = contents
        if args["filter"] is not None:
            contents0 = hh.select(contents0, args["filter"])
        contents1 = hh.sort(contents0, args["sort_fields"])
        ss = hh.render(contents1, args["sep_fields"], args["sum_fields"], args["show_fields"])
        if args["output"] is None:
            print(ss)
        else:
            with open(args["output"], "w") as ffff:
                ffff.write(ss)

SH_FILE='''
PYFILE="../tool/gen_md.py"
echo "Generate them to 'all.md'."
python3 ${PYFILE}  -f nmt-summary.csv  > all.md
echo "Generate the tag files."
python ${PYFILE} -f nmt-summary.csv --list_fields "tag"
for i in analysis attention domain model multi phrase prac search semi smt syntax train vocab;
do
python ${PYFILE} -f nmt-summary.csv  --filter "tag==$i" > $i.md
done
echo "done"
'''

if __name__ == '__main__':
    main()
