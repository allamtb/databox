from util.RequestUtil import  *

def generateUserAgent():
    for i in range(100):
        print(generate_user_agent())

def generateCaptecha():
    for i in tqdm(range(200)):
        get_captcha()

if __name__ == '__main__':
   # generateUserAgent()
    generateCaptecha()