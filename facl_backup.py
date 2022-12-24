#!/usr/bin/env python3
import grp
import os
import pwd
import stat
import sys

def octal_to_rwx(octal):
    rwx = 'r' if octal & 4 else '-'
    rwx += 'w' if octal & 2 else '-'
    rwx += 'x' if octal & 1 else '-'
    return rwx

def print_file(fpath, lstat=None):
    if lstat is None:
        lstat = os.lstat(fpath)

    print(f'# file: {fpath}')
    print(f'# owner: {pwd.getpwuid(lstat.st_uid).pw_name}')
    print(f'# group: {grp.getgrgid(lstat.st_gid).gr_name}')
    print(f'user::{octal_to_rwx((lstat.st_mode >> 6) & 0o7)}')
    print(f'group::{octal_to_rwx((lstat.st_mode >> 3) & 0o7)}')
    print(f'other::{octal_to_rwx(lstat.st_mode & 0o7)}')
    print('')

def read_files(path):
    print_file(path)

    for fname in os.listdir(path):
        fpath = os.path.join(path, fname)
        lstat = os.lstat(fpath)

        if stat.S_ISDIR(lstat.st_mode):
            read_files(fpath)
        else:
            print_file(fpath, lstat)

def main():
    for fpath in sys.argv[1:]:
        read_files(fpath)

if __name__ == '__main__':
    main()
