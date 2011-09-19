#!/bin/bash
# run this as the user who owns the project
SRCDIR=/some-dir-for-downloading-git-source/
DSTDIR=/srv/petit-website.example.com/

cd $SRCDIR
git pull
rsync -avC $SRCDIR $DSTDIR

cd $DSTDIR/bdjango
python manage.py collectstatic --noinput
python manage.py migrate petit
python manage.py compilemessages

rsync -avC $SRCDIR $DSTDIR2

echo
echo "/----------------------------------------------\\"
echo "| - Updated source files                       |"
echo "| - Collected static                           |"
echo "| - Ran South migrations                       |"
echo "| - Compile language definitions               |"
echo "|                                              |"
echo "| Finished all tasks!                          |"
echo "| Reload apache for all changes to take effect |"
echo "\\----------------------------------------------/"
