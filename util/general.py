from scipy.signal import butter, filtfilt
import numpy as np

def butter_filter(signal: np.ndarray, filter_order: int, cutoffs: list, sampling_freq: int, 
    filter_type: str) -> np.ndarray:
    """Applies a Butterworth filter to a signal.

    Args:
        signal (np.ndarray): The input signal to filter.
        filter_order (int): The order of the filter.
        cutoffs (list): List of cutoff frequencies for the filter.
        sampling_freq (int): Sampling frequency of the signal.
        filter_type (str): Type of the filter ('low', 'high', or 'band').

    Returns:
        np.ndarray: The filtered signal.
    """
    if filter_type == 'band':
        b, a = butter(filter_order, [cutoffs[0] / (0.5 * sampling_freq), 
            cutoffs[1] / (0.5 * sampling_freq)], btype = filter_type)
    else:
        b, a = butter(filter_order, cutoffs[0] / (0.5 * sampling_freq), btype = filter_type)
    # Apply the band-pass filter
    return filtfilt(b, a, signal)

def get_fft(signal: np.ndarray, sampling_freq: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the FFT magnitude and frequency for a given signal.

    Args:
        signal (np.ndarray): The input signal.
        sampling_freq (int): The sampling frequency of the signal.

    Returns:
        tuple: A tuple containing the FFT magnitude and corresponding frequencies.
    """
    # Compute FFT and frequency axis
    fft_values = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), d=1/sampling_freq)

    # Extract the positive half of the FFT result (due to symmetry for real signals)
    half_N = len(signal) // 2
    fft_magnitude = np.abs(fft_values[:half_N])
    frequencies = frequencies[:half_N]

    return fft_magnitude, frequencies
