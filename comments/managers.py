"""
Custom manager which managers of objects which allow commenting can
inherit from.

Copyright (c) 2007, James Bennett
All rights reserved.

Modified by PreFab Software, Inc.
"""


from django.db import backend, connection, models
from oi.comments.models import Comment
from django.contrib.contenttypes.models import ContentType


class CommentedObjectManager(models.Manager):
    """
    A custom manager class which provides useful methods for types of
    objects which allow comments.
    
    Models which allow comments but don't need the overhead of their
    own fully-defined custom manager should use an instance of this
    manager as their default manager.
    
    Models which allow comments and which do have fully-defined custom
    managers should have those managers subclass this one.
    
    """
    def most_commented(self, num=5):
        """
        Returns the ``num`` objects of a given model with the highest
        comment counts, in order.
        
        The return value will be a list of dictionaries, each with the
        following keys::
        
            object
                An object of this model.
        
            comment_count
                The number of comments on the object.
        
        """
        comment_opts = Comment._meta

        ctype = ContentType.objects.get_for_model(self.model)
        query = """SELECT %s, COUNT(*) AS score
        FROM %s
        WHERE content_type_id = %%s
        AND is_public = 1
        GROUP BY %s
        ORDER BY score DESC""" % (backend.quote_name('object_id'),
                                  backend.quote_name(comment_opts.db_table),
                                  backend.quote_name('object_id'),)
        
        cursor = connection.cursor()
        cursor.execute(query, [ctype.id])
        object_data = [row for row in cursor.fetchall()[:num]]
        
        # Use ``in_bulk`` here instead of an ``id__in`` filter, because ``id__in``
        # would clobber the ordering.
        object_dict = self.in_bulk([tup[0] for tup in object_data])
        result_list = []
        for row in object_data:
            result_list.append({ 'object': object_dict[row[0]],
                            'comment_count': row[1] })
        return result_list
