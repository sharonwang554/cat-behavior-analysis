# Import configuration first to set matplotlib backend
from config import *

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import glob
import os


def analyze_cat_meow(file_path):
    """
    Analyze a cat's meow audio file to interpret potential meanings
    """
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)

    # Basic audio properties
    duration = len(y) / sr

    # Extract key features
    # 1. Fundamental frequency (pitch)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, threshold=0.1)
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)

    avg_pitch = np.mean(pitch_values) if pitch_values else 0
    pitch_variation = np.std(pitch_values) if pitch_values else 0

    # 2. Intensity/loudness
    rms = librosa.feature.rms(y=y)[0]
    avg_loudness = np.mean(rms)
    loudness_variation = np.std(rms)

    # 3. Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    avg_spectral_centroid = np.mean(spectral_centroids)

    # 4. Zero crossing rate (roughness indicator)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    avg_zcr = np.mean(zcr)

    # 5. MFCC features for vocal characteristics
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Analyze meow characteristics and interpret meaning
    interpretation = interpret_meow(duration, avg_pitch, pitch_variation,
                                    avg_loudness, loudness_variation,
                                    avg_spectral_centroid, avg_zcr)

    # Create visualization
    plt.figure(figsize=(15, 10))

    # Waveform
    plt.subplot(3, 2, 1)
    plt.plot(np.linspace(0, duration, len(y)), y)
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Spectrogram
    plt.subplot(3, 2, 2)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')

    # Pitch contour
    plt.subplot(3, 2, 3)
    times = librosa.frames_to_time(np.arange(len(pitch_values)), sr=sr)
    plt.plot(times[:len(pitch_values)], pitch_values)
    plt.title('Pitch Contour')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')

    # RMS Energy
    plt.subplot(3, 2, 4)
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
    plt.plot(times, rms)
    plt.title('RMS Energy (Loudness)')
    plt.xlabel('Time (s)')
    plt.ylabel('RMS')

    # Spectral Centroid
    plt.subplot(3, 2, 5)
    times = librosa.frames_to_time(np.arange(len(spectral_centroids)), sr=sr)
    plt.plot(times, spectral_centroids)
    plt.title('Spectral Centroid')
    plt.xlabel('Time (s)')
    plt.ylabel('Hz')

    # MFCC
    plt.subplot(3, 2, 6)
    librosa.display.specshow(mfccs, sr=sr, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')

    plt.tight_layout()

    # Save the plot to the project folder
    base_name = file_path.split(
        '/')[-1].replace('.m4a', '').replace('.wav', '').replace('.mp3', '')
    output_filename = f"meow_analysis_{base_name}.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Analysis graph saved as: {output_filename}")
    plt.close()  # Close the figure to free memory

    return interpretation


def interpret_meow(duration, avg_pitch, pitch_variation, avg_loudness,
                   loudness_variation, spectral_centroid, zcr):
    """
    Interpret the meaning of a cat's meow based on acoustic features
    """
    interpretation = {
        'primary_meaning': '',
        'emotional_state': '',
        'urgency_level': '',
        'confidence': '',
        'details': []
    }

    # Duration analysis
    if duration < 0.5:
        interpretation['details'].append(
            "Short meow - likely a greeting or acknowledgment")
        urgency_base = "Low"
    elif duration > 2.0:
        interpretation['details'].append(
            "Long meow - indicates strong desire or complaint")
        urgency_base = "High"
    else:
        interpretation['details'].append(
            "Medium length meow - general communication")
        urgency_base = "Medium"

    # Pitch analysis
    if avg_pitch > 400:
        interpretation['details'].append(
            "High pitch - kitten-like, seeking attention or affection")
        emotional_state = "Seeking attention/affection"
        if avg_pitch > 600:
            interpretation['primary_meaning'] = "Demanding attention or food"
    elif avg_pitch < 200:
        interpretation['details'].append(
            "Low pitch - more serious communication, possibly complaint")
        emotional_state = "Serious/Complaining"
        interpretation['primary_meaning'] = "Complaint or serious request"
    else:
        interpretation['details'].append(
            "Medium pitch - neutral communication")
        emotional_state = "Neutral"
        interpretation['primary_meaning'] = "General communication"

    # Pitch variation analysis
    if pitch_variation > 50:
        interpretation['details'].append(
            "High pitch variation - expressive, emotional meow")
        if emotional_state == "Neutral":
            emotional_state = "Expressive"
    elif pitch_variation < 20:
        interpretation['details'].append(
            "Stable pitch - calm, controlled communication")
        if emotional_state == "Neutral":
            emotional_state = "Calm"

    # Loudness analysis
    if avg_loudness > 0.1:
        interpretation['details'].append("Loud meow - demanding attention")
        urgency_level = "High"
        if interpretation['primary_meaning'] == "General communication":
            interpretation['primary_meaning'] = "Demanding attention"
    elif avg_loudness < 0.05:
        interpretation['details'].append(
            "Quiet meow - gentle request or greeting")
        urgency_level = "Low"
        if interpretation['primary_meaning'] == "General communication":
            interpretation['primary_meaning'] = "Gentle request or greeting"
    else:
        urgency_level = urgency_base

    # Spectral centroid (brightness)
    if spectral_centroid > 3000:
        interpretation['details'].append(
            "Bright, sharp meow - alert or excited")
        if emotional_state == "Neutral":
            emotional_state = "Alert/Excited"
    elif spectral_centroid < 1500:
        interpretation['details'].append("Mellow meow - relaxed or content")
        if emotional_state == "Neutral":
            emotional_state = "Relaxed"

    # Zero crossing rate (roughness)
    if zcr > 0.1:
        interpretation['details'].append(
            "Rough/raspy meow - possible distress or illness")
        emotional_state = "Distressed"
        interpretation['primary_meaning'] = "Possible distress or discomfort"

    # Final interpretation
    interpretation['emotional_state'] = emotional_state
    interpretation['urgency_level'] = urgency_level

    # Confidence based on feature consistency
    confidence_score = 0
    if avg_pitch > 0:
        confidence_score += 25
    if len(interpretation['details']) >= 3:
        confidence_score += 25
    if urgency_level != "Medium":
        confidence_score += 25
    if emotional_state != "Neutral":
        confidence_score += 25

    if confidence_score >= 75:
        interpretation['confidence'] = "High"
    elif confidence_score >= 50:
        interpretation['confidence'] = "Medium"
    else:
        interpretation['confidence'] = "Low"

    return interpretation


def print_analysis_results(interpretation):
    """
    Print the meow analysis results in a readable format
    """
    print("🐱 CAT MEOW ANALYSIS RESULTS 🐱")
    print("=" * 40)
    print(f"Primary Meaning: {interpretation['primary_meaning']}")
    print(f"Emotional State: {interpretation['emotional_state']}")
    print(f"Urgency Level: {interpretation['urgency_level']}")
    print(f"Analysis Confidence: {interpretation['confidence']}")
    print("\nDetailed Analysis:")
    for detail in interpretation['details']:
        print(f"• {detail}")
    print("\n" + "=" * 40)
    print("Note: This analysis is based on general acoustic patterns.")
    print("Individual cats may have unique vocal characteristics.")


if __name__ == "__main__":
    # Automatically find all .m4a files in the current directory
    meow_files = glob.glob("*.m4a")
    meow_files.sort()  # Sort files alphabetically for consistent ordering

    if not meow_files:
        print("❌ No .m4a files found in the current directory!")
        print("Please make sure you have .m4a audio files to analyze.")
        exit(1)

    print("🐱 ANALYZING MULTIPLE CAT MEOWS 🐱")
    print("=" * 50)
    print(f"Found {len(meow_files)} .m4a file(s): {', '.join(meow_files)}")
    print("=" * 50)

    for i, file_path in enumerate(meow_files, 1):
        print(
            f"\n📁 ANALYZING {file_path.upper()} (Recording {i}/{len(meow_files)})")
        print("-" * 30)

        try:
            results = analyze_cat_meow(file_path)
            print_analysis_results(results)
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            print("Make sure the file exists and librosa is installed")

        print("\n" + "=" * 50)
