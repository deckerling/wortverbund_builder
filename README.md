# *wortverbund_builder*
A program providing tools to track the development of complex signs in a discourse.

*wortverbund_builder* provides self-explanatory tools to track the growth of a complex sign (especially a so-called "[wortverbund](http://www.baer-linguistik.de/hlr/028.htm)"). Such a complex sign (or "wortverbund") can be a certain object or character in a book, a movie or a discourse.  
You could, for example, create a project "The Lord of the Rings" and a wortverbund "Frodo" within this project. The next step would be to add all the characteristics and semantic features that define "Frodo" within the novel or movie entering not only the information (feature) itself but also the location of the information within the text (i.e. a page, perhaps also a line on a certain page, or a point in time in a movie). Having entered those features, *wortverbund_builder* allows you to show the features within a certain range (e.g. from page 163 to 271) in a list or even plot them. It is also possible to show every wortverbund of a project together in one single plot (i.e. showing their development regarding their features in a single plot). Such a visualization makes it easy to see, which characters appear together and how much information we can gather about each of the characters in relation to one another. This provides a structured starting point for a quantitative analysis of a novel, a movie or a discourse.  
A bit of an exemplary project (regarding [Theodor Fontane](https://en.wikipedia.org/wiki/Theodor_Fontane)’s novella "[Irrungen, Wirrungen](https://de.wikipedia.org/wiki/Irrungen,_Wirrungen)") can be found in this package as well (see "[wb_files](wb_files)").

*wortverbund_builder* is based on GUIs so you can easily provide it to researchers who aren’t used to work with Python codes (you could, for example, create an executable file for them).

## "wb2sc_file_converter.py"
"wb2sc_file_converter.py" is a simple, self-explanatory tool to convert files created by *wortverbund_builder* into files readable by [*sign_compare*](https://github.com/deckerling/sign_compare) to calculate similarities. Make sure that "sign_compare.py", wortverbund_builder.py", and "wb2sc_file_converter.py" have access to all the required files either by saving them in the same directory or by adjusting the paths to the directories "sc_files" and "wb_files" in the code of "wb2sc_file_converter.py" (lines 40, 60, 70, 71, 72, 123, 125, 134, 135 and 156).  
Just like *sign_compare* and "wortverbund_builder.py", "wb2sc_file_converter.py" is based on GUIs.

## License
The work contained in this package is licensed under the Apache License, Version 2.0 (see the file "[LICENSE](LICENSE)").
