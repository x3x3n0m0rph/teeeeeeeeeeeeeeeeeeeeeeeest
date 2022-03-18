import csv
from unittest.main import main

# функция красивой печати листов
def pprint(list):
	for row in list:
		print(row)

# поиск доступного свободного эвента
def find_best_event(event_list, no_more_than):
	for i in range(len(event_list)):
		if not event_list[i]["used"]:
			if event_list[i]["hours"] <= no_more_than:
				event_list[i]["used"] = True
				return i
	return -1

# заполняем день 
def build_day(event_list, daylen):
	day_list = list()
	sum_hours = 0
	sum_points = 0
	while sum_hours < daylen:
		ev_i = find_best_event(event_list, daylen - sum_hours)
		if ev_i == -1:
			break

		day_list.append(event_list[ev_i])
		sum_hours += event_list[ev_i]["hours"]
		sum_points += event_list[ev_i]["points"]

	return day_list, sum_hours, sum_points

# читаем цсв, сортируем
def make_sorted_eventlist(csv_file):
	event_list = list()

	csvfile = open(csv_file)
	reader = csv.reader(csvfile, delimiter=';')
	for event in reader:
		event_list.append(
			{
				"name": event[0],
				"hours": float(event[1]),
				"points": float(event[2]),
				"points_in_h": float(event[2])/float(event[1]), # вводится эффективность задачи, условно - сколько пойнтов в час приносит ее выполнение
				"used": False
			}
		)
	csvfile.close()
	event_list.sort(key=lambda e: (e["points_in_h"], e["points"]), reverse=True) # сортировка по эффективности, второй ключ - либо пойнты либо часы

	return event_list

def main():
	DAYCOUNT = 2
	DAYLEN = 24
	SLEEP = 8

	event_list = make_sorted_eventlist("events.csv")

	for day_i in range(DAYCOUNT):
		daylist, hours_used, points_got = build_day(event_list, DAYLEN - SLEEP)
		print(f"Day #{day_i}:\n\tHours used: {hours_used}\n\tPoints got: {points_got}")
		pprint(["\t\t{}".format(event["name"]) for event in daylist])

if __name__ == "__main__":
	main()