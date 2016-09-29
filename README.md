Calculate "white" based on the time of day (see color.py).  I like
cold light in the morning and the day, warming up from a couple of
hours before dusk, reaching maximum warmth about an hour after dusk.

Set up a virtualenv, install requirements and put usernames and other
parameters into hue_config.json, and then just create a cron job.

daylite.py calculates what "white" should be, adjusts a scene to apply
that to a collection of lights (in my kitchen), and "attaches" that
scene to a specified button on my tap switch.

Now I can tap the button, whatever time of day, and the "correct" "white"
comes on.  Tapping again adjusts "white" to the current time.

    virtualenv .env
    source .env/bin/activate
    pip install pytz
    pip install -r requirements.txt
    cp hue_config.sample.json hue_config.json # edit to include secret params
    python daylite.py

    # set up the above as a cron job. Remember end crontab with blank line
    */15 * * * * /home/pi/daylite/.env/bin/python /home/pi/daylite/daylite.py >> /dev/null


