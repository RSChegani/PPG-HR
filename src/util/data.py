
class IMUDataConversion():
    """Convert the units:
        Based on the data ReadMe file the is a "6-axis inertial measurement unit (IMU; LSM6DSMUSTR, STMicroelectronics)".  
        The data sheet can be found here: https://www.mouser.ca/datasheet/2/389/en.DM00218116-1107506.pdf  
        The information in the datasheet is sued to convert the values from raw digital readings to acceleration and angular velocity units

    ## Coversion factor
        Depending on the sensitivity set on the device different conversion factors need to be used. The overall formula is:  
        Acceleration (m/s²) = raw_data × sensitivity (m/s² per LSB)  
        To convert these to m/s² per LSB:
        - ±2g:  0.061 × 9.80665 × e-3 ≈ 0.000598 m/s2/LSB
        - ±4g:  0.122 × 9.80665 × e-3 ≈ 0.001196 m/s2/LSB
        - ±8g:  0.244 × 9.80665 × e-3 ≈ 0.002392 m/s2/LSB
        - ±16g: 0.488 × 9.80665 × e-3 ≈ 0.004784 m/s2/LSB

        Since there is no information in the data ReadMe file about the resolution, I tried all 4 and decided ±2g makes sense and assumed that as the resolution.  
        The readme mentioned that they added 32768 to the digital data to remove any negative value, with a ±2g this is 2 * 9.79 (2*g). So the assumption makes sense.  
        
        For Gyro the conversion table is:  
        - ±125°/s:   0.0000763 rad/s per LSB
        - ±250°/s:   0.0001527 rad/s per LSB
        - ±500°/s:   0.0003054 rad/s per LSB
        - ±1000°/s:  0.0006109 rad/s per LSB
        - ±2000°/s:  0.0012217 rad/s per LSB
    """

    def __init__(self):
        """Consatants used for conversion
        """
        # Set the conversion factors based on the datasheet to convert raw digital values to mps2 and rps
        self.acc_convertion_factor = 0.000598
        self.gyro_conversion_factor = 0.0000763
        # based on the data ReadMe file: a value of 32768 added to remove the negative number.   
        self.added_constant_value = 32768

    def convert_acc(self, acc_list: list, zero_corrected: bool = True) -> list:
        """Convert ACC data from digital values to m/s2 values

        Args:
            acc_list (list): A list of X, Y, and Z values to be converted
            zero_corrected (bool, optional): A flag to use zero corrected or not. Defaults to True.

        Returns:
            list: A list of converted values in m/s2 with the same order 
        """
        if zero_corrected:
            return [vec * self.acc_convertion_factor for vec in acc_list]
        else:
            return [(vec - self.added_constant_value) * self.acc_convertion_factor for vec in acc_list]

    def convert_gyro(self, gyro_list: list, zero_corrected: bool = True) -> list:
        """Convert Gyro data from digital values to rad/s values

        Args:
            gyro_list (list): A list of X, Y, and Z values to be converted
            zero_corrected (bool, optional): A flag to use zero corrected or not. Defaults to True.

        Returns:
            list: A list of converted values in rad/s with the same order 
        """
        if zero_corrected:
            return [vec * self.gyro_conversion_factor for vec in gyro_list]
        else:
            return [(vec - self.added_constant_value) * self.gyro_conversion_factor for vec in gyro_list]
    


