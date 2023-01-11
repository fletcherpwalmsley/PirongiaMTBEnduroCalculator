import PySimpleGUI as sg
from datetime import datetime
import csv
import os
import pickle


# Global Functions
valid_time_flag = False
valid_name_flag = False

def set_save_lap_activity(values):
    if valid_name_flag and valid_time_flag:
        window["-SAVELAP-"].update(disabled=False)
    else:
        window["-SAVELAP-"].update(disabled=True)


    # Show/Hide Buttons
    if values["-RIDERLAPTIMES-"]:
        window["-DELETELAP-"].update(disabled=False)
    else:
        window["-DELETELAP-"].update(disabled=True)


# Making this global so it is easer to find the indexes of
race_classes = ["Mens", "Womens", "Open", "Youth Male", "Youth Female", "EBike"]

def get_class_index(val):
    for _class in enumerate(race_classes):
        if _class[1] == val:
            return _class[0]
    return -1

def clear_rider_data_fields(window):
    # Clear data fields
    window["-NAME-"].update("")
    window["-NUMBER-"].update("")
    window["-EMECONTACT-"].update("")
    # window["-CLASSLIST-"].update(set_to_index=0)
    window["-SAVED RIDERS-"].update(set_to_index=-1)

    # Clear lap data fields

def save_data():
    data.csv_save()
    athletes_file = open('rider_data.pkl', 'wb')
    pickle.dump(data, athletes_file)


input_list_column = [
    [
        sg.Text("Name   "),
        sg.In(size=(25, 1), enable_events=True, key="-NAME-"),
    ],
    [
        sg.Text("Number"),
        sg.In(size=(25, 1), enable_events=True, key="-NUMBER-"),
    ],
    [
        sg.Text("Emerg. Contact"),
        sg.In(size=(25, 1), enable_events=True, key="-EMECONTACT-"),
    ],
    [
        sg.Listbox(
            values=race_classes,
            default_values=race_classes[0],
            enable_events=True, 
            size=(20, 10), 
            key="-CLASSLIST-"
        )
    ],
    [
        sg.Button(button_text="Save Rider", key = "-SAVE-"),
        sg.Button(button_text="Clear Fields", key = "-CLEAR-"),
        sg.Button(button_text="Delete Rider", key = "-DELETE-"),
    ],
]

rider_viewer_column = [
    [
        sg.Listbox(
            values=[], 
            enable_events=True, 
            size=(20, 30),
            key="-SAVED RIDERS-"
        )
    ]
]

data_enter_column = [
    [
        sg.Listbox(
            values=["Race 1", "Race 2"],
            default_values=["Race 1"],
            enable_events=True,
            size=(10, 3),
            key="-RACELIST-"
        )
    ],
    [
        sg.Text("Rider Number"),
        sg.In(size=(25, 1), enable_events=True, key="-DATANUM-"),
    ],
    [
        sg.Text("Start Time"),
        sg.In(size=(25, 1), enable_events=True, key="-STARTTIME-"),
    ],
    [
        sg.Text("End Time"),
        sg.In(size=(25, 1), enable_events=True, key="-ENDTIME-"),
    ],
    [
        sg.Text("Rider Name:"),
        sg.Text("", size=(25, 1), enable_events=True, key="-DATANAME-"),
    ],
    [
        sg.Text("Lap Time:"),
        sg.Text("", size=(25, 1), enable_events=True, key="-DATATIME-"),
    ],
    [
        sg.Button(button_text="Save Lap", key="-SAVELAP-", disabled=True),
        sg.Button(button_text="Delete Lap", key="-DELETELAP-", disabled=True),
    ]
]

rider_lap_times = [
    [
        sg.Text("Lap Times", size=(15, 1)),
    ],
    [
        sg.Listbox(
            values=[],
            enable_events=True,
            size=(20, 15),
            key="-RIDERLAPTIMES-"
        )
    ]
]

result_view = [
    [
        sg.Listbox(
            values=["Race 1", "Race 2", "Series"],
            default_values=["Race 1"],
            enable_events=True,
            size=(10, 6),
            key="-RACERESULTLIST-"
        ),
            sg.Listbox(
            values=race_classes,
            default_values=race_classes[0],
            enable_events=True,
            size=(10, 6),
            key="-RESULTCLASSLIST-"
        )
    ],
    [
        sg.Listbox(
            values=[],
            enable_events=True,
            size=(70, 30),
            key="-RESULTS-"
        )
    ]
]


rider_layout = [
    [
        sg.Column(input_list_column),
        sg.VSeperator(),
        sg.Column(rider_viewer_column),
    ]
]

data_layout = [
    [
        sg.Column(data_enter_column),
        sg.VSeperator(),
        sg.Column(rider_lap_times),
    ]
]

result_layout = [
    [
        sg.Column(result_view)
    ]
]


layout = [[
        sg.TabGroup(
            [[
                sg.Tab('Rider Data', rider_layout, background_color='darkslateblue'),
                sg.Tab('Race Data', data_layout, background_color='tan1'),
                sg.Tab('Results', result_layout, background_color='green'),
            ]]
        )
    ]
]

window = sg.Window("Pirongia MTB  ", layout)


class DataHandler:
    """
    Single handler of all data
    """
    def __init__(self, csv_file):
        self.rider_data = {}
        self.race1_times = {}
        self.race2_times = {}
        self.race3_times = {}
        self.csv_file = csv_file
    
    # The CSV is used incase someone wants to use the data in excel
    def csv_save(self):
        csv_writer = csv.writer(open(self.csv_file, 'w'))
        for rider in self.rider_data.keys():
            out_row = []
            out_row.append(rider)
            out_row.append(self.rider_data[rider]["-NUMBER-"])
            out_row.append(self.rider_data[rider]["-EMECONTACT-"])
            out_row.append(self.rider_data[rider]["-CLASSLIST-"])
            out_row.append(f"?")
            # Save lap times
            number = self.rider_data[rider]["-NUMBER-"]
            if number in self.race1_times:
                for time in self.race1_times[number]:
                    out_row.append(f"1")
                    out_row.append(f"{time}")

            if number in self.race2_times:
                for time in self.race2_times[number]:
                    out_row.append(f"2")
                    out_row.append(f"{time}")

            if number in self.race3_times:
                for time in self.race3_times[number]:
                    out_row.append(f"3")
                    out_row.append(f"{time}")
            csv_writer.writerow(out_row)

    # Data create/delete functions
    def create_rider(self, rider):
        self.rider_data[rider] = {'Races':{}}

    def update_rider_data(self, rider, field, value):
        self.rider_data[rider][field] = value

    def add_lap_time(self, race, number, time):
        riderName = self.get_name_from_number(number)
        if race in self.rider_data[riderName]['Races']:
            self.rider_data[riderName]['Races'][race].append(time)
        else:
            self.rider_data[riderName]['Races'][race]=[time]


    def delete_rider(self, rider):
        del self.rider_data[rider]

    # Getters don't interact with the CSV, just loaded values
    def get_rider_list(self):
        return self.rider_data.keys()

    def get_rider_data(self, rider, field):
        single_rider = self.rider_data[rider]
        return single_rider[field]

    def get_name_from_number(self, number):
        for rider in self.rider_data:
            if self.rider_data[rider]["-NUMBER-"] == number:
                return rider
        return 0

    def get_number_laptimes_str_list(self, race, number):
        retlist = []
        riderName = self.get_name_from_number(number)
        for time in self.rider_data[riderName]['Races'][race]:
            retlist.append(str(time[2]))
        return retlist

    def get_lap_data_from_time(self, race, number, deltatime):
        riderName = self.get_name_from_number(number)
        for time in self.rider_data[riderName]['Races'][race]:
            if deltatime == str(time[2]):
                return time
        return ("","","")

    def delete_lap(self, race, number, deltatime):
        riderName = self.get_name_from_number(number)
        for time in self.rider_data[riderName]['Races'][race]:
            if deltatime == str(time[2]):
                self.rider_data[riderName]['Races'][race].remove(time)

    def get_race_winner(self, race, _class):
        sort_list = []
        ret_list = []

        for rider in self.rider_data.values():
            if (race in rider['Races']) and (rider['-CLASSLIST-'] == _class):
                lowest_time = rider['Races'][race][0][2]
                for lap in rider['Races'][race]:
                    if lap[2] < lowest_time:
                        lowest_time = lap[2]
                sort_list.append((lowest_time, rider["-NUMBER-"]))

            # if (self.number_in_class(number, _class)):
            #     lowest_time = race_dict[number][0][2]
            #     for result in race_dict[number]:
            #         if result[2] < lowest_time:
            #             lowest_time = result[2]
            #     sort_list.append((lowest_time, number))
        sort_list.sort()

        i = 1
        for val in sort_list:
            ret_list.append(f'({i}): #{val[1]} - {self.get_name_from_number(val[1])} - {val[0]} ')
            i = i+1

        return ret_list

    def number_in_class(self, number, _class):
        name = self.get_name_from_number(number)
        if self.get_rider_data(name, "-CLASSLIST-") == _class:
            return True
        return False


# Run the Event Loop
if os.path.isfile("rider_data.pkl"):
    pickle_file = open("rider_data.pkl", "rb")
    data = pickle.load(pickle_file)
else:
    data = DataHandler("rider_data.csv")
start_up_ready = True

while True:
    event, values = window.read()

    if start_up_ready:
        window["-SAVED RIDERS-"].update(data.get_rider_list())
        start_up_ready = False

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

# ***** Rider Data Tab ******
    # Rider data needs to be saved
    if event == "-SAVE-":
        data.create_rider(values["-NAME-"])
        data.update_rider_data(values["-NAME-"], "-NUMBER-", values["-NUMBER-"])
        data.update_rider_data(values["-NAME-"], "-EMECONTACT-", values["-EMECONTACT-"])
        data.update_rider_data(values["-NAME-"], "-CLASSLIST-", values["-CLASSLIST-"][0])

        window["-SAVED RIDERS-"].update(data.get_rider_list())
        clear_rider_data_fields(window)
        save_data()
    
    # Existing Rider Selected, load values in
    if event == "-SAVED RIDERS-":
        rider = values["-SAVED RIDERS-"]
        window["-NAME-"].update(rider[0])
        window["-NUMBER-"].update(data.get_rider_data(rider[0], "-NUMBER-"))
        window["-EMECONTACT-"].update(data.get_rider_data(rider[0], "-EMECONTACT-"))
        window["-CLASSLIST-"].update(set_to_index=get_class_index(data.get_rider_data(rider[0], "-CLASSLIST-")))

    if event == "-CLEAR-":
        clear_rider_data_fields(window)

    if event == "-DELETE-":
        data.delete_rider(values["-SAVED RIDERS-"][0])
        window["-SAVED RIDERS-"].update(data.get_rider_list())
        clear_rider_data_fields(window)
        save_data()

# ***** Race Data Tab ******
    # If the number is valid, show the corresponding name
    if event == "-DATANUM-":
        name = data.get_name_from_number(values["-DATANUM-"])
        if name != 0:
            window["-DATANAME-"].update(name, text_color="Lime")
            try:
                window["-RIDERLAPTIMES-"].update(data.get_number_laptimes_str_list(values["-RACELIST-"][0], values["-DATANUM-"]))
            except:
                window["-RIDERLAPTIMES-"].update([])
            valid_name_flag = True
        else:
            window["-DATANAME-"].update("Invalid Number", text_color="Red")
            valid_name_flag = False

    # A time as been entered, try to calculate the delta
    if (event == "-STARTTIME-") or (event == "-ENDTIME-"):
        valid_time_flag = False
        try:
            start_time = datetime.strptime(values["-STARTTIME-"], "%H.%M.%S")
            end_time = datetime.strptime(values["-ENDTIME-"], "%H.%M.%S")
            window["-DATATIME-"].update((end_time - start_time), text_color="Lime")
            valid_time_flag = True
        except:
            window["-DATATIME-"].update("Invalid Values", text_color="White")
            valid_time_flag = False

    # Save the timedelta
    if event == "-SAVELAP-":
        data.add_lap_time(
            values["-RACELIST-"][0],
            values["-DATANUM-"],
            (
                datetime.strptime(values["-ENDTIME-"], "%H.%M.%S"),
                datetime.strptime(values["-STARTTIME-"], "%H.%M.%S"),
                datetime.strptime(values["-ENDTIME-"], "%H.%M.%S") -
                datetime.strptime(values["-STARTTIME-"], "%H.%M.%S")
             )
        )
        window["-RIDERLAPTIMES-"].update(data.get_number_laptimes_str_list(values["-RACELIST-"][0], values["-DATANUM-"]))
        window["-STARTTIME-"].update("")
        window["-ENDTIME-"].update("")
        save_data()

    # Race has been updated, update the lap times if the number is valid
    if event == "-RACELIST-":
        if valid_name_flag:
            try:
                window["-RIDERLAPTIMES-"].update(data.get_number_laptimes_str_list(values["-RACELIST-"][0], values["-DATANUM-"]))
            except:
                window["-RIDERLAPTIMES-"].update([])

    # Previously entered lap has been selected, load it's data in
    if event == "-RIDERLAPTIMES-":
        # As we only can the the value from the list, not the index. We have to loop over all times to find which one
        # it corresponds to
        timedata = data.get_lap_data_from_time(values["-RACELIST-"][0], values["-DATANUM-"][0], values["-RIDERLAPTIMES-"][0])
        window["-STARTTIME-"].update(timedata[1].strftime("%H.%M.%S"))
        window["-ENDTIME-"].update(timedata[0].strftime("%H.%M.%S"))
        window["-DATATIME-"].update(timedata[2])

    # Delete a lap
    if event == "-DELETELAP-":
        data.delete_lap(values["-RACELIST-"][0], values["-DATANUM-"][0], values["-RIDERLAPTIMES-"][0])
        window["-RIDERLAPTIMES-"].update(data.get_number_laptimes_str_list(values["-RACELIST-"][0], values["-DATANUM-"]))
        window["-STARTTIME-"].update("")
        window["-ENDTIME-"].update("")
        save_data()

# ***** Result Tab ******
    if event == "-RACERESULTLIST-" or event == "-RESULTCLASSLIST-" :

        if values["-RACERESULTLIST-"][0] == "Series":
            window["-RESULTS-"].Update(
                data.get_race_winner(values["-RESULTCLASSLIST-"][0]))
        else:
            window["-RESULTS-"].Update(
                data.get_race_winner(values["-RACERESULTLIST-"][0], values["-RESULTCLASSLIST-"][0]))

    # Functions to run after any update
    set_save_lap_activity(values)

save_data()
window.close()
