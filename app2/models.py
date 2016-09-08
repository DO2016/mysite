from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ItemManager(models.Manager):
    # returns only published items
    def get_list_via_sql(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT t.id, t.created_date, t.updated_date, t.name, t.content, t.is_published, t.date_published, t.price, t.currency_id
            FROM app2_item t
            WHERE t.is_published;""")
        result_list = []
        for row in cursor.fetchall():
            p = self.model(id=row[0], created_date=row[1], updated_date=row[2])
            p.name = row[3]
            p.content = row[4]
            p.is_published = row[5]
            p.date_published = row[6]
            p.price = row[7]
            p.currency_id = row[8]
            result_list.append(p)
        return result_list


    def get_list_via_filter(self):
        return self.filter(is_published=True)




class AbstractModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        abstract = True       


class Currency(AbstractModel):
    name = models.CharField(max_length=200)


# Item(AbstractModel) with title, content(will be contains html), is published, date published, price,  currency (FK on Currency model)
class Item(AbstractModel):
    name = models.CharField(max_length=400, verbose_name='first name, last name')
    content = models.TextField(null=True, blank=True, verbose_name='html content')
    is_published = models.BooleanField(default=False)
    date_published = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency)   
    objects = ItemManager()

    def __unicode__(self):
        return self.name + " of " + Item._meta.verbose_name

    class Meta:
        # A human-readable name for the object, singular:
        verbose_name = "Item class derived from Abstract model" 


#################
#      M2M      #
#################


class M2ModelBase1(models.Model):
    col1 = models.CharField(max_length=400, verbose_name='first name, last name')


class M2ModelBase2(models.Model):
    col2 = models.CharField(max_length=400, verbose_name='first name, last name')
    col3 = models.ManyToManyField(M2ModelBase1)


