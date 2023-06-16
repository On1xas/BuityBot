import datetime


days=[(datetime.datetime.now()+datetime.timedelta(days=shift)).strftime("%d.%m") for shift in range(0,31)]

while days != []:
    rows=[]
    while len(rows) != 7:
        day = days.pop(0)
        rows.append(day)
    kb.row(*rows, wight=7)
print(days)