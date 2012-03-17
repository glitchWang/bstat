#-*-coding: utf-8-*-
import os, os.path, sys, csv, zipfile, glob, shutil, itertools

def list_archives(path='.'):
    base_path = os.path.abspath(path)
    zip_files = [f for f in glob.glob('%s/%s' % (base_path, '*.zip')) if zipfile.is_zipfile(f)]
    return zip_files
    
def extract_file(fname, basedir='./tmp', redo=False):
    abs_dir = os.path.abspath(basedir)
    tgt_dir = os.path.join(abs_dir, os.path.basename(fname))
    if os.path.exists(tgt_dir):
        if redo:
            shutil.rmtree(tgt_dir)
        else:
            return tgt_dir
    os.makedirs(tgt_dir)
    with zipfile.ZipFile(fname, 'r') as zip_file:
        zip_file.extractall(tgt_dir)
        return tgt_dir
        
def find_extract(srcdir='.', tgtdir='./tmp'):
    files = list_archives(srcdir)
    dirs = []
    for f in files:
        print('extracting %s to %s' % (os.path.basename(f), tgtdir))
        dirs.append(extract_file(f, basedir=tgtdir))
    return dirs
    

players = set()
types = set()

class Row(object):
    
    ATTRS = 'a1,a2,a3,a4,a5,h1,h2,h3,h4,h5,period,time,team,etype,assist,away,block,entered,home,left,num,opponent,outof,player,points,possession,reason,result,steal,type,x,y'
    ATTR_MAP = dict(zip(ATTRS.split(','), range(0, 1 + ATTRS.count(','))))
    
    def __init__(self, row_data):
        self._d = row_data
        
    def __getattr__(self, name):
        if name in Row.ATTR_MAP.keys():
            return self._d[Row.ATTR_MAP[name]]
        return getattr(object, name)
        
    def __str__(self):
        kvs = [(k, self._d[Row.ATTR_MAP[k]]) for k in Row.ATTR_MAP.keys() \
            if (self._d[Row.ATTR_MAP[k]] and (not (k.startswith('a') or k.startswith('h'))))]
        return '%s=%s:' * len(kvs) % tuple(itertools.chain(*kvs))
        
    def __repr__(self):
        return self.__str__()
        

def read_lines(fname):
    with open(fname, 'r') as csv_file:
        rdr = csv.reader(csv_file)
        for i, row in enumerate(rdr):
            if i > 0:
                yield row
                
def analyse(dirname):
    global players
    fnames = sorted(glob.glob('%s/*LAL*.csv' % dirname))
    for f in fnames:
        analyse_game(f)
        break

def analyse_game(fname):
    global types
    print('analysing %s' % fname)
    lines = read_lines(fname)
    rows = [Row(l) for l in lines]
    timeline = itertools.groupby(rows, lambda r: r.time)
    for t, e in timeline:
        print(t, list(e))
        #types.add(t)
        #print(t)
    print(','.join(types))


if __name__ == '__main__':
    all_dir = find_extract()
    for d in all_dir:
        analyse(d)
        break
        #print('total players:%s' % len(players))
    #print(players)
