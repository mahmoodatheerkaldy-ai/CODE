import STRINGTH as st

from time import sleep
s = st.HEXAPOD()
s.stand_up()
while True:
    s.fix_body_slop()
    sleep(0.1)

