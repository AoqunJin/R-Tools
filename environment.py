from config import *


class Env():
    def __init__(self, config: Config) -> None:
        env = suite.make(
            **config.env_config,
            has_renderer=True,
            has_offscreen_renderer=False,
            ignore_done=True,
            use_camera_obs=False,
            horizon=(config.steps_per_action + config.steps_per_rest) * config.num_test_steps,
            control_freq=20,
        )
        env.reset()
        env.viewer.set_camera(camera_id=0)

        # To accommodate for multi-arm settings (e.g.: Baxter), we need to make sure to fill any extra action space
        # Get total number of arms being controlled
        n = 0
        gripper_dim = 0
        for robot in env.robots:
            gripper_dim = robot.gripper["right"].dof if isinstance(robot, Bimanual) else robot.gripper.dof
            n += int(robot.action_dim / (config.action_dim + gripper_dim))

        # Define neutral value
        neutral = np.zeros(config.action_dim + gripper_dim)

        # Keep track of done variable to know when to break loop
        count = 0
        # Loop through controller space
        while count < config.num_test_steps:
            action = neutral.copy()
            for i in range(config.steps_per_action):
                if config.controller_name in {"IK_POSE", "OSC_POSE"} and count > 2:
                    # Set this value to be the scaled axis angle vector
                    vec = np.zeros(3)
                    vec[count - 3] = config.test_value
                    action[3:6] = vec
                else:
                    action[count] = config.test_value
                total_action = np.tile(action, n)
                env.step(total_action)
                env.render()
            for i in range(config.steps_per_rest):
                total_action = np.tile(neutral, n)
                env.step(total_action)
                env.render()
            count += 1

        # Shut down this env before starting the next test
        env.close()
    
    def step():
        ...
        