AWS Tools
=========
Higher level tools for working with AWS.

backup-instance
---------------
Automated backups. This command can be cronned.

The script will get a list of tags for the instance it's running on. If it
is tagged with all tags passed in the `--backup-master-tags` option, with
corresponding values matching `--backup-master-tag-values` it will assume
it is reponsible for taking backups.

The backup master will then get a list of all instances, and only those
tagged with the tags and values passed in the `--backup-tags` and
`--backup-tag-values` options will be backed up.

Sample invocation:

    ./awstools.py backup-instance --access-key-id=xxx \
    --secret-access-key=yyy --region=eu-west-1 --identifier=daily
    --backup-master-tags=BackupMaster,Env --backup-master-tag-values=True,live
    --backup-tags=BackupBy,Env --backup-tag-values=ami,live
    --keep=7

Above the script will only continue executing if the instance it's running
on is tagged 'BackupMaster'='True' and 'Env'='live'. It will then backup
all instances tagged 'BackupBy'='ami' and 'Env'='live'. After backing up,
it will delete old backups so only 7 are left.