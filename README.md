# pyfacl

Super basic implementations of facl (because macOS is lame and doesn't have support...)

Only supports basic permissions (rwx)

## Usage

    facl_backup.py DIR|FILE [DIR|FILE1]...
    facl_restore.py FILE

## Examples

### Backup

    facl_backup.py some_directory > backup.facl

### Restore

    facl_restory.py backup.facl
