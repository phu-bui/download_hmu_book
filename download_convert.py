import requests # to get image from the web
import shutil # to save it locally
import os
from PIL import Image
from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

def download_image(url, filename):
    r = requests.get(url, stream = True)
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')


def save_image(maxpage, book_name, imageFolderUrl):
    if not os.path.exists(book_name):
        os.makedirs(book_name)
    try:
        for i in range(1, maxpage+1):
            file_name = f'{book_name}/{i}.jpg'
            url = f'{imageFolderUrl}/00000{i}.jpg'
            if 9 < i < 100:
                url = f'{imageFolderUrl}/0000{i}.jpg'
            if 99 < i < 1000:
                url = f'{imageFolderUrl}/000{i}.jpg'
            download_image(url, file_name)
    except:
        return "Download Done!!!"


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/success/<book_name>')
def success(book_name):
    return 'Congratulations on successfully downloading the book: %s' % book_name

@app.route('/failed/<book_name>')
def failed(book_name):
    return 'Download the book: %s failed' % book_name

@app.route('/download', methods=['POST'])
def main():
    if request.method == 'POST':
        maxpage = request.form.get('maxpage')
        book_name = request.form.get('book_name')
        imageFolderUrl = request.form.get('imageFolderUrl')
        try:
            save_image(maxpage, book_name, imageFolderUrl)
            filename = f'{book_name}.pdf'
            number_file = len(os.listdir(book_name))
            image_list = []
            image1 = Image.open(f'{book_name}/1.jpg')
            image1.convert('RGB')
            for i in range(2, number_file+1):
                image = Image.open(f'{book_name}/{i}.jpg')
                image.convert('RGB')
                image_list.append(image)
            image1.save(filename, save_all=True, append_images=image_list)

            return redirect(url_for('success', book_name=book_name))
        except:
            return redirect(url_for('failed', book_name=book_name))
    else:
        return redirect(url_for('/'))




# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='127.0.0.1', port=5000)
