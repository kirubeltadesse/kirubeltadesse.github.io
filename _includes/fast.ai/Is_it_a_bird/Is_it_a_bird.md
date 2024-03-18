```python
from fastcore.all import *
from fastbook import search_images_ddg
```


```python
def search_images(term, max_images=30):
    print(f"Searching for '{term}'")
    return search_images_ddg(term, max_images)
```


```python
urls = search_images('bird photos', max_images=1)
urls[0]
```

    Searching for 'bird photos'

    'https://chilternchatter.com/wp-content/uploads/2018/01/RED-Bird.jpg'



## Downloading image using the URL 


```python
from fastdownload import download_url
dest = 'bird.jpg'
download_url(urls[0], dest, show_progress=False)

from fastai.vision.all import *
im = Image.open(dest)
im.to_thumb(256,256)
```




    
![png](/assets/img/fast.ai/birds/output_6_0.png)
    


```python
# hide
```


```python
download_url(search_images('forest photos', max_images=1)[0], 'forest.jpg', show_progress=False)
Image.open('forest.jpg').to_thumb(256,256)
```

    Searching for 'forest photos'





    
![png](/assets/img/fast.ai/birds/output_8_1.png)
    




```python
searches = 'forest', 'bird'
path = Path('bird_or_not')
from time import sleep
```


```python
for o in searches:
    dest = (path/o)
    dest.mkdir(exist_ok=True, parents=True)
    download_images(dest, urls=search_images(f'{o} photo'))
    sleep(2)
    download_images(dest, urls=search_images(f'{o} sun photo'))
    sleep(1)
    download_images(dest, urls=search_images(f'{o} shade photo'))
    sleep(2)
    resize_images(path/o, max_size=400, dest=path/o)
```

    Searching for 'forest photo'
    Searching for 'forest sun photo'
    Searching for 'forest shade photo'
    Searching for 'bird photo'
    Searching for 'bird sun photo'
    Searching for 'bird shade photo'


## Step 2: Train our model 


```python
failed = verify_images(get_image_files(path))
failed.map(Path.unlink)
len(failed)
```




    6



### Using the DataLoaders


```python
dls = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=[Resize(192, method='squish')]
).dataloaders(path, bs=32)
```


```python
dls.show_batch(max_n=6)
```


    
![png](/assets/img/fast.ai/birds/output_15_0.png)
    



```python
learn = vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(3)
```

    Downloading: "https://download.pytorch.org/models/resnet18-f37072fd.pth" to /home/kirubel/.cache/torch/hub/checkpoints/resnet18-f37072fd.pth
    100%|██████████| 44.7M/44.7M [00:01<00:00, 44.1MB/s]




<style>
    /* Turns off some styling */
    progress {
        /* gets rid of default border in Firefox and Opera. */
        border: none;
        /* Needs to be in here for Safari polyfill so background images work as expected. */
        background-size: auto;
    }
    progress:not([value]), progress:not([value])::-webkit-progress-bar {
        background: repeating-linear-gradient(45deg, #7e7e7e, #7e7e7e 10px, #5c5c5c 10px, #5c5c5c 20px);
    }
    .progress-bar-interrupted, .progress-bar-interrupted::-webkit-progress-bar {
        background: #F44336;
    }
</style>




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>epoch</th>
      <th>train_loss</th>
      <th>valid_loss</th>
      <th>error_rate</th>
      <th>time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>0.349523</td>
      <td>0.017476</td>
      <td>0.012903</td>
      <td>00:42</td>
    </tr>
  </tbody>
</table>




<style>
    /* Turns off some styling */
    progress {
        /* gets rid of default border in Firefox and Opera. */
        border: none;
        /* Needs to be in here for Safari polyfill so background images work as expected. */
        background-size: auto;
    }
    progress:not([value]), progress:not([value])::-webkit-progress-bar {
        background: repeating-linear-gradient(45deg, #7e7e7e, #7e7e7e 10px, #5c5c5c 10px, #5c5c5c 20px);
    }
    .progress-bar-interrupted, .progress-bar-interrupted::-webkit-progress-bar {
        background: #F44336;
    }
</style>




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>epoch</th>
      <th>train_loss</th>
      <th>valid_loss</th>
      <th>error_rate</th>
      <th>time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>0.055393</td>
      <td>0.066558</td>
      <td>0.012903</td>
      <td>00:50</td>
    </tr>
    <tr>
      <td>1</td>
      <td>0.044839</td>
      <td>0.027144</td>
      <td>0.012903</td>
      <td>00:52</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.026491</td>
      <td>0.048613</td>
      <td>0.012903</td>
      <td>00:49</td>
    </tr>
  </tbody>
</table>


## Step 3: Use our model (and build your own!)


```python
is_bird,_,probs = learn.predict(PILImage.create('bird.jpg'))
print(f"This is a: {is_bird}.")
print(f"Probability it's a bird: {probs[0]:.4f}")
```



<style>
    /* Turns off some styling */
    progress {
        /* gets rid of default border in Firefox and Opera. */
        border: none;
        /* Needs to be in here for Safari polyfill so background images work as expected. */
        background-size: auto;
    }
    progress:not([value]), progress:not([value])::-webkit-progress-bar {
        background: repeating-linear-gradient(45deg, #7e7e7e, #7e7e7e 10px, #5c5c5c 10px, #5c5c5c 20px);
    }
    .progress-bar-interrupted, .progress-bar-interrupted::-webkit-progress-bar {
        background: #F44336;
    }
</style>







    This is a: bird.
    Probability it's a bird: 1.0000

