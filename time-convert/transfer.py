"""
convert timestamp and datetime
"""
import json
import datetime
import sys


def timestampms2date(ts):
    if len(ts) == 13:
        d = datetime.datetime.fromtimestamp(int(ts) / 1000)
        return d.strftime("%Y-%m-%d")


def timestampms2datetime(ts):
    if len(ts) == 13:
        d = datetime.datetime.fromtimestamp(int(ts) / 1000)
        return d.strftime("%Y-%m-%d %H:%M:%S")


def timestamp2date(ts):
    if len(ts) == 10:
        d = datetime.datetime.fromtimestamp(int(ts))
        return d.strftime("%Y-%m-%d")


def timestamp2datetime(ts):
    if len(ts) == 10:
        d = datetime.datetime.fromtimestamp(int(ts))
        return d.strftime("%Y-%m-%d %H:%M:%S")


def datetime2timestampms(dt):
    return int(datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timestamp()) * 1000


def date2timestampms(dt):
    return int(datetime.datetime.strptime(dt, "%Y-%m-%d").timestamp()) * 1000


def datetime2timestamp(dt):
    return int(datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timestamp())


def date2timestamp(dt):
    return int(datetime.datetime.strptime(dt, "%Y-%m-%d").timestamp())


def main():
    query = sys.argv[1]
    alfred_results = []
    if not query:
        ts = int(datetime.datetime.now().timestamp())
        tsm = int(ts * 1000)
        for name, value in [("ts", ts), ("tsm", tsm)]:
            alfred_results.append(
                {
                    "title": value,
                    "subtitle": name,
                    "arg": value,  # 向后传递
                    "autocomplete": value,  # 自动补全
                    "icon": {"path": "./icon.png"},
                }
            )
    else:
        for func in [
            timestamp2date,
            timestamp2datetime,
            datetime2timestamp,
            date2timestamp,
            timestampms2date,
            timestampms2datetime,
            datetime2timestampms,
            date2timestampms,
        ]:
            try:
                result = func(query)
                if not result:
                    continue
                alfred_results.append(
                    {
                        "title": result,
                        "subtitle": func.__name__,
                        "arg": result,  # 向后传递
                        "autocomplete": result,  # 自动补全
                        "icon": {"path": "./icon.png"},
                    }
                )
            except:
                pass

    if not alfred_results:
        alfred_results.append({"title": "...", "icon": {"path": "./icon.png"}})


    response = json.dumps({"items": alfred_results})

    sys.stdout.write(response)


if __name__ == "__main__":
    main()
