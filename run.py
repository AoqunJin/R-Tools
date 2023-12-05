import robosuite as suite
import numpy as np
import cv2


def norm_depth_map(depth_map):
    # Normalize the depth map to the 0-255 range (assuming it"s not already)
    depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)

    # Convert the depth map to uint8, as imwrite expects 8-bit images
    depth_map_uint8 = depth_map_normalized.astype(np.uint8)

    return depth_map_uint8


if __name__ == "__main__":
    # Notice how the environment is wrapped by the wrapper
    env = suite.make(
        "Lift",  # env
        robots="Panda",  # use Sawyer robot
        # --- * ---
        use_camera_obs=True,  # do not use pixel observations
        use_object_obs=False,  # don"t provide object observations to agent
        has_renderer=True,  # make sure we can render to the screen
        has_offscreen_renderer=True,  # not needed since not using pixel obs
        reward_shaping=True,  # use dense rewards
        # --- * ---
        control_freq=20,  # control should happen fast enough so that simulation looks smooth
        controller_configs=suite.load_controller_config(default_controller="OSC_POSITION"),  # OSC_POSE IK_POSE
        # --- * ---
        camera_heights=256, 
        camera_widths=256, 
        camera_depths=True, 
        camera_segmentations=None, 
        camera_names="frontview",  # agentview frontview
        # --- * ---
        renderer="mujoco",  # mujoco nvisii
    )
    # print(env)
    env.reset()

    for i_episode in range(1):
        observation = env.reset()
        for k, v in observation.items():
            print(k, v.shape)
        for t in range(200):
            
            low, high = env.action_spec  # (array([-0.02, -0.02, -0.02, -0.05, -0.05, -0.05, -1.  ]), array([0.02, 0.02, 0.02, 0.05, 0.05, 0.05, 1.  ]))
            # print(env.action_spec[0].shape)
            
            action = np.random.uniform(low, high)
            action = np.array([0, 0.1, 0, 0])
            obs, reward, done, _ = env.step(action)
            env.render()
            
            # (
            #     "world", "table", "robot0_base", "robot0_link0", 
            #     "robot0_link1", "robot0_link2", "robot0_link3", 
            #     "robot0_link4", "robot0_link5", "robot0_link6", 
            #     "robot0_link7", "robot0_right_hand", "gripper0_right_gripper", 
            #     "gripper0_eef", "gripper0_leftfinger", "gripper0_finger_joint1_tip", 
            #     "gripper0_rightfinger", "gripper0_finger_joint2_tip", 
            #     "mount0_base", "mount0_controller_box", "mount0_pedestal_feet", 
            #     "mount0_torso", "mount0_pedestal", "cube_main"
            # )

            exit()
            print(env.robots[0].pose_in_base_from_name("gripper0_eef")[:3, -1])
            continue
            
            # visualize
            cv2.imwrite("test{}.png".format(0), obs["frontview_image"])            
            cv2.imwrite("test{}.png".format(1), norm_depth_map(obs["frontview_depth"]))
            # cv2.imwrite("test{}.png".format(1), obs[""])
            
            # print(obs["frontview_image"])
            # print(obs["frontview_depth"])
            
            print(env.robots[0].pose_in_base_from_name("world"))
            
            break
            

