from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django.contrib import messages
from .tasks import gor_button

from selenium import webdriver

import time
from selenium.webdriver.common.keys import Keys
import mysql.connector
from mysql.connector import Error
from webdriver_manager.chrome import ChromeDriverManager

# Create your views here.
def form(request):
    # form düzenle req olarak
    #formu göstercek
    return render(request,'form.html',{})
def index(request):
    #ana sayfam
    return render(request,'index.html',{})
def hata(request):
    return render(request,'404.html',{})

def sonuc(request):
    #gelen veri db ye kaydetmeden önce burdaalınıp kontrol edilcek
    #hata gelirse hata 404 sayfaına 
    # değilse db ye kaydet diğer işlem fonksiyonuna
    #orda hata gelirse 404 yoksa selenium devam iş bitince sonuca
    if request.method == 'POST':
        username=request.POST.get('username')
        parola=request.POST.get('password')
        try:
            try:


                connection = mysql.connector.connect(host='127.0.0.1',
                                                                user='root',
                                                                
                                                                password='elso3306',
                                                                database='labinstagram',
                                                                buffered=True)
                cursor=connection.cursor()    
            except Error :
                return render(request,'404.html',{}) # bunlarıredirect yap
            sql="INSERT INTO  users (name,password) VALUES ('{}','{}');".format(username,parola)
            cursor.execute(sql)
            connection.commit()   
        except Error :
            return render(request,'404.html',{}) # bunlarıredirect yap
        return render(request,'sonuc.html',{'username':username,'parola':parola})
    else :
        return render(request,'404.html',{})  
    #return render(request,'sonuc.html',{'username':username,'password':password})

    #kayıttamam ve doğruysa seleniuma yolla değilse  404 verdir button ile forma gitsin 
    #password düzeltilmeli
    

##şimdilik kayıt atana kadar ki kısım 
# sonra selenium fonksiyonuunu çalıştır
# sonra celery

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            userr = authenticate(username=username, password=raw_password)
            login(request, userr)
        
            try:
                try:


                    connection = mysql.connector.connect(host='127.0.0.1',
                                                                    user='root',
                                                                    
                                                                    password='elso3306',
                                                                    database='labinstagram',
                                                                    buffered=True)
                    cursor=connection.cursor()    
                except Error :
                    return render(request,'404.html',{}) # bunlarıredirect yap
                sql="INSERT INTO  users (name,password) VALUES ('{}','{}');".format(username,raw_password)
                cursor.execute(sql)
                connection.commit()   
            except Error :
                return render(request,'404.html',{}) # bunlarıredirect yap

            return render(request,'sonuc.html',{'userr':userr})
        
            
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def gorbutton(request,username , id):
    
    task = gor_button.delay(username , id)
    return render(request,'sonbuton.html',{'task_id':task.task_id})
    

    # gelen kullanıcı parola ile şimdilik selenium ile giriş yapıp çıksın
    #ilk olarak dbden bu kullanıcıya ait bilgileri mysqlden çekelim
    # sonra selenium kodlarım çalışsın
'''
    class Instagram:
        def __init__(self,name,passw):
            self.browser=webdriver.Chrome(ChromeDriverManager().install())
            self.browser.set_window_size(900,900)
            self.name=name
            self.passw=passw
        def signIn(self):
            self.browser.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
    
            nameInput=self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
            passwordInput=self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")
            nameInput.send_keys(self.name)
            passwordInput.send_keys(self.passw)
            passwordInput.send_keys(Keys.ENTER)
            time.sleep(2)
        
    
        def kapatma(self):

            self.browser.get("https://www.instagram.com/"+self.name)
            time.sleep(2)
            self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/div/button").click()

            self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div/button[9]").click()
            time.sleep(2)
            self.browser.quit()
        
        
    
    
    def db_delete():
        try:

            connection=mysql.connector.connect(host='127.0.0.1',
                                                            user='root',
                                                            
                                                            password='elso3306',
                                                            database='labinstagram',
                                                            buffered=True)
            cursor=connection.cursor()
            
        except Error as e:
            print("Error while connecting to MySQL", e)   
        time.sleep(2)
            #following tablosu silinecek follow tablosu silinecek 
        cursor.execute("DELETE FROM following")
        connection.commit()
        cursor.execute("DELETE FROM followers")
        connection.commit()
        cursor.execute("DELETE FROM notfollow")
        connection.commit()
        cursor.execute("DELETE FROM notfollowing")
        connection.commit()
        cursor.close()

 
   
   
   
   
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
        cursor=connection.cursor()
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    sql="SELECT password FROM users WHERE name = '{}';".format(username)
    cursor.execute(sql)
    m=cursor.fetchone()
    connection.commit()
    password= m[0]
    #çağırmaişlemleri ve fonksiyonu çalıştırma

    instagram=Instagram(username,password)
    try:
        instagram.signIn()
    except:
        if instagram.browser != None:
            instagram.browser.quit()
    time.sleep(2)
    try:
        instagram.kapatma()
    except:
        instagram.browser.quit()
    
    # seleniumile işlmeler tamam db ye yazmış olacak diğer notları da db ye yazacak gösterilecek olanları alalım sonrası sil    
    
    #en son almaişlemleri followers following notfollow not following

    #sil dbleri ve postu 
    try:
        post=get_object_or_404(User,id=id)
    #silincek postu getiriyoruz
        post.delete()
        messages.success(request, "The user is deleted")            

    except Error: 
        return render(request, '404.html')
    
    db_delete()

    
    return render(request,'finish.html',{})

 
'''


def deleteuserbutton(request,id):
    try:
        post=get_object_or_404(User,id=id)
    #silincek postu getiriyoruz
        post.delete()
        messages.success(request, "The user is deleted")            

    except Error: 
        return render(request, '404.html')
    #return render(request, 'signup.html',{'form':form}) 
    return redirect("/signup")

'''    
def deneme(request,username):
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
        cursor=connection.cursor()
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    sql="SELECT password FROM users WHERE username = '{}';".format(username)
    cursor.execute(sql)
    m=cursor.fetchone()
    connection.commit()
    password= m[0]
    dosya_name= username + ".txt"
    dosya= open(dosya_name,"w")
    yaz = "username: "+ username + "\n password: "+password
    dosya.write(yaz)
'''


'''
name="sinems_hn"
password="fenerFB1.wert"
'''

