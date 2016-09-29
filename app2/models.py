from __future__ import unicode_literals

from django.db import models
from django.utils import six, timezone
from django.db.models import Count, Sum, Avg
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.contrib.auth.models import User, AbstractUser, UserManager, AbstractBaseUser, PermissionsMixin

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
    from django.utils import timezone
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        abstract = True       


class Currency(AbstractModel):
    name = models.CharField(max_length=200)

    class Meta:
        # A human-readable name for the object, singular:
        verbose_name = "Currencie"


# Item(AbstractModel) with title, content(will be contains html), is published, date published, price,  currency (FK on Currency model)
class Item(AbstractModel):
    name = models.CharField(max_length=400, verbose_name='first name, last name')
    content = models.TextField(null=True, blank=True, verbose_name='html content')
    is_published = models.BooleanField(default=False)
    date_published = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency)   
    objects = ItemManager()

    # WRONG: Produces A LOT OF QUERIES to DB
    #@property
    #def sum_ings_price(self):
    #    return self.ings.aggregate(Sum('price'))['price__sum']

    def __unicode__(self):
        return self.name


class Review(AbstractModel):
    content = models.TextField(null=True, blank=True, verbose_name='Review content')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')

    def __unicode__(self):
        return self.content

# Create Ingredient(AbstractModel) with price with M2M on Item (one item can have a lot of ing and one ing can have a lot of items)
class Ingredient(AbstractModel):
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    name = models.CharField(max_length=400, verbose_name='Ingredient')
    items = models.ManyToManyField(Item, related_name='ings', through='Composition')


class Composition(models.Model):
    ing = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    short_info = models.CharField(max_length=400, null=True, blank=True)



class AbstractCustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    timezone = models.CharField(max_length=50, default='Europe/Moscow')
    confirmation_code = models.CharField(max_length=128, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('custom_user')
        verbose_name_plural = _('custom_users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class CustomUser(AbstractCustomUser):
    class Meta(AbstractCustomUser.Meta):
        swappable = 'AUTH_USER_MODEL'


#########################
#      Experiments      #
#########################

# Experiment 1
class M2ModelBase1(models.Model):
    col1 = models.CharField(max_length=400, verbose_name='first name, last name')


class M2ModelBase2(models.Model):
    col2 = models.CharField(max_length=400, verbose_name='first name, last name')
    col3 = models.ManyToManyField(M2ModelBase1)


# Experiment 2
class DerivedItem(Item):
    derived_col_1 = models.CharField(max_length=400, null=True, blank=True)
    derived_col_2 = models.CharField(max_length=400, null=True, blank=True)
    objects = ItemManager()

    def __unicode__(self):
        return self.name + " of " + DerivedItem._meta.verbose_name

    class Meta:
        # A human-readable name for the object, singular:
        verbose_name = "DerivedItem cls"
