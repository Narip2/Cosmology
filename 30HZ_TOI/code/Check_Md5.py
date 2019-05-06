import hashlib
import sys

def md5sum(filename):
    m = hashlib.md5()
    n = 1024*4
    inp = open(filename,'rb')
    while True:
        buf = inp.read(n)
        if buf:
            m.update(buf)
        else:
            break
    return m.hexdigest()

if __name__ == '__main__':
    createpath = "/home/narip/md5cmp.txt"
    w = open(createpath,'w')
    for i in range(91,605):
        filename1 = "/media/narip/新加卷/TOI_Data/{:0>4d}/LFI_TOI_030-PTG_R2.10_OD{:0>4d}.fits".format(i,i)
        filename2 = "/media/narip/新加卷/TOI_Data/{:0>4d}/LFI_TOI_030-SCI_R2.00_OD{:0>4d}.fits".format(i,i)
        w.write(md5sum(filename1)+"\n")
        w.write(md5sum(filename2)+"\n")
    w.close()
