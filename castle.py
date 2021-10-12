import matplotlib.pyplot as plt
import datetime

th_raw_bt = [0,25,40,100,1800, 9000, 30000, 60000, 93600, 134400]
# Stable, Academy, Sorcs tower
milit2_bt = [22, 164, 960, 7200, 16200, 32400, 59040, 95400, 143640, 217800]
# Training Grounds
training_bt = [0, 20, 108, 720, 5400, 12150, 24300, 44280, 71550, 107730, 163350]
# Shipyard
shpyard_bt = [0, 27, 216, 1440, 10800, 24300, 48600, 88560, 107100, 215460, 326700]
# Barracks
barracks_bt = [0, 15, 36, 240, 1800, 4050, 8100, 14760, 23850, 35910, 54450]

class cabin():
    def __init__(self, id):
        self.level = 1
        self.id = id
        self.cabin_bonus = [4, 6, 6, 9, 10, 11, 12, 13, 14, 15]  # added to total when going from lvl 1 to lvl 2 add 6
        self.total_bonus = 4

    def lvl_up(self):
        self.total_bonus += self.cabin_bonus[self.level]
        self.level += 1

class city():
    def __init__(self, max_cabins, military_number, military_type):
        self.th_lvl = 4
        self.const_speed = 100
        self.cabin_max = max_cabins
        self.total_build_time = 165
        self.cabins = {}
        self.milit_max = military_number
        # 1 castle, 1 wiz, 3 storage, 2 market, 3 extra
        self.barracks_max = 90 - max_cabins - military_number
        self.naval = [0]
        if military_type == 1: # Training grounds
            self.milit_bt = training_bt
        elif military_type == 2: # All other units
            self.milit_bt = milit2_bt
        elif military_type == 3: # Navel Castle w/ Training ground
            self.milit_bt = training_bt
            self.naval = shpyard_bt
            self.barracks_max -= 8
        elif military_type == 4: # Naval Castle w/ Any other unit
            self.milit_bt = training_bt
            self.naval = shpyard_bt
            self.barracks_max -= 8
        self.cabin_raw_bt = [0, 15, 54, 360, 2700, 6075, 12150, 22500, 35820, 53880, 81720, ]
        self.all_raw = self.barracks_max * sum(barracks_bt) + \
                       self.milit_max * sum(self.milit_bt) + \
                       8*sum(self.naval)

    def finish_time(self,  build_time):
        ttfinish = build_time/(self.const_speed/100)
        return ttfinish

    def setCS(self):
        self.const_speed = 100
        for cabid, data in self.cabins.items():
            self.const_speed += data.total_bonus

    def level_townhall(self):
        total_bt = 0
        if self.th_lvl <= 10:
            self.th_lvl += 1
            total_bt += self.finish_time(th_raw_bt[self.th_lvl])
        return total_bt

    def level_cabin(self):
        if len(self.cabins.keys()) >= self.th_lvl*10:
            self.level_townhall()
        if len(self.cabins.keys()) >= self.cabin_max:
            #Level lowest level cabin
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
                    if self.cabins[cabin_id-1].level == self.cabins[cabin_id].level:
                        continue
                    else:
                        self.cabins[cabin_id].lvl_up()
                        self.total_build_time += self.finish_time(self.cabin_raw_bt[self.cabins[cabin_id].level])
                        break
        else:
            cabin_id = len(self.cabins.keys()) + 1
            self.cabins[cabin_id] = cabin(cabin_id)
        self.setCS()

    def build_all(self):
        current_build_time = self.total_build_time
        current_build_time += self.finish_time(self.all_raw)
        # print(f"City can build Senators in {datetime.timedelta(seconds=current_build_time)}")
        return current_build_time

levels_y = [0, 5000000]
fig, ax = plt.subplots()
cities = {}
for i in range(4,6):
    cities[i] = city(10*i, 51, 2)
    plot_data = {}
    plot_data["x"] = [cities[i].const_speed]
    plot_data["y"] = [cities[i].build_all()]
    for j in range(i*100):
        cities[i].level_cabin()
        plot_data["x"].append(cities[i].const_speed)
        plot_data["y"].append(cities[i].build_all())

    print(f"construction speed for {i*10} cabins:", cities[i].const_speed)
    print(f"CS at low: {plot_data['x'][plot_data['y'].index(min(plot_data['y']))] } Time To Finish",datetime.timedelta(seconds = min(plot_data["y"])))
    ax.plot(plot_data["x"], plot_data["y"], label=f"TimeTaken {i*10} cabins")

cs = [0, 4,10,16,25,35,46,58,71,85,100]
for i in range(10):
    levels_x = [40*cs[i+1]+100, 40*cs[i+1]+100]
    #ax.plot(levels_x, levels_y)#, label=f"All Cabins Level: {i+1}")
for i in range(4, 14):
    levels_x = [0, 4000]
    levels_y = [24*60*60*i, 24*60*60*i]
    ax.plot(levels_x, levels_y, label=f"Days {i}")

ax.set_title("Time to 1st Sen vs Con Speed")
ax.set_ylabel("Time (sec)")
ax.set_xlabel("Cons Speed")
ax.legend()
plt.ylim(24*60*60*6, 24*60*60*14)
plt.show()

