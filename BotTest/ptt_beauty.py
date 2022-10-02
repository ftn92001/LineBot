import random
from .models import Photo

def get_beauty_img():
    pk = random.randint(0, Photo.objects.count() - 1)
    photo = Photo.objects.get(pk=pk)
    return photo.image_src, photo.name

def get_beauty_imgs():
    imgs = []
    texts = []
    for _ in range(10):
        pk = random.randint(0, Photo.objects.count() - 1)
        photo = Photo.objects.get(pk=pk)
        imgs.append(photo.image_src)
        texts.append(photo.name)
    return imgs, texts