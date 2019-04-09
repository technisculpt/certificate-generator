from PIL import Image, ImageDraw
from PIL import ImageFont
from PyPDF2 import PdfFileMerger, PdfFileReader
import os
import csv
import string

counter = 0

#generate student certs
def MakeCert(fname, lname, award, school):
    dir = r'C:\Users\mark\PycharmProjects\certs18'
    os.chdir(dir)
    # dimensions for A4 at 300 dpi
    size = (3508, 2480)
    height, width = size
    logo = Image.open("usydL.png")
    sig1 = Image.open("signature.jpg")
    # Image size measurement pre
    # mmWidth, mmHeight = mm1.size
    logoWidth, logoHeight = logo.size
    sigWidth, sigHeight = sig1.size
    # Image Sizing
    sigScale = 0.09
    logoScale = 0.1
    img = Image.new("RGB", (width, height), "white")
    logos = logo.resize(((int(logoWidth * ((height * logoScale) / logoHeight))), int(height * logoScale)),Image.ANTIALIAS)
    sig = sig1.resize(((int(sigWidth * ((height * sigScale) / sigHeight))), int(height * sigScale)), Image.ANTIALIAS)
    xPos = 0.165  # horizontal position on the page where all elements are drawn
    # Image Placement
    img.paste(logos, (int(width * 0.15), int(height * 0.09)))
    img.paste(sig, (int(width * 0.2), int(height * 0.781)))
    font = ImageFont.truetype("mrrobot.ttf", 175)
    font3 = ImageFont.truetype("TCM.TTF", 75)
    fontb = ImageFont.truetype("twbold.ttf", 85)
    font5 = ImageFont.truetype("TCM.ttf", 57)
    fontS = ImageFont.truetype("TCM.ttf", 45)
    d = ImageDraw.Draw(img)
    d.text((width * xPos, height * 0.29), "The University of Sydney", font=font3, fill=(0))
    d.text((width * xPos, height * 0.32), "Electrical and Information Engineering", font=font3, fill=(0))
    d.text((width * 0.21, height * 0.37), "The MadMaker", font=font, fill=(0))
    d.text((width * 0.19, height * 0.42), "Challenge 2018", font=font, fill=(0))
    d.text((width * xPos, height * 0.49), "This certificate is awarded to", font=font3, fill=(0))
    d.text((width * xPos, height * 0.54), fname + ' ' + lname, font=fontb, fill=(0))
    d.text((width * xPos, height * 0.59), "For achieving a " + award + " in the", font=font3, fill=(0))
    d.text((width * xPos, height * 0.62), "MadMaker Challenge 2018", font=font3, fill=(0))
    d.text((width * xPos, height * 0.7), "4th February 2019", font=font5, fill=(0))
    d.text((width * xPos, height * 0.875), "Associate Professor", font=fontS, fill=(0))
    d.text((width * xPos, height * 0.89), "Abelardo Pardo", font=fontS, fill=(0))
    d.text((width * xPos, height * 0.905), "Electrical & Information Engineering", font=fontS, fill=(0))
    os.chdir(r'C:\Users\mark\PycharmProjects\certs18\output' + '\\' + school)
    img.save(fname + lname + ".pdf")

#join all PDFs into 1 file for each school for printing
def pdf_cat(input_files, school):
    input_streams = []
    for i in input_files:
        input_streams.append(open(i, 'rb'))
    merger = PdfFileMerger()
    for pdf in input_streams:
        merger.append(PdfFileReader(pdf), 'rb')
    dir2 = r'C:\Users\mark\PycharmProjects\certs18\output'
    os.chdir(dir2)
    if not os.path.exists("ForPrinting"):
        os.makedirs("ForPrinting")  # make a folder for that school
    dir3 = r'C:\Users\mark\PycharmProjects\certs18\output\ForPrinting'
    os.chdir(dir3)
    merger.write(school+ "_merged.pdf")
    for f in input_streams:
        f.close()
    os.chdir(dir)

studentGrade = {} # student = dict{student_username : grade}

dir = r'C:\Users\mark\PycharmProjects\certs18'
os.chdir(dir)


with open('grades.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        studentGrade[row[3][0:2]+row[4][0:2]] = row[5]

errors = 0

with open('students.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
            if "@" not in row[2]:
                if row[1][0:2]+row[2][0:2] in studentGrade:
                    file1.write(row[0]+","+row[1]+","+row[2]+","+ str(studentGrade[row[1][0:2]+row[2][0:2]]) + '\n')
                else:
                    file1.write(row[0] + "," + row[1] + "," + row[2] + "," + "ERROR NO GRADE" + '\n')
                    errors += 1

            else:
                    file1 = open("output/"+row[2]+"_"+row[1]+".csv", "w")
                    file1.write(row[0] + "," + row[1] + "," + row[2] + '\n')

file1.close()

dir = r'C:\Users\mark\PycharmProjects\certs18\output'
os.chdir(dir)

#open a schools grade sheet, make certificates for students who scored >50
for root,dirs,files in os.walk(dir):
     for file in files:
        dir = r'C:\Users\mark\PycharmProjects\certs18\output'
        if file.endswith(".csv"):
            os.chdir(dir)
            with open(file, 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                firstLine = 1
                for row in spamreader:
                    if row:
                         if firstLine == 1: #make folder for school if it doesn't exist
                            school = row[0]
                            print school
                            if not os.path.exists(school):
                                os.makedirs(school)
                            dir = r'C:\Users\mark\PycharmProjects\certs18\output' + '\\' + school
                            os.chdir(dir)  # go into folder
                            firstLine = 0
                         else: # make student cert
                            grade = row[3]
                            if (grade=="ERROR NO GRADE"):
                                test=0
                            else:
                                test = float(grade)
                            if test > 0.50:
                                counter+=1
                                print counter
                                firstName = string.capwords(row[1])
                                lastName = string.capwords(row[2])
                                if test >= 0.85:
                                    award = "High Distinction"
                                if ((test >= 0.75) and (test < 0.85)):
                                    award = "Distinction"
                                if ((test >= 0.50) and (test < 0.75)):
                                    award = "Credit"
                                MakeCert(firstName, lastName, award, school)

                filesT = []
                cwd = os.getcwd()

                for root, dirs, files in os.walk(cwd):
                    for file in files:
                        if file.endswith(".pdf"):
                           filesT.append(file)
                pdf_cat(filesT,school)
