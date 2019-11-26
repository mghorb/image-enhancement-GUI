import cv2
from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import numpy as np

global image
# kernal size smoothing filter
global x
# kernal size sobel filters
global s

# credit goes to this person for the toggle feature:
# https://stackoverflow.com/questions/13141259/expandable-and-contracting-frame-in-tkinter?fbclid=IwAR0XPP0jR_SZ8ZOp-mIWa7t_gXnJZIgg_fKU7F5uHKeaZrJGMhf4SSpFgrc
# https://stackoverflow.com/users/979203/onlyjus
class ToggledFrame(Frame):
    def __init__(self, parent, text="", *args, **options):
        Frame.__init__(self, parent, *args, **options)

        self.show = IntVar()
        self.show.set(0)

        self.title_frame = Frame(self, width=1000, bg="gray")
        self.title_frame.pack(fill="x", expand=1)

        Label(self.title_frame, text=text, bg="gray").pack(side="left", fill="x", expand=1)

        self.plusMinus = Label(self.title_frame, text="+", bg="gray")
        self.plusMinus.pack(side="left")
        self.toggle_button = Checkbutton(self.title_frame, width=1, bg="gray", cursor="plus", command=self.toggle, variable=self.show)
        self.toggle_button.pack(side="left")

        self.sub_frame = Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.plusMinus.configure(text='-')
        else:
            self.sub_frame.forget()
            self.plusMinus.configure(text='+')

# function to browse for an image
def browseImage():
    # global "current" image
    global image
    # global original image
    global imageEdit
    # global file path name
    global path

    # opens a file dialog to select an image
    path = filedialog.askopenfilename()
    # read the image to edit
    imageEdit = cv2.imread(path)
    # current image = image read
    image = imageEdit

    # OpenCV represents images in BGR order; however we need gray scale
    orig = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # original image = converted gray scale image
    ImageEdit = orig

    # convert the image to PIL format (to display in GUI)
    origPIL = PIL.Image.fromarray(orig)
    # converts PIL format ImageTk format
    origTK = ImageTk.PhotoImage(origPIL)
    # display the image on the GUI
    newImg.configure(image=origTK)
    newImg.image = origTK
    # change th label on to the image
    editLabel.configure(text="Original")

    # current image = original image
    image = orig
    originalImage()

# function that saves image to current directory
def saveImage(img):
    # global "current" image
    global image
    global path

    # save image to current directory
    cv2.imwrite(path+".jpg", img)

# function that reverts back to original image
def originalImage():
    global image
    global imageEdit

    # reset image to original
    image = imageEdit

    # convert to make it viewable in Tkinter
    imagePIL = PIL.Image.fromarray(imageEdit)
    imageTK = ImageTk.PhotoImage(imagePIL)
    newImg.configure(image=imageTK)
    newImg.image=imageTK
    showNewImage(imageTK)
    # change label
    editLabel.configure(text="Original")

    # convert back
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function that applies the histogram equalizer
def histoEqualizer(img):
    global image

    # apply equalized histogram
    equ = cv2.equalizeHist(img)

    # convert to make it viewable in Tkinter
    equPIL = PIL.Image.fromarray(equ)
    equTk = ImageTk.PhotoImage(equPIL)
    showNewImage(equTk)
    # change label
    editLabel.configure(text="Histogram Equalization")

    # changes global image to filtered image, convert it back
    image = equ
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function that applies sharpening
def sharpen(img):
    global image
    global imageEdit
    global x

    # apply sharpening
    kernel = np.array([[-1,-1,-1], [-1, 9,-1],[-1,-1,-1]])
    sharp = cv2.filter2D(img, -1, kernel)

    # make it viewable in Tkinter
    sharpPIL = PIL.Image.fromarray(sharp)
    sharpTk = ImageTk.PhotoImage(sharpPIL)
    showNewImage(sharpTk)
    # edits label
    editLabel.configure(text="Sharpening\nKernel Size: 9 (default)")

    # changes global image to filtered image, converts back to type for other functions
    image = sharp
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function that applies gaussian mask
def gaussianMask(img):
    global image
    global x

    # apply gaussian blur mask
    gauss = cv2.GaussianBlur(img, (x,x), 0)

    # convert it to make it viewable in tkinter
    gaussPIL = PIL.Image.fromarray(gauss)
    gaussTk = ImageTk.PhotoImage(gaussPIL)
    showNewImage(gaussTk)
    # edits label
    editLabel.configure(text="Gaussian Mask\nKernel Size: " + str(x))

    #Changes global image to filtered image
    image = gauss
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function that applies median filter
def medianFilter(img):
    global image
    global x

    # applies median blur
    med = cv2.medianBlur(img, x)

    # converts to make it viewable in Tkinter
    medPIL = PIL.Image.fromarray(med)
    medTk = ImageTk.PhotoImage(medPIL)
    showNewImage(medTk)
    # edits label
    editLabel.configure(text="Median Filtering\nKernel Size: " + str(x))

    # changes global image to filtered image, converts back
    image = med
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function that applies averaging mask
def averageMask(img):
    global image
    global x

    # apply averaging mask
    avg = cv2.blur(img, (x, x))

    # converts and makes it viewable in Tkinter
    avgPIL = PIL.Image.fromarray(avg)
    avgTk = ImageTk.PhotoImage(avgPIL)
    showNewImage(avgTk)
    #editLabel
    editLabel.configure(text="Averaging Mask\nKernel Size: " + str(x))

    # changes global image to filtered image, converts it back
    image = avg
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function does edge detection using canny
def edgeCanny(img):
    global image

    # apply edge canny detection
    edge = cv2.Canny(img, 100, 200)

    # converts and makes it viewable in Tkinter
    edgePIL = PIL.Image.fromarray(edge)
    edgeTK = ImageTk.PhotoImage(edgePIL)
    showNewImage(edgeTK)
    # edits label
    editLabel.configure(text="Canny Edge Detection")

    # changes global image to filtered image, converts it back
    image = edge
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function does edge detection using laplacian
def laplacian(img):
    global image

    # apply lapalacian edge detection
    laplacian = cv2.Laplacian(img,cv2.CV_64F)

    # convert to make it viewable in Tkinter
    laplacianPIL = PIL.Image.fromarray(laplacian)
    laplacianTK = ImageTk.PhotoImage(laplacianPIL)
    showNewImage(laplacianTK)
    # edits label
    editLabel.configure(text="Laplacian Edge Detection")

    # changes global image to filtered image, converts it back
    image = laplacian
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function does edge detection using Sobel
def edgeSobelX(img):
    global image
    global s

    # apply sobel vertical filters
    edge = cv2.Sobel(img,cv2.COLOR_BGR2GRAY,1,0,ksize=s)

    # convert to make it viewable in Tkinter
    edgePIL = PIL.Image.fromarray(edge)
    edgeTK = ImageTk.PhotoImage(edgePIL)
    showNewImage(edgeTK)
    # edit label
    editLabel.configure(text="Vertical\nSobel Filter\nKernel Size:" + str(s))

    # changes global image to filtered image, converts it back
    image = edge
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function does edge detection using Sobel
def edgeSobelY(img):
    global image
    global s

    # apply sobel horizontal filters
    edge = cv2.Sobel(img,cv2.COLOR_BGR2GRAY,0,1,ksize=s)

    # convert to make it viewable in Tkinter
    edgePIL = PIL.Image.fromarray(edge)
    edgeTK = ImageTk.PhotoImage(edgePIL)
    showNewImage(edgeTK)
    # edits label
    editLabel.configure(text="Horizontal\nSobel Filter\nKernel Size:" + str(s))

    # changes global image to filtered image, converts it back
    image = edge
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function does edge detection using Sobel
def binary(img):
    global image

    # convert it to binary
    binary = cv2.threshold(img, ThreshMin.get(), ThreshMax.get(), cv2.THRESH_BINARY_INV)[1]

    # convert to display on Tkinter
    binaryPIL = PIL.Image.fromarray(binary)
    binaryTK = ImageTk.PhotoImage(binaryPIL)
    showNewImage(binaryTK)
    # updates label
    editLabel.configure(text="Binary\n Min Threshold: " + str(ThreshMin.get()) + "\nMax Threshold: " + str(ThreshMax.get()))

    # changes global image to filtered image, converts it back
    image = binary
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function that dilates pixels
def dilation(img):
    global image

    # apply one iteration of dilation
    kernel = np.ones((kern.get(),kern.get()), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations=1)

    # convert and make it viewable in Tkinter
    dilationPIL = PIL.Image.fromarray(dilation)
    dilationTK = ImageTk.PhotoImage(dilationPIL)
    showNewImage(dilationTK)
    #edit label
    editLabel.configure(text="Dilation\nKernel: " + str(kern.get()))

    # changes global image to filtered image, converts it back
    image = dilation
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function that erodes pixels
def erosion(img):
    global image

    # apply one iteration of dilation
    kernel = np.ones((kern.get(), kern.get()), np.uint8)
    erosion = cv2.erode(img, kernel, iterations = 1)

    # convert and make it viewable in Tkinter
    erosionPIL = PIL.Image.fromarray(erosion)
    erosionTK = ImageTk.PhotoImage(erosionPIL)
    showNewImage(erosionTK)
    # edit label
    editLabel.configure(text="Erosion\nKernel: " + str(kern.get()))

    # changes global image to filtered image, converts it back
    image = erosion
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gamma(img):
    global image

    # apply gamma
    lookUpTable = np.empty((1, 256), np.uint8)
    for i in range(256):
        lookUpTable[0, i] = np.clip(pow(i / 255.0, g.get()) * 255.0, 0, 255)

    gamma = cv2.LUT(img, lookUpTable)

    # convert and make it viewable in Tkinter
    gammaPIL = PIL.Image.fromarray(gamma)
    gammaTK = ImageTk.PhotoImage(gammaPIL)
    showNewImage(gammaTK)
    # edit label
    editLabel.configure(text="Gamma Correction\nGamma = " + str(g.get()))

    # changes global image to filtered image, converts it back
    image = gamma
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function that displays all objects
def objects(img):
    global image
    global imageEdit
    global x

    # Create labels on the closed binary image
    ret, labels = cv2.connectedComponents(img)

    # Find contours and label all connected components
    # https://stackoverflow.com/questions/46441893/connected-component-labeling-in-python?rq=1
    contours, hierarchy = cv2.findContours(img, 1, 2)
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0

    # Loop for each contour (object)
    x = 1
    i = 1
    y = 0
    while i <= len(contours):
        cnt = contours[i-1]
        # Get area of contour and put it in the table
        area = cv2.contourArea(cnt)
        if area >= 20:
            y +=1
        # Get moments
        M = cv2.moments(cnt)
        rect = cv2.minAreaRect(cnt)
        # Get bounding box and put it in table
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if M['m00'] > 0:
            # Get centroid and put it in the table
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
        if area < 20:
            x += 1
        else:
            # Draws bounding box on the image
            cv2.drawContours(labeled_img, [box], 0, (150, 150, 255), 1)
            # Draw centroid on image
            cv2.circle(labeled_img, (cx, cy), 2, (150, 150, 255), -1)
            # Draw Index
            cv2.putText(labeled_img, str(y), (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))
        i += 1

    # convert to make viewable in Tkinter
    labeledPIL = PIL.Image.fromarray(labeled_img)
    labeledTK = ImageTk.PhotoImage(labeledPIL)
    showNewImage(labeledTK)
    # edit label
    editLabel.configure(text="Labeled Objects")

    # changes global image to filtered image, converts it back
    image = imageEdit
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function that outputs the edited image
def showNewImage(img):
    newImg.configure(image=img)

    newImg.image = img

# sets the kernel (for smoothing) to chosen value
def setX(kernel):
    global x
    x = kernel

# sets the kernel (for Sobel) to chosen value
def setS(kernel):
    global s
    s = kernel

# opens a message box about the details of the program
def aboutProgram():
    tkinter.messagebox.showinfo("About this Program", "This program may be used for image enhancement, edge detection, and object detection. The OpenCV library was used.")

# opens a message box on how to use the program
def helpBox():
    tkinter.messagebox.showinfo("Help", "1. Click Browse to choose image.\n2. Use the dropdown menus to apply desired filters.\n3. Apply desired edge detection.\n4. Save image if desired.")

# opens up a window, config title bar and size
root = Tk()
root.title("Image Enhancement Software")
root.geometry('1500x800')

### menu bar ####
menu = Menu(root)
root.config(menu=menu)
# add a "File" dropdown menu
fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Browse...", command=browseImage)
fileMenu.add_command(label="Save Image", command=lambda: saveImage(image))
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=quit)
# add a "Help" dropdown menu
helpMenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="Help", command=helpBox)
helpMenu.add_command(label="About", command=aboutProgram)


### features side bar (toggle bar) ###
fileButtons = Frame(root, bd=1, relief="raised")
fileButtons.pack(side=LEFT, fill=Y)

# add an Options toggle frame to side bar
options = ToggledFrame(fileButtons, width=1000, text='Options', relief="raised")
options.pack(side=TOP, fill=X)
# add buttons under Options
Button(options.sub_frame, text="Browse...", command=browseImage).pack(side=TOP, padx=2, pady=2, fill=X)
Button(options.sub_frame, text="Save Image", command=lambda: saveImage(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(options.sub_frame, text="Show Original", command=lambda: originalImage()).pack(side=TOP, padx=2, pady=2, fill=X)

# add an Enhance toggle frame to side bar
enhance = ToggledFrame(fileButtons, text='Enhancements', relief="raised")
enhance.pack(side=TOP, fill=X)
# add buttons under Enhancements
Button(enhance.sub_frame, text="Histogram Equalization", command=lambda: histoEqualizer(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(enhance.sub_frame, text="Gamma Correction (Contrast)", command=lambda: gamma(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(enhance.sub_frame, text="Averaging Mask", command=lambda: averageMask(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(enhance.sub_frame, text="Median Filtering", command=lambda: medianFilter(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(enhance.sub_frame, text="Gaussian Mask", command=lambda: gaussianMask(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(enhance.sub_frame, text="Sharpen", command=lambda: sharpen(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(enhance.sub_frame, text="Dilation", command=lambda: dilation(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(enhance.sub_frame, text="Erosion", command=lambda: erosion(image)).pack(side=TOP, padx=2, pady=2, fill=X)
# add Gamma scale, set to 3 as default
Label(enhance.sub_frame, text="Gamma (for Contrast): ", font='Helvetica 12 bold').pack(side=TOP, padx=2)
g = Scale(enhance.sub_frame, from_=0.0, to=4, resolution=0.5, tickinterval=1, font="Helvetica 9", orient=HORIZONTAL)
g.pack(side=TOP, padx=2, pady=2)
g.set(2.0)
# add Erosion/Dilation scale, set to 3 as default
Label(enhance.sub_frame, text="Erosion/Dilation Kernel: ", font='Helvetica 12 bold').pack(side=TOP, padx=2)
kern = Scale(enhance.sub_frame, from_=1, to=9, tickinterval=2, font="Helvetica 9", orient=HORIZONTAL)
kern.pack(side=TOP, padx=2, pady=2)
kern.set(3)
# add radio buttons for Smoothing kernel size, set default to 3
x = 3
label = Label(enhance.sub_frame, text="Smoothing Kernel Size: ", font='Helvetica 12 bold').pack(side=TOP, padx=2, pady=2)
Radiobutton(enhance.sub_frame, text="9X9", variable=x, value=9, command=lambda: setX(9)).pack(side=RIGHT, padx=2, pady=2)
Radiobutton(enhance.sub_frame, text="5x5", variable=x, value=5, command=lambda: setX(5)).pack(side=RIGHT, padx=2, pady=2)
kernel3 = Radiobutton(enhance.sub_frame, text="3x3", variable=x, value=3, command=lambda: setX(3))
kernel3.pack(side=RIGHT, padx=2, pady=2)
kernel3.select()

# add a smoothing toggle frame to side bar
convert = ToggledFrame(fileButtons, text='Binary Conversion', relief="raised")
convert.pack(side=TOP, fill=X)
Button(convert.sub_frame, text="Binary Conversion", command=lambda: binary(imageEdit)).pack(side=TOP, padx=2, pady=2, fill=X)
# add thresholding scale for binary thresholding, set min to 150 and max to 255 as default
Label(convert.sub_frame, text="Binary Conversion Thresholding", font='Helvetica 12 bold').pack(side=TOP, padx=2)
Label(convert.sub_frame, text="Min Threshold: ", font='Helvetica 12').pack(side=TOP, padx=2)
ThreshMin = Scale(convert.sub_frame, from_=0, to=255, tickinterval=255, font="Helvetica 10", orient=HORIZONTAL)
ThreshMin.pack(side=TOP, padx=2, pady=2)
ThreshMin.set(150)
Label(convert.sub_frame, text="Max Threshold: ", font='Helvetica 12').pack(side=TOP, padx=2)
ThreshMax = Scale(convert.sub_frame, from_=0, to=255, tickinterval=255, font="Helvetica 10", orient=HORIZONTAL)
ThreshMax.pack(side=TOP, padx=2, pady=2)
ThreshMax.set(255)

# add an Edge Detection toggle frame to side bar
edge = ToggledFrame(fileButtons, text='Edge Detection', relief="raised")
edge.pack(side=TOP, fill=X)
# add buttons under edge detection
Button(edge.sub_frame, text="Sobel (Vertical edges)", command=lambda: edgeSobelX(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(edge.sub_frame, text="Sobel (Horizontal edges)", command=lambda: edgeSobelY(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(edge.sub_frame, text="Canny Edges", command=lambda: edgeCanny(image)).pack(side=TOP, padx=2, pady=2, fill=X)
Button(edge.sub_frame, text="Laplacian Edges", command=lambda: laplacian(image)).pack(side=TOP, padx=2, pady=2, fill=X)
# add radio buttons for Sobel kernel size, set default to 3
s = 3
label = Label(edge.sub_frame, text="Sobel Kernel Size: ", font='Helvetica 12 bold').pack(side=TOP, padx=2, pady=2)
Radiobutton(edge.sub_frame, text="9X9 ", variable=s, value=9, command=lambda: setS(9)).pack(side=RIGHT, padx=2, pady=2)
Radiobutton(edge.sub_frame, text="5x5 ", variable=s, value=5, command=lambda: setS(5)).pack(side=RIGHT, padx=2, pady=2)
kern3 = Radiobutton(edge.sub_frame, text="3x3 ", variable=s, value=3, command=lambda: setS(3))
kern3.pack(side=RIGHT, padx=2, pady=2)
kern3.select()

# add an Object Detection toggle frame to side bar
obj = ToggledFrame(fileButtons, text='Object Detection', relief="raised")
obj.pack(side=TOP, fill=X)
Button(obj.sub_frame, text="Labeled Objects", command=lambda: objects(image)).pack(side=TOP, padx=2, pady=2, fill=X)

# add a main frame
mainFrame = Frame(root, width=700, height=700)
mainFrame.pack()

# add a label to display information
editLabel = Label(mainFrame, text="Welcome! To begin Options -> Browse.\nTo view the dropdown menus, click the checkbox next to each option.", font="Helvetica 14 bold", fg="black")
editLabel.pack(side=TOP, pady=2)

# displays image
newImg = Label(mainFrame, width=900, height=900, bg='white')
newImg.pack(anchor=CENTER)

# label at the bottom of the screen
Label(root, text="When finished, File --> Exit...", bd=1, relief=SUNKEN, anchor=W).pack(side=BOTTOM, fill=X)

# keeps window running
root.mainloop()