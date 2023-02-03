from django import template

register = template.Library()


@register.filter
def getFeasibilityTag(enum):
    if enum == 1:
        return "High"
    elif enum == 2:
        return "Medium"
    else:
        return "Low"


@register.filter
def getStatusColor(status):
    print("status  "+str(status))
    if status == 0:
        return "#d95656"
    elif status == 1:
        return "#ffffff"
    else:
        return "#dce377"
