# notedraft
#### Video Demo:  https://youtu.be/NVo1nJ0tCdM
#### Description: This project takes user input and uses it to generate the rough draft of a psychiatric consultation note.

The index page is a form that is filled out by the user. The form includes typical information that is included in a psychiatric consultation note. The form is divided into the typical sections of a consultation note.

The first section is the patient identification section. This section includes basic demographic information, such as name, age, and gender. The pronouns used for the note depend on the gender selected here.

The next section is simply the reason for referral.

The following section is the history of present illness section. This section is divided into subsections: depression, safety, mania/hypomania, anxiety, and psychosis. Here, the user indicates whether particular symptoms are present or absent. The input fields can also be omitted if these questions were not asked. Most of the symptoms can be indicated by checking off radio buttons, to save time for the user. Certain symptoms also have textboxes to allow for atypical responses or to include additional information.

The next section is a textbox for entering the past psychiatric history.

The following sections are the past medical history and medication sections. If the "present" radio button is selected, additional textboxes will appear to allow the user to include the details.

The next sections are for allergies, substance use history, and family psychiatric history.

The following section is the mental status examination. The mood, suicidality, and violent ideation fields are populated by the answers provided to the corresponding fields in the history of present illness section, if those were completed.

The final sections include the diagnosis, assessment, and plan.

At the bottom of the page is the "submit" button. If pressed, the information entered into the form above will be used to generate the rough draft of a psychiatric consultation note, which is displayed in the "note.html" webpage. The user can then copy this note and edit it to produce the final version of the note. At the bottom of the note webpage is a link back to the index page, which allows the user to complete a new form.

The app.py file includes the python code that processes the information entered by the user and generates the strings that make up the note. The index.html page includes the form that is filled by the user. The note.html page includes the generated note. The styles.css file includes the CSS styles used by the html pages.

The website was designed to make it as quick and easy to generate the note as possible. Only the name and gender fields are required. Different users may have different preferences for what to include in the note, so having minimal requirements allows for greater flexibility and minimizes frustration with unclear requirements. The history of present illness section was designed to be able to capture most typical patient presentations, including depression, mania/hypomania, anxiety, and psychosis. There is a safety subsection as well, due to the importance of screening for safety. Most of the typical responses can be indicated by checking a radio button, which makes it very quick to indicate the responses. However, some of the questions also include textboxes to allow the user some flexibility in providing atypical responses. There are also additional textboxes that allow the user to provide additional information, or to include additional subsections in the history of present illness. The past psychiatric history section is simply a large textbox, to allow for maximum flexibility in this area, as different users will likely have difference preferences for how to structure this section, depending on the patient's clinical history. The past medical history and medications sections have a "none" option, to indicate that the patient does not have a past medical history or is not on any medications, rather than the information being omitted or unknown. If the user indicates the "present" option, then the list can be completed. The mental status examination section mostly consists of radio buttons to allow it to be completed quickly.

The style is very simple to avoid distracting the user and to allow the user to clearly see what information is to be provided. The different sections of the note have different background colors so that the user can clearly see what the current section is. In general, each set of options is left justified and on its own line, so that it is easy to make sure one does not miss a question, and so that it is easy to move from one question to the next.


