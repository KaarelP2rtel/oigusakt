from cached_property import cached_property
import xml.etree.ElementTree as ElementTree

def attribute(func):
    @cached_property
    def findAttribute(context):
        return context._element.attrib.get(func.__name__)
    return findAttribute

def text(func):
    @cached_property
    def findChildText(context):
        element=context.findChild(func.__name__)
        return element.text if element is not None else None
    return findChildText


def element(clss):
    def findElement(func):
        @cached_property
        def wrapper(context):
            element = context.findChild(func.__name__)
            return clss(element) if element is not None else None
        return wrapper
    return findElement



def text_with_html_tags(func):
    @cached_property
    def findChildTextWithHtml(context):
        element=context.findChild(func.__name__)
        if element is not None:
            text=element.text
            for child in element:
                tag = BaseElement(child).tag
                text+=f'<{tag}>{child.text if child.text else ""}</{tag}>{child.tail}'
            return text
        return None
    return findChildTextWithHtml


def element_list(clss, name=None):
    
    def findElements(func):
        @cached_property
        def wrapper(context):
            return tuple(clss(i) for i in context.findChildren(name if name else clss.__name__.lower()))
        return wrapper
    return findElements


class BaseElement:

    def __init__(self,element):
        self._element=element
        nsAndTag=element.tag.split('}')
        self._tag=nsAndTag.pop()
        ns = nsAndTag.pop().split('{').pop()
        self._ns={'ns':f'{ns}'}

    def findChild(self,name):
        return self._element.find(f'ns:{name}',namespaces=self._ns)

    def findChildren(self,name):
        return self._element.findall(f'ns:{name}',namespaces=self._ns)

    def attrib(self,name):
        return self

    @property
    def tag(self):
        return self._tag


