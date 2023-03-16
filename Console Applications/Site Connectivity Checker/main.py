import urllib.request as urllib

def main(url):
    print("Checking connectivity...")

    try:
        response = urllib.urlopen(url)
        print("Connected to", url, "successfully")
        print("The response code was", response.getcode())
    except:
        print("Connection failed")

print("This is a site connectivity checker program")
input_url = input("Input the url of the site you want to check: ")

main(input_url)