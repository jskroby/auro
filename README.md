# ATTENTION: THIS IS EXPERIMENTAL SOFTWARE. USE AT YOUR OWN RISK. THE AUTHORS OF THE SOFTWARE ARE NOT LIABLE FOR ANY LOSSES DUE TO USING THIS SOFTWARE.
***
## A Simple Proof-of-Concept Freqtrade bot that uses the [Aurox Indicator](https://getaurox.com) for buy/sell signals.

### [How to Get Aurox Indicator Webhooks](http://help.getaurox.com/en/articles/4771137-setting-up-using-alerts-on-aurox-scanner)

<p>This bot is meant as a proof-of-concept/baseline project to demonstrate how to use the Aurox indicator with Freqtrade. The bot uses (https://gitlab.com/5queezer/aurox/) to take in the Aurox indicator webhooks and store them in a MongoDB. The Freqtrade bot then reads the latest signal from the MongoDB and buys/sells depending on the signal. If you plan to use this in a real trading environment, I highly recommend you secure the Docker stack behind a reverse proxy as it is currently exposing ports to the internet in the current state. This can easily be achieved with a simple Traefik setup.</p>

## Instructions

#### Refer to [Freqtrade](https://freqtrade.io) and [Aurox-Signals](https://gitlab.com/5queezer/aurox/) for more information about how to use each.

##### These instructions were written assuming you are running Ubuntu 18.04 and have Docker and Docker-Compose installed
<ol>
<li>Clone this repo with <code>git clone https://git.partd.guru/root/freqtrade-aurox.git</code></li>
<li>Move into the newly created directory with <code>cd freqtrade-aurox</code></li>
<li>Change the MongoDB login details in the <code>.env</code>, <code>aurox-signals/settings.py</code>, and <code>freqtrade/user_data/strategies/Aurox.py</code> files</li>
<li>Follow [this tutorial](https://www.freqtrade.io/en/stable/telegram-usage/) and edit <code>freqtrade/user_data/config.json</code> with your Telegram Bot details so that you can interact with the bot</li>
<li>Run the Docker Stack with <code>docker-compose up -d</code></li>
</ol>

## Want more?
##### Check out the [Aurox Trading Bot Telegram Group](https://t.me/aurox_bots)
<p>Once you have the bot running, the next steps are to start building a more sophisticated strategy that uses more than just a single Aurox indicator as the buy/sell signal. I would recommend checking out the Freqtrade strategy [MoniGoMani](https://github.com/Rikj000/MoniGoMani). It is one of the most advanced public Freqtrade strategies that is still fairly easy to understand, uses ML to optimize the trading parameters, and can be incorporated with the Aurox indicator using the code from this project.</p>
