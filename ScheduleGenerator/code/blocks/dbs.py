"""
Base Databank structure
"""


class Dbase:
    def __init__(self, fnames, noise):
        self.shout = noise
        self.fnames = fnames
        self.cls_list = []
        self.cls_idx = {}
        self.all_props = {}

    def setup(self):
        # name --> index in list association
        self.cls_idx = {c.__name__:i for i,c in enumerate(self.cls_list)}
        # Initialize
        for p in self.all_props['Databank']['D']:
            setattr(self, p, {})
        # Prepare blocks
        self.prepare()

    def prepare(self):
        """Prepare class with props"""
        for cls in self.cls_list:
            cls.prepare(self.all_props)

    def pcs_step(self, cls, **kwargs):
        # Pcs input
        obj_info = cls.pcs_input(**kwargs)
        # relevant bank
        bank_name = "{}s".format(cls.__name__.lower())
        if self.shout:
            print("Bank: {}...".format(bank_name))
        # Create objects
        bank = {key: cls(**obj) for key,obj in obj_info.items()}
        # Set bank
        setattr(self, bank_name, bank)

