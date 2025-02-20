import numpy as np

class Config:
    """Configurations for IMU analysis
    """
    def __init__(self):
        """Initialize default parameters based on the dataset."""

        self.sampling_rate = 50 # Based on the dataset's README file
        
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
    
    Complementary filter approach based on @PhilsLab YouTube videos:
    - https://www.youtube.com/watch?v=RZd6XDx5VXo
    - https://www.youtube.com/watch?v=BUW2OdAtzBw
    - https://www.youtube.com/watch?v=hQUkiC5o0JI
    """
    def __init__(self):
        """initialize the variables for complementry filter and init values for pitch and roll
        """
        self.comp_filt_alpha: float = 0.05 # 5% ACC, 95% Gyro weighting
        
        # Initialize roll and pitch estimates (in radians)
        self.phiHat_rad: float = 4.2
        self.thetaHat_rad: float = 1.2

        # constant values
        self.g_value: float = 9.81 # Gravity constant
        self.rad_to_degree: float = 180 / np.pi  # Convert radians to degrees

    def calculate_roll_pitch(self, ax_acc: np.ndarray, ay_acc: np.ndarray, az_acc: np.ndarray,
     p_gyro: np.ndarray, q_gyro: np.ndarray, r_gyro: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Calculate roll and pitch. The output is in degree. To avoid zero devision, Use zero 
        corrected ACC and Gyro values. All inputs should have the same length.

        Args:
            ax_acc (np.ndarray): ACC X (m/s²)
            ay_acc (np.ndarray): ACC Y (m/s²)
            az_acc (np.ndarray): ACC Z (m/s²)
            p_gyro (np.ndarray): Gyro X (rad/s)
            q_gyro (np.ndarray): Gyro Y (rad/s)
            r_gyro (np.ndarray): Gyro Z (rad/s)

        Returns:
            tuple[np.ndarray, np.ndarray]: Roll and Pitch in degrees
        """
        # init the estimated vectores
        n_samples = len(ax_acc)
        estimated_phi = np.zeros(len(n_samples)) # roll
        estimated_theta = np.zeros(len(n_samples)) # pitch

        phiHat_rad = self.phiHat_rad  # Initialize roll estimate
        thetaHat_rad = self.thetaHat_rad  # Initialize pitch estimate

        dt = 1 / Config.sampling_rate  # Time step

        for i in range(n_samples):

            # Using ACC for pitch and roll in Rad.
            phiHat_acc_rad = np.arctan(ay_acc[i] / az_acc[i])
            thetaHat_acc_rad = np.arctan(ax_acc[i] / self.g_value)

            # Compute roll and pitch rates from gyroscope
            phiDot_gyro = p_gyro[i] + np.tan(thetaHat_acc_rad) * (np.sin(phiHat_acc_rad) * q_gyro[i] \
                + np.cos(phiHat_acc_rad) * r_gyro[i]) # roll
            thetaDot_gyro = np.cos(phiHat_acc_rad) * q_gyro[i] - np.sin(phiHat_acc_rad) * r_gyro[i] # pitch
            
            # Complementary filter: Blend ACC and Gyro estimates
            phiHat_rad = self.comp_filt_alpha * phiHat_acc_rad + ((1 - self.comp_filt_alpha) * \
                (phiHat_rad + phiDot_gyro * (1 / dt)))
            thetaHat_rad = self.comp_filt_alpha * thetaHat_acc_rad + ((1 - self.comp_filt_alpha) * \
                (thetaHat_rad + thetaDot_gyro * (1 / dt)))

            # convert it to degree
            estimated_phi[i] = phiHat_rad * self.rad_to_degree
            estimated_theta[i] = thetaHat_rad * self.rad_to_degree

        
        return estimated_phi, estimated_theta
            
