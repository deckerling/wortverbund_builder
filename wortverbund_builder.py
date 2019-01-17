#!/usr/bin/env python3

# wortverbund_builder.py
#
# Copyright 2019 E. Decker
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A program providing tools to track the development of complex signs in a
    discourse."""

import csv
import os
import random
import shutil
import tkinter as tk

import matplotlib.pyplot as plt

import wb_func # imports miscellaneous calculation and sort functions needed


class ProjectCreator(tk.Frame):
    """GUI-frame to create new projects."""

    def __init__(self, master):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7,
                  command=self.__del__).pack()
        tk.Label(self, font='Arial 16', text='Name your new project: ').pack()
        self.project_name_entry = tk.Entry(self, font='Arial 16', width=16)
        self.project_name_entry.pack()
        tk.Label(self, font='Arial 16', text='Select criteria for the chronological order of the constituents of your wortverbund: ').pack()
        self.var = tk.IntVar(value=0)
        options = [('page (e.g. if your corpus is a single book)              ', 1),
                   ('date (e.g. if you are doing research on a discourse)     ', 2),
                   ('time (e.g. if you are using a speech recording as corpus)', 3)]
        for option_text, option_value in options:
            tk.Radiobutton(self, font='Courier 12 italic', text=option_text,
                           variable=self.var, value=option_value).pack()
        tk.Button(self, font='Arial 16', text='Save', width=7,
                  command=self.create_project).pack()

    def __del__(self):
        self.forget()
        ROOT_FRAME.pack()

    def create_project(self):
        """Creates a project considering the chosen option - works only if an
            option has been chosen and if a project name was entered."""
        if self.project_name_entry.get() and self.var.get() != 0:
            # Changes the background colour of "self.project_name_entry" to
            # green if the entry was accepted (and the project saved) and to red
            # if not.
            try:
                if self.var.get() == 1:
                    if not os.path.exists('wb_files/'+self.project_name_entry.get()+'_page'):
                        os.makedirs('wb_files/'+self.project_name_entry.get()+'_page')
                elif self.var.get() == 2:
                    if not os.path.exists('wb_files/'+self.project_name_entry.get()+'_date'):
                        os.makedirs('wb_files/'+self.project_name_entry.get()+'_date')
                elif self.var.get() == 3:
                    if not os.path.exists('wb_files/'+self.project_name_entry.get()+'_time'):
                        os.makedirs('wb_files/'+self.project_name_entry.get()+'_time')
                self.project_name_entry.delete(0, 'end')
                self.project_name_entry['bg'] = 'green'
            except OSError:
                self.project_name_entry['bg'] = 'red'


class ProjectSelecter(tk.Frame):
    """GUI-frame to select a project in order to work on it later.

        The argument "case", which is needed for "__init__", is used (and passed
        on) in order to execute certain functions of this programm (case==0 ->
        create_wortverbund; case==1 -> delete_project; case==2 ->
        delete_wortverbund; case==3 -> work_on_features; case==4 ->
        show_wortverbund)."""

    def __init__(self, master, case):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7,
                  command=self.__del__).pack()
        self.label = tk.Label(self, font='Arial 16', text='Select a project: ')
        self.label.pack()
        self.project_listbox = tk.Listbox(self, font='Arial 16', height=18,
                                          width=26)
        self.project_listbox.pack()
        self.case = case
        try:
            no_projects = True
            for project in os.listdir('wb_files'):
                if not '.' in project:
                    self.project_listbox.insert('end', project)
                    no_projects = False
            if no_projects:
                raise IOError
            else:
                if self.case != 1:
                    tk.Button(self, font='Arial 16', text='Ok', width=7,
                              command=self.select_project).pack()
                else: # in order to delete a project
                    delete_button = tk.Button(self, font='Arial 16 italic',
                                              text='Delete', width=7,
                                              command=self.select_project)
                    delete_button.configure(fg='red')
                    delete_button.pack()
        except IOError:
            self.label.forget()
            self.project_listbox.forget()
            tk.Label(self, font='Arial 16', text='There are no projects. Create a new project first!').pack()

    def __del__(self):
        try:
            self.forget()
            ROOT_FRAME.pack()
        except tk.TclError:
            pass

    def select_project(self):
        self.forget()
        if self.case == 0: # coming from "create_wortverbund"
            WortverbundCreator(ROOT, self.project_listbox.get('active')).pack()
        elif self.case == 1: # coming from "delete_project"
            shutil.rmtree('wb_files/'+self.project_listbox.get('active'))
            ROOT_FRAME.pack()
        elif self.case == 2:# coming from "delete_wortverbund"
            WortverbundSelecter(ROOT, self.project_listbox.get('active'), 2).pack()
        elif self.case == 3: # coming from "work_on_features"
            WortverbundSelecter(ROOT, self.project_listbox.get('active'), 3).pack()
        elif self.case == 4: # coming from "show_wortverbund"
            WortverbundSelecter(ROOT, self.project_listbox.get('active'), 4).pack()


class WortverbundCreator(tk.Frame):
    """GUI-frame to create a new wortverbund in an existing project."""
    
    def __init__(self, master, project):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7,
                  command=self.__del__).pack()
        tk.Label(self, font='Arial 16', text='Enter a name (signifier) for the new wortverbund: ').pack()
        self.wortverbund_name_entry = tk.Entry(self, font='Arial 16', width=16)
        self.wortverbund_name_entry.pack()
        tk.Button(self, font='Arial 16', text='Save', width=7,
                  command=self.save_wortverbund).pack()
        self.project = project

    def __del__(self):
        try:
            self.forget()
            ROOT_FRAME.pack()
        except tk.TclError:
            pass

    def save_wortverbund(self):
        if self.wortverbund_name_entry.get():
            # Changes the background colour of "self.wortverbund_name_entry" to
            # green if the entry was accepted (and the wortverbund saved) and to
            # red if not.
            try:
                open('wb_files/'+self.project+'/'+self.wortverbund_name_entry.get()+'.csv', 'a').close()
                self.wortverbund_name_entry.delete(0, 'end')
                self.wortverbund_name_entry['bg'] = 'green'
            except OSError:
                self.wortverbund_name_entry['bg'] = 'red'


class WortverbundSelecter(tk.Frame):
    """GUI-frame to select a project in order to work on it later.

        The argument "case", which is needed for "__init__", is used (and passed
        on) in order to execute certain functions of this programm (case==2 ->
        delete_wortverbund; case==3 -> work_on_features; case==4 ->
        show_wortverbund).
        If case==4 this class allows not only to select a wortverbund but also
        to plot all of them together."""

    def __init__(self, master, project, case):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7,
                  command=self.__del__).pack()
        if case == 2: # in order to delete a wortverbund
            self.label = tk.Label(self, font='Arial 16', text='Select a wortverbund to delete: ')
        else: # in order to work on features of a wortverbund or to show a wortverbund
            self.label = tk.Label(self, font='Arial 16', text='Select a wortverbund: ')
        self.label.pack()
        self.wortverbund_listbox = tk.Listbox(self, font='Arial 16', height=18,
                                              width=26)
        self.wortverbund_listbox.pack()
        self.project = project
        self.case = case

        if os.listdir('wb_files/'+self.project):
            for wortverbund_file in os.listdir('wb_files/'+self.project):
                self.wortverbund_listbox.insert('end', wortverbund_file[:-4])
            if self.case == 2: # in order to delete a wortverbund
                delete_button = tk.Button(self, font='Arial 16 italic',
                                          text='Delete', width=7,
                                          command=self.select_wortverbund)
                delete_button.configure(fg='red')
                delete_button.pack()
            elif self.case == 3: # in order to work on features of a wortverbund
                tk.Button(self, font='Arial 16', text='Ok', width=7,
                          command=self.select_wortverbund).pack()
            else: # in order to show a wortverbund
                tk.Button(self, font='Arial 16', text='Select', width=7,
                          command=self.select_wortverbund).pack()
                tk.Button(self, font='Arial 16', text='Plot all', width=7,
                          command=self.plot_all).pack()
        else:
            self.label.forget()
            self.wortverbund_listbox.forget()
            tk.Label(self, font='Arial 16',
                     text='There is no wortverbund in the project.').pack()

    def __del__(self):
        try:
            plt.close(self.figure)
        except AttributeError:
            pass
        try:
            self.forget()
            ROOT_FRAME.pack()
        except tk.TclError:
            pass

    def terminate(self):
        try:
            plt.close(self.figure)
        except AttributeError:
            pass
        ROOT.destroy()

    def select_wortverbund(self):
        if self.case == 2: # in order to delete a wortverbund
            try:
                os.remove('wb_files/'+self.project+'/'+self.wortverbund_listbox.get('active')+'.csv')
                self.wortverbund_listbox.delete('active')
            except FileNotFoundError:
                self.__del__()
        elif self.case == 3: # in order to work on features of a wortverbund
            self.forget()
            FeatureManager(ROOT, self.project,
                           self.wortverbund_listbox.get('active')).pack()
        else: # in order to show a wortverbund
            try:
                plt.close(self.fig)
            except AttributeError:
                pass
            self.forget()
            WortverbundShow(ROOT, self.project,
                            self.wortverbund_listbox.get('active')).pack()

    def plot_all(self):
        """Plots every wortverbund of the project in a single plot."""
        ROOT.protocol('WM_DELETE_WINDOW', self.terminate)

        content_lists = []
        wortverbund_names = []
        i = 0
        # Generates "content_lists" for all of the wortverbund files in the
        # directory of the project (every "content_list" of a wortverbund
        # contains the features and their occurrences).
        for wortverbund_file in os.listdir('wb_files/'+self.project):
            with open('wb_files/'+self.project+'/'+wortverbund_file, 'r') as csv_file:
                content_of_csv_file = csv.reader(csv_file, delimiter=';')
                content_lists.append([])
                wortverbund_names.append(wortverbund_file[:-4])
                for row in content_of_csv_file:
                    content_lists[i].append(row)
                for j in range(len(content_lists[i])):
                    content_lists[i][j][1] = content_lists[i][j][1].split('/')
                    for k in range(len(content_lists[i][j][1])):
                        content_lists[i][j][1][k] = int(content_lists[i][j][1][k])
            i += 1
        smallest_values = []
        highest_values = []
        x_values = []
        for i in range(len(content_lists)):
            # Sorts the "content_lists" (enables the program to work correctly
            # even if the features of a wortverbund were not entered in the
            # right order (i.e. the order of their occurrence)).
            content_lists[i] = wb_func.mergesort(content_lists[i],
                                                 len(content_lists[i]))
            smallest_value, highest_value = wb_func.find_extremes(content_lists[i])
            smallest_values.append(smallest_value)
            highest_values.append(highest_value)
            # Calculates the x-values of the "content_lists".
            x_values.append(wb_func.calculate_position_values(content_lists[i],
                                                              smallest_value,
                                                              highest_value))

        # Plots the "content_lists" (every wortverbund of the project).
        self.figure = plt.figure(0)
        self.figure.canvas.set_window_title('Plot of all wortverbund in \"'+self.project[:-5]+'\"')
        plt.xlabel('Position of addition of a feature ('+self.project[-4:]+' of occurrence)')
        plt.ylabel('Number of features')
        for i in range(len(content_lists)):
            features = [None]*(len(x_values[i])+1)
            positions = [None]*(len(x_values[i])+1)
            indices = [None]*(len(x_values[i])+1)
            for j in range(len(x_values[i])):
                if x_values[i][j] > 0:
                    positions[j+1] = x_values[i][j]
                    features[j+1] = content_lists[i][j][0]
                    indices[j+1] = j+1
            plt.plot(positions, indices, label=wortverbund_names[i])
            plt.plot(positions, indices, '.')
        plt.legend(loc='upper left')
        plt.grid(alpha=0.4)
        plt.show()


class FeatureManager(tk.Frame):
    """GUI-frame to add or remove features of a wortverbund."""

    def __init__(self, master, project, wortverbund):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7,
                  command=self.__del__).pack()
        tk.Label(self, font='Arial 16', text='Add or remove features in the wortverbund \"'+wortverbund+'\": ').pack()
        self.feature_listbox = tk.Listbox(self, font='Arial 16', height=16,
                                          width=36)
        self.feature_listbox.pack()
        try:
            with open('wb_files/'+project+'/'+wortverbund+'.csv', 'r') as csv_file:
                content_of_csv_file = csv.reader(csv_file, delimiter=';')
                for row in content_of_csv_file:
                    self.feature_listbox.insert('end', '\"'+row[0]+'\"'+'| at '+row[1])
        except IOError:
            pass
        remove_button = tk.Button(self, font='Arial 16 italic', text='Remove',
                                  width=12, command=self.remove)
        remove_button.configure(fg='red')
        remove_button.pack()
        tk.Label(self, font='Arial 16', text='Enter a feature to add: ').pack()
        self.feature_name_entry = tk.Entry(self, font='Arial 16', width=24)
        self.feature_name_entry.pack()
        tk.Label(self, font='Arial 16',
                 text='Enter the '+project[-4:]+' of its occurrence: ').pack()
        if project[-4:] == 'page':
            self.explanation_label = tk.Label(self, font='Arial 11',
                                              text='If you want to add the line of occurrence enter it like: page/line (e.g. \"134/12\").')
        elif project[-4:] == 'date':
            self.explanation_label = tk.Label(self, font='Arial 11',
                                              text='Enter it like: year/month/day/hour/minute/second (as specific as you want it to be; e.g. \"2018/11/27\").')
        elif project[-4:] == 'time':
            self.explanation_label = tk.Label(self, font='Arial 11',
                                              text='Enter it like: hour/minute/second (as specific as you want it to be; e.g. \"13/47\").')
        self.explanation_label.pack()
        self.feature_position_entry = tk.Entry(self, font='Arial 16', width=24)
        self.feature_position_entry.pack()
        add_button = tk.Button(self, font='Arial 16 italic', text='Add',
                               width=12, command=self.add)
        add_button.configure(fg='green')
        add_button.pack()
        self.project = project
        self.wortverbund = wortverbund

    def __del__(self):
        try:
            self.forget()
            ROOT_FRAME.pack()
        except tk.TclError:
            pass

    def add(self):
        if self.feature_name_entry.get() and self.feature_position_entry.get():
            try:
                if '/' in self.feature_position_entry.get():
                    int_check_list = self.feature_position_entry.get().split('/')
                    for i in range(len(int_check_list)):
                        if int_check_list[i] and not self.check_if_integer(int_check_list[i]):
                            raise ValueError
                else:
                    if not self.check_if_integer(self.feature_position_entry.get()):
                        raise ValueError
                with open('wb_files/'+self.project+'/'+self.wortverbund+'.csv', 'a') as wortverbund_file:
                    wortverbund_file.write(self.feature_name_entry.get()+';'+self.feature_position_entry.get()+'\n')
                self.feature_listbox.insert('end', '\"'+self.feature_name_entry.get()+'\"| at '+self.feature_position_entry.get())
                self.feature_name_entry.delete(0, 'end')
                self.feature_position_entry.delete(0, 'end')
            # Raises an exception if the string entered in
            # "self.feature_name_entry" (and perhaps split by "/") is not an
            # integer.
            except ValueError:
                self.explanation_label['text'] = 'You have to enter a number (an integer)! Letters are not accepted. Use \"/\" for separations.'
                self.explanation_label['fg'] = 'red'

    def check_if_integer(self, value_entered):
        try:
            int(value_entered)
            return True
        except ValueError:
            return False

    def remove(self):
        """Removes a selected feature from wortverbund by rebuilding the file's
            (i.e. the wortverbund's) content."""
        try:
            with open('wb_files/'+self.project+'/'+self.wortverbund+'.csv',
                      'r') as csv_file_to_read:
                content_of_csv_file_to_read = csv.reader(csv_file_to_read,
                                                         delimiter=';')
                i = 0
                feature_string_list = []
                feature_to_remove_found = False
                # Creates a "feature_string_list" with the content of each line
                # of the "csv_file_to_read" (every index stores a line).
                for row in content_of_csv_file_to_read:
                    feature_string_list.append(row[0]+';'+row[1]+'\n')
                    if self.feature_listbox.get('active').split('|')[0][1:-1] == row[0] and not feature_to_remove_found:
                        self.feature_listbox.delete('active')
                        feature_to_remove_found = True
                    # Counts up until "feature_to_remove_found" is True to get
                    # the index ("i") of the line that shall be removed.
                    if not feature_to_remove_found:
                        i += 1
            with open('wb_files/'+self.project+'/'+self.wortverbund+'.csv',
                      'w') as csv_file_to_write:
                j = 0
                feature_string = ''
                # Rebuilds a string ("feature_string") out of the elements of
                # the "feature_string_list", but skips the line with index "i",
                # so the feature that should be removed finally is removed.
                for k in range(len(feature_string_list)):
                    if i != j:
                        feature_string += feature_string_list[k]
                    j += 1
                csv_file_to_write.write(feature_string)
        except IOError:
            pass


class WortverbundShow(tk.Frame):
    """GUI-frame to show the features of a wortverbund and their positions of
        occurrence.

        Allows visualizing those features as a list and as a plot. Not all
        features have to be shown for the user can choose a start and an end
        position by using sliders or by entering the desired start and end
        values."""

    def __init__(self, master, project, wortverbund):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7,
                  command=self.__del__).pack()
        self.project = project
        self.wortverbund = wortverbund

        with open('wb_files/'+self.project+'/'+self.wortverbund+'.csv', 'r') as csv_file:
            content_of_csv_file = csv.reader(csv_file, delimiter=';')
            content_list = []
            for row in content_of_csv_file:
                content_list.append(row)
            for i in range(len(content_list)):
                content_list[i][1] = content_list[i][1].split('/')
                for j in range(len(content_list[i][1])):
                    content_list[i][1][j] = int(content_list[i][1][j])
        if not content_list:
            tk.Label(self, font='Arial 16', text='There are no features saved for \"'+self.wortverbund+'\"!').pack()
        else:
            self.content_list = wb_func.mergesort(content_list,
                                                  len(content_list)) # sorts the "content_list"
            self.smallest_values, self.highest_values = wb_func.find_extremes(self.content_list)
            self.x_values = wb_func.calculate_position_values(self.content_list,
                                                      self.smallest_values,
                                                      self.highest_values)

            tk.Label(self, font='Arial 16 bold', text='\nSelect a start and an end as limits: ').pack()
            self.scale_0 = tk.Scale(self, font='Arial 14', from_=0,
                                    to=self.x_values[-1]+1, length=360,
                                    orient='horizontal')
            self.scale_0.pack()
            self.scale_1 = tk.Scale(self, font='Arial 14', from_=0,
                                    to=self.x_values[-1]+1, length=360,
                                    orient='horizontal')
            self.scale_1.set(self.x_values[-1]+1)
            self.scale_1.pack()
            tk.Label(self, font='Arial 16 bold', text='\nEnter a precise start and a precise end as limits: ').pack()
            if self.project[-4:] == 'page':
                tk.Label(self, font='Arial 11',
                         text='If you want to add the line of occurrence enter it like: page/line (e.g. \"134/12\").').pack()
            elif self.project[-4:] == 'date':
                tk.Label(self, font='Arial 11',
                         text='Enter it like: year/month/day/hour/minute/second (as specific as you want it to be; e.g. \"2018/11/27\").').pack()
            elif self.project[-4:] == 'time':
                tk.Label(self, font='Arial 11',
                         text='Enter it like: hour/minute/second (as specific as you want it to be; e.g. \"13/47\").').pack()
            self.entry_precise_0 = tk.Entry(self, font='Arial 14', width=16)
            self.entry_precise_0.pack()
            self.entry_precise_1 = tk.Entry(self, font='Arial 14', width=16)
            self.entry_precise_1.pack()
            tk.Label(self, font='Arial 16 bold',
                     text='\nShow features within the selected range using the sliders: ').pack()
            tk.Button(self, font='Arial 16',
                      text='Show list (sliders)', width=39,
                      command=self.show_list_sliders).pack()
            sliders_button_frame = tk.Frame(self)
            tk.Button(sliders_button_frame, font='Arial 16',
                      text='Plot (sliders)', width=19, command=self.show_plot_sliders).pack(side='left')
            tk.Button(sliders_button_frame, font='Arial 16',
                      text='Plot annotated (sliders)', width=19,
                      command=self.show_plot_annotated_sliders).pack(side='left')
            sliders_button_frame.pack()
            tk.Label(self, font='Arial 16 bold',
                     text='\nShow features within the selected range using precise limits: ').pack()
            precise_button_frame = tk.Frame(self)
            tk.Button(self, font='Arial 16', text='Show list (precise)',
                      width=39, command=self.show_list_entries).pack()
            tk.Button(precise_button_frame, font='Arial 16',
                      text='Plot (precise)', width=19,
                      command=self.show_plot_entries).pack(side='left')
            tk.Button(precise_button_frame, font='Arial 16',
                      text='Plot annotated (precise)', width=19,
                      command=self.show_plot_annotated_entries).pack(side='left')
            precise_button_frame.pack()

            ROOT.protocol('WM_DELETE_WINDOW', self.terminate)

    def __del__(self):
        try:
            self.feature_list_show.destroy()
        except (AttributeError, tk.TclError):
            try:
                plt.close(self.figure)
            except AttributeError:
                pass
        try:
            self.forget()
            ROOT_FRAME.pack()
        except tk.TclError:
            pass

    def terminate(self):
        try:
            self.feature_list_show.destroy()
        except (AttributeError, tk.TclError):
            try:
                plt.close(self.figure)
            except AttributeError:
                pass
        ROOT.destroy()

    def show_list_sliders(self):
        self.show_sliders(0)

    def show_plot_sliders(self):
        self.show_sliders(1)

    def show_plot_annotated_sliders(self):
        self.show_sliders(2)

    def show_sliders(self, case):
        start = self.scale_0.get()
        end = self.scale_1.get()

        if start == end:
            self.show_error(start, end)
            return

        if case == 0: # coming from "self.show_list_sliders"
            self.show_list(start, end)
        elif case == 1: # coming from "self.show_plot_sliders"
            self.show_plot(start, end, 1)
        else: # coming from "self.show_plot_annotated_sliders"
            self.show_plot(start, end, 2)

    def show_list_entries(self):
        self.show_entries(0)

    def show_plot_entries(self):
        self.show_entries(1)

    def show_plot_annotated_entries(self):
        self.show_entries(2)

    def show_entries(self, case):
        start = self.entry_precise_0.get()
        end = self.entry_precise_1.get()

        limit_list = [None]*2
        if not start:
            start = 0
            limit_list[0] = [None, [start]]
        else:
            limit_list[0] = [None, start.split('/')]

        if not end:
            end = self.x_values[-1]+1
            limit_list[1] = [None, [end]]
        else:
            limit_list[1] = [None, end.split('/')]

        if (not '/' in str(start) and not '/' in str(end) and float(start) == float(end)) or str(start) == str(end):
            self.show_error(start, end)
            return

        for i in range(len(limit_list[0][1])):
            limit_list[0][1][i] = int(limit_list[0][1][i])
        for i in range(len(limit_list[1][1])):
            limit_list[1][1][i] = int(limit_list[1][1][i])

        x_values = wb_func.calculate_position_values(limit_list,
                                                     self.smallest_values,
                                                     self.highest_values)
        if case == 0: # coming from "self.show_list_entries"
            self.show_list(x_values[0], x_values[1])
        elif case == 1: # coming from "self.show_plot_entries"
            self.show_plot(x_values[0], x_values[1], 1)
        else: # coming from "self.show_plot_annotated_entries"
            self.show_plot(x_values[0], x_values[1], 2)

    def show_list(self, start, end):
        if start > end:
            temp = start
            start = end
            end = temp
        try:
            self.feature_list_show.destroy()
        except (AttributeError, tk.TclError):
            try:
                plt.close(self.figure)
            except AttributeError:
                pass
        self.feature_list_show = tk.Tk()
        self.feature_list_show.title('\"'+self.wortverbund+'\" in range from '+str(start)+' to '+str(end))
        content_list_string = ''
        for i in range(len(self.x_values)):
            if self.x_values[i] >= start and self.x_values[i] <= end:
                position = ''
                for j in range(len(self.content_list[i][1])):
                    position += str(self.content_list[i][1][j])+'/'
                content_list_string += ' - \"'+self.content_list[i][0]+'\"'+' at '+position[:-1]+'\n'
        if content_list_string:
            featList = tk.Text(self.feature_list_show, font='Arial 16 italic',
                               height=22, width=40)
            featList.insert('end', content_list_string)
            featList.configure(state='disabled', wrap='word')
            featList.pack()
        else:
            tk.Label(self.feature_list_show, font='Arial 16 italic',
                     text='No features in the range\nyou have selected...',
                     width=28).pack()

    def show_plot(self, start, end, case):
        if start > end:
            temp = start
            start = end
            end = temp
        try:
            self.feature_list_show.destroy()
        except (AttributeError, tk.TclError):
            try:
                plt.close(self.figure)
            except AttributeError:
                pass
        self.figure = plt.figure(0)
        self.figure.canvas.set_window_title('\"'+self.wortverbund+'\" in range from '+str(start)+' to '+str(end))
        plt.xlabel('Position of addition of a feature ('+self.project[-4:]+' of occurrence)')
        plt.ylabel('Number of features')

        features = [None]*(len(self.x_values)+1)
        positions = [None]*(len(self.x_values)+1)
        indices = [None]*(len(self.x_values)+1)
        for i in range(len(self.x_values)):
            if self.x_values[i] >= start and self.x_values[i] <= end:
                positions[i+1] = self.x_values[i]
                features[i+1] = self.content_list[i][0]
                indices[i+1] = i+1
        plt.plot(positions, indices, '-b')
        plt.plot(positions, indices, 'xr')

        if case == 2: # coming from "self.show_plot_annotated_sliders" or "self.show_plot_annotated_entries"
            # Annotates the plot by showing the features.
            for i in range(len(features)):
                if features[i]:
                    plt.annotate(features[i], (positions[i], indices[i]),
                                 xytext=(-22, 17), textcoords='offset points',
                                 arrowprops=dict(arrowstyle='-'))
        plt.grid(alpha=0.4)
        plt.show()

    def show_error(self, start, end):
        """Shows an error message to the user if the selected start position and
            the selected end position are equal."""
        try:
            self.feature_list_show.destroy()
        except (AttributeError, tk.TclError):
            try:
                plt.close(self.figure)
            except AttributeError:
                pass
        self.feature_list_show = tk.Tk()
        self.feature_list_show.title('')
        tk.Label(self.feature_list_show, font='Arial 16',
                 text='\nNo range selected...').pack()
        tk.Label(self.feature_list_show, font='Arial 11',
                 text='(Your start (\"'+str(start)+'\") equals your end (\"'+str(end)+'\")!)\n').pack()


def create_project():
    ROOT_FRAME.forget()
    ProjectCreator(ROOT).pack()


def create_wortverbund():
    ROOT_FRAME.forget()
    ProjectSelecter(ROOT, 0).pack()


def delete_project():
    ROOT_FRAME.forget()
    ProjectSelecter(ROOT, 1).pack()


def delete_wortverbund():
    ROOT_FRAME.forget()
    ProjectSelecter(ROOT, 2).pack()


def work_on_features():
    ROOT_FRAME.forget()
    ProjectSelecter(ROOT, 3).pack()


def show_wortverbund():
    ROOT_FRAME.forget()
    ProjectSelecter(ROOT, 4).pack()


ROOT = tk.Tk()
ROOT.title('wortverbund_builder')

ROOT_FRAME = tk.Frame(ROOT)
tk.Button(ROOT_FRAME, font='Arial 16', text='New project', width=28,
          command=create_project).pack()
tk.Button(ROOT_FRAME, font='Arial 16', text='New wortverbund', width=28,
          command=create_wortverbund).pack()
tk.Button(ROOT_FRAME, font='Arial 16', text='Delete project', width=28,
          command=delete_project).pack()
tk.Button(ROOT_FRAME, font='Arial 16', text='Delete wortverbund', width=28,
          command=delete_wortverbund).pack()
tk.Button(ROOT_FRAME, font='Arial 16', text='Work on features of a wortverbund',
          width=28, command=work_on_features).pack()
tk.Button(ROOT_FRAME, font='Arial 16', text='Show wortverbund', width=28,
          command=show_wortverbund).pack()
ROOT_FRAME.pack()

ROOT.mainloop()
