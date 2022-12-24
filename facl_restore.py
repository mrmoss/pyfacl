#!/usr/bin/env python3
import grp
import os
import pwd
import re
import sys

def remove_empty_lines(lines, expected_label):
    while lines and not lines[0].strip():
        lines = lines[1:]

    if not lines:
        raise Exception(f'Expected "{expected_label}" (no more lines)')

    return lines

def parse_comment(lines, expected_label):
    lines = remove_empty_lines(lines, expected_label)
    line = lines[0].strip()
    values = re.findall(f'^#\\s*{expected_label}:\\s*([^\n]+)$', line)

    if not values:
        raise Exception(f'Expected comment "{expected_label}" (got "{line}")')

    return (lines[1:], values[0])

def parse_permission(lines, expected_label):
    lines = remove_empty_lines(lines, expected_label)
    line = lines[0].strip()

    values = re.findall(f'^{expected_label}:([^:]*):([r-])([w-])([x-])$', line)
    if not values or values[0][0]:
        raise Exception(f'Expected permission with basic perms "{expected_label}" (got "{line}")')

    value = 0
    if values[0][1] == 'r':
        value += 4
    if values[0][2] == 'w':
        value += 2
    if values[0][3] == 'x':
        value += 1

    return (lines[1:], value)

def main():
    with open(sys.argv[1], 'r', encoding='utf8') as facl_fd:
        lines = facl_fd.read().strip().split('\n')

        while lines:
            lines, fpath = parse_comment(lines, 'file')
            lines, user = parse_comment(lines, 'owner')
            lines, group = parse_comment(lines, 'group')
            lines, perm_user = parse_permission(lines, 'user')
            lines, perm_group = parse_permission(lines, 'group')
            lines, perm_other = parse_permission(lines, 'other')

            if not os.path.exists(fpath):
                print(f'Skipping "{fpath}" because it does not exist')
                continue

            os.chown(fpath, pwd.getpwnam(user).pw_uid, grp.getgrnam(group).gr_gid)
            os.chmod(fpath, perm_user * 0o100 + perm_group * 0o010 + perm_other * 0o001)

if __name__ == '__main__':
    main()
