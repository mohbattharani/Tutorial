import numpy as np
from imantics import Polygons, Mask, Category, Image
import cv2, glob, os, warnings, json
#from gluoncv.data.transforms import mask as tmask

def resize_polygon (points, height_ratio =1, width_ratio =1):
    points = np.multiply (points, [height_ratio, width_ratio])
    return points
    
def resize_polygons (points, height_ratio =1, width_ratio =1):
    for i in range(len(points)):
        points[i] = np.multiply (points[i], [height_ratio, width_ratio])
    return points

def resize_mask(mask, height, width ):
    old_height, old_width, c = mask.shape
    new_mask =  np.zeros((height, width, c))
    for i in range(0, c):
        color = [0,0,0]
        color[i] = i+1
        polygons = Mask(mask[:,:,i]).polygons()
        #print (polygons.points)
        for points in polygons.points:
            points = (resize_polygon(points, height_ratio = int(height/old_height), width_ratio = int(width/old_width)))
            cv2.fillPoly(new_mask,pts= [points],color=tuple(color))
    return new_mask

def set_dataset_name (dataset, name = 'Example'):
    for i in range(len(dataset)):
        dataset[i].dataset = 'Trash'
    return dataset

def add_annotations (dataset, dir_mask):
    for i in range(len(dataset)):
        path_mask = os.path.join (dir_mask, dataset[i].path.split('/')[-1])
        height = dataset[i].height
        width = dataset[i].width
        mask = cv2.imread(path_mask)
        polygons = Mask(mask[:,:,1]).polygons()
        #print (type(polygons.points), polygons.points)
        points = resize_polygons (polygons.points, height_ratio =2, width_ratio =2)
        #mask = resize_mask(mask, height, width)
        dataset[i].add(Polygons(points), category=Category("garbage"))
        print (path_mask, mask.shape)
    return dataset

def save_dataset(dataset, dir_ann, style = 'coco'):
    for data in dataset:
        path = os.path.join (dir_ann, data.path.split('/')[-1].split('.')[0])
        if (style == 'coco'):
            data.save(path+'.json', style=style)
        elif (style == 'voc'):
            data.save(path+'.xml', style=style)
        else:
            warnings.warn("Warning: Please select right style for dataset.")

def save_dataset_(dataset, dir_ann, style = 'coco'):
    annotations = []
    images = []
    id = 0
    for data in dataset:
        coco_json = data.export(style='coco')
        image = coco_json['images'][0]
        image['id'] = id
        id += 1
        images.append (image)
        annotations.append (coco_json['annotations'])
    print (images)
    
    coco_json['images'] = images    
    coco_json['annotations'] = annotations

    file_path = os.path.join (dir_ann, 'annotations.json')
    with open(file_path, 'w') as fp:
        json.dump(coco_json, fp)



images_path = 'mask_trash/'
mask_path = 'annotation_rgb'
save_annotation_path = 'coco_ann'
dataset = Image.from_folder(images_path)
# optional: add name of the dataset 
dataset = set_dataset_name (dataset, 'Trash')
dataset = add_annotations (dataset, mask_path)
save_dataset_ (dataset, save_annotation_path, style = 'coco')