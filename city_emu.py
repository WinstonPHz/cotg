import matplotlib.pyplot as plt
import datetime

th_raw_bt = [0, 25, 40, 100, 1800, 9000, 30000, 60000, 93600, 134400]
aca_raw_bt = [22, 164, 960, 7200, 16200, 32400, 59040, 95400, 143640, 217800]


class cabin():
    def __init__(self, id):
        self.level = 1
        self.id = id
        self.cabin_bonus = [4, 6, 6, 9, 10, 11, 12, 13, 14,
                            15]  # added to total when going from lvl 1 to lvl 2 add 6
        self.total_bonus = 4

    def lvl_up(self):
        self.total_bonus += self.cabin_bonus[self.level]
        self.level += 1


class city():
    def __init__(self, max_cabins):
        self.th_lvl = 4
        self.const_speed = 100
        self.cabin_max = max_cabins
        self.total_build_time = 0
        self.cabins = {}
        self.cabin_raw_bt = [0, 15, 54, 360, 2700, 6075, 12150, 22500, 35820, 53880, 81720, ]

    def finish_time(self, build_time):
        ttfinish = build_time / (self.const_speed / 100)
        return ttfinish

    def setCS(self):
        self.const_speed = 100
        for cabid, data in self.cabins.items():
            self.const_speed += data.total_bonus

    def level_townhall(self):
        if self.th_lvl <= 8:
            self.th_lvl += 1
            self.total_build_time += self.finish_time(th_raw_bt[self.th_lvl])

    def shadow_level_townhall(self, shadow_level, shadow_time):
        th_level = shadow_level
        current_build_time = shadow_time
        if th_level <= 8:
            th_level += 1
            current_build_time += self.finish_time(th_raw_bt[self.th_lvl])
        return current_build_time

    def level_cabin(self):
        if len(self.cabins.keys()) >= self.th_lvl * 10:
            self.level_townhall()
        if len(self.cabins.keys()) >= self.cabin_max:
            # Level lowest level cabin
            for cabin_id, data in self.cabins.items():
                if cabin_id == 1:
                    # Check the last Cabins level if equal level up else continue
                    if self.cabins[cabin_id].level == self.cabins[self.cabin_max].level:
                        self.cabins[cabin_id].lvl_up()
                        self.total_build_time += self.finish_time(self.cabin_raw_bt[self.cabins[cabin_id].level])
                        break
                    else:
                        continue
                else:
                    # Check Previous Cabin if same level continue otherwise level up
                    if self.cabins[cabin_id - 1].level == self.cabins[cabin_id].level:
                        continue
                    else:
                        self.cabins[cabin_id].lvl_up()
                        self.total_build_time += self.finish_time(self.cabin_raw_bt[self.cabins[cabin_id].level])
                        break
        else:
            cabin_id = len(self.cabins.keys()) + 1
            self.cabins[cabin_id] = cabin(cabin_id)
        self.setCS()

    def build_academy(self):
        current_build_time = self.total_build_time
        th_level = self.th_lvl
        if th_level <= 8:
            for th in range(th_level, 9):
                th_level += 1
                current_build_time += self.finish_time(th_raw_bt[th_level])
        for i, data in enumerate(aca_raw_bt):
            current_build_time += self.finish_time(data)
        # print(f"City can build Senators in {datetime.timedelta(seconds=current_build_time)}")
        return current_build_time


#### All building should be a child of the city this allows for inheritance of CS ####
class market(city):
    def __init__(self, id):
        self.id = id
        self.level = 1
        self.raw_bt = []
        self.bonus = []
        self.total_bonus = 0
        print(city.const_speed)

    def level_up(self, to):
        print("Placeholder")


## Build list and what not, easy stuff
levels_y = [0, 500000]
fig, ax = plt.subplots()
cities = {}
for i in range(5, 6):
    cities[i] = city(10 * i)
    market(cities[i])
    plot_data = {}
    plot_data["x"] = [cities[i].const_speed]
    plot_data["y"] = [cities[i].build_academy()]
    for j in range(i * 100):
        cities[i].level_cabin()
        plot_data["x"].append(cities[i].const_speed)
        plot_data["y"].append(cities[i].build_academy())

    print(f"construction speed for {i * 10} cabins:", cities[i].const_speed)
    print(f"CS at low: {plot_data['x'][plot_data['y'].index(min(plot_data['y']))]} Time To Finish",
          datetime.timedelta(seconds=min(plot_data["y"])))
    ax.plot(plot_data["x"], plot_data["y"], label=f"TimeTaken {i * 10} cabins")

cs = [0, 4, 10, 16, 25, 35, 46, 58, 71, 85, 100]
for i in range(10):
    levels_x = [50 * cs[i + 1] + 100, 50 * cs[i + 1] + 100]
    ax.plot(levels_x, levels_y, label=f"All Cabins Level: {i + 1}")
ax.set_title("Time to 1st Sen vs Con Speed")
ax.set_ylabel("Time (sec)")
ax.set_xlabel("Cons Speed")
ax.legend()
plt.show()
