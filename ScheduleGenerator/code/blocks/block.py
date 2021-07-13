"""
Base class for data structures
"""
from tools.xl import read_dframe

class Block:
    def __init__(self, *args, **kwargs):
        # set properties
        # named args first
        for p in self.props_v:
            val = kwargs.get(p, None)
            setattr(self, p, val)
        # now reset if unnamed exist
        for i, val in enumerate(args):
            setattr(self, self.props_v[i], val)
        # List props
        for p in self.props_l:
            setattr(self, p, [])
        # List props
        for p in self.props_d:
            setattr(self, p, {})
    
    def __repr__(self):
        cname = type(self).__name__
        values = [p + " = " + str(getattr(self, p)) for p in self.props_v]
        params = ", ".join(values)
        return '{0}({1})'.format(cname, params)

    @classmethod
    def get_props(cls, props):
        cls.props_v = props.get("V", [])
        cls.props_l = props.get("L", [])
        cls.props_d = props.get("D", [])

    @classmethod
    def prepare(cls, all_props):
        cls.get_props(all_props[cls.__name__])

    @classmethod
    def aggregate(cls, *args):
        key = args[0]
        obj = dict(zip(cls.props_v, args))
        return (key, obj)
    
    @classmethod
    def pcs_input(cls, **kwargs):
        #from tools.xl import read_file
        #_, rows = read_file(kwargs['fname'])
        _, rows = read_dframe(kwargs['fname'])
        obj_info = {}
        for row in rows:
            key, obj = cls.pcs_row(row)
            #key, obj = cls.pcs_row(*row)
            obj_info[key] = obj
        return obj_info
