import STRINGTH as st
from time import sleep
stru = st.HEXAPOD()
stru.stand_up()
sleep(1)
stru.forward(2)
sleep(1)
stru.defult_pos()
