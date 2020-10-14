# ------------------------------------------------------------------------------
# Copyright (c) Microsoft
# Licensed under the MIT License.
# Created by Tianheng Cheng(tianhengcheng@gmail.com)
# ------------------------------------------------------------------------------

import os
import pprint
import argparse
import cv2
import numpy as np

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.utils.data import DataLoader
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import lib.models as models
from lib.config import config, update_config  #import config是嘛意思
from lib.utils import utils
from lib.datasets import get_dataset
from lib.core import function

#
def parse_args():

    parser = argparse.ArgumentParser(description='Train Face Alignment')

    parser.add_argument('--cfg', help='experiment configuration filename',
                        required=True, type=str)
    parser.add_argument('--model-file', help='model parameters', required=True, type=str)

    args = parser.parse_args()
    update_config(config, args)
    return args


def main():

    args = parse_args()

    logger, final_output_dir, tb_log_dir = \
        utils.create_logger(config, args.cfg, 'test')

    logger.info(pprint.pformat(args))
    logger.info(pprint.pformat(config))

    cudnn.benchmark = config.CUDNN.BENCHMARK
    cudnn.determinstic = config.CUDNN.DETERMINISTIC
    cudnn.enabled = config.CUDNN.ENABLED

    config.defrost()
    config.MODEL.INIT_WEIGHTS = False
    config.freeze()
    model = models.get_face_alignment_net(config)

    gpus = list(config.GPUS)
    model = nn.DataParallel(model, device_ids=gpus).cuda()

    # load model
    state_dict = torch.load(args.model_file)
    if 'state_dict' in state_dict.keys():
        state_dict = state_dict['state_dict']
        model.load_state_dict(state_dict)
    else:
        model.module.load_state_dict(state_dict)

    dataset_type = get_dataset(config)
    #读测试集文件
    test_loader = DataLoader(
        dataset=dataset_type(config,
                             is_train=False),
        batch_size=config.TEST.BATCH_SIZE_PER_GPU*len(gpus),
        shuffle=False,
        num_workers=config.WORKERS,
        pin_memory=config.PIN_MEMORY
    )

    nme, predictions = function.inference(config, test_loader, model)    #50*28*2 50张-28点-2个坐标  nme准确率 反比
    with open('../data/crabs/crabs_data_test.csv', 'r') as f:
        data = np.loadtxt(f, str, delimiter=",", skiprows=1)
    paths = data[:, 0]
    for index, path in enumerate(paths):
        img = cv2.imread("../data/crabs/images/{}".format(path))
        a = predictions[index]
        b = a.numpy()

        for index, px in enumerate(b):
            # print(tuple(px))
            cv2.circle(img, tuple(px), 1, (0, 0, 255), 3, 8, 0)

        # cv2.imwrite("/home/njtech/Jiannan/crabs/dataset/result_new/{}".format(path.split('/')[-1]), img)

        cv2.imshow("img", img)

        cv2.waitKey(1000) & 0xFF

    torch.save(predictions, os.path.join(final_output_dir, 'predictions.pth')) #可以注释


if __name__ == '__main__':
    main()

