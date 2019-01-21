#!/usr/bin/env python3

# wb2sc_file_converter.py
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

"""A simple tool converting files created by wortverbund_builder to files that
    sign_compare can work with."""

import csv
import os
import tkinter as tk


class WortverbundSelecter(tk.Frame):
    """GUI-frame to select a wortverbund of a project and to convert it."""

    def __init__(self, master, project):
        tk.Frame.__init__(self)
        tk.Button(self, font='Arial 16', text='Back', width=7, command=self.__del__).pack()
        self.label = tk.Label(self, font='Arial 16', text='Select a wortverbund to convert to a sc-file: ')
        self.label.pack()
        self.wortverbund_listbox = tk.Listbox(self, font='Arial 16', height=18, width=26)
        self.wortverbund_listbox.pack()
        self.project = project
        
        if os.listdir('wb_files/'+self.project):
            for wortverbund_file in os.listdir('wb_files/'+self.project):
                self.wortverbund_listbox.insert('end', wortverbund_file[:-4])
            self.convert_button = tk.Button(self, font='Arial 16', text='Convert', width=7, command=self.convert_wortverbund)
            self.convert_button.pack()
        else:
            self.label.forget()
            self.wortverbund_listbox.forget()
            tk.Label(self, font='Arial 16', text='There is no wortverbund in the project.').pack()
       
    def __del__(self):
        self.forget()
        ROOT_FRAME.pack()
        
    def convert_wortverbund(self):
        """Converts the selected wortverbund_builder file to a sign_compare file
            by reading the features saved in the input file (wortverbund_builder
            file) and writing them into the output file (sign_compare file)."""
        self.wortverbund_listbox.forget()
        self.convert_button.forget()
        try:
            with open('wb_files/'+self.project+'/'+self.wortverbund_listbox.get('active')+'.csv', 'r') as csv_file:
                content_of_csv_file = csv.reader(csv_file, delimiter=';')
                self.feature_string = ''
                for row in content_of_csv_file:
                    if row[0]:
                        self.feature_string += row[0]+';'
            if self.feature_string:
                # If there is no sign_compare file (or even no directory) with
                # the same name as the selected wortverbund_builder file:
                # creates a new sign_compare file.
                if not os.path.exists('sc_files'):
                    os.makedirs('sc_files')
                if not os.path.exists('sc_files/'+self.wortverbund_listbox.get('active')+'.txt'):
                    self.save_converted_file_0(0)
                # If a sign_compare file with the same name as the selected
                # wortverbund_builder file already exists: 3 new options.
                else:
                    self.label['text'] = 'A sign \"'+self.wortverbund_listbox.get('active')+'\" already exists!\nWhat do you want to do?'
                    self.convert_button = tk.Button(self, font='Arial 16', text='Append existing file', width=40, command=self.save_by_appending)
                    self.convert_button.pack()
                    self.replace_button = tk.Button(self, font='Arial 16', text='Replace existing file (the old file will be lost)', width=40, command=self.save_by_replacing)
                    self.replace_button.pack()
                    self.rename_button = tk.Button(self, font='Arial 16', text='Rename existing file and save the newly converted', width=40, command=self.rename_and_save)
                    self.rename_button.pack()
            else:
                self.label['text'] = '\"'+self.wortverbund_listbox.get('active')+'\" was not converted because there are no features in it!'
        except IOError:
            self.label['text'] = 'Sorry, \"'+self.wortverbund_listbox.get('active')+'\" couldn\'t be converted!'

    def save_by_appending(self):
        """Saves the features of the input file (wortverbund_builder file) in an
            already existing sign_compare file by adding them to it."""
        self.save_converted_file_0(0)

    def save_by_replacing(self):
        """Saves the features of the input file (wortverbund_builder file) in a
            "new" sign_compare file replacing the one that already existed -
            this means that the old sign_compare file gets lost."""
        self.save_converted_file_0(1)

    def rename_and_save(self):
        """Allows to rename an already existing sign_compare file and to save
            the features of the input file (wortverbund_builder file) in a
            new sign_compare file - i.e. creating a new file and keeping the old
            one."""
        self.convert_button.forget()
        self.replace_button.forget()
        self.rename_button.forget()
        
        self.label['text'] = 'Enter new name for the existing sign \"'+self.wortverbund_listbox.get('active')+'\": '
        self.entry = tk.Entry(self, font='Arial 16', width=16)
        self.entry.pack()
        self.convert_button = tk.Button(self, font='Arial 16', text='Rename and save', width=15, command=self.save_converted_file_1)
        self.convert_button.pack()
        
    def save_converted_file_0(self, case):
        self.convert_button.forget()
        try:
            self.replace_button.forget()
            self.rename_button.forget()
        except AttributeError:
            pass
        if case == 0: # coming from "self.save_by_appending"
            sign_compare_file = open('sc_files/'+self.wortverbund_listbox.get('active')+'.txt', 'a')
        else: # coming from "self.save_by_replacing"
            sign_compare_file = open('sc_files/'+self.wortverbund_listbox.get('active')+'.txt', 'w')
        sign_compare_file.write(self.feature_string)
        sign_compare_file.close()
        self.label['text'] = '\"'+self.wortverbund_listbox.get('active')+'\" converted!'

    def save_converted_file_1(self): # coming from "self.rename_and_save"
        self.convert_button.forget()
        self.entry.forget()
        try:
            os.rename('sc_files/'+self.wortverbund_listbox.get('active')+'.txt', 'sc_files/'+self.entry.get()+'.txt')
            with open('sc_files/'+self.wortverbund_listbox.get('active')+'.txt', 'w') as sign_compare_file:
                sign_compare_file.write(self.feature_string)
            self.label['text'] = '\"'+self.wortverbund_listbox.get('active')+'\" converted and already existing file renamed \"'+self.entry.get()+'\"!'
        except:
            self.label['text'] = 'Your new file name was not accepted!'


def select_project():
    ROOT_FRAME.forget()
    WortverbundSelecter(ROOT, project_listbox.get('active')).pack()


ROOT = tk.Tk()
ROOT.title('wb2sc_file_converter')

# Main frame to select a wortverbund_builder project.
ROOT_FRAME = tk.Frame(ROOT)
project_listbox = tk.Listbox(ROOT_FRAME, font='Arial 16', height=18, width=26)
project_listbox.pack()
try:
    no_projects = True
    for project in os.listdir('wb_files'):
        if not '.' in project:
            project_listbox.insert('end', project)
            no_projects = False
    if no_projects:
        raise IOError
    else:
        tk.Button(ROOT_FRAME, font='Arial 16', text='Select project', width=26, command=select_project).pack()
except IOError:
    project_listbox.forget()
    tk.Label(ROOT_FRAME, font='Arial 16', text='\nThere are no wortverbund_builder projects!\n').pack()
ROOT_FRAME.pack()

ROOT.mainloop()
