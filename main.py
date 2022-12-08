import PySimpleGUI as sg
from datetime import datetime
import csv
import os
import pickle


# Global Functions
valid_time_flag = False
valid_name_flag = False

def set_save_lap_activity():
    if valid_name_flag and valid_time_flag:
        window["-SAVELAP-"].update(disabled=False)
    else:
        window["-SAVELAP-"].update(disabled=True)

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
    window["-CLASSLIST-"].update(set_to_index=0)
    window["-SAVED RIDERS-"].update(set_to_index=-1)

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
        sg.Text("Test", size=(25, 1), enable_events=True, key="-DATANAME-"),
    ],
    [
        sg.Text("Lap Time:"),
        sg.Text("Test", size=(25, 1), enable_events=True, key="-DATATIME-"),
    ],
    [
        sg.Button(button_text="Save Lap", key="-SAVELAP-", disabled=True),
    ],
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
        self.rider_data[rider] = {}

    def update_rider_data(self, rider, field, value):
        self.rider_data[rider][field] = value

    def add_lap_time(self, race, number, time):
        match race:
            case "Race 1":
                if number in self.race1_times:
                    self.race1_times[number].append(time)
                else:
                    self.race1_times[number] = [time]

            case "Race 2":
                if number in self.race2_times:
                    self.race2_times[number].append(time)
                else:
                    self.race2_times[number] = [time]

            case "Race 3":
                if number in self.race3_times:
                    self.race3_times[number].append(time)
                else:
                    self.race3_times[number] = [time]
            case _:
                assert ("Not a valid race type")

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

    def get_number_laptimes_str(self, race, number):
        dt_list = []
        match race:
            case "Race 1":
                dt_list = self.race1_times[number]

            case "Race 2":
                dt_list = self.race2_times[number]

            case "Race 3":
                dt_list = self.race3_times[number]

        retlist = []
        for time in dt_list:
            retlist.append(str(time))
        return retlist

    def get_race_winner(self, race, _class):
        race_dict = {}
        sort_list = []
        ret_list = []
        match race:
            case "Race 1":
                race_dict = self.race1_times
            case "Race 2":
                race_dict = self.race2_times
            case "Race 3":
                race_dict = self.race3_times

        for number in race_dict.keys():
            if (self.number_in_class(number, _class)):
                sort_list.append((min(race_dict[number]), number))

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
                window["-RIDERLAPTIMES-"].update(data.get_number_laptimes_str(values["-RACELIST-"][0], values["-DATANUM-"]))
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
                datetime.strptime(values["-ENDTIME-"], "%H.%M.%S") -
                datetime.strptime(values["-STARTTIME-"], "%H.%M.%S")
             )
        )
        window["-RIDERLAPTIMES-"].update(data.get_number_laptimes_str(values["-RACELIST-"][0], values["-DATANUM-"]))
        save_data()

    # Race has been updated, update the lap times if the number is valid
    if event == "-RACELIST-":
        if valid_name_flag:
            try:
                window["-RIDERLAPTIMES-"].update(data.get_number_laptimes_str(values["-RACELIST-"][0], values["-DATANUM-"]))
            except:
                window["-RIDERLAPTIMES-"].update([])

# ***** Result Tab ******
    if event == "-RACERESULTLIST-" or event == "-RESULTCLASSLIST-" :
        window["-RESULTS-"].Update(data.get_race_winner(values["-RACERESULTLIST-"][0], values["-RESULTCLASSLIST-"][0]))

    # Functions to run after any update
    set_save_lap_activity()

save_data()
window.close()

