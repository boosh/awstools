AWS Tools
=========
Higher level tools for working with AWS.

Project Status
==============
This is incomplete alpha software.

To do
-----
    * Implement deleting excess backups for backup-instance
    * Give the option to create snapshots of volumes instead of AMIs of
      instances

Installation
------------
Clone this repo, create a virtualenv, then install dependencies and activate.

backup-instance
---------------
Automated backups. Instances with particular tags will be backed up as AMIs.

This command can be cronned. To cron it, cron with different intervals (e.g.
daily, weekly, monthly), and make sure to pass a different `--identifier`
option. This is used to group the different backups and delete old ones.

The script will get a list of tags for the instance it's running on. If it
is tagged with all tags passed in the `--backup-master-tags` option, with
corresponding values matching `--backup-master-tag-values` it will assume
it is reponsible for taking backups.

The backup master will then get a list of all instances, and only those
tagged with the tags and values passed in the `--backup-tags` and
`--backup-tag-values` options will be backed up.

Sample invocation:

    ./bin/awstools.py backup-instance --access-key-id=xxx \
    --secret-access-key=yyy --region=eu-west-1 --identifier=daily
    --backup-master-tags=BackupMaster,Env --backup-master-tag-values=True,live
    --backup-tags=BackupBy,Env --backup-tag-values=ami,live
    --keep=7

Above the script will only continue executing if the instance it's running
on is tagged 'BackupMaster'='True' and 'Env'='live'. It will then backup
all instances tagged 'BackupBy'='ami' and 'Env'='live'. After backing up,
it will delete old backups so only 7 are left.