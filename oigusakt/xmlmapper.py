from cached_property import cached_property
import xml.etree.ElementTree as ElementTree

def attribute(func):
    @cached_property
    def findAttribute(context):
        return context._element.attrib.get(func.__name__)
    return findAttribute
def element(func):
    @cached_property
    def findElement(context):
        element = context.findChild(func.__name__)
        return eval(func.__name__.capitalize())(element) if element is not None else None
    return findElement