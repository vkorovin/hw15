import csv
class DataStore():

    def __init__(self, filename, fieldnames=['username','birthdate']):
        self.filename = filename
        self.data = list()
        try:
            with open(self.filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for item in reader:
                    self.data.append(item)

        except FileNotFoundError:
          #  f = open(self.filename, 'w', newline='')
          #  f.close()
            pass

    def save(self, dict, fieldnames=['username','birthdate']):
        self.data.append(dict)
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(dict)

    def get(self):
        for item in self.data:
            yield item


if __name__== '__main__':

    data = DataStore("data.csv")
    data.save({'username':'Petya','birthdate':'05-12-1978'})
    data.save({'username': 'Petya', 'birthdate': '05-12-1978'})

    for item in data.get():
        print(item)
