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
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_filename = f"meow_analysis_{base_name}.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Analysis graph saved as: {output_filename}")
    plt.close()  # Close the figure to free memory

    return interpretation


def detect_vocal_patterns(duration, avg_pitch, pitch_variation, avg_loudness,
                          loudness_variation, spectral_centroid, zcr):
    """
    Detect specific vocal patterns and characteristics in cat vocalizations
    """
    patterns = []

    # Trill Pattern Detection
    if (pitch_variation > 80 and duration > 0.5 and spectral_centroid > 2000 and
            avg_pitch > 200 and zcr < 0.05):
        patterns.append({
            'pattern': 'trill_detected',
            'description': 'Friendly social communication trill - indicates welcoming, social behavior often used in greeting familiar humans or other cats',
            'confidence': 'High',
            'behavioral_meaning': 'Social bonding, contentment, friendly approach'
        })

    # Chirping Pattern Detection
    if (duration < 0.4 and avg_pitch > 400 and pitch_variation > 60 and
            spectral_centroid > 3000):
        patterns.append({
            'pattern': 'chirp_pattern',
            'description': 'Hunting instinct chirp - rapid, bird-like vocalization indicating prey interest or excitement about potential hunting opportunity',
            'confidence': 'High',
            'behavioral_meaning': 'Predatory excitement, environmental stimulation, hunting instincts'
        })

    # Purr-Meow Combination Detection
    if (zcr < 0.03 and spectral_centroid < 1500 and duration > 0.8 and
            avg_loudness > 0.03 and pitch_variation < 30):
        patterns.append({
            'pattern': 'purr_meow_combo',
            'description': 'Purr-meow combination - contentment mixed with specific request, indicating comfortable cat making polite demand',
            'confidence': 'Medium',
            'behavioral_meaning': 'Contentment with request, comfortable demanding, trust-based communication'
        })

    # Yowling Pattern Detection
    if (duration > 2.0 and avg_pitch > 300 and pitch_variation > 100 and
            avg_loudness > 0.1):
        patterns.append({
            'pattern': 'yowling_pattern',
            'description': 'Yowling vocalization - intense, prolonged call indicating territorial behavior, mating calls, or significant distress',
            'confidence': 'High',
            'behavioral_meaning': 'Territorial assertion, mating behavior, distress, or medical discomfort'
        })

    # Silent Meow Detection (very quiet with mouth movement)
    if (avg_loudness < 0.01 and duration > 0.3 and pitch_variation < 20):
        patterns.append({
            'pattern': 'silent_meow',
            'description': 'Silent meow - visual communication with trusted human, indicates strong bond and expectation of attention without vocalization',
            'confidence': 'Medium',
            'behavioral_meaning': 'Trust-based communication, intimate bonding, confident expectation of response'
        })

    # Rapid Sequence Pattern (short duration, high urgency indicators)
    if (duration < 0.5 and avg_loudness > 0.08 and pitch_variation > 40):
        patterns.append({
            'pattern': 'rapid_sequence',
            'description': 'Rapid sequence meow - part of quick succession indicating high urgency or excitement',
            'confidence': 'Medium',
            'behavioral_meaning': 'High urgency, excitement, impatience, demanding immediate attention'
        })

    # Descending Pitch Pattern
    if (pitch_variation > 50 and avg_pitch > 250 and spectral_centroid < 2000):
        patterns.append({
            'pattern': 'descending_pitch',
            'description': 'Descending pitch pattern - disappointment or resignation vocalization, often after unmet expectations',
            'confidence': 'Medium',
            'behavioral_meaning': 'Disappointment, resignation, mild frustration, unmet expectations'
        })

    # Ascending Pitch Pattern (question-like)
    if (pitch_variation > 60 and duration < 1.0 and spectral_centroid > 2500):
        patterns.append({
            'pattern': 'ascending_pitch',
            'description': 'Ascending pitch pattern - question-like vocalization indicating uncertainty or seeking confirmation',
            'confidence': 'Medium',
            'behavioral_meaning': 'Uncertainty, questioning, seeking confirmation or permission'
        })

    # Harmonic Richness Detection
    if (spectral_centroid > 2000 and spectral_centroid < 4000 and zcr < 0.06 and
            pitch_variation > 30):
        patterns.append({
            'pattern': 'harmonic_richness',
            'description': 'Harmonically rich vocalization - emotionally complex communication with sophisticated tonal qualities',
            'confidence': 'High',
            'behavioral_meaning': 'Emotional sophistication, complex communication intent, nuanced expression'
        })

    return patterns


def analyze_contextual_indicators(duration, avg_pitch, pitch_variation, avg_loudness,
                                  loudness_variation, spectral_centroid, zcr):
    """
    Analyze contextual indicators for time-of-day patterns, frequency clusters, and breath patterns
    """
    indicators = []

    # Morning Demand Pattern (high urgency, demanding characteristics)
    if (avg_loudness > 0.1 and avg_pitch > 350 and duration < 1.0):
        indicators.append({
            'context': 'morning_demand_pattern',
            'description': 'Morning demand characteristics - loud, high-pitched, brief vocalizations typical of breakfast requests or attention-seeking after overnight separation',
            'likely_timing': 'Early morning (6-9 AM)',
            'behavioral_context': 'Food demands, attention after separation, routine establishment'
        })

    # Evening Social Pattern (moderate, social characteristics)
    if (avg_pitch < 300 and pitch_variation > 40 and duration > 0.5 and
            spectral_centroid > 1500 and spectral_centroid < 3000):
        indicators.append({
            'context': 'evening_social_pattern',
            'description': 'Evening social characteristics - moderate pitch with expressive variation, typical of social interaction and bonding time',
            'likely_timing': 'Evening (6-10 PM)',
            'behavioral_context': 'Social bonding, play initiation, companionship seeking'
        })

    # Urgency Cluster Analysis
    urgency_score = 0
    if avg_loudness > 0.08:
        urgency_score += 2
    if duration < 0.5:
        urgency_score += 1
    if pitch_variation > 50:
        urgency_score += 2
    if avg_pitch > 400:
        urgency_score += 1

    if urgency_score >= 4:
        indicators.append({
            'context': 'high_urgency_cluster',
            'description': 'High urgency cluster - multiple indicators suggest immediate need or high motivation',
            'urgency_level': 'Critical',
            'behavioral_context': 'Immediate attention required, possible distress or strong need'
        })
    elif urgency_score >= 2:
        indicators.append({
            'context': 'moderate_urgency_cluster',
            'description': 'Moderate urgency cluster - some urgency indicators present',
            'urgency_level': 'Moderate',
            'behavioral_context': 'Attention desired, routine request, mild impatience'
        })

    # Breath Pattern Analysis (stress indicators)
    if (loudness_variation > 0.04 and zcr > 0.08):
        indicators.append({
            'context': 'irregular_breath_pattern',
            'description': 'Irregular breath pattern detected - volume fluctuations and vocal roughness may indicate stress or respiratory effort',
            'health_concern': 'Monitor for stress or respiratory issues',
            'behavioral_context': 'Possible stress, anxiety, or physical discomfort'
        })
    elif (loudness_variation < 0.02 and zcr < 0.04):
        indicators.append({
            'context': 'controlled_breath_pattern',
            'description': 'Controlled breath pattern - steady volume and smooth vocalization indicates calm, deliberate communication',
            'health_indicator': 'Good respiratory control and calm state',
            'behavioral_context': 'Relaxed, controlled communication, good health indicators'
        })

    return indicators


def generate_health_indicators(duration, avg_pitch, pitch_variation, avg_loudness,
                               loudness_variation, spectral_centroid, zcr):
    """
    Generate health-related indicators from vocal analysis
    """
    health_indicators = []

    # Respiratory Health Assessment
    if zcr > 0.12:
        health_indicators.append({
            'category': 'respiratory_concern',
            'severity': 'High',
            'description': 'Significant vocal roughness detected - may indicate respiratory distress, upper respiratory infection, or throat irritation',
            'recommendation': 'Veterinary examination recommended, especially if persistent or accompanied by other symptoms'
        })
    elif zcr > 0.08:
        health_indicators.append({
            'category': 'mild_respiratory_roughness',
            'severity': 'Low',
            'description': 'Mild vocal roughness - could indicate minor throat irritation, recent vocalization strain, or early respiratory symptoms',
            'recommendation': 'Monitor for persistence or worsening, ensure adequate hydration'
        })

    # Vocal Strain Assessment
    if (avg_loudness > 0.15 and loudness_variation > 0.05):
        health_indicators.append({
            'category': 'vocal_strain',
            'severity': 'Medium',
            'description': 'High volume with significant variation may indicate vocal strain from excessive vocalization or underlying discomfort',
            'recommendation': 'Monitor vocalization frequency, check for sources of stress or discomfort'
        })

    # Energy Level Assessment
    if (avg_loudness < 0.02 and spectral_centroid < 1000):
        health_indicators.append({
            'category': 'low_energy_vocalization',
            'severity': 'Medium',
            'description': 'Very quiet, low-energy vocalization may indicate lethargy, illness, or depression',
            'recommendation': 'Monitor for other signs of illness, changes in appetite, or behavioral changes'
        })

    # Neurological Function (pitch control assessment)
    if (pitch_variation > 150 and duration > 1.0):
        health_indicators.append({
            'category': 'pitch_control_concern',
            'severity': 'Medium',
            'description': 'Extreme pitch variation in long vocalizations may indicate neurological issues or extreme distress',
            'recommendation': 'Veterinary evaluation if pattern persists, especially with other neurological symptoms'
        })

    # Age-Related Changes
    if (avg_pitch < 150 and zcr > 0.06 and spectral_centroid < 1200):
        health_indicators.append({
            'category': 'age_related_changes',
            'severity': 'Low',
            'description': 'Low pitch with mild roughness may indicate age-related vocal changes in senior cats',
            'recommendation': 'Normal aging process, but monitor for significant changes or discomfort'
        })

    return health_indicators


def generate_behavioral_insights(interpretation, vocal_patterns, contextual_indicators, health_indicators):
    """
    Generate comprehensive behavioral insights by combining all analysis results
    """
    insights = []

    # Pattern-based insights
    pattern_types = [p['pattern'] for p in vocal_patterns]

    if 'trill_detected' in pattern_types:
        insights.append({
            'category': 'social_behavior',
            'insight': 'Cat is displaying friendly, social behavior with trill vocalizations - indicates comfort and positive social engagement',
            'recommendation': 'Respond positively to encourage continued social bonding'
        })

    if 'chirp_pattern' in pattern_types:
        insights.append({
            'category': 'hunting_behavior',
            'insight': 'Hunting instincts are activated - cat may be observing prey or showing predatory excitement',
            'recommendation': 'Provide interactive toys or hunting-simulation play to satisfy natural instincts'
        })

    if 'purr_meow_combo' in pattern_types:
        insights.append({
            'category': 'comfortable_requesting',
            'insight': 'Cat is in comfortable state while making requests - indicates trust and security in relationship',
            'recommendation': 'Cat feels secure enough to make demands - maintain consistent care routine'
        })

    if 'yowling_pattern' in pattern_types:
        insights.append({
            'category': 'intense_communication',
            'insight': 'Intense vocalization detected - may indicate territorial behavior, mating calls, or significant distress',
            'recommendation': 'Investigate potential causes: territory issues, mating behavior, or sources of distress'
        })

    if 'silent_meow' in pattern_types:
        insights.append({
            'category': 'intimate_communication',
            'insight': 'Silent meow indicates strong human-cat bond and expectation of visual communication response',
            'recommendation': 'Respond with visual cues, gentle touch, or verbal acknowledgment to maintain bond'
        })

    # Contextual insights
    context_types = [c['context'] for c in contextual_indicators]

    if 'high_urgency_cluster' in context_types:
        insights.append({
            'category': 'urgent_needs',
            'insight': 'Multiple urgency indicators suggest immediate attention or care is needed',
            'recommendation': 'Check for immediate needs: food, water, litter box, or potential distress sources'
        })

    if 'morning_demand_pattern' in context_types:
        insights.append({
            'category': 'routine_behavior',
            'insight': 'Morning demand pattern suggests established routine and expectation of morning care',
            'recommendation': 'Maintain consistent morning routine to reduce anxiety and demanding behavior'
        })

    if 'evening_social_pattern' in context_types:
        insights.append({
            'category': 'social_bonding',
            'insight': 'Evening social pattern indicates desire for companionship and bonding time',
            'recommendation': 'Dedicate evening time for interactive play and social bonding activities'
        })

    # Health-based insights
    health_concerns = [h['category']
                       for h in health_indicators if h['severity'] in ['High', 'Medium']]

    if health_concerns:
        insights.append({
            'category': 'health_monitoring',
            'insight': f'Health indicators detected: {", ".join(health_concerns)} - monitoring recommended',
            'recommendation': 'Monitor for additional symptoms and consider veterinary consultation if patterns persist'
        })

    # Combined pattern insights
    if len(vocal_patterns) >= 3:
        insights.append({
            'category': 'complex_communication',
            'insight': 'Multiple vocal patterns detected - cat is using sophisticated communication strategies',
            'recommendation': 'Cat is highly communicative - pay attention to subtle vocal cues and respond appropriately'
        })

    # Confidence-based insights
    if interpretation.get('confidence') == 'Very High':
        insights.append({
            'category': 'analysis_reliability',
            'insight': 'High confidence analysis - vocal patterns are clear and interpretable',
            'recommendation': 'Analysis results are highly reliable - act on recommendations with confidence'
        })
    elif interpretation.get('confidence') in ['Low', 'Very Low']:
        insights.append({
            'category': 'analysis_uncertainty',
            'insight': 'Lower confidence analysis - vocal patterns may be ambiguous or unusual',
            'recommendation': 'Consider additional context and observe other behavioral cues for complete understanding'
        })

    return insights


def interpret_meow(duration, avg_pitch, pitch_variation, avg_loudness,
                   loudness_variation, spectral_centroid, zcr):
    """
    Advanced interpretation of cat meow with detailed vocal characteristics and contextual analysis
    """
    interpretation = {
        'primary_meaning': '',
        'emotional_state': '',
        'urgency_level': '',
        'confidence': '',
        'details': [],
        'vocal_patterns': [],
        'contextual_indicators': [],
        'health_indicators': [],
        'behavioral_insights': [],
        'acoustic_metrics': {
            'duration_ms': round(duration * 1000, 1),
            'pitch_hz': round(avg_pitch, 1),
            'pitch_variation_hz': round(pitch_variation, 1),
            'loudness_db': round(avg_loudness, 3),
            'loudness_variation': round(loudness_variation, 3),
            'spectral_centroid_hz': round(spectral_centroid, 1),
            'zero_crossing_rate': round(zcr, 3)
        }
    }

    # Advanced Vocal Pattern Detection
    vocal_patterns = detect_vocal_patterns(duration, avg_pitch, pitch_variation,
                                           avg_loudness, loudness_variation,
                                           spectral_centroid, zcr)
    interpretation['vocal_patterns'] = vocal_patterns

    # Contextual Analysis
    contextual_indicators = analyze_contextual_indicators(duration, avg_pitch, pitch_variation,
                                                          avg_loudness, loudness_variation,
                                                          spectral_centroid, zcr)
    interpretation['contextual_indicators'] = contextual_indicators

    # Health Assessment
    health_indicators = generate_health_indicators(duration, avg_pitch, pitch_variation,
                                                   avg_loudness, loudness_variation,
                                                   spectral_centroid, zcr)
    interpretation['health_indicators'] = health_indicators

    # Enhanced Duration analysis with behavioral context
    if duration < 0.3:
        interpretation['details'].append(
            f"Very short meow ({duration:.2f}s) - Quick acknowledgment, chirp-like greeting, or attention check. Often used when cat wants to announce presence without being demanding.")
        urgency_base = "Very Low"
        duration_category = "chirp"
    elif duration < 0.8:
        interpretation['details'].append(
            f"Short meow ({duration:.2f}s) - Standard greeting, acknowledgment, or polite request. Classic 'hello' or 'please' vocalization commonly used in human-cat interaction.")
        urgency_base = "Low"
        duration_category = "greeting"
    elif duration < 1.5:
        interpretation['details'].append(
            f"Medium meow ({duration:.2f}s) - Deliberate communication with clear intent. Cat is making effort to convey specific message or request.")
        urgency_base = "Medium"
        duration_category = "communication"
    elif duration < 3.0:
        interpretation['details'].append(
            f"Long meow ({duration:.2f}s) - Emphatic communication indicating strong desire, complaint, or urgent need. Cat is being persistent and expressive.")
        urgency_base = "High"
        duration_category = "complaint"
    else:
        interpretation['details'].append(
            f"Very long meow ({duration:.2f}s) - Intense vocalization suggesting distress, strong complaint, or medical issue. Unusual duration may indicate discomfort.")
        urgency_base = "Very High"
        duration_category = "distress"

    # Enhanced Pitch analysis with frequency ranges
    if avg_pitch > 600:
        interpretation['details'].append(
            f"Very high pitch ({avg_pitch:.0f}Hz) - Kitten-like vocalization designed to trigger nurturing response. Often indicates urgent need for food, attention, or comfort. May suggest anxiety or excitement.")
        emotional_state = "Urgent/Anxious"
        interpretation['primary_meaning'] = "Urgent demand for attention or resources"
        pitch_category = "kitten-like"
    elif avg_pitch > 400:
        interpretation['details'].append(
            f"High pitch ({avg_pitch:.0f}Hz) - Attention-seeking vocalization with friendly intent. Cat is using appealing frequency to engage human interaction. Indicates positive social motivation.")
        emotional_state = "Seeking attention/affection"
        interpretation['primary_meaning'] = "Friendly request for attention or interaction"
        pitch_category = "attention-seeking"
    elif avg_pitch > 250:
        interpretation['details'].append(
            f"Medium-high pitch ({avg_pitch:.0f}Hz) - Balanced communication frequency indicating normal social interaction. Cat is comfortable and engaging in routine communication.")
        emotional_state = "Social/Friendly"
        interpretation['primary_meaning'] = "Normal social communication"
        pitch_category = "social"
    elif avg_pitch > 150:
        interpretation['details'].append(
            f"Medium-low pitch ({avg_pitch:.0f}Hz) - More serious communication tone. Cat may be expressing dissatisfaction, making formal request, or indicating mild stress.")
        emotional_state = "Serious/Formal"
        interpretation['primary_meaning'] = "Serious request or mild complaint"
        pitch_category = "formal"
    else:
        interpretation['details'].append(
            f"Low pitch ({avg_pitch:.0f}Hz) - Deep, adult-like vocalization indicating strong emotion. May suggest complaint, territorial assertion, or physical discomfort. Uncommon in human-directed communication.")
        emotional_state = "Serious/Complaining"
        interpretation['primary_meaning'] = "Strong complaint or territorial assertion"
        pitch_category = "complaint"

    # Enhanced Pitch variation analysis
    if pitch_variation > 100:
        interpretation['details'].append(
            f"Very high pitch variation ({pitch_variation:.0f}Hz range) - Highly expressive, melodic meow with complex emotional content. Cat is using sophisticated vocal modulation to convey nuanced message.")
        expressiveness = "highly_expressive"
        if emotional_state in ["Social/Friendly", "Seeking attention/affection"]:
            emotional_state = "Playful/Expressive"
    elif pitch_variation > 50:
        interpretation['details'].append(
            f"High pitch variation ({pitch_variation:.0f}Hz range) - Expressive meow with emotional inflection. Cat is actively modulating voice to enhance communication effectiveness.")
        expressiveness = "expressive"
        if emotional_state == "Social/Friendly":
            emotional_state = "Expressive/Engaging"
    elif pitch_variation > 25:
        interpretation['details'].append(
            f"Moderate pitch variation ({pitch_variation:.0f}Hz range) - Some vocal expression with controlled modulation. Balanced between monotone and highly expressive.")
        expressiveness = "moderate"
    elif pitch_variation > 10:
        interpretation['details'].append(
            f"Low pitch variation ({pitch_variation:.0f}Hz range) - Stable, controlled vocalization with minimal inflection. Cat is communicating in calm, measured manner.")
        expressiveness = "controlled"
        if emotional_state == "Social/Friendly":
            emotional_state = "Calm/Controlled"
    else:
        interpretation['details'].append(
            f"Very low pitch variation ({pitch_variation:.0f}Hz range) - Monotone vocalization with little emotional inflection. May indicate resignation, illness, or very calm state.")
        expressiveness = "monotone"
        if emotional_state == "Social/Friendly":
            emotional_state = "Subdued/Calm"

    # Enhanced Loudness analysis with decibel context
    # Convert to approximate dB
    loudness_db = 20 * np.log10(avg_loudness + 1e-10)
    if avg_loudness > 0.15:
        interpretation['details'].append(
            f"Very loud meow (amplitude: {avg_loudness:.3f}) - Demanding, assertive vocalization designed to ensure attention. Cat is being insistent and may be frustrated or very motivated.")
        urgency_level = "Very High"
        volume_category = "demanding"
        if interpretation['primary_meaning'] in ["Normal social communication", "Friendly request for attention or interaction"]:
            interpretation['primary_meaning'] = "Insistent demand for attention"
    elif avg_loudness > 0.08:
        interpretation['details'].append(
            f"Loud meow (amplitude: {avg_loudness:.3f}) - Clear, assertive communication with confident delivery. Cat expects response and is comfortable making presence known.")
        urgency_level = "High"
        volume_category = "assertive"
        if interpretation['primary_meaning'] == "Normal social communication":
            interpretation['primary_meaning'] = "Confident request or announcement"
    elif avg_loudness > 0.04:
        interpretation['details'].append(
            f"Moderate volume meow (amplitude: {avg_loudness:.3f}) - Standard communication volume indicating normal comfort level and social engagement.")
        urgency_level = urgency_base
        volume_category = "normal"
    elif avg_loudness > 0.02:
        interpretation['details'].append(
            f"Quiet meow (amplitude: {avg_loudness:.3f}) - Gentle, polite vocalization showing respect for environment. Cat is being considerate or may be uncertain.")
        urgency_level = "Low"
        volume_category = "gentle"
        if interpretation['primary_meaning'] in ["Confident request or announcement", "Normal social communication"]:
            interpretation['primary_meaning'] = "Polite request or gentle greeting"
    else:
        interpretation['details'].append(
            f"Very quiet meow (amplitude: {avg_loudness:.3f}) - Whisper-like vocalization indicating timidity, illness, or very gentle approach. May suggest cat is being cautious.")
        urgency_level = "Very Low"
        volume_category = "whisper"
        if interpretation['primary_meaning'] == "Normal social communication":
            interpretation['primary_meaning'] = "Tentative greeting or weak vocalization"

    # Enhanced Spectral centroid analysis (voice quality)
    if spectral_centroid > 4000:
        interpretation['details'].append(
            f"Very bright, sharp voice quality ({spectral_centroid:.0f}Hz centroid) - Piercing, attention-grabbing vocal quality often associated with excitement, alarm, or urgent needs.")
        voice_quality = "piercing"
        if emotional_state in ["Social/Friendly", "Calm/Controlled"]:
            emotional_state = "Alert/Excited"
    elif spectral_centroid > 2500:
        interpretation['details'].append(
            f"Bright, clear voice quality ({spectral_centroid:.0f}Hz centroid) - Crisp, well-defined vocalization indicating alertness and good vocal health. Typical of engaged, healthy cats.")
        voice_quality = "bright"
        if emotional_state == "Subdued/Calm":
            emotional_state = "Alert/Healthy"
    elif spectral_centroid > 1800:
        interpretation['details'].append(
            f"Balanced voice quality ({spectral_centroid:.0f}Hz centroid) - Well-rounded vocal tone with good harmonic content. Indicates relaxed, comfortable vocalization.")
        voice_quality = "balanced"
    elif spectral_centroid > 1200:
        interpretation['details'].append(
            f"Mellow voice quality ({spectral_centroid:.0f}Hz centroid) - Soft, warm vocal tone suggesting contentment and relaxation. Often heard in comfortable, secure cats.")
        voice_quality = "mellow"
        if emotional_state in ["Serious/Formal", "Serious/Complaining"]:
            emotional_state = "Relaxed/Content"
    else:
        interpretation['details'].append(
            f"Very mellow, deep voice quality ({spectral_centroid:.0f}Hz centroid) - Unusually soft or muffled vocal quality. May indicate extreme relaxation, illness, or respiratory issues.")
        voice_quality = "deep"

    # Enhanced Zero crossing rate analysis (vocal roughness)
    if zcr > 0.15:
        interpretation['details'].append(
            f"Very rough, raspy voice texture (ZCR: {zcr:.3f}) - Significant vocal roughness suggesting possible respiratory distress, illness, or extreme emotional state. Veterinary attention may be needed.")
        vocal_health = "concerning"
        emotional_state = "Distressed/Unwell"
        interpretation['primary_meaning'] = "Possible health issue or extreme distress"
    elif zcr > 0.08:
        interpretation['details'].append(
            f"Rough voice texture (ZCR: {zcr:.3f}) - Noticeable vocal roughness indicating stress, aging, or mild respiratory issues. Monitor for other symptoms.")
        vocal_health = "rough"
        if emotional_state not in ["Distressed/Unwell"]:
            emotional_state = "Stressed/Strained"
            # Update primary meaning to be consistent with stressed state
            if "Friendly request" in interpretation['primary_meaning']:
                interpretation['primary_meaning'] = "Stressed vocalization with underlying request"
            elif "Normal social communication" in interpretation['primary_meaning']:
                interpretation['primary_meaning'] = "Stressed communication attempt"
    elif zcr > 0.04:
        interpretation['details'].append(
            f"Slightly rough voice texture (ZCR: {zcr:.3f}) - Minor vocal roughness within normal range. May indicate mild excitement or normal vocal variation.")
        vocal_health = "normal_rough"
    else:
        interpretation['details'].append(
            f"Smooth voice texture (ZCR: {zcr:.3f}) - Clean, clear vocal production indicating good respiratory health and relaxed vocalization.")
        vocal_health = "smooth"

    # Loudness variation analysis
    if loudness_variation > 0.05:
        interpretation['details'].append(
            f"High volume variation (σ: {loudness_variation:.3f}) - Dynamic volume changes throughout meow, indicating emotional emphasis or uncertainty.")
    elif loudness_variation < 0.02:
        interpretation['details'].append(
            f"Stable volume (σ: {loudness_variation:.3f}) - Consistent loudness throughout vocalization, suggesting controlled, deliberate communication.")

    # Final interpretation
    interpretation['emotional_state'] = emotional_state
    interpretation['urgency_level'] = urgency_level

    # Enhanced confidence scoring with multiple factors
    confidence_score = 0
    feature_count = 0

    # Pitch confidence
    if 100 < avg_pitch < 800:  # Reasonable cat vocal range
        confidence_score += 20
        feature_count += 1

    # Duration confidence
    if 0.1 < duration < 5.0:  # Reasonable meow duration
        confidence_score += 15
        feature_count += 1

    # Spectral centroid confidence
    if 500 < spectral_centroid < 6000:  # Reasonable spectral range
        confidence_score += 15
        feature_count += 1

    # Feature consistency
    if len(interpretation['details']) >= 5:
        confidence_score += 20
    elif len(interpretation['details']) >= 3:
        confidence_score += 10

    # Urgency level determination confidence
    if urgency_level in ["Very High", "High", "Very Low"]:
        confidence_score += 15
    elif urgency_level in ["Medium", "Low"]:
        confidence_score += 10

    # Emotional state determination confidence
    if emotional_state not in ["Social/Friendly", "Neutral"]:
        confidence_score += 15

    # Adjust confidence based on feature count
    if feature_count >= 3:
        confidence_score += 10

    if confidence_score >= 85:
        interpretation['confidence'] = "Very High"
    elif confidence_score >= 70:
        interpretation['confidence'] = "High"
    elif confidence_score >= 50:
        interpretation['confidence'] = "Medium"
    elif confidence_score >= 30:
        interpretation['confidence'] = "Low"
    else:
        interpretation['confidence'] = "Very Low"

    # Generate Comprehensive Behavioral Insights
    behavioral_insights = generate_behavioral_insights(interpretation, vocal_patterns,
                                                       contextual_indicators, health_indicators)
    interpretation['behavioral_insights'] = behavioral_insights

    # Enhance details with pattern-specific information
    for pattern in vocal_patterns:
        interpretation['details'].append(f"🎵 {pattern['description']}")

    for indicator in contextual_indicators:
        interpretation['details'].append(f"⏰ {indicator['description']}")

    for health_indicator in health_indicators:
        if health_indicator['severity'] in ['High', 'Medium']:
            interpretation['details'].append(
                f"🏥 {health_indicator['description']}")

    return interpretation


def print_analysis_results(interpretation):
    """
    Print the comprehensive meow analysis results in a readable format
    """
    print("🐱 ADVANCED CAT MEOW ANALYSIS RESULTS 🐱")
    print("=" * 60)
    print(f"Primary Meaning: {interpretation['primary_meaning']}")
    print(f"Emotional State: {interpretation['emotional_state']}")
    print(f"Urgency Level: {interpretation['urgency_level']}")
    print(f"Analysis Confidence: {interpretation['confidence']}")

    # Acoustic Metrics
    if 'acoustic_metrics' in interpretation:
        print(f"\n🔬 ACOUSTIC METRICS:")
        metrics = interpretation['acoustic_metrics']
        print(f"  Duration: {metrics['duration_ms']} ms")
        print(f"  Pitch: {metrics['pitch_hz']} Hz")
        print(f"  Pitch Variation: {metrics['pitch_variation_hz']} Hz")
        print(f"  Loudness: {metrics['loudness_db']}")
        print(f"  Spectral Centroid: {metrics['spectral_centroid_hz']} Hz")
        print(f"  Zero Crossing Rate: {metrics['zero_crossing_rate']}")

    # Vocal Patterns
    if interpretation.get('vocal_patterns'):
        print(f"\n🎵 VOCAL PATTERNS DETECTED:")
        for pattern in interpretation['vocal_patterns']:
            print(
                f"  • {pattern['pattern'].replace('_', ' ').title()}: {pattern['description']}")
            print(f"    Behavioral Meaning: {pattern['behavioral_meaning']}")
            print(f"    Confidence: {pattern['confidence']}")

    # Contextual Indicators
    if interpretation.get('contextual_indicators'):
        print(f"\n⏰ CONTEXTUAL ANALYSIS:")
        for indicator in interpretation['contextual_indicators']:
            print(
                f"  • {indicator['context'].replace('_', ' ').title()}: {indicator['description']}")
            if 'likely_timing' in indicator:
                print(f"    Likely Timing: {indicator['likely_timing']}")
            if 'behavioral_context' in indicator:
                print(f"    Context: {indicator['behavioral_context']}")

    # Health Indicators
    if interpretation.get('health_indicators'):
        print(f"\n🏥 HEALTH ASSESSMENT:")
        for health in interpretation['health_indicators']:
            severity_emoji = "🔴" if health['severity'] == 'High' else "🟡" if health['severity'] == 'Medium' else "🟢"
            print(
                f"  {severity_emoji} {health['category'].replace('_', ' ').title()} ({health['severity']} Priority)")
            print(f"    {health['description']}")
            print(f"    Recommendation: {health['recommendation']}")

    # Behavioral Insights
    if interpretation.get('behavioral_insights'):
        print(f"\n🧠 BEHAVIORAL INSIGHTS:")
        for insight in interpretation['behavioral_insights']:
            print(
                f"  • {insight['category'].replace('_', ' ').title()}: {insight['insight']}")
            print(f"    💡 Recommendation: {insight['recommendation']}")

    print("\nDetailed Analysis:")
    for detail in interpretation['details']:
        print(f"• {detail}")

    print("\n" + "=" * 60)
    print("Note: This analysis combines acoustic science with feline behavioral research.")
    print("Individual cats may have unique vocal characteristics and personal communication styles.")
    print("For health concerns, consult with a veterinarian for professional assessment.")


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
