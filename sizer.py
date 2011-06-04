#!/usr/bin/python
import urllib
import sys

Verbose, Scale, Name  = False, 1, "bytes"

def GetSize(link):
    site = urllib.urlopen(link)
    size = int(site.info().getheaders("Content-Length")[0])
    if Verbose: print "%s / %.2f %s" % ( link.split('/')[-1].strip(), size/Scale, Name )
    return size

# generator for opening files
def gen_open(filenames):
    for name in filenames:
        yield open(name)

# cat all files in one
def gen_cat(sources):
    for s in sources:
        for item in s: yield item


if __name__ == "__main__":
    
    if len(sys.argv)==1:
        print """Usage: sizer.py [-key] [-key2] filename-with-urls [another-one-filename]
       Keys are: -v verbose, -m megabytes, -g gigabyte"""
        exit(1)

    if "-v" in sys.argv:
        Verbose = True
        sys.argv.remove("-v")

    if "-m" in sys.argv:
        Scale, Name = 1048576.0, "Mb"
        sys.argv.remove("-m")

    if "-g" in sys.argv:
        Scale, Name = 1073741824.0, "Gb"
        sys.argv.remove("-g")

    urlfiles = gen_open(sys.argv[1:])
    urllist = gen_cat(urlfiles)
    bytes = (GetSize(x) for x in urllist)
    total = sum(bytes)
    print "Total: %d %s" % (total/Scale, Name)
