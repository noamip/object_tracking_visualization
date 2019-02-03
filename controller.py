from model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.run()

    def run(self):
        while True:
            command = self.view.get_filter()
            while int(command) < 1 or int(command) > 6:
                print("invalid choice")
                command = self.view.get_filter()
            if command == '6':
                return
            file, pic = self.view.get_files()

            self.model.set_file(file,pic)
            self.view.set_attr(pic)
            res = self.apply_filter(command)

    def edit(self, command,res):
        if command == '1':
            filter = self.view.get_filter()
            self.apply_filter(filter)
        elif command == '2':
            self.model.reset()
            filter = self.view.get_filter()
            self.apply_filter(filter)
        elif command == '3':
            self.model.reset()
            return

    def apply_filter(self, command):
        if command == '1':
            t1,t2=self.view.get_hours()
            res = self.model.filter_by_hours(t1, t2)  # ("04:00:02", "09:03:02")
        elif command == '2':
            t1, t2 = self.view.get_hours()
            date = self.view.get_hours()
            res = self.model.filter_by_date_and_hour(date, t1, t2)
        elif command == '3':
            x0, y0, x1, y1=self.view.get_area()
            res = self.model.filter_by_area(int(x0), int(x1), int(y0), int(y1))
        elif command == '4':
            self.view.draw_grid()
            areas = self.view.get_areas()
            res = self.model.filter_by_areas(areas)
        elif command == '5':
            res = self.model.no_filter()
        else:
            return
            # add view on by one option
        self.view.draw_path(res)
        command = self.view.edit()
        self.edit(command,res)
