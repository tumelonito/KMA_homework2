import pandas as pd

df = "alarms-240222-010325.csv"

alarms = pd.read_csv(df, delimiter=';', parse_dates=['start'])
alarms["start"] = pd.to_datetime(alarms["start"])
alarms["end"] = pd.to_datetime(alarms["end"])


def regions_at_time(df, day, start_time, end_time):
    """
    Returns the number of regions where events happened at a specific time on a given day.
    df: pandas DataFrame containing the timetable data
    day: string in the format 'YYYY-MM-DD' representing the day to filter by
    start_time: string in the format 'HH:MM' representing the time alarm started to filter by
    end_time: string in the format 'HH:MM' representing the time alarms ended to filter by
    """
    ds = (alarms["start"] >= pd.to_datetime(day + " " + start_time + ":00")) & (
                alarms["start"] <= pd.to_datetime(day + " " + end_time + ":59"))
    return len(alarms[ds]["region_id"].unique())


def events_in_region(df, region_id, day):
    """
    Returns the number of events that occurred in a specific region during a given day (24 hours).
    df: pandas DataFrame containing the timetable data
    region_id: integer representing the region ID to filter by
    day: string in the format 'YYYY-MM-DD' representing the day to filter by
    """
    ds = (alarms['region_id'] == region_id) & (alarms["start"].dt.date == pd.to_datetime(day).date())
    alarms_filtered = alarms[ds]

    num_events = len(alarms_filtered)
    return num_events


# test
if __name__ == "__main__":
    print(alarms.columns)
    num_regions = regions_at_time(alarms, '2022-05-09', '12:00', '13:59')
    print(num_regions)

    num_events = events_in_region(alarms, 4, '2022-05-09')
    print(num_events)