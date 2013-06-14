#!/usr/bin/env python

import aaargh
import sys
import os

# add the parent dir to the path so it can load the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from awstools.admin.tools import backup_instances
from awstools.logger import get_logger

log = get_logger(__name__)

app = aaargh.App(description="Provides higher-level interactions with AWS")
app.arg('-k', '--access-key-id', type=str, help="AWS access key ID", default=None)
app.arg('-s', '--secret-access-key', type=str, help="AWS secret key", default=None)
app.arg('-r', '--region', type=str, help="AWS region", default=None)

@app.cmd(name="backup-instance",
         help="Backup instances by creating AMIs from them. This is intended "
              "to be run on an instance running in AWS. It can be cronned "
              "with different frequencies (e.g daily, weekly, etc). Make "
              "sure to set a different identifier for each frequency so old "
              "snapshots are deleted properly (e.g. only keep 7 dailies, "
              "4 weeklies and 12 monthlies).")
@app.cmd_arg('--keep', type=str,
             help="Number of old snapshots to keep (grouped by identifier)")
@app.cmd_arg('--identifier', type=str,
             help="An identifier to add to snapshots. This is used to "
                  "identify which snapshots to delete when deleting old "
                  "snapshots.")
@app.cmd_arg('--backup-tag', type=str,
             help="Only instances tagged with this tag will be backed up. "
                  "Default=BackupBy",
             default="BackupBy")
@app.cmd_arg('--backup-tag-value', type=str,
    help="Only instances where the value of the backup-tag is this will be "
         "backed up. Default=ami", default="ami")
@app.cmd_arg('--backup-master-tag', type=str,
             help="Only instances tagged with this tag will take backups "
                  "(this lets this command be cronned on all instances, but "
                  "only those with this tag will actually take backups). "
                  "Default=BackupMaster",
             default="BackupMaster")
@app.cmd_arg('--backup-master-tag-value', type=str,
    help="Only instances where the value of the backup-master-tag is this "
         "will be actually run this command. Default=True", default="True")
def backup_instance(**kwargs):
    for key in sorted(locals().keys()):
        log.debug("Got arg '%s' = '%s'" % (key, locals().get(key)))

    backup_instances(**kwargs)


if __name__ == '__main__':
    app.run()