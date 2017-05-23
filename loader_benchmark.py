import time
import numpy as np

start = 0
current = 0
num = 500

def concat(vector_list):
	size = len(vector_list)
	y = np.ndarray(shape=([5*size] +  vector_list[0].shape[1:]))
	for i in range(vector_list):
		for j in range(5):
			y[5*i + j] = vector_list[i][j]
	return y

def generate_next_batch(frames,batch_size,start, current):
	global images_train, text_train,num
	t = (5*num) // batch_size
	if current >= t or start == 0:
		start_time = time.time()
		images_train, text_train, start, current = load_batches(num, batch_size, start, current)
		print("Batch loading time:" + str(time.time() - start_time))
		current = 0
	batch_size = batch_size // 5
	images = images_train[current*batch_size:current*batch_size + batch_size]
	text = text_train[current*batch_size:current*batch_size + batch_size]
	current += 1
	return concat(images), concat(text), start, current

def load_batches(num,batch_size,start, current):
	image = "bouncing_data/image_%d.npy"%(start+1)
	text_file = "bouncing_data/text_%d.npy"%(start+1)
	t = [i for i in range(num)]
	img = [i for i in range(num)]
	for i in range(num):
		image = "bouncing_data/image_%d.npy"%(start+i+1)
		print(image)
		text_file = "bouncing_data/text_%d.npy"%(start+i+1)
		t2 = np.load(text_file)
		im2 = np.load(image)
		img[i] = im2
		t[i] = t2
	start += num
	if start > 50000:
		start = 0
		current = 0
	return im, t, start,current

def save_visualization(X,ep,nh_nw=(20,100),batch_size = 100, frames=20):
	h,w = 32,32
	Y = X.reshape(batch_size*frames, h,w,1)
	image = np.zeros([h*nh_nw[0], w*nh_nw[1],3])
	for n,x in enumerate(Y):
		j = n // nh_nw[1]
		i = n % nh_nw[1]
		image[j*h:j*h + h, i*w:i*w + w,:] = x
	scipy.misc.imsave(("bouncingmnist/sample_%d.jpg"%(ep+1)),image)


batch_size = 25

embedding_size = 96
text_embedding_size = 150
num_examples = 500
epoch = 200
frames = 20

start_time = time.time()
sample_video, sample_text,start, current = generate_next_batch(20,batch_size,start,current)
print("Total load time:" + str(time.time() - start_time))
save_visualization(sample_video,-1)