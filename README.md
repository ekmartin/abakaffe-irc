#### The new bot uses hubot and can be found here: https://github.com/ekmartin/abakaffe-irc-hubot

abakaffe-irc
============

An IRC-bot utilizing the API from [kaffe.abakus.no](http://kaffe.abakus.no) to return coffee-statistics. 

## Installation
	
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt
	
## Usage

	python abacoffee.py <server[:port]> <channel1,channel2,channel3...> nickname

## Example

	python abacoffee.py irc.efnet.org:6667 abakus,mtdt Abacoffee

