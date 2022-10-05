import requests # to get image from the web
import shutil # to save it locally
import os
from PIL import Image


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

def main(maxpage, book_name, imageFolderUrl):
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

    print('Done')


if __name__ == '__main__':
    main(149, 'chua_rang_noi_nha_2', 'http://thuvien.hmu.edu.vn/pages/cms/TempDir/books/205559b7-a16a-4584-bfb5-1d687d7d809e/2022/01/25/202201251559-d7ec760e-9a57-40aa-a88d-05769107c150/FullPreview')
