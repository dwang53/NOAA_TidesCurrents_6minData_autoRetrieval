"""
LIB_NOAATideCurrentsDataDownload.py

Utility functions for downloading NOAA Tides & Currents 6-minute water-level
data through the NOAA CO-OPS API.

This module is designed for coastal, oceanographic, and climate-data workflows
where users need reproducible station-based water-level time series.
"""

from datetime import datetime, timedelta
import pandas as pd


def genNOAALink(stationNo, begin_date, end_date, datum, timezone, unit, format):
    """
    Build a NOAA CO-OPS API request URL for water-level data.

    Parameters
    ----------
    stationNo : str
        NOAA station ID.
    begin_date : str
        Start date in YYYYMMDD format.
    end_date : str
        End date in YYYYMMDD format.
    datum : str
        Vertical datum such as 'MLLW' or 'MLW'.
    timezone : str
        Time zone string accepted by the NOAA API, e.g. 'GMT'.
    unit : str
        Unit system, such as 'metric' or 'english'.
    format : str
        Output format, typically 'csv'.

    Returns
    -------
    str
        Fully formatted NOAA API URL for the requested water-level data.
    """
    outLink = (
        "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        "?product=water_level"
        "&application=NOS.COOPS.TAC.WL"
        f"&begin_date={begin_date}"
        f"&end_date={end_date}"
        f"&datum={datum}"
        f"&station={stationNo}"
        f"&time_zone={timezone}"
        f"&units={unit}"
        f"&format={format}"
    )
    return outLink


def get_monthly_periods(start_date, end_date):
    """
    Split a start/end date range into monthly chunks.

    Long NOAA API requests are often easier to manage when split into monthly
    periods. This function creates inclusive month-by-month date windows.

    Parameters
    ----------
    start_date : str
        Start date in YYYYMMDD format.
    end_date : str
        End date in YYYYMMDD format.

    Returns
    -------
    list of list of str
        A list of [start_date, end_date] pairs for each month.

    Raises
    ------
    ValueError
        If the provided date strings are not valid or if start_date is later
        than end_date.
    """
    try:
        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")
    except ValueError as exc:
        raise ValueError(
            "Dates must be provided in YYYYMMDD format, e.g. '20250101'."
        ) from exc

    if start > end:
        raise ValueError("start_date must be earlier than or equal to end_date.")

    current = start
    periods = []

    while current <= end:
        next_month = current.replace(day=28) + timedelta(days=4)
        last_day_of_month = next_month - timedelta(days=next_month.day)

        if end.year == current.year and end.month == current.month:
            periods.append([current.strftime("%Y%m%d"), end.strftime("%Y%m%d")])
            break

        periods.append(
            [current.strftime("%Y%m%d"), last_day_of_month.strftime("%Y%m%d")]
        )

        current = (last_day_of_month + timedelta(days=1)).replace(day=1)

    return periods


def downloadNOAA_WSE(
    NOAAstationNo,
    NOAAbegin_date,
    NOAAend_date,
    datum="MLLW",
    timezone="GMT",
    unit="metric",
    format="csv",
    debugFlag=False,
):
    """
    Download NOAA water-level data and return a merged pandas DataFrame.

    The requested date range is split into monthly chunks, each chunk is
    downloaded separately, and all results are concatenated into a single
    time-indexed dataframe.

    Parameters
    ----------
    NOAAstationNo : str
        NOAA station ID.
    NOAAbegin_date : str
        Start date in YYYYMMDD format.
    NOAAend_date : str
        End date in YYYYMMDD format.
    datum : str, optional
        Vertical datum. Default is 'MLLW'.
    timezone : str, optional
        NOAA API time zone setting. Default is 'GMT'.
    unit : str, optional
        Output units. Default is 'metric'.
    format : str, optional
        Output format. Default is 'csv'.
    debugFlag : bool, optional
        If True, print detailed warnings when a monthly chunk fails.

    Returns
    -------
    pandas.DataFrame
        Combined dataframe indexed by datetime.

    Raises
    ------
    RuntimeError
        If no valid data could be downloaded.
    """
    listDateTimes = get_monthly_periods(NOAAbegin_date, NOAAend_date)

    if len(listDateTimes) == 0:
        raise RuntimeError("No valid monthly download windows were generated.")

    print(f"Downloading NOAA data in {timezone} time zone for station {NOAAstationNo}.")

    all_frames = []

    for datetimepairs in listDateTimes:
        downloadLink = genNOAALink(
            NOAAstationNo,
            datetimepairs[0],
            datetimepairs[1],
            datum,
            timezone,
            unit,
            format,
        )

        if debugFlag:
            print(f"Requesting: {downloadLink}")

        try:
            dfNOAA = pd.read_csv(downloadLink)
            dfNOAA.columns = [col.strip() for col in dfNOAA.columns]

            if "Date Time" not in dfNOAA.columns:
                raise ValueError("NOAA response does not contain the 'Date Time' column.")

            dfNOAA["datetime"] = pd.to_datetime(dfNOAA["Date Time"])
            dfNOAA = dfNOAA.set_index("datetime")

            all_frames.append(dfNOAA)

        except Exception as exc:
            if debugFlag:
                print(
                    "Warning: failed to download NOAA data for period "
                    f"{datetimepairs[0]} to {datetimepairs[1]}. Reason: {exc}"
                )

    if len(all_frames) == 0:
        raise RuntimeError(
            "No NOAA data could be downloaded for the requested station and date range."
        )

    df_all = pd.concat(all_frames)
    df_all = df_all[~df_all.index.duplicated(keep="first")]
    df_all = df_all.sort_index()

    return df_all


if __name__ == "__main__":
    NOAAstation = "8764314"
    NOAAbegindate = "20150401"
    NOAAenddate = "20241231"

    dfNOAA_example = downloadNOAA_WSE(
        NOAAstation,
        NOAAbegindate,
        NOAAenddate,
        datum="MLLW",
        timezone="GMT",
        unit="metric",
        format="csv",
        debugFlag=True,
    )

    print(dfNOAA_example.head())
    print(dfNOAA_example.tail())