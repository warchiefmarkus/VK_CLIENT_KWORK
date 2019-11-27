# -*- coding: utf-8 -*-

import vk_api, sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication,    
QLabel, QLineEdit,  QPushButton, QTextEdit,
QFileDialog, QListWidget, QWidget)
from PyQt5.QtCore import pyqtSlot
 

class App(QWidget): 
    def __init__(self):
        super().__init__()
        self.title = 'VK'
        self.left = 200
        self.top = 200
        self.width = 900
        self.height = 480   
        
        self.photowall_counter=0
        
        self.loginVK()
        self.initUI()
        
    def loginVK(self):
        print("LOGING VK")
        self.vk_session = vk_api.VkApi('', '')
        self.vk_session.auth()        
        self.vk = self.vk_session.get_api()
        
        print("GET ALBUM LIST")
        #self.album_list        
        self.albums_list = self.vk.photos.getAlbums()      
            
        
    @pyqtSlot()
    def post(self):        
        self.attachments_photo=[]
        for item in self.listWidget.findItems('*', QtCore.Qt.MatchWildcard):
            self.attachments_photo.append(item.text())
        print(self.vk.wall.post(message=self.textbox.toPlainText(),attachment=','.join(self.attachments_photo)))
        
        self.photowall_counter=0
            
        
    @pyqtSlot()
    def addPhoto(self):  
        if (self.photowall_counter<3):
            print("ADD PHOTO")
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"SELECT PHOTO", "","All Files (*);;", options=options)
            if fileName:
                print(fileName)
                upload = vk_api.VkUpload(self.vk_session)
                photo = upload.photo_wall(fileName)        
                vk_photo_url = 'photo{}_{}'.format(
                    photo[0]['owner_id'], photo[0]['id']
                )        
                self.listWidget.addItem(vk_photo_url); 
                self.photowall_counter+=1
                #print(photo, '\nLink: ', vk_photo_url)
        else:
            print("MAX PHOTO UPLOADED")
            
    @pyqtSlot()
    def addPhotos(self):         
            print("ADD PHOTOS TO ALBUM")
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(self,"SELECT PHOTOS", "","All Files (*);;", options=options)
            if (files):
                print(files)               
                
                upload = vk_api.VkUpload(self.vk_session)
                photo = upload.photo(photos=files,album_id=self.current_album_id)    
                print(photo)
#                vk_photo_url = 'photo{}_{}'.format(
#                    photo[0]['owner_id'], photo[0]['id']
#                )        
#                #self.listWidget.addItem(vk_photo_url); 
                
    @pyqtSlot()
    def addAudios(self):         
            print("ADD AUDIOS TO ALBUM")
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file, _ = QFileDialog.getOpenFileName(self,"SELECT AUDIO FILE", "","All Files (*);;", options=options)
            if (file):
                print(file)             
                upload = vk_api.VkUpload(self.vk_session)
                res = upload.audio(audio=file,artist=self.artist.text(),title=self.titlea.text())    
                print(res)

    @pyqtSlot()
    def print_info(self):
        self.current_album_id = self.albumList.currentItem().text().split("~")[1]
        print (self.albumList.currentItem().text().split("~")[1])


        
     
    def initUI(self): 
        print("INIT UI")        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)    
        
        # POSTER
        # Create textbox
        self.textbox = QTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,80)
        
        # Create a post button
        buttonPost = QPushButton('POST', self)
        buttonPost.move(310,20)
        buttonPost.resize(40,80)        
        buttonPost.clicked.connect(self.post)
        
        # Create a add photo button
        buttonAddPhoto = QPushButton('ADD PHOTO', self)
        buttonAddPhoto.move(20,110)
        buttonAddPhoto.resize(280,20)        
        buttonAddPhoto.clicked.connect(self.addPhoto)
        
        #create photo list
        self.listWidget = QListWidget(self)
        self.listWidget.move(20,140)
        self.listWidget.resize(280,280)
        
        #UPLOAD PHOTO
        
        #create album list
        self.albumList = QListWidget(self)
        self.albumList.move(360,110)
        self.albumList.resize(280,310)
        
        self.albumList.currentItemChanged.connect(self.print_info)
        
        for item in self.albums_list['items']:
           self.albumList.addItem(item['title']+"~"+str(item['id']))
        
        # Create a add photos button
        buttonAddPhotos = QPushButton('ADD PHOTOS', self)
        buttonAddPhotos.move(360,20)
        buttonAddPhotos.resize(280,80)        
        buttonAddPhotos.clicked.connect(self.addPhotos)
        
        # Create a add photos button
        buttonAddAudio = QPushButton('ADD AUDIOS', self)
        buttonAddAudio.move(650,20)
        buttonAddAudio.resize(200,80)        
        buttonAddAudio.clicked.connect(self.addAudios)
        
        # Artist
        l1 = QLabel(self)	
        l1.setText("Artist")        
        l1.move(650,110)
        l1.resize(200,20)             
        self.artist = QLineEdit(self)
        self.artist.move(650,140)
        self.artist.resize(200,20)  
        
        # Title
        l2 = QLabel(self)	
        l2.setText("Title")        
        l2.move(650,170)
        l2.resize(200,20)             
        self.titlea = QLineEdit(self)
        self.titlea.move(650,200)
        self.titlea.resize(200,20) 
        
        
 
        self.show()
     
#if __name__ == '__main__':
app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
    
    

