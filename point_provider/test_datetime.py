import datetime

print(datetime.datetime.today())

# render = datetime.datetime(2021, 7, 27, 13, 8)

render = datetime.timedelta(days=3)

print(datetime.datetime.today() + render)