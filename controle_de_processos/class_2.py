from abc import ABC
from college_crap_lib.college_crap_lib import Exercise
from college_crap_lib.phisics.electric import ohml

class Ex(Exercise, ABC):
    def __init__(self):
        ref = ""
        enun = ""
        super().__init__(ref, enun)

        # Declare atributes


    def run(self):
        # implement run
        pass
