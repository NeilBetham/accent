from croniter import croniter
from datetime import datetime
from datetime import timedelta
from logging import info

from schedule_data import SCHEDULE
from timezone import get_now


# The client sleep duration may be early by a few minutes, so we add a buffer
# to avoid waking up twice in a row.
DELAY_BUFFER_S = 15 * 60


def get_scheduled_image(width, height):
    """Generates the current image based on the schedule."""

    # Find the current schedule entry by parsing the cron expressions.
    now = get_now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    while True:
        entries = [(croniter(entry["start"], today).get_next(datetime), entry)
                   for entry in SCHEDULE]
        past_entries = filter(lambda x: x[0] <= now, entries)

        # Use the most recent past entry.
        if past_entries:
            latest_datetime, latest_entry = max(past_entries,
                                                key=lambda x: x[0])
            break

        # If there were no past entries, try the previous day.
        today -= timedelta(days=1)

    # Generate the image from the current schedule entry.
    info("Using image from schedule entry: %s (%s)" % (
         latest_entry["name"],
         latest_datetime.strftime("%H:%M:%S %Z")))
    image = latest_entry["image"](width, height)

    return image


def get_scheduled_delay():
    """Calculates the delay in milliseconds to the next schedule entry."""

    # Find the next schedule entry by parsing the cron expressions.
    now = get_now()
    entries = [(croniter(entry["start"], now).get_next(datetime), entry)
               for entry in SCHEDULE]
    next_datetime, next_entry = min(entries, key=lambda x: x[0])

    # Calculate the delay in milliseconds.
    seconds = (next_datetime - now).total_seconds() + DELAY_BUFFER_S
    milliseconds = int(seconds * 1000)
    info("Using time from schedule entry: %s (%s, in %d ms)" % (
         next_entry["name"],
         next_datetime.strftime("%H:%M:%S %Z"),
         milliseconds))

    return milliseconds