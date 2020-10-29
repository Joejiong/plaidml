### TODO: migrate the rest of this code over to c++

import argparse
import glob
import os
import pathlib
import tarfile
import tempfile

import numpy as np

import tensorflow as tf
import flatbuffers
from plaidml.bridge.tensorflow.tests import archive_py_generated as schema
from plaidml.bridge.tensorflow.tests import util


def main(args):
    saved_model = tarfile.open(args.saved_model_path)
    saved_model.extractall()

    input_shape = [1, 224, 224, 3]
    model_name = "resnext50_tf_saved_model"

    with tf.compat.v1.Session() as sess:
        model = tf.saved_model.load(sess, ["train"], model_name)
        x_name = model.signature_def['serving_default'].inputs['input'].name
        x = tf.get_default_graph().get_tensor_by_name(x_name)
        y = tf.get_default_graph().get_tensor_by_name('pool1:0')

        # Run an inference with random inputs to generate a correctness baseline for the archive
        x_input = np.random.uniform(size=input_shape)
        y_output = sess.run(y, feed_dict={x: x_input})

    archive = schema.ArchiveT()
    archive.name = 'resnext'
    archive.inputs = [util.convertBuffer('input', x_input)]
    archive.outputs = [util.convertBuffer('output', y_output)]

    builder = flatbuffers.Builder(0)
    packed = archive.Pack(builder)
    builder.Finish(packed)
    args.archive.write(builder.Output())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate archive for resnext')
    parser.add_argument('saved_model_path', help='location where the saved_model is located')
    parser.add_argument('archive',
                        type=argparse.FileType('wb'),
                        help='location to write the generated archive')
    #parser.add_argument('graphdef', type=str, help='location to write the frozen graphdef')
    args = parser.parse_args()
    main(args)
