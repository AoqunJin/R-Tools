from robosuite.controllers import load_controller_config
from robosuite.utils.input_utils import *

if __name__ == "__main__":
    # Create dict to hold options that will be passed to env creation call
    options = {}


    # Choose environment and add it to options
    # options["env_name"] = choose_environment()
    options["env_name"] = 'Lift'
    controller_name = 'JOINT_POSITION'  # given desired positions for each joint change to torque
    # Load the desired controller
    options["controller_configs"] = load_controller_config(default_controller=controller_name)
    options["robots"] = 'Jaco'

    env = suite.make(
            **options,
            has_renderer=True,
            has_offscreen_renderer=False,
            ignore_done=True,
            use_camera_obs=False,
            control_freq=20,
            reward_shaping=True,
        )

    # Help message to user
    print()
    print("Press \"H\" to show the viewer control panel.")

    env.reset()
    env.viewer.set_camera(camera_id=0)

    # Get action limits
    low, high = env.action_spec

    for i in range(1000):
        
        # (1):
        # joint_position_end = [4, 4, -0.59, 2, 1.1, 4, 0]
        # env.robots[0].set_robot_joint_positions(joint_position_end) #gripper not included
    
        # (2):
        # Jaco delta for JOINT_POSITION Controller:
        action_pos_delta = [0.808, 0.32, -0.59, 0.83, 1.05, 0.24, -3.142, -1]
        obs, reward, done, _ = env.step(action_pos_delta)

        env.render()
        
def control_loop(tgt_jpos, env, max_n=500, eps=0.01):
    obs = env._get_observations()
    print(obs.keys())
    for i in range(max_n):
        observed_value = obs[proprio_obs_name]
        if i == 0:
            observed_value = env.robots[0].init_qpos

        q_diff =  tgt_jpos - observed_value
        q_diff_max = np.max(np.abs(q_diff))
        if q_diff_max < eps:
            break

        action = list(q_diff) + list([1])
        assert len(action) == 8, len(action)
        obs, _, _, _ = env.step(action)

        #env.render()

desired_joint_positions = [0.808, 0.32, -0.59, 0.83, 1.05, 0.24, -3.142, -1]
obs = control_loop(desired_joint_positions, env) 