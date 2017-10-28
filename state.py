#!/usr/bin/env python

import re
import time

class State():
    'State of a game of UNO™, like if there\'s a game and so on…'

    def __init__(self):
        # Assume that there isn't a game unless we see it
        self.running = False
        # Timestamp of last known message… or now.
        self.last_msg = time.time()

    def parse_message(self, msg):
        '''Reads IRC-messages from UNO-bot and adjusts the running-state.
           To ensure a working time-foo please only call this function for
           UNO-bot's messages!'''

        def chk(regs, desired_state):
            for r in regs:
                if r.search(msg):
                    self.running = desired_state
                    print('{} matched for "{}", state = {}'.format(msg, r, desired_state))
                    break

        pos_regs = map(re.compile, [
          r'Current discard:',
          r'has UNO!!',
          r'joins this game of UNO!',
          r' plays ',
          r'There is already an UNO! game running here, managed by pim. say \'jo\' to join in',
          r'game will start in 20 seconds',
          r'it\'s (.*)\'s turn',
          r'it\'s your turn, sleepyhead'
        ])
        neg_regs = map(re.compile, [
          r'UNO! game finished after (.*)! The winner is',
          r' still had (.*)'
        ])

        chk(pos_regs, True)
        chk(neg_regs, False)
        self.last_msg = time.time()
