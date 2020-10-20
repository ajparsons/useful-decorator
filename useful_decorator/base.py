"""
useful_decorator

generic decorator class for quick creation of complex decorators

"""
import six
from inspect import isfunction, isclass


class DecortorMeta(type):

    def __new__(cls, name, parents, dct):
        """
        only apply decorator to non abstract models
        """

        abstract = dct.pop("abstract", None)

        cls = super(DecortorMeta, cls).__new__(cls, name, parents, dct)
        if cls.allow_bare() == False or abstract:
            return cls
        else:
            return cls()  # if no args, return an instance immediately


class GenericDecorator(six.with_metaclass(DecortorMeta)):
    """
    Tidies up russian doll of decorators. 
    arguments passed to the decorator at creation
    end up as self.args and self.kwargs.
    kwargs are also added to self. 
    if args_map is populated - will also add those to self

    args_map = ("foo",)

    populates self.foo with args[0]

    if there is no args_map can be used bare (without initalisation)

    default_kwargs sets the default value of any kwargs that might be passed in 
    (also added to self)

    override self.gateway if it's a choice between using this function and 
    a different one

    overide self.arg_decorator to adjust arguments being passed in

    expects self, function, then delivers any args and kwargs passed to 
    the function

    If creating a decorator you will then subclass again, set:

    abstract = True

    """
    args_map = []
    default_kwargs = {}
    abstract = True  # disappears for children,

    def __call__(self, *args, **kwargs):
        """
        grabs the function and all arguments being passed to it
        """

        func = args[0]

        """
        if this can be used bare (but isn't) - reinit with the correct defaults
        """

        if (isfunction(func) == False and isclass(func) == False) or kwargs:
            return self.__class__(*args, **kwargs)

        # this is a bare class that's already been used, create new child
        if self.name:
            return self.__class__()(func)

        self.function = func
        self.name = func.__name__

        def inner(*args, **kwargs):
            self.function_args = args
            self.function_kwargs = kwargs
            return self.gateway()

        inner.__name__ = self.name

        inner = self.modify_function(inner)



        return inner

    @classmethod
    def allow_bare(cls):
        """
        can this decorator be used without initialisation?

        only if no args_map - or all values in args_map are already 
        provided by default_kwargs

        """
        if cls.args_map:
            non_default = [
                x for x in cls.args_map if x not in cls.default_kwargs]
            if non_default:
                return False
            else:
                return True
        else:
            return True

    def __init__(self, *args, **kwargs):
        """
        uses the args_map and kwargs to load details in
        """
        self.args = args
        self.name = ""
        self.kwargs = {}
        if self.__class__.default_kwargs:
            self.kwargs = dict(self.__class__.default_kwargs)
        self.kwargs.update(kwargs)

        self.__dict__.update(self.kwargs)
        for x, a in enumerate(self.__class__.args_map):
            try:
                setattr(self, a, args[x])
            except IndexError:
                if a in self.kwargs:
                    continue
                else:
                    raise ValueError("Value {0} not provided".format(a))        
            
    def gateway(self):
        """
        override if this is a "return this or something else" decorator

        Use super or call self.raw_decorator() to proceed
        """
        return self.trigger_decorator()


    def trigger_decorator(self):
        """
        accesses properties passed to decorator through self reference
        """
        result = self.decorator(self.function,
                                    *self.function_args,
                                    **self.function_kwargs)
        return self.modify_result(result)

    def decorator(self, function, *args, **kwargs):
        """"
        is given as arguments func, and then any args and kwargs
        """
        return function(*args, **kwargs)

    def modify_result(self, result):
        """
        passed self and the result of the function
        return final object when done
        """
        return result

    def modify_function(self, func):
        """
        passed self and the function
        return function when done
        """
        return func
