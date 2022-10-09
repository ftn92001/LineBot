import random
from ..models import Photo

def get_beauty_imgs(amount):
    imgs = []
    texts = []
    for _ in range(amount):
        pk = random.randint(0, Photo.objects.count() - 1)
        photo = Photo.objects.get(pk=pk)
        imgs.append(photo.image_src)
        texts.append(photo.name)
    return imgs, texts