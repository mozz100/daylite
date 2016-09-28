from astral import Location
import datetime

LOCATION = Location(('Cambridge', 'Europe', 52.2053, 0.1218, 'Europe/London', 6))  # last param is elevation

# Color temperatures are in reciprocal megakelvin (mirek).
# See http://www.developers.meethue.com/documentation/core-concepts

WARM = 500      # ct value. Max poss value is 500. Too warm?
COLD = 242      # ct value. Min poss value is 153.
EARLY = 3       # at 3am (UTC) jump from warm to cold for morning
START_SLOPE = 3 # hours before dusk
END_SLOPE = 1.0 # hours after dusk

def get_color(when):
    """
    Return a tuple of (color_temp, explanation).
    color_temp = an integer describing "white" in mirek, calculated using the time (passed in as when)
    explanation = a string, may be useful for debugging
    """

    # Variation of "white" over time
    #    wee hours     daylite               slope    night
    #               |-------------------------\
    #               |                          -\
    #               |                            -\
    #   ____________|                              -\____________

    assert type(when) is datetime.datetime

    early = when.replace(hour=EARLY, minute=0, second=0, microsecond=0)

    if when < early:
        return WARM, "wee hours"

    dusk = LOCATION.sun(date=when, local=False)['dusk']
    start_slope = dusk - datetime.timedelta(hours=START_SLOPE)
    end_slope   = dusk + datetime.timedelta(hours=END_SLOPE)
    if when < start_slope:
        return COLD, "daylite"
    if when > end_slope:
        return WARM, "night"

    # calculate slope
    fraction = (when - start_slope).total_seconds() / (end_slope - start_slope).total_seconds()
    value = COLD + fraction * (WARM-COLD)
    return int(value), "slope %d%%" % (fraction * 100)

# usage example
# from pytz import UTC
# now = datetime.datetime.now(tz=UTC)
# print "now",    get_color(now)
# print "\n\n"
# when = datetime.datetime.now(tz=UTC).replace(hour=0, minute=0, second=0, microsecond=0) # midnight, start of today
# end  = when + datetime.timedelta(hours=24)
# while when < end:
#     print when, get_color(when)
#     when += datetime.timedelta(minutes=10)