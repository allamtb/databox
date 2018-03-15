import string
from keras.models import load_model
from service.DataPrepare import  *
from sklearn.preprocessing import LabelBinarizer
import cv2
dp = DataPrepare()
(x_train, y_train), (x_test, y_test) = dp.getTrainAndTestData()
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = os.path.join(save_dir,'ocr_model.h5')
theModel = load_model(model_name)
theModel.summary()
encoder = LabelBinarizer().fit(list(string.ascii_lowercase + '0123456789'))
print(encoder.inverse_transform(theModel.predict(x_test[0:1])))
print(y_test[0:1])
array = np.array(x_test[0:1])[0]
cv2.imshow('img', array)
cv2.waitKey()
