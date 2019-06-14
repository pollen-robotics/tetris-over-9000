from stable_baselines import A2C
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.policies import FeedForwardPolicy

from cnn import cnn
from tetris import TetrisEnv
from dataset_loader import TetrisDataset


class CnnPolicy(FeedForwardPolicy):
    def __init__(self, *args, **kwargs):
        FeedForwardPolicy.__init__(self, *args, **kwargs,
                                   cnn_extractor=cnn, feature_extraction='cnn')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('dataset')
    parser.add_argument('epochs', type=int)
    parser.add_argument('save_path')
    parser.add_argument('--log')
    args = parser.parse_args()

    dataset = TetrisDataset(args.dataset)

    env = TetrisEnv()
    env = DummyVecEnv([lambda: env])

    model = A2C(CnnPolicy, env, verbose=1, tensorboard_log=args.log)

    model.pretrain(dataset, n_epochs=args.epochs)
    model.save(args.save_path)
