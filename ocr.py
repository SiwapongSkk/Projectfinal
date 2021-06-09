import cv2
import numpy as np
import pytesseract
import io

def read_img(img):

    width=700
    height=700
    y1=0
    y2=700
    x1=500
    x2=700
    #img=cv2.imread('IMG_25640601_111717.jpg') #read image

    img=cv2.resize(img,(width,height)) #resize image

    imgSAVE = img

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert roi into gray
    Blur=cv2.GaussianBlur(gray,(5,5),1) #apply blur to roi
    Canny=cv2.Canny(Blur,10,50) #apply canny to roi

    #Find my contours
    contours =cv2.findContours(Canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]

    #Loop through my contours to find rectangles and put them in a list, so i can view them individually later.
    cntrRect = []
    for i in contours:
            epsilon = 0.05*cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i,epsilon,True)
            if len(approx) == 4:
                #cv2.drawContours(img,cntrRect,-1,(0,255,0),2)
                #cv2.imshow('img Rect ONLY',img)
                cntrRect.append(approx)

                if len(contours) != 0:
                    # draw in blue the contours that were founded
    #                 cv2.drawContours(output, contours, -1, 255, 3)

                    # find the biggest countour (c) by the area
                    c = max(contours, key = cv2.contourArea)
                    x,y,w,h = cv2.boundingRect(c)

                    # draw the biggest contour (c) in green
    #                 cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

    img0 = cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),10)

    #cv2.imshow('img 000',img0)


    cropimg = img[y:y+h, x:x+w]

    #resized image
    width = 410
    height = 310
    dim = (width, height)
     
    # resize image
    resizedcropimg = cv2.resize(cropimg, dim, interpolation = cv2.INTER_AREA)

    returnresizedcropimg = cv2.imencode('.jpg', resizedcropimg)[1].tostring()

    #encoded_image_string = base64.b64encode(returnresizedcropimg)
    #print(returnresizedcropimg)



    #converting image into gray scale image

    resized = cv2.cvtColor(resizedcropimg, cv2.COLOR_BGR2GRAY)

    # converting it to binary image by Thresholding

    # this step is require if you have colored image because if you skip this part

    # then tesseract won't able to detect text correctly and this will give incorrect result

    resized = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


    #img99=cv2.imread('IMG_25640601_111717.jpg')
    text = pytesseract.image_to_string(resized, lang='tha+eng')


    #crop image 01 1 9209 00014 28 8 ID card number
    y= int(10.32*height*0.01)
    x=int(43.9*width*0.01)
    h=28
    w=150
    crop01 = resized[y:y+h, x:x+w]
    resultIDcardnumber = pytesseract.image_to_string(crop01, lang='tha+eng')
    resultIDcardnumber = resultIDcardnumber.replace("\n", "")
    resultIDcardnumber = resultIDcardnumber.replace("\f", "")

    #crop image 02 นาย ศิรพงษ์ กอบกิจ resultnamethai
    y=int(18.387*height*0.01)
    x=int(28.5365*width*0.01)
    h=40
    w=300
    crop01 = resized[y:y+h, x:x+w]
    resultnamethai = pytesseract.image_to_string(crop01, lang='tha+eng')
    resultnamethai = resultnamethai.replace("\n", "")
    resultnamethai = resultnamethai.replace("\f", "")

    #crop image 03 Mr. Siwapong resultnameeng
    y=int(28.387*height*0.01)
    x=int(39.02*width*0.01)
    h=30
    w=180
    crop01 = resized[y:y+h, x:x+w]
    resultnameeng = pytesseract.image_to_string(crop01, lang='eng')
    resultnameeng = resultnameeng.replace("\n", "")
    resultnameeng = resultnameeng.replace("\f", "")

    #crop image 04 Kopkit resultlastname
    y=int(35.483*height*0.01)
    x=int(43.9*width*0.01)
    h=30
    w=180
    crop01 = resized[y:y+h, x:x+w]
    resultlastname = pytesseract.image_to_string(crop01, lang='eng')
    resultlastname = resultlastname.replace("\n", "")
    resultlastname = resultlastname.replace("\f", "")

    #crop image 05 30 กย, 2541 resultbirthday
    y=int(43.548*height*0.01)
    x=int(43.17*width*0.01)
    h=25
    w=180
    crop01 = resized[y:y+h, x:x+w]
    resultbirthday = pytesseract.image_to_string(crop01, lang='tha')
    resultbirthday = resultbirthday.replace("\n", "")
    resultbirthday = resultbirthday.replace("\f", "")

    #crop image 06 30 Sep. 1998 resultbirthdayeng
    y=int(50*height*0.01)
    x=int(50*width*0.01)
    h=27
    w=120
    crop01 = resized[y:y+h, x:x+w]
    resultbirthdayeng = pytesseract.image_to_string(crop01, lang='eng')
    resultbirthdayeng = resultbirthdayeng.replace("\n", "")
    resultbirthdayeng = resultbirthdayeng.replace("\f", "")

    #crop image 07 ศาสนา พุทธ
    y=int(58.06*height*0.01)
    x=int(30*width*0.01)
    h=25
    w=180
    crop01 = resizedcropimg[y:y+h, x:x+w]
    resultreligion = pytesseract.image_to_string(crop01, lang='tha')
    resultreligion = resultreligion.replace("\n", "")
    resultreligion = resultreligion.replace("\f", "")

    #crop image 08 246 หมู่ที 1 ต.เขาไพร resultaddress
    y=int(64.516*height*0.01) #200
    x=int(20.5*height*0.01) #65
    h=28
    w=180
    crop01 = resizedcropimg[y:y+h, x:x+w]
    resultaddress = pytesseract.image_to_string(crop01, lang='tha')
    resultaddress = resultaddress.replace("\n", "")
    resultaddress = resultaddress.replace("\f", "")

    #crop image 09  resultresultlastaddress
    y=int(70.716*height*0.01) #200
    x=int(10.5*height*0.01) #65
    h=28
    w=180
    crop01 = resizedcropimg[y:y+h, x:x+w]
    resultresultlastaddress = pytesseract.image_to_string(crop01, lang='tha+eng')
    resultresultlastaddress = resultresultlastaddress.replace("\n", "")
    resultresultlastaddress = resultresultlastaddress.replace("\f", "")

    return {#"image_to_string":text,
     "เลขบัตรประจำตัวประชาชน":resultIDcardnumber, "ชื่อภาษาไทย":resultnamethai, "ชื่อภาษาอังกฤษ":resultnameeng,
     "นามสกุลภาษาอังกฤษ":resultlastname, "วันเกิดไทย":resultbirthday, "วันเกิดอังกฤษ":resultbirthdayeng
     , "ศาสนา":resultreligion, "address":resultaddress+resultresultlastaddress}, returnresizedcropimg

#  , file: bytes = File(...)


