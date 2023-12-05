import robosuite as suite
from robosuite.controllers import load_controller_config
from robosuite.robots import Bimanual
from robosuite.utils.input_utils import *
import yaml


class Config():
    def __init__(self, config_path) -> None:
        with open(config_path, 'r') as stream: 
            self.env_config = yaml.safe_load(stream)
        print(self.env_config)
        self.controller_name = None
        self.action_dim = None
        self.num_test_steps = None
        self.test_value = None
        self.steps_per_action = None
        self.steps_per_rest = None
        self.process_config()
        
    def process_config(self):
        # For multiple arm
        if "TwoArm" in self.env_config["env_name"]:
            # If chosen configuration was bimanual, the corresponding robot must be Baxter
            if self.env_config["env_configuration"] == "bimanual":
                self.env_config["robots"] = "Baxter"
                print("Baxter was chosen.\n")
            else:
                print("A multiple single-arm configuration was chosen.\n")

        # Hacky way to grab joint dimension for now
        joint_dim = 6 if self.env_config["robots"] == "UR5e" else 7

        # Choose controller
        controller_name = self.env_config.pop("controller_name")
        self.controller_name = controller_name
        # Define the pre-defined controller actions to use (action_dim, num_test_steps, test_value)
        
        controller_settings = {
            "OSC_POSE": [6, 6, 0.1],
            "OSC_POSITION": [3, 3, 0.1],
            "IK_POSE": [6, 6, 0.01],
            "JOINT_POSITION": [joint_dim, joint_dim, 0.2],
            "JOINT_VELOCITY": [joint_dim, joint_dim, -0.1],
            "JOINT_TORQUE": [joint_dim, joint_dim, 0.25],
        }
        
        # Load the desired controller
        self.env_config["controller_configs"] = suite.load_controller_config(default_controller=controller_name)

        # Define variables for each controller test
        self.action_dim = controller_settings[controller_name][0]
        self.num_test_steps = controller_settings[controller_name][1]
        self.test_value = controller_settings[controller_name][2]

        # Define the number of timesteps to use per controller action as well as timesteps in between actions
        self.steps_per_action = 75
        self.steps_per_rest = 75
        
        print(self.env_config)

if __name__ == "__main__":
    c = Config("./config.yaml")
