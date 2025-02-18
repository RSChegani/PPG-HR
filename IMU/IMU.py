import numpy as np

class Config:
    """Configurations for ACC analysis
    """
    def __init__(self):
        # intialize the params based on the data
        self.sampling_rate = 50 # based on the data readMe file
        
        # filter design init values
        self.filter_type: str = 'band'
        self.filter_order: int = 4
        self.highpass_cutoff: float = 0.2
        self.lowpass_cutoff: float = 15

    def update_config(self, **kwargs):
        """Update configuration settings dynamically."""
        for key, value in kwargs.items():
            if hasattr(self, key):  # Ensure the key exists
                setattr(self, key, value)
            else:
                print(f"Warning: {key} is not a valid configuration option")
    
    def display_config(self):
        """Print the current configuration settings."""
        config_dict = {
            "Sampling Rate (Hz)": self.sampling_rate,
            "Filter Type": self.filter_type,
            "Filter Order": self.filter_order,
            "High Pass Cutoff Frequency (Hz)": self.highpass_cutoff,
            "Low Pass Cutoff Frequency (Hz)": self.lowpass_cutoff,
        }
        for key, value in config_dict.items():
            print(f"{key}: {value}")

class RollPitch:
    """Calculate Roll (Phi) and Pitch (Theta) from ACC and Gyro
    See the following links from @PhilsLab on youtube
    - https://www.youtube.com/watch?v=RZd6XDx5VXo
    - https://www.youtube.com/watch?v=BUW2OdAtzBw
    - https://www.youtube.com/watch?v=hQUkiC5o0JI
    """
    def __init__(self):
        """initialize the variables for complementry filter and init values for pitch and roll
        """
        self.comp_filt_alpha: float = 0.05 #This means we use 5% of ACC and 95% of Gyro fot Roll and Pitch
        
        # initialize the roll and pitch values based on the data
        self.phiHat_rad: float = 4.2
        self.thetaHat_rad: float = 1.2

        # constant values
        self.g_value = 9.81
        self.rad_to_degree = 57.2957795131

    def calculate_roll_pitch(self, ax_acc: np.ndarray, ay_acc: np.ndarray, az_acc: np.ndarray,
     p_gyro: np.ndarray, q_gyro: np.ndarray, r_gyro: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Calculate roll and pitch. The output is in degree. To avoid zero devision, Use zero 
        corrected ACC and Gyro values. All inputs should have the same length.

        Args:
            ax_acc (np.ndarray): ACC X, in m/s2
            ay_acc (np.ndarray): ACC Y, in m/s2
            az_acc (np.ndarray): ACC Z, in m/s2
            p_gyro (np.ndarray): Gyro X, radian per seconds
            q_gyro (np.ndarray): Gyro Y, radian per seconds
            r_gyro (np.ndarray): Gyro Z, radian per seconds

        Returns:
            tuple[np.ndarray, np.ndarray]: Roll and Pitch in degree
        """
        # init the estimated vectores
        estimated_phi = np.zeros(len(ax_acc)) # roll
        estimated_theta = np.zeros(len(ax_acc)) # pitch

        for i in range(len(ax_acc)):

            ax_acc_i = ax_acc[i]
            ay_acc_i = ay_acc[i]
            az_acc_i = az_acc[i]

            # Using ACC for pitch and roll in Rad.
            phiHat_acc_rad = np.arctan(ay_acc_i / az_acc_i)
            thetaHat_acc_rad = np.arctan(ax_acc_i / self.g_value)

            p_gyro_i = p_gyro[i]
            q_gyro_i = q_gyro[i]
            r_gyro_i = r_gyro[i]

            # Use a weighted average between ACC and Gyro for Pitch and Roll calculation
            phiDot_gyro = p_gyro_i + np.tan(thetaHat_acc_rad) * (np.sin(phiHat_acc_rad) * q_gyro_i \
                + np.cos(phiHat_acc_rad) * r_gyro_i) # roll
            thetaDot_gyro = np.cos(phiHat_acc_rad) * q_gyro_i - np.sin(phiHat_acc_rad) * r_gyro_i # pitch

            phiHat_rad = self.comp_filt_alpha * phiHat_acc_rad + ((1 - self.comp_filt_alpha) * \
                (phiHat_rad + phiDot_gyro * (1 / Config.sampling_rate)))
            thetaHat_rad = self.comp_filt_alpha * thetaHat_acc_rad + ((1 - self.comp_filt_alpha) * \
                (thetaHat_rad + thetaDot_gyro * (1 / Config.sampling_rate)))

            # convert it to degree
            estimated_phi[i] = phiHat_rad * self.rad_to_degree
            estimated_theta[i] = thetaHat_rad * self.rad_to_degree

        
        return estimated_phi, estimated_theta