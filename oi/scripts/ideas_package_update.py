#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from ideas.models import Related, RelatedCategory

#packages.txt contains output of this (one package name per line):
#import pisi;pisi.db.PackageDB().get_isa_packages("app:gui")
package_list = [p[:-1] for p in open("packages.txt").readlines()]
c = RelatedCategory.objects.get(name__icontains="Pak")

#remove packages that are not in new packages but in old packages and not used
packages_to_remove = set([p.name for p in c.related_set.all()])-set(package_list)
for p in tuple(packages_to_remove):
    if Related.objects.get(name=p).idea_set.count():
        packages_to_remove.remove(p)
for p in packages_to_remove:
    Related.objects.get(name=p).delete()
    
#add packages that are in new packages but not in old packages, filter langpacks
packages_to_add = set(package_list)-set([p.name for p in c.related_set.all()])
for x in ("help-", "langpack-"):
    for i in tuple(packages_to_add):
        if x in i:
            packages_to_add.remove(i)
for p in packages_to_add:
    Related.objects.create(name=p, category=c)