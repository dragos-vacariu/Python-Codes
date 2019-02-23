import random #used for getting random numbers
import urllib.request #using for processing url requests

def download_image(url):
    filename = "image_downloaded_by_web_crawler"
    filename += str(random.randrange(1,40))
#random.randrange(start,stop) -> gets a random number between start value and stop value.
    filename+=".jpg" #add the extension to the name
    urllib.request.urlretrieve(url,filename) #retrieve the content of the url.

url=input("Enter the URL for the image file: ")
print(url)
download_image(url)

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
