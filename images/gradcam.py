import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import Model

def make_gradcam_heatmap(img_array, model, last_conv_layer_name="top_conv", pred_index=None):
    # Create a model that maps the input image to the activations
    # of the last conv layer and the final predictions
    grad_model = Model([
        model.inputs,
        model.get_layer(last_conv_layer_name).output
    ], model.output)

    # Compute the gradient of the top predicted class for the input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])  # Use top class if none is specified
        class_channel = predictions[:, pred_index]  # Focus on this class

    # Compute gradients of the selected class score w.r.t. the conv outputs
    grads = tape.gradient(class_channel, conv_outputs)

    # Average the gradients spatially to get the importance of each feature map
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Multiply each channel by its importance and sum to get heatmap
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]  # Linear combination
    heatmap = tf.squeeze(heatmap)

    # Normalize the heatmap to [0, 1] and apply ReLU
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def overlay_heatmap(heatmap, image, alpha=0.4):
    # Resize heatmap to match original image size
    heatmap = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
    heatmap = np.uint8(255 * heatmap)  # Convert to 0-255 range

    # Apply color map for visualization
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Superimpose heatmap onto original image
    output = cv2.addWeighted(heatmap, alpha, image, 1 - alpha, 0)
    return output