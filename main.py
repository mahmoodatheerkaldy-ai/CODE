import STRINGTH as st
from time import sleep
structure = st.HEXAPOD()

while True:
    structure.forward(1)
    sleep(4)
    structure.turn_left(2)
    sleep(4)
    structure.turn_right(2)
    sleep(4)
    
