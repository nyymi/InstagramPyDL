import urllib.request
import urllib.parse
import json
import os

# Main function
def main():
    # Request target information as keyboard input
    target_username = input("Enter instagram target user: ")

    # GET request for JSON data about target media
    request = urllib.request.Request("http://instagram.com/" + target_username + "/media/")
    response = urllib.request.urlopen(request)
    media = json.loads(response.read().decode(response.info().get_param("charset") or "utf-8"))

    # Find all URLs to standard res images
    num_items = len(media["items"])
    media_urls_url = []
    media_urls_lst = []
    for i in range(num_items):
        media_urls_url.append(media["items"][i]["images"]["standard_resolution"]["url"])
        parsed_url = urllib.parse.urlparse(media_urls_url[i])
        media_urls_url[i] = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        media_urls_lst.append(media_urls_url[i].split("/"))

        # Parse things that aren't native resolution
        # Getting native res image requires only slicing the URI a bit
        output = ""
        n = len(media_urls_lst[i])
        if n > 6:
            result = ""
            for j in range(n):

                # Skip resolution info
                if j == 4 or j == 5:
                    continue

                # Rebuild URL
                result += media_urls_lst[i][j]
                result += "/"

            output = result[:len(result) - 1]
        else:
            output = media_urls_url[i]

        path = "./downloads/" + target_username + "/"
        output_split = output.split("/")

        try:
            os.makedirs(path)
        except:
            pass

        print("Downloading: " + output)
        urllib.request.urlretrieve(output, path + output.split("/")[len(output_split) - 1])


# Function hooks
if __name__ == "__main__":
    main()