import dropbox



class Dropbox:
    def __init__(self, access_token):
        self.access_token = access_token
        self.client = None
        self.configure()

    def configure (self):
        self.client = dropbox.Dropbox(self.access_token)


    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2 """
        with open(file_from, 'rb') as f:
            self.client.files_upload(f.read(), file_to)

def main():
    access_token = '***************'

    DBox = Dropbox(access_token)

    file_from = 'uploadDropBox.py'
    file_to = '/uploadDropBox.py'  

    # Upload file
    DBox.upload_file(file_from, file_to)

if __name__ == '__main__':
    main()