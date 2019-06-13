import numpy as np


class TetrisDataset(object):
    def __init__(self, filename,
                 train_fraction=0.7, batch_size=64,
                 randomize=True, shuffle=True):

        traj_data = np.load(filename)

        self.observations = traj_data['obs']
        self.actions = traj_data['actions']

        if randomize:
            indices = np.random.permutation(len(self.observations)).astype(np.int64)
        else:
            indices = np.arange(len(self.observations)).astype(np.int64)

        self.train_indices = indices[:int(train_fraction * len(indices))]
        self.val_indices = indices[int(train_fraction * len(indices)):]

        self.train_loader = DataLoader(self.train_indices, batch_size, shuffle,
                                       self.observations, self.actions)
        self.val_loader = DataLoader(self.val_indices, batch_size, shuffle,
                                     self.observations, self.actions)

    def get_next_batch(self, split):
        loader = self.train_loader if split == 'train' else self.val_loader
        return loader.get_next_batch()


class DataLoader(object):
    def __init__(self, indices, batch_size, shuffle,
                 observations, actions):
        self.indices = indices
        self.shuffle = shuffle
        if self.shuffle:
            np.random.shuffle(self.indices)

        self.observations = observations
        self.actions = actions

        self.start_idx = 0
        self.batch_size = batch_size

    def __len__(self):
        return len(self.indices) // self.batch_size

    def next_minibatch_indices(self):
        if self.start_idx + self.batch_size >= len(self.indices):
            self.start_idx = 0
            if self.shuffle:
                np.random.shuffle(self.indices)

        return self.indices[self.start_idx:self.start_idx + self.batch_size]

    def get_next_batch(self):
        minibatch_indices = self.next_minibatch_indices()
        self.start_idx += self.batch_size

        obs = self.observations[minibatch_indices]
        actions = self.actions[minibatch_indices]

        return obs, actions
