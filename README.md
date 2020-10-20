# useful_decorator

Tidied up common decorator tasks to avoid the russian doll structure. 

Arguments passed to the decorator at creation end up as self.args and self.kwargs.
Kwargs are also added to self. 

if args_map is populated - will also add those to self. For instance:

`args_map = ("foo",)`


populates self.foo with args[0]

if there is no args_map can be used bare (without initalisation)

default_kwargs is a dictionary that sets the default value of any kwargs that might be passed in 
(also added to self)

## Useful overrides:


override `self.gateway` if it's a choice between using this function and 
a different one

overide `self.arg_decorator` to adjust arguments being passed in

overide `self.modify_result` to adjust the result of the function

## Examples

```
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
                value = getattr(self.func_self,self.property_to_use)
                return function(*args+(value,),**kwargs)
            else:
                return function(*args,**kwargs)      
            
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
```