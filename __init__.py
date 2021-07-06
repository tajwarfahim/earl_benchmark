"API to load Persistent RL environments."

import numpy as np
from persistent_rl_benchmark.wrappers import persistent_state_wrapper

# for every environment, add an entry for the configuration of the environment
# make a default configuration for environment, the user can change the parameters by passing it to the constructor.

# number of initial states being provided to the user
# for deterministic initial state distributions, it should be 1
# for stochastic initial state distributions, sample the distribution randomly and save the initial state distribution
env_config = {
	'tabletop_manipulation': {
		'num_initial_state_samples': 1,
		'train_horizon': int(2e5),
		'eval_horizon': 200,
	},
}

class PersistentRLEnvs:
	def __init__(env_name,
							 # parameters which need to be set for environment
							 reward_type='sparse',
							 reset_train_env_at_goal=False,
							 # parameters with a default value in benchmark, can be changed by the user
							 **kwargs,
							 )
		self._env_name = env_name
		self._reward_type = reward_type
		self._reset_train_env_at_goal = reset_train_env_at_goal

		# resolve to default parameters if not provided by the user
		self._train_horizon = kwargs.get('train_horizon', env_config[env_name]['train_horizon'])
		self._eval_horizon = kwargs.get('eval_horizon', env_config[env_name]['eval_horizon'])
		self._num_initial_state_samples = kwargs.get('num_initial_state_samples', env_config[env_name]['num_initial_state_samples'])

	def get_train_env(self):
		if env_name == 'tabletop_manipulation':
		 	from persistent_rl_benchmark.envs import tabletop_manipulation
		 	train_env = tabletop_manipulation.TabletopManipulation(task_list='rc_o-rc_k-rc_p-rc_b',
		 																												 reward_type=reward_type,
		 																												 reset_at_goal=reset_train_env_at_goal)

		return persistent_state_wrapper.PersistentStateWrapper(train_env, episode_horizon=self._train_horizon)

	def get_eval_env(self):
		if env_name == 'tabletop_manipulation':
		 	from persistent_rl_benchmark.envs import tabletop_manipulation
			eval_env = tabletop_manipulation.TabletopManipulation(task_list='rc_o-rc_k-rc_p-rc_b',
		 																												reward_type=reward_type)

		return persistent_state_wrapper.PersistentStateWrapper(eval_env, episode_horizon=self._eval_horizon)

	def get_initial_states(self, num_samples=None):
		'''
		Always returns initial state of the shape N x state_dim
		'''
		if num_samples is None:
			num_samples = self._num_initial_state_samples

		# TODO: potentially load environments from disk
		if self._env_name == 'tabletop_manipulation':
			from persistent_rl_benchmark.envs import tabletop_manipulation
			return tabletop_manipulation.initial_states
		else:
			cur_env = self.get_eval_env()
			reset_states = []
			while len(reset_states) < self._num_initial_state_samples:
				reset_states.append(cur_env.reset())
				reset_states = list(set(reset_states))

			return np.stack(reset_states)

	def get_goal_states(self):
		if self._env_name == 'tabletop_manipulation':
			from persistent_rl_benchmark.envs import tabletop_manipulation
			return tabletop_manipulation.goal_states

	def get_demonstrations(self):
		pass