from stable_baselines.gail import generate_expert_traj

from tetris import TetrisEnv
from tetris.bot import Bot


if __name__ == '__main__':
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('episod', type=int)
    parser.add_argument('outputdir')
    args = parser.parse_args()

    save_path = os.path.join(args.outputdir, 'trajs-{}'.format(args.episod))
    if os.path.exists(save_path):
        raise OSError(save_path, 'already exists!')

    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    env = TetrisEnv()
    model = Bot(env)
    trajs = generate_expert_traj(model.predict, env=env,
                                 n_episodes=args.episod,
                                 save_path=save_path,
                                 image_folder=os.path.join(save_path, 'img'))
