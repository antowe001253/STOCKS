import time
import pyautogui
def use_mouse_to_run_stocks_scanner():
    pyautogui.moveTo(150, 150)
    pyautogui.click()
    pyautogui.press('f5')
    print(""*10,"[ Stock Scanner has been restrated ]",""*10)
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)  
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        print ('successfully sent the mail')
        return 1
    except:
        print ("failed to send mail")
        return 0
number_of_time_restarted = 0    
while(1):
    time.sleep(60)
    try:
        
        f = open("cheker.txt","r")
        message = f.read()
        f.close()
        print(len(message),end=" ")
        if(len(message)<=0): 
            print("Number of time -> ", number_of_time_restarted+1)
            print(time.strftime("%b %d, %Y---%H:%M:%S "))
            if number_of_time_restarted>5: 
                use_mouse_to_run_stocks_scanner() 
                print("****************************Restarted ...")
                number_of_time_restarted=0
				
            validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com","********************APP STOPPED RUNNING","APP STOPPED RUNNING")
            number_of_time_restarted+=1
        else:  number_of_time_restarted=0
        f = open("cheker.txt","w").close()
    except:
        print("Not runing")
        validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com","===== [APP STOPPED RUNNING] =====","APP STOPPED RUNNING")
                                        
