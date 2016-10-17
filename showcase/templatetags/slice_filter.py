from django import template

register = template.Library()

@register.filter(name='use_slice')
def use_slice(value):
    try:
        tmp_iter = iter(value)
    except TypeError, te:
        print value, ' is not iterable'
    else:
        return value[1::2]


@register.filter(name='use_slice_arg')
def use_slice_arg(value, arg):
    i = 0
    try:
        tmp_iter = iter(value)
        i = int(arg)
    except TypeError, te:
        print 'Invalid data!'
    else:
        return value[i - 1::i]



@register.inclusion_tag('app1/range.html')
def show_range(value):
    ret = []
    try:
        ret = [x for x in xrange(int(value))]
    except:
        print "int value only allowed"
    return { "xlist" : ret }