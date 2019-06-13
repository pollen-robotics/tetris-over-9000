import numpy as np

from stable_baselines.gail import generate_expert_traj

from tetris import TetrisEnv
from tetris.bot import Bot


if __name__ == '__main__':
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('episod', type=int)
    parser.add_argument('output_dir')
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    filename = os.path.join(args.output_dir, 'dataset-{}.npz'.format(args.episod))
    if os.path.exists(filename):
        raise OSError(filename, 'already exists!')

    env = TetrisEnv()
    model = Bot(env)
    trajs = generate_expert_traj(model.predict, env=env,
                                 n_episodes=args.episod,
                                 save_path=None, image_folder=None)
    np.savez(filename, **trajs)
