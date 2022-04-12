class Exercise:
    def __init__(self, ref, enun):
        self.ref = ref
        self.enun = enun

    def run(self):
        raise NotImplementedError("self.run method must be defined after object intantiation")

    def __str__(self):
        print(self.ref)
        print(self.enun)

# EX OVERRIDE EXAMPLE

# class Ex(Exercise, ABC):
#     def __init__(self):
#         ref = ""
#         enun = ""
#         super().__init__(ref, enun)
#
#         # Declare atributes
#         self...
#
#     def run(self):
#         # implement run
#         pass







