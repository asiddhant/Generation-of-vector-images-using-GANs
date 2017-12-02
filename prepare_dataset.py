from keras.preprocessing import image
from vgg16 import VGG16
import numpy as np 
from keras.applications.imagenet_utils import preprocess_input	
import pickle
import os

def load_image(path):
    img = image.load_img(path, target_size=(224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return np.asarray(x)

def load_encoding_model():
	model = VGG16(weights='imagenet', include_top=True, input_shape = (224, 224, 3))
	return model

def get_encoding(model, img):
	global counter
	image = load_image(img)
	pred = model.predict(image)
	pred = np.reshape(pred, pred.shape[1])
	return pred

sketch_dir='sketch_sml'
image_dir='pixel_images'
clusterinfo=pickle.load(open('clusters.p','rb'))

categories=[]
with open('categories.txt') as f:
	for line in f:
		categories+=[line.strip()]

image_embed={}
model=load_encoding_model()
for category in categories:
	catimagedir=os.path.join(image_dir,category)
	for img in os.listdir(catimagedir):
		inputimage=os.path.join(catimagedir,img)
		image_embed[img.split('.')[0]]=get_encoding(model,inputimage)
	print category +'Done'
pickle.dump(image_embed,open('image_embed.p','wb'))

final_dataset=[]
for category in categories:
	inputfile=os.path.join(sketch_dir,'sketchrnn%2F'+category+'.npy')
	sketches=np.load(inputfile)
	for i in range(len(sketches)):
		cat_num = category+'%'+str(sketches[i,1]).zfill(5)
		corrimage=category+'%'+str(clusterinfo[category][cat_num]).zfill(2)
		final_dataset+=[[sketches[i,0],image_embed[corrimage]]]
pickle.dump(final_dataset,open('final_dataset.p','wb'))

