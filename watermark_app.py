from tkinter import Label, Tk, Button, filedialog, Scale, HORIZONTAL
from PIL import Image, ImageTk, ImageEnhance

current_image = None
current_image_label =None
original_image=None

#getting the path of the image from the user.
def open_file():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if file_path:
        load_image(file_path)

#saving the new image 
def save_image():
    if current_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            current_image.save(file_path)

#changes the brightness of the logo
def adjust_logo_brightness(image, brightness):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(brightness)

#updates the brightness of the image every time the slider is moved
def update_brightness(value):
    global original_image
    brightness = float(value)
    img_with_watermark = add_watermark(original_image, brightness)
    display_image(img_with_watermark)

#responsible for displaying the image on the screen
def display_image(img):
    global current_image
    current_image = img
    img_width, img_height = image_size(img)
    img_resized = img.resize((img_width, img_height - 200))
    img_tk = ImageTk.PhotoImage(img_resized)

    global current_image_label
    current_image_label.config(image=img_tk)
    current_image_label.image = img_tk

#image width and height
def image_size(image):
    img_width, img_height = image.size

    screen_width = window.winfo_screenwidth()  
    screen_height = window.winfo_screenheight() 

    ratio_width = screen_width / img_width
    ratio_height = screen_height / img_height

    ratio = min(ratio_width, ratio_height)

    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)

    return new_width , new_height

#putting the watermark on the img
def add_watermark(image,brightness=1.0):
    watermark = Image.open("logo\logo2.png")  
    watermark = watermark.convert("RGBA") 

    watermark = adjust_logo_brightness(watermark, brightness)

    img_width, img_height = image.size
    wm_width, wm_height = watermark.size

    scale = 0.1 
    new_wm_width = int(img_width * scale) 
    new_wm_height = int((new_wm_width / wm_width) * wm_height)

    min_width = 250
    min_height = 250

    new_wm_width = max(new_wm_width, min_width)
    new_wm_height = max(new_wm_height, min_height)

    watermark = watermark.resize((new_wm_width, new_wm_height))
    
    position = (img_width - new_wm_width , img_height - new_wm_height)

    image.paste(watermark, position, watermark) 

    return image

#loading the image with the logo
def load_image(file_path):
    global current_image_label  
    global current_image
    global original_image

    img = Image.open(file_path) 
    original_image =img
    img = add_watermark(img)

    img_width,img_height = image_size(img)

    img = img.resize((img_width, img_height-200))
    img_tk = ImageTk.PhotoImage(img)  

    window.geometry(f"{img_width}x{img_height-100}+{100}+{0}")

    if current_image_label:
        current_image_label.grid_forget()

    current_image_label = Label(window, image=img_tk)
    current_image_label.image = img_tk
    current_image_label.grid(row=0, column=0,columnspan=3, pady=20)

    current_image = img

    change_screen()

def change_screen():
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1) 
    window.grid_columnconfigure(2, weight=1)

    button_save_img.grid(row=5, column=0, pady=10)
    brightness_slider.grid(row=5, column=1, pady=10)
    button_reset.grid(row=5, column=2, pady=10)

    welcome_label.grid_forget()
    second_label.grid_forget()
    button_label.grid_forget()
    button_upload_img.grid_forget()

def reset_screen():
    global current_image
    current_image = None 

    open_file()



def setup_ui():
    global welcome_label, second_label, button_upload_img, button_save_img, button_reset,button_label,brightness_slider

    button_label = Label(text="Click on the button to start", bg='white', highlightthickness=0, font=("Arial", 14 ))
    button_label.grid(row=2, column=0,pady=1)

    #Button to upload the image 
    button_upload_img = Button(text="Upload image", command=open_file)
    button_upload_img.grid(row=3,column=0)

    button_save_img = Button(text="Save image", command=save_image)

    button_reset = Button(text="Choose new image", command=reset_screen)

    brightness_slider = Scale(
        window, from_=0.0, to=2.0, resolution=0.1, orient=HORIZONTAL,
        label="Adjust Brightness", command=update_brightness
    )
    brightness_slider.set(1.0)  

    window.grid_columnconfigure(0, weight=1)

    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=1)

#---------------------------- UI SETUP ----------------------------#   
window = Tk()
window.title("Watermark GUI website")
window.minsize(500,300)

welcome_label = Label(text="Welcome to the Watermark creator", bg='white', highlightthickness=0, font=("Arial", 20, "bold"))
welcome_label.grid(row=0, column=0 ,pady=4)

second_label = Label(text="Where you can put your logo on your image.", bg='white', highlightthickness=0, font=("Arial", 17 ))
second_label.grid(row=1, column=0,pady=4)

setup_ui()

window.mainloop()