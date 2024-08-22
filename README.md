# Py Sort ganizer

This is a small tool to sort file by type and date on the Linux or Unix file system.
On a lost partition or on a HDD storage where you have a lot of unsorted files, this
help to organized everything in a destination directory.

    python3 sort.py --help
    usage: sort.py [-h] -o ORIGIN -d DESTINATION [-dp DEPHT] [-e {image/jpeg,video/mp4,audio/mpeg,image/gif,image}] [-nt]

    Sort all file by creation time and date.

    options:
      -h, --help            show this help message and exit
      -o ORIGIN, --origin ORIGIN
                            Origin path of the files
      -d DESTINATION, --destination DESTINATION
                            Destination path of the sorted files
      -dp DEPHT, --depht DEPHT
                            Depht of the tree, 0 is no tree, 1 is year level, 2 is year/month, 3 is year/month/day (default)
      -e {image/jpeg,video/mp4,audio/mpeg,image/gif,image}, --extension {image/jpeg,video/mp4,audio/mpeg,image/gif,image}
                            Select mime type of file
      -nt, --notree         Do not create tree

    python3 sort.py -o Documents -d /tmp/testsorted -e image/jpeg -dp 2