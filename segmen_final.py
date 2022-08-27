
import cv2 #cv = computer vison
from PIL import Image
import matplotlib.pyplot as plt
import pytesseract as p
import numpy as np
###################################################################
def read_image(path):
    img = cv2.imread(path)
    img_copy = cv2.imread(path)
    #cv2.imshow('input Image',img)
    height, width, channels = img.shape
    #print(height, width, channels)
    return height, width, channels,img, img_copy
###################################################################
def gray_scale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray scale', gray)
    return gray

###################################################################
def find_edges(gray):
    edges = cv2.Canny(gray, 5000, 5000, apertureSize=7)
    #cv2.imshow('Edges',edges)
    return edges
###################################################################
def hough_lines(img,edges):
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200, None, 0, 0)
    upper_x = []
    lower_x = []
    upper_y = []
    lower_y = []
    for line in lines:
        rho,theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        upper_x.append(x1)
        lower_x.append(x2)
        upper_y.append(y1)
        lower_y.append(y2)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
        #cv2.imshow(img)
    upper_x.sort()
    lower_x.sort()
    #print(upper_x)
    #print(lower_x)
    #print(upper_y)
    #print(lower_y)
    cv2.imshow('Segmented Image',img)
    return img,upper_x,lower_x
###################################################################
def cropping(img_copy,upper_x,lower_x,height,width):
    croped_images = []
    k = 1
    prev = 0
    for i in range(len(upper_x)):
      up_x = upper_x[i]
      low_x = lower_x[i]
      maxi = max(up_x, low_x)
      dif = maxi-prev
      if dif >50:
        cropped = img_copy[0:height,prev:maxi]
        #cv2.imshow('Segmented {num}'.format(num = k),cropped)
        croped_images.append(cropped)
      prev = maxi
      k = k+1
    end_line = width-maxi
    if end_line >50:
      cropped = img_copy[0:height,maxi:width]
      #cv2.imshow('Cropped Image',cropped)
      croped_images.append(cropped)
    return croped_images
def show_croped_images(images):
    k = 1 
    for img in images:
        cv2.imshow('Cropped Image {num}'.format(num = k),img)
        cv2.imwrite('Cropped Image {num}.jpg'.format(num = k),img)
        k = k+1
###################################################################

def text_extraction(croped_images):
    text = []
    #is_prev = 0
    #is_prev_prev = 0
    for i in range(len(croped_images)):
        crop_img = croped_images[i]
        #cv2.imshow('Cropped Image',crop_img)
        t=p.image_to_string(crop_img,lang='eng', config='--psm 6 --oem 3')
        #print(t)
        text.append(t)
    text_splited = []
    for i in range(len(text)):
        s = text[i].replace('\n',' ')
        lis = list(s.split(" "))
        text_splited.append(lis)
    #print(text_splited)
    index = 0
    text = []
    flag2 = 0
    book_num = 0
    for book in text_splited:
        for book_text in book:
            flag = book_text.isnumeric()
            if flag is True and len(book_text)==4:
                flag2 = flag2+1
                if flag2 == 2:
                    index = book.index(book_text)
                    text.append(text_splited[book_num][index-3])
                    text.append(text_splited[book_num][index-2])
                    text.append(text_splited[book_num][index-1])
                    text.append(text_splited[book_num][index])
        book_num = book_num+1
        flag2 = 0
    genre = ['005.14', '629.892']
    genre_inex = 0
    genres_of_books = []
    num_of_books = len(text)/4
    text = np.array((np.array(text)).reshape(int(num_of_books),4))
    #print(text)
    for book in text:
        genres_of_books.append(book[0])
    #print(genres_of_books)
    common_genre = list(set(genre).intersection(set(genres_of_books)))
    for book in text:
        book[0] = common_genre[0] #############################
    return text
##########################################  Check books are in order   #############################
def check_in_order(text):
    genre = []
    auther = []
    year = []
    numbr = []
    for book in text:
        genre.append(book[0])
        auther.append(book[1])
        year.append(book[2])
        numbr.append(book[3])
    length = len(auther)
    un_sorted_flag = 0
    for i in range(length-1):
        a1 = auther[i]
        a2 = auther[i+1]
        if a1 < a2:
            continue
        elif a1 > a2:
            un_sorted_flag = 1
            print("Following is not in order")
            print("Book Author ::" , a1, "\nyear ::",y1,"\index:: ",nmbr[i])
            break
        elif a1 == a2:
            y1 = year[i]
            y2 = year[i+1]
            if y1<y2:
                continue
            elif y1>y2:
                un_sorted_flag = 1
                print("Following is not in order")
                print("Book Author ::" , a1, "\nyear ::",y1,"\index:: ",nmbr[i])
                break
            elif y1==y2:
                n1 = numbr[i]
                n2 = numbr[i+1]
                if n1<n2:
                    continue
                elif n1>n2:
                    un_sorted_flag = 1
                    print("Following is not in order")
                    print("Book Author ::" , a1, "\nyear ::",y1,"\index:: ",nmbr[i])
                    break
    return un_sorted_flag

def spine_extraction(path):
    height,width,channels,img,img_copy = read_image(path)
    cv2.imshow('input Image',img)
    cv2.imwrite('Input Image.jpg',img)
    gray = gray_scale(img)
    cv2.imshow('Gray Scale',gray)
    cv2.imwrite('Gray Scale.jpg',gray)
    edges = find_edges(gray)
    cv2.imshow('Edges',edges)
    cv2.imwrite('Edges.jpg',edges)
    segmented,upper_x,lower_x = hough_lines(img,edges)
    cv2.imshow('Segmented Image',segmented)
    cv2.imwrite('Segmented Image.jpg',segmented)
    croped_images = cropping(img_copy,upper_x,lower_x,height,width)
    return croped_images
"""
def find_position(books, book):
    genre = []
    auther = []
    year = []
    numbr = []
    if books[0][0] != book[0]:
        print("At wrong path")
        return -1
    for label in books:
        genre.append(book[0])
        auther.append(book[1])
        year.append(book[2])
        numbr.append(book[3])
        
    for i in range(len(auther)-1):
        a1 = auther[0]
        a2= auther[1]
        
    for label in books:
        if label[0] is book[0]:
            if label[1] > book[1]:
"""                
def main():
    path = "pic4.jpg"
    croped_images = spine_extraction(path)
    show_croped_images(croped_images)
    text = text_extraction(croped_images)
    print(text)
    flag = check_in_order(text)
    if flag == 0:
        print("BOOKS are in order")
    else:
        print("BOOKS are NOT in order")
    
       
main()
