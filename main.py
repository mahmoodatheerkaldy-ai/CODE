import STRINGTH as st
from time import sleep
structure = st.HEXAPOD()
structure.stand_up()
sleep(0.5)
structure.forward(2)
sleep(0.5)
structure.back_ward(3) 
structure.turn_right(3)
structure.forward(10)
structure.turn_left(3)
structure.defult_pos()
structure.recennect_to_port() 
