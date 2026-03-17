import warnings
warnings.filterwarnings('ignore')
from ultralytics import RTDETR

if __name__ == '__main__':
    model = RTDETR(r"E:\runs\train\MDT_exp\weights\best.pt") # select your model.pt path
    model.predict(source=r'G:\IOUvs',
                  conf=0.5,
                  project='runs/detect',
                  name='ONE_IOU_exp',
                  save=True,
                  visualize=False # visualize model features maps
                  )

