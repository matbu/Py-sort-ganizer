#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import datetime
import hashlib
import mimetypes
import os
import random
import shutil
import string
import time

month_map = {1: 'Janvier', 2: 'Fevrier', 3: 'Mars', 4: 'Avril', 5: 'Mai',
             6: 'Juin', 7: 'Juillet', 8: 'Aout', 9: 'Septembre',
             10: 'Octobre', 11: 'Novembre', 12: 'Decembre'}


def _md5(fname):
    """ create a md5 hash """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def _create_dir(path):
    """ create dir like mkdir -p """
    if not os.path.exists(path):
        os.makedirs(path)


def _random_id(size=6, chars=string.ascii_uppercase + string.digits):
    """ return a 6 chars random hash """
    return ''.join(random.choice(chars) for _ in range(size))


def _get_mime(file):
    """ get mime type of a file """
    return mimetypes.MimeTypes().guess_type(file)[0]


def sort_file(path, working_dir, type_mime=None, notree=False, depht=3):
    """
    Sort file from a path to a working directory. It can be filtered by mime
    type (pattern like 'image').
    By default, it will create subdirectories in working dir with the following
    -| working_dir
    ----| year
    --------| month (french name)
    -------------| day
    ------------------| filename

    If a similar filename is present, the checksum is compare in order to
    avoid erasing different files.
    If the checksum are different but name are similar, the current filename
    will have a 6 chars hash.

    If notree option specified, all the file will be put at the root of the
    working directory.

    Depht parameter manage the creation of the destionation path:
      0 is equivalent as no tree: all files will be written in the working directory
      1 is year level: all files will be sorted by years
      2 is month level: all files will be sorted by years and months
      3 is day level: all files will be sorted by years, months and days.
      This is the deeper level.
    """
    if os.path.exists(path):
        # Create working dir if not exists
        if not os.path.exists(working_dir):
            _create_dir(working_dir)
        for pathname, dirname, files in os.walk(path):
            if len(files) != 0:
                for f in files:
                    mime = _get_mime(f)
                    if mime:
                        if type_mime is None or type_mime in mime:
                            cur_file = '%s/%s' % (pathname, f)
                            if notree or depht == 0:
                                new_file = '%s/%s' % (working_dir, f)
                            else:
                                date = datetime.datetime.fromtimestamp(
                                        os.path.getmtime(cur_file))
                                if depht == 1:
                                    file_path = "{0}/{1}".format(
                                                                    working_dir,
                                                                    date.year)
                                elif depht == 2:
                                    file_path = "{0}/{1}/{2}".format(
                                                                    working_dir,
                                                                    date.year,
                                                                    month_map.get(
                                                                    date.month))
                                else:
                                    file_path = "{0}/{1}/{2}/{3}".format(
                                                                    working_dir,
                                                                    date.year,
                                                                    month_map.get(
                                                                    date.month),
                                                                    date.day)
                                new_file = '%s/%s' % (file_path, f)
                                # Create directory
                                if not os.path.exists(file_path):
                                    _create_dir(file_path)
                            # If file do not exists, move it
                            if not os.path.exists(new_file):
                                shutil.copy2(cur_file, new_file)
                            else:
                                if _md5(cur_file) != _md5(new_file):
                                    shutil.copy2(cur_file,
                                                 '%s_%s' % (new_file,
                                                            _random_id()))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Sort all file by creation "
                                                 "time and date.")
    parser.add_argument("-o",
                        "--origin",
                        help="Origin path of the files",
                        required=True)
    parser.add_argument("-d",
                        "--destination",
                        help="Destination path of the sorted files",
                        required=True)
    parser.add_argument("-dp",
                        "--depht",
                        help=("Depht of the tree, 0 is no tree, 1 is year level, "
                              "2 is year/month, 3 is year/month/day (default)"),
                        required=False,
                        type=int,
                        default=3)
    parser.add_argument("-e",
                        "--extension",
                        help="Select mime type of file",
                        choices=["image/jpeg", "video/mp4",
                                 "audio/mpeg", "image/gif", "image"],
                        default=None)
    parser.add_argument("-nt",
                        "--notree",
                        help="Do not create tree",
                        action='store_true',
                        default=False)
    args = parser.parse_args()
    sort_file(args.origin, args.destination, args.extension, args.notree, args.depht)
