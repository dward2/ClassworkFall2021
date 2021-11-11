import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from health_db_client import add_patient_to_server


def load_and_resize_image(filename):
    """ Creates a tkinter image variable that can be displayed on GUI

    This function receives a filename as a parameter.  This should be the
    name of a file containing a digital image.  The file is first open
    and stored as a Pillow image file.  It uses the Image.size property and
    Image.resize() method to decrease the image size by 50%.  It then
    converts the Pillow image to a tk image.

    Note, while this code is written to decrease the size by 50%, a better
    approach may be to determine the aspect ratio of the picture and then
    adjust its size up or down to reach a default size.

    Args:
        filename (str): the name of the file containing an image to be loaded

    Returns:
        Pillow.ImageTk.PhotoImage: a tk-compatible image variable


    """
    pil_image = Image.open(filename)
    original_size = pil_image.size
    adj_factor = 0.5
    new_width = round(original_size[0] * adj_factor)
    new_height = round(original_size[1] * adj_factor)
    resized_image = pil_image.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image


def create_output(name, id, blood_letter, rh_factor, center):
    """Interface between GUI and server

    This function is call by the GUI command function attached to the "Ok"
    button of the GUI.  As input, it takes the data entered into the GUI.
    It creates an output string that is sent back to the GUI that is
    printed in the console.  It also call a function in the client module
    that will send the data to the server.  It returns the response that
    is received from the server

    Args:
        name (str): patient name entered in GUI
        id (str): patient id (medical record number) entered in GUI
        blood_letter (str):  patient blood type entered in GUI
        rh_factor (str):  patient rh_factor entered in GUI
        center (str): nearest donation center entered in GUI

    Returns:
        str, str: a formatted string containing patient information from the
            GUI, the response from the server when adding the patient

    """
    out_string = "Patient name: {}\n".format(name)
    out_string += "Blood type: {}{}\n".format(blood_letter, rh_factor)
    out_string += "Donation Center: {}\n".format(center)
    answer = add_patient_to_server(name, id,
                                   "{}{}".format(blood_letter, rh_factor))
    return out_string, answer


def design_window():
    """Creates the main GUI window for the health database

    A GUI window is created that is the main interface for the health
    database.  It accepts information from the user (patient name, id,
    blood type, rh factor, and nearest donation center).  Upon hitting the
    Ok button, this information is sent to the server.  Upon hitting the
    Cancel button, the window closes.

    Returns: None

    """

    def ok_button_cmd():
        """Event to run when Ok button is pressed

        This function is connected to the "Ok" button of the GUI.  It follows
        the typical pattern for these command functions:
        1. It gets the needed information from the GUI.
        2. It calls a function external to the GUI to process the data and
        receive the results
        3. It updates the GUI based on the received results.  In this case,
        that includes printing to the console and updating a Label in the GUI.

        Returns: None

        """
        # Get needed data from GUI
        name = name_data.get()
        id = id_data.get()
        blood_letter = blood_letter_data.get()
        rh_factor = rh_data.get()
        center = donation_center_data.get()

        # Call external function to do the work that can be tested
        out_string, answer = create_output(name, id, blood_letter, rh_factor,
                                           center)

        # Update GUI
        print(out_string)
        output_string.configure(text=answer)

    def cancel_cmd():
        """Closes window upon click of Cancel button

        This function is connected to the "Cancel" button of the GUI.  It
        destroys the root window causing the GUI interface to close.
        """
        root.destroy()

    def change_picture_cmd():
        """Allows user to select a new image to display

        This function opens a dialog box to allow the user to choose an image
        file.  If the user does not cancel the dialog box, the chosen filename
        is sent to an external function for opening and resizing.  The
        returned image is then added to the image_label widget for display
        on the GUI.

        """
        filename = filedialog.askopenfilename(initialdir="images")
        if filename == "":
            messagebox.showinfo("Cancel", "You cancelled the image load")
            return
        tk_image = load_and_resize_image(filename)
        image_label.configure(image=tk_image)
        image_label.image = tk_image  # Stores image as part of widget to
        # prevent garbage collection and loss of image

    root = tk.Tk()
    root.title("Health Database GUI")
    # root.geometry("10x2")

    top_label = ttk.Label(root, text="Blood Donor Database")
    top_label.grid(column=0, row=0, columnspan=2, sticky='w')

    ttk.Label(root, text="Name").grid(column=0, row=1, sticky='e')

    name_data = tk.StringVar()
    name_entry_box = ttk.Entry(root, width=40, textvariable=name_data)
    name_entry_box.grid(column=1, row=1, sticky='w', columnspan=2)

    ttk.Label(root, text="ID").grid(column=0, row=2)

    id_data = tk.StringVar()
    id_entry_box = ttk.Entry(root, width=10, textvariable=id_data)
    id_entry_box.grid(column=1, row=2, sticky='w')

    blood_letter_data = tk.StringVar()
    ttk.Radiobutton(root, text='A', variable=blood_letter_data,
                    value='A').grid(column=0, row=3, sticky=tk.W)
    ttk.Radiobutton(root, text='B', variable=blood_letter_data,
                    value='B').grid(column=0, row=4, sticky=tk.W)
    ttk.Radiobutton(root, text='AB', variable=blood_letter_data,
                    value='AB').grid(column=0, row=5, sticky=tk.W)
    ttk.Radiobutton(root, text='O', variable=blood_letter_data,
                    value='O').grid(column=0, row=6, sticky=tk.W)

    rh_data = tk.StringVar()
    rh_data.set('-')
    rh_checkbox = ttk.Checkbutton(root, text="Rh Positive",
                                  variable=rh_data, onvalue='+',
                                  offvalue='-')
    rh_checkbox.grid(column=1, row=4)

    ttk.Label(root, text="Nearest Donation Center").grid(column=3, row=0)

    donation_center_data = tk.StringVar()
    combo_box = ttk.Combobox(root, textvariable=donation_center_data)
    combo_box["values"] = ("Durham", "Raleigh", "Cary", "Apex")
    combo_box.state(["readonly"])
    combo_box.grid(column=3, row=1)

    # This output_string will be used to display results from the server
    output_string = ttk.Label(root)
    output_string.grid(column=0, row=10)

    ok_button = ttk.Button(root, text="Ok", command=ok_button_cmd)
    ok_button.grid(column=1, row=6)

    cancel_button = ttk.Button(root, text="Cancel", command=cancel_cmd)
    cancel_button.grid(column=2, row=6)

    # Creates a place holder for an image.
    tk_image = load_and_resize_image("images/blank_pic.jpeg")
    image_label = ttk.Label(root)
    image_label.grid(column=0, row=7)

    # Creates a button to allow user to change the image
    change_picture_btn = ttk.Button(root, text="Change Picture",
                                    command=change_picture_cmd)
    change_picture_btn.grid(column=1, row=7)

    root.mainloop()


if __name__ == '__main__':
    design_window()
