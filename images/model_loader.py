import tensorflow as tf

def load_model(model_path="lung_disease_model_final.h5"):
    return tf.keras.models.load_model(model_path, compile=False)