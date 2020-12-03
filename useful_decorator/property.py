
from base import GenericDecorator

class use_self_property(GenericDecorator):
    """
    for one argument class functions.
    if non-self argument is missing, use a property from self
    
    e.g.
    
    @use_self_property("foobar")
    def bar(self,foo):
        print foo
        
    if bar doesn't recieve foo - it will use self.foobar
    
    """
    args_map = ["property_to_use"]
    
    def decorator(self,function,func_self,*args,**kwargs):
            if len(args) == 0 and len(kwargs) < 1:
                value = getattr(func_self,self.property_to_use)
                return function(func_self, *args+(value,),**kwargs)
            else:
                return function(func_self, *args,**kwargs)    
            
class return_input_if_none(GenericDecorator):
    """
    if the function returns none, return the second (not self) input
    """
    def modify_result(self,value):
        if value is None:
            return self.function_args[1]
        else:
            return value

class print_result(GenericDecorator):
    """
    print the output of function
    """
    @return_input_if_none
    def modify_result(self,value):
        print(value)


class register_class(GenericDecorator):
    """
    add item to defined register
    """

    args_map = ["register"]
    
    def modify_function(self,func):
        self.register.append(func)
        return func
    
class_list = []

@register_class(class_list)
class foo(object):
    pass
            