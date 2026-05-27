import STRINGTH  as st
from time import sleep

s = st.HEXAPOD()
s.stand_up()
sleep(1)
s.support_leg_on()
sleep(1)
s.set_sting_ready()
sleep(1)
s.all_body_down(20)
sleep(1)
s.all_body_up(20)
sleep(1)
s.set_sting_back()
sleep(1)
s.support_leg_off()
sleep(1)
s.default_pos()


