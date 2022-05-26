from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_mail(mail,code):
        email_body="You requested to login in Keep-Me-Fit.\n Your 4-digit code is: "+ str(code)
        subject="OTP to verify Keep-me-Fit "
        email= EmailMessage(
            subject=subject,
            body=email_body,to=[mail]
        )
        print("Sending email",mail)
        email.send()