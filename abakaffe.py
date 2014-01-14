import irc.bot
import irc.strings
import os
import urllib2
import simplejson
from urlparse import urljoin
from datetime import datetime

class AbakusCoffeeBot(irc.bot.SingleServerIRCBot):
    API_URL = "http://kaffe.abakus.no/api/"
    def __init__(self, channelList, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname.lower())
        self.channelList = channelList

    def get_file(self, api_base, api_module):
        try:
            url = urljoin(api_base, api_module)
            req = urllib2.Request(url)
            opener = urllib2.build_opener()
            f = opener.open(req)
            return f
        except:
            return ""

    def get_status(self, time_delta):
        try:
            message = ""
            print "getting status"
            if int(time_delta.days):
                message += "Det er ingen som har traktet kaffe i dag."
            else:
                hours = time_delta.seconds // (60 * 60)
                minutes = (time_delta.seconds // 60) % 60

                if not hours and not minutes:
                    return "Kaffen ble nettopp traktet!"

                message += "Kaffen ble sist traktet for "
                if hours:
                    if hours == 1:
                        message += "en time"
                    else:
                        message += str(hours) + " timer"
                if hours and minutes:
                    message += " og "
                if minutes:
                    if minutes == 1:
                        message += "ett minutt "
                    else:
                        message += str(minutes) + " minutter "
                message += "siden."
            return message
        except:
            return ""

    def print_kaffe(self, target):
        try:
            connection = self.connection
            f = self.get_file(self.API_URL, 'status')
            status_json = simplejson.load(f)
            coffee = status_json['coffee']
            on = coffee['status']
            last_start = coffee['last_start']
            last_start = datetime.strptime(last_start, "%Y-%m-%d %H:%M")
            time_delta = datetime.now() - last_start

            if on:
                connection.privmsg(target, "Kaffetrakteren er startet!")

            connection.privmsg(target, self.get_status(time_delta))
        except:
            pass

    def on_nicknameinuse(self, connection, event):
        connection.nick(connection.get_nickname() + "_")


    def on_privmsg(self, connection, event):
        command = event.arguments[0].split()
        if command[0] == "!join":
            if len(command) > 1:
                connection.join(command[1])
        elif command[0] == "!kaffe":
            self.print_kaffe(event.target)

    def on_welcome(self, connection, event):
        for chan in self.channelList:
            try:
                connection.join(chan)
            except:
                pass

    def on_pubmsg(self, connection, event):
        command = event.arguments[0].split()
        if command[0] == "!kaffe":

            self.print_kaffe(event.target)
        elif command[0] == "!join":
            if len(command) > 1:
                connection.join(command[1])
        return


def main():
    while True:
        try:
            import sys
            if len(sys.argv) != 4:
                print("Usage: python abacoffee.py <server[:port]> <channel1,channel2,channel3..> <nickname>")
                sys.exit(1)

            s = sys.argv[1].split(":", 1)
            channelList = sys.argv[2].split(",")
            server = s[0]
            if len(s) == 2:
                try:
                    port = int(s[1])
                except ValueError:
                    print("Error: Erroneous port.")
                    sys.exit(1)
            else:
                port = 6667
            nickname = sys.argv[3]
            for i,chan in enumerate(channelList):
                channelList[i] = '#'+chan
            print channelList, nickname, server,
            bot = AbakusCoffeeBot(channelList, nickname, server, port)
            bot.start()
        except:
            pass

if __name__ == "__main__":
    main()