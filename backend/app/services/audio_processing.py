import numpy as np
from scipy.io import wavfile
import soundfile as sf
import io

class AudioProcessingService:
    @staticmethod
    def normalize_audio(audio_data, target_dBFS=-20.0):
        """
        Normalize audio to a target decibel full scale (dBFS)
        
        :param audio_data: Input audio data
        :param target_dBFS: Target decibel full scale
        :return: Normalized audio data
        """
        try:
            # Calculate current RMS
            rms = np.sqrt(np.mean(audio_data**2))
            
            # Convert target dBFS to linear scale
            scaling_factor = 10 ** (target_dBFS / 20)
            
            # Normalize
            normalized_audio = audio_data * (scaling_factor / rms)
            
            return normalized_audio
        except Exception as e:
            print(f"Error normalizing audio: {e}")
            return audio_data
    
    @staticmethod
    def remove_silence(audio_data, sample_rate, silence_threshold=0.01):
        """
        Remove silence from audio data
        
        :param audio_data: Input audio data
        :param sample_rate: Audio sample rate
        :param silence_threshold: Threshold below which audio is considered silence
        :return: Audio data with silence removed
        """
        try:
            # Convert to absolute values
            audio_abs = np.abs(audio_data)
            
            # Find non-silent segments
            non_silent = audio_abs > silence_threshold
            
            # Trim leading and trailing silence
            start = np.argmax(non_silent)
            end = len(non_silent) - np.argmax(non_silent[::-1])
            
            return audio_data[start:end]
        except Exception as e:
            print(f"Error removing silence: {e}")
            return audio_data
    
    @staticmethod
    def convert_audio_format(input_audio, input_format, output_format):
        """
        Convert audio between different formats
        
        :param input_audio: Input audio data or file-like object
        :param input_format: Input audio format
        :param output_format: Desired output format
        :return: Converted audio data
        """
        try:
            # Read input audio
            sample_rate, audio_data = wavfile.read(input_audio)
            
            # Create output buffer
            output_buffer = io.BytesIO()
            
            # Write to output format
            sf.write(output_buffer, audio_data, sample_rate, format=output_format)
            
            return output_buffer.getvalue()
        except Exception as e:
            print(f"Error converting audio format: {e}")
            return None
    
    @staticmethod
    def get_audio_features(audio_data, sample_rate):
        """
        Extract audio features
        
        :param audio_data: Input audio data
        :param sample_rate: Audio sample rate
        :return: Dictionary of audio features
        """
        try:
            return {
                'duration': len(audio_data) / sample_rate,
                'sample_rate': sample_rate,
                'channels': 1 if len(audio_data.shape) == 1 else audio_data.shape[1],
                'rms': np.sqrt(np.mean(audio_data**2)),
                'peak_amplitude': np.max(np.abs(audio_data))
            }
        except Exception as e:
            print(f"Error extracting audio features: {e}")
            return {}