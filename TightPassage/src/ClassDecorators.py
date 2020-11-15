""" some decorators for python classes
"""


class ExtendableProperty(property):
    """a property decorator that calls the base class property setter and then the derived-class setter
    use like this:
    class A(object):
        @ExtendableProperty
        def prop(self):
            return self._prop

        @prop.setter
        def prop(self, v):
            self._prop = v

    class B(A):
        @A.prop.append_setter
        def prop(self, v):
            print('Set', v)      #A.prop(v) get called before automatically
            #another way would be 
            #A.prop.fset(self, v)  # ..or fget/fdel
"""
    def append_setter(self, fset):
        # Create a wrapper around the new fset that also calls the current fset
        _old_fset = self.fset

        def _appended_setter(obj, value):
            _old_fset(obj, value)
            fset(obj, value)
        # Use that wrapper as setter instead of only the new fset
        return self.setter(_appended_setter)

