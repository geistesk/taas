#! /usr/bin/env python

from configparser import ConfigParser
from irc.bot import SingleServerIRCBot
from state import State
from threading import Thread
from time import sleep, time


class TuBot(SingleServerIRCBot):
    '''A simple IRC-bot to annoy^W remind the current player in the our
       UNO-channel to play by requesting `tu` from the bot.
       Based on scripts/testbot.py'''

    def __init__(self, nickname, realname, timeout, unobot, channel, server, port):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, realname)

        self.timeout = timeout
        self.unobot  = unobot
        self.channel = channel
        self.state   = State()

        thrd = Thread(target=self.tu_loop, args=())
        thrd.daemon = True
        thrd.start()

    def tu_loop(self):
        'Checks every $timeout seconds if there is tu to post.'
        while True:
            sleep(self.timeout)

            if self.state.running and self.state.last_msg <= time() - self.timeout:
                print('Requesting tu!')
                self.connection.privmsg(self.channel, 'tu')

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        'Only acknowledge messeges from $unobot and pass them to State.'
        if e.type == 'pubmsg' and e.source.startswith(self.unobot):
            msg = ' '.join(e.arguments)
            self.state.parse_message(msg)


if __name__ == "__main__":
    conf = ConfigParser()
    conf.read('config.ini')

    tb = TuBot(
      conf.get('irc', 'nick'),
      'tu as a service',
      conf.getint('uno', 'waittime'),
      conf.get('uno', 'botname'),
      conf.get('irc', 'channel'),
      conf.get('irc', 'host'),
      conf.getint('irc', 'port'))
    tb.start()
