from django.core.management.base import BaseCommand, CommandError
from app2.models import Item, Currency
import random

class Command(BaseCommand):

    def add_arguments(self, parser):

    def handle(self, *args, **options):
        Item.objects.bulk_create([Item(name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
        content = '',
        is_published = True,
        date_published = '2016-10-10',
        created_date = '2016-09-02',
        updated_date = '2016-09-02',
        currency = 2,
        ) for _ in xrange(5)])
