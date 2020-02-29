from src.protocol.VDF import *
from src.protocol.utils import *

assert comp(27, 2, 3) == (2 ** (2**3)) % 27

assert div(5,2) == 3