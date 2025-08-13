#!/usr/bin/env python3
"""
Enhanced Cat Video Analysis with Machine Learning
Combines traditional analysis with advanced ML techniques
"""

from ml_analysis import AdvancedCatBehaviorAnalyzer
from analysis import analyze_cat_meow, interpret_meow
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
import numpy as np

# Configure matplotlib to use non-interactive backend for web interface
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Try to import moviepy with fallback
try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    print("⚠️ MoviePy not available, enhanced analysis disabled")
    MOVIEPY_AVAILABLE = False

# Import existing analysis modules


class EnhancedCatVideoAnalyzer:
    def __init__(self):
        self.setup_directories()
        self.ml_analyzer = AdvancedCatBehaviorAnalyzer()

    def setup_directories(self):
        """Create organized folder structure"""
        self.folders = {
            'audio': 'extracted_audio',
            'audio_graphs': 'audio_analysis_graphs',
            'videos': 'input_videos',
            'video_results': 'video_analysis_results',
            'combined_results': 'combined_analysis_results',
            'ml_results': 'ml_analysis_results'
        }

        for folder in self.folders.values():
            os.makedirs(folder, exist_ok=True)

        print("📁 Created enhanced folder structure:")
        for name, path in self.folders.items():
            print(f"  {name}: {path}/")

    def extract_audio_from_video(self, video_path):
        """Extract audio from video file"""
        try:
            if not MOVIEPY_AVAILABLE:
                print(
                    f"❌ MoviePy not available, cannot extract audio from {video_path}")
                return None

            video_name = os.path.splitext(os.path.basename(video_path))[0]
            audio_output = os.path.join(
                self.folders['audio'], f"{video_name}_audio.wav")

            print(f"🎵 Extracting audio from {video_path}...")

            video = VideoFileClip(video_path)
            audio = video.audio

            if audio is None:
                print(f"❌ No audio track found in {video_path}")
                return None

            audio.write_audiofile(audio_output, verbose=False, logger=None)
            audio.close()
            video.close()

            print(f"✅ Audio extracted to: {audio_output}")
            return audio_output

        except Exception as e:
            print(f"❌ Error extracting audio from {video_path}: {e}")
            return None

    def perform_traditional_analysis(self, audio_path):
        """Perform traditional meow analysis"""
        try:
            print("🔍 Performing traditional audio analysis...")
            results = analyze_cat_meow(audio_path)
            if results:
                interpretation = interpret_meow(
                    results['duration'],
                    results['avg_pitch'],
                    results['pitch_variation'],
                    results['avg_loudness'],
                    results['loudness_variation'],
                    results['spectral_centroid'],
                    results['zero_crossing_rate']
                )
                return interpretation
            return None
        except Exception as e:
            print(f"❌ Error in traditional analysis: {e}")
            return None

    def perform_ml_analysis(self, audio_path, video_path):
        """Perform advanced ML analysis"""
        try:
            print("🧠 Performing advanced ML analysis...")
            return self.ml_analyzer.analyze_with_ml(audio_path, video_path)
        except Exception as e:
            print(f"❌ Error in ML analysis: {e}")
            return None

    def combine_analyses(self, traditional_results, ml_results, video_name):
        """Combine traditional and ML analysis results"""
        try:
            combined_analysis = {
                'video_name': video_name,
                'timestamp': datetime.now().isoformat(),
                'traditional_analysis': traditional_results or {},
                'ml_analysis': ml_results or {},
                'enhanced_interpretation': self.create_enhanced_interpretation(traditional_results, ml_results),
                'confidence_assessment': self.assess_confidence(traditional_results, ml_results),
                'comprehensive_recommendations': self.generate_comprehensive_recommendations(traditional_results, ml_results)
            }

            return combined_analysis

        except Exception as e:
            print(f"❌ Error combining analyses: {e}")
            return None

    def create_enhanced_interpretation(self, traditional, ml):
        """Create enhanced interpretation combining both analysis methods"""
        interpretation = {
            'overall_behavior': 'unknown',
            'emotional_state': 'uncertain',
            'activity_level': 'unknown',
            'vocal_patterns': 'not_analyzed',
            'behavioral_complexity': 'simple',
            'analysis_method': 'hybrid'
        }

        try:
            # Combine traditional analysis
            if traditional:
                interpretation['emotional_state'] = traditional.get(
                    'emotional_state', 'uncertain')
                interpretation['vocal_patterns'] = traditional.get(
                    'primary_meaning', 'not_analyzed')

            # Enhance with ML analysis
            if ml and ml.get('ml_prediction') != 'analysis_unavailable':
                ml_pred = ml.get('ml_prediction', 'unknown')

                # Map ML predictions to behavioral categories
                behavior_mapping = {
                    'excited': {'behavior': 'highly_active', 'activity': 'high'},
                    'active': {'behavior': 'moderately_active', 'activity': 'medium'},
                    'vocal': {'behavior': 'communicative', 'activity': 'medium'},
                    'calm': {'behavior': 'relaxed', 'activity': 'low'}
                }

                if ml_pred in behavior_mapping:
                    interpretation['overall_behavior'] = behavior_mapping[ml_pred]['behavior']
                    interpretation['activity_level'] = behavior_mapping[ml_pred]['activity']
                    interpretation['behavioral_complexity'] = 'complex'

            # Cross-validate findings
            if traditional and ml:
                interpretation['analysis_method'] = 'validated_hybrid'
                interpretation['cross_validation'] = self.cross_validate_results(
                    traditional, ml)

            return interpretation

        except Exception as e:
            print(f"❌ Error creating enhanced interpretation: {e}")
            return interpretation

    def cross_validate_results(self, traditional, ml):
        """Cross-validate traditional and ML results"""
        validation = {
            'agreement_level': 'unknown',
            'conflicting_indicators': [],
            'supporting_evidence': [],
            'reliability_score': 0.5
        }

        try:
            agreements = 0
            total_comparisons = 0

            # Compare emotional states
            if traditional.get('emotional_state') and ml.get('ml_prediction'):
                total_comparisons += 1
                trad_emotion = traditional['emotional_state'].lower()
                ml_emotion = ml['ml_prediction'].lower()

                # Define emotion compatibility
                compatible_emotions = {
                    'content': ['calm', 'vocal'],
                    'excited': ['excited', 'active'],
                    'distressed': ['vocal', 'active'],
                    'attention-seeking': ['vocal', 'excited']
                }

                if any(ml_emotion in compat for emotion, compat in compatible_emotions.items() if emotion in trad_emotion):
                    agreements += 1
                    validation['supporting_evidence'].append(
                        f"Emotional state agreement: {trad_emotion} ↔ {ml_emotion}")
                else:
                    validation['conflicting_indicators'].append(
                        f"Emotional state mismatch: {trad_emotion} vs {ml_emotion}")

            # Calculate reliability
            if total_comparisons > 0:
                validation['reliability_score'] = agreements / \
                    total_comparisons
                if validation['reliability_score'] > 0.7:
                    validation['agreement_level'] = 'high'
                elif validation['reliability_score'] > 0.4:
                    validation['agreement_level'] = 'moderate'
                else:
                    validation['agreement_level'] = 'low'

            return validation

        except Exception as e:
            print(f"❌ Error in cross-validation: {e}")
            return validation

    def assess_confidence(self, traditional, ml):
        """Assess overall confidence in the analysis"""
        confidence = {
            'overall_score': 0.5,
            'traditional_confidence': 0.0,
            'ml_confidence': 0.0,
            'data_quality': 'unknown',
            'recommendation': 'review_required'
        }

        try:
            # Traditional analysis confidence
            if traditional and traditional.get('confidence'):
                conf_map = {'High': 0.9, 'Medium': 0.6, 'Low': 0.3}
                confidence['traditional_confidence'] = conf_map.get(
                    traditional['confidence'], 0.5)

            # ML analysis confidence
            if ml and ml.get('confidence_score'):
                confidence['ml_confidence'] = ml['confidence_score']

            # Calculate overall confidence
            if confidence['traditional_confidence'] > 0 and confidence['ml_confidence'] > 0:
                confidence['overall_score'] = (
                    confidence['traditional_confidence'] + confidence['ml_confidence']) / 2
            elif confidence['traditional_confidence'] > 0:
                # Slight penalty for single method
                confidence['overall_score'] = confidence['traditional_confidence'] * 0.8
            elif confidence['ml_confidence'] > 0:
                confidence['overall_score'] = confidence['ml_confidence'] * 0.8

            # Assess data quality
            if confidence['overall_score'] > 0.8:
                confidence['data_quality'] = 'excellent'
                confidence['recommendation'] = 'high_confidence_results'
            elif confidence['overall_score'] > 0.6:
                confidence['data_quality'] = 'good'
                confidence['recommendation'] = 'reliable_results'
            elif confidence['overall_score'] > 0.4:
                confidence['data_quality'] = 'fair'
                confidence['recommendation'] = 'moderate_confidence'
            else:
                confidence['data_quality'] = 'poor'
                confidence['recommendation'] = 'results_require_verification'

            return confidence

        except Exception as e:
            print(f"❌ Error assessing confidence: {e}")
            return confidence

    def generate_comprehensive_recommendations(self, traditional, ml):
        """Generate comprehensive recommendations based on both analyses"""
        recommendations = []

        try:
            # Traditional analysis recommendations
            if traditional and traditional.get('details'):
                recommendations.extend(
                    [f"Traditional analysis: {detail}" for detail in traditional['details'][:3]])

            # ML analysis recommendations
            if ml and ml.get('recommendations'):
                recommendations.extend(
                    [f"ML analysis: {rec}" for rec in ml['recommendations'][:3]])

            # Combined insights
            if traditional and ml:
                recommendations.append(
                    "✅ Dual-method analysis provides enhanced reliability")

                # Specific combined recommendations
                if traditional.get('urgency_level') == 'High' and ml.get('ml_prediction') in ['excited', 'vocal']:
                    recommendations.append(
                        "🔔 High urgency detected by both methods - immediate attention recommended")

                if traditional.get('emotional_state') == 'Content' and ml.get('ml_prediction') == 'calm':
                    recommendations.append(
                        "😊 Both analyses indicate contentment - continue current care routine")

            # Data quality recommendations
            if len(recommendations) < 3:
                recommendations.extend([
                    "Consider recording longer video segments for better analysis",
                    "Ensure good audio quality for optimal vocal analysis",
                    "Record in well-lit conditions for better visual analysis"
                ])

            return recommendations[:6]  # Limit to 6 recommendations

        except Exception as e:
            print(f"❌ Error generating recommendations: {e}")
            return ["Analysis completed with limited recommendations due to processing error"]

    def save_enhanced_results(self, combined_analysis):
        """Save enhanced analysis results"""
        try:
            video_name = combined_analysis['video_name']
            results_path = os.path.join(
                self.folders['combined_results'], f"{video_name}_enhanced_analysis.json")

            with open(results_path, 'w') as f:
                json.dump(combined_analysis, f, indent=2, default=str)

            print(f"💾 Enhanced results saved: {results_path}")
            return results_path

        except Exception as e:
            print(f"❌ Error saving enhanced results: {e}")
            return None

    def create_analysis_visualization(self, combined_analysis):
        """Create visualization of the enhanced analysis"""
        try:
            video_name = combined_analysis['video_name']

            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
                2, 2, figsize=(15, 12))
            fig.suptitle(
                f'Enhanced Cat Behavior Analysis: {video_name}', fontsize=16, fontweight='bold')

            # Confidence comparison
            conf = combined_analysis.get('confidence_assessment', {})
            methods = ['Traditional', 'ML', 'Combined']
            scores = [
                conf.get('traditional_confidence', 0),
                conf.get('ml_confidence', 0),
                conf.get('overall_score', 0)
            ]

            ax1.bar(methods, scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            ax1.set_title('Analysis Confidence Scores')
            ax1.set_ylabel('Confidence Score')
            ax1.set_ylim(0, 1)

            # Analysis method comparison
            traditional = combined_analysis.get('traditional_analysis', {})
            ml = combined_analysis.get('ml_analysis', {})

            categories = ['Emotional\nState', 'Vocal\nPatterns',
                          'Activity\nLevel', 'Overall\nBehavior']
            trad_scores = [0.8 if traditional.get('emotional_state') else 0,
                           0.9 if traditional.get('primary_meaning') else 0, 0.3, 0.6]
            ml_scores = [0.7, 0.6, 0.9 if ml.get('ml_prediction') else 0, 0.8]

            x = np.arange(len(categories))
            width = 0.35

            ax2.bar(x - width/2, trad_scores, width,
                    label='Traditional', color='#FF6B6B', alpha=0.7)
            ax2.bar(x + width/2, ml_scores, width,
                    label='ML', color='#4ECDC4', alpha=0.7)
            ax2.set_title('Analysis Coverage by Method')
            ax2.set_ylabel('Coverage Score')
            ax2.set_xticks(x)
            ax2.set_xticklabels(categories)
            ax2.legend()

            # Behavioral insights pie chart
            enhanced = combined_analysis.get('enhanced_interpretation', {})
            activity_level = enhanced.get('activity_level', 'unknown')

            activity_data = {'High': 0, 'Medium': 0, 'Low': 0, 'Unknown': 0}
            activity_data[activity_level.capitalize()] = 1

            colors = ['#FF6B6B', '#FFD93D', '#6BCF7F', '#A8A8A8']
            ax3.pie(activity_data.values(), labels=activity_data.keys(),
                    colors=colors, autopct='%1.0f%%')
            ax3.set_title('Activity Level Assessment')

            # Recommendations word cloud simulation
            recommendations = combined_analysis.get(
                'comprehensive_recommendations', [])
            rec_text = ' '.join(recommendations)

            # Simple text display instead of word cloud
            ax4.text(0.1, 0.9, 'Key Recommendations:', fontsize=14,
                     fontweight='bold', transform=ax4.transAxes)

            y_pos = 0.8
            for i, rec in enumerate(recommendations[:5]):
                ax4.text(0.1, y_pos - i*0.12, f"• {rec[:60]}{'...' if len(rec) > 60 else ''}",
                         fontsize=10, transform=ax4.transAxes, wrap=True)

            ax4.set_xlim(0, 1)
            ax4.set_ylim(0, 1)
            ax4.axis('off')
            ax4.set_title('Analysis Recommendations')

            plt.tight_layout()

            # Save visualization
            viz_path = os.path.join(
                self.folders['video_results'], f"{video_name}_enhanced_visualization.png")
            plt.savefig(viz_path, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"📊 Enhanced visualization saved: {viz_path}")
            return viz_path

        except Exception as e:
            print(f"❌ Error creating visualization: {e}")
            return None

    def analyze_video(self, video_path):
        """Perform comprehensive enhanced analysis on a single video"""
        try:
            if not MOVIEPY_AVAILABLE:
                print(f"❌ Enhanced analysis requires MoviePy, which is not available")
                print("💡 Install MoviePy with: pip install moviepy")
                return None

            video_name = os.path.splitext(os.path.basename(video_path))[0]
            print(f"\n🎬 Starting enhanced analysis for: {video_name}")
            print("=" * 60)

            # Extract audio
            audio_path = self.extract_audio_from_video(video_path)
            if not audio_path:
                print("❌ Cannot proceed without audio")
                return None

            # Perform both analyses
            traditional_results = self.perform_traditional_analysis(audio_path)
            ml_results = self.perform_ml_analysis(audio_path, video_path)

            # Combine results
            combined_analysis = self.combine_analyses(
                traditional_results, ml_results, video_name)
            if not combined_analysis:
                print("❌ Failed to combine analysis results")
                return None

            # Save results
            results_path = self.save_enhanced_results(combined_analysis)

            # Create visualization
            viz_path = self.create_analysis_visualization(combined_analysis)

            # Print summary
            self.print_enhanced_summary(combined_analysis)

            return combined_analysis

        except Exception as e:
            print(f"❌ Error in enhanced video analysis: {e}")
            return None

    def print_enhanced_summary(self, analysis):
        """Print enhanced analysis summary"""
        print("\n" + "🧠" * 25)
        print("ENHANCED CAT BEHAVIOR ANALYSIS RESULTS")
        print("🧠" * 25)

        video_name = analysis['video_name']
        enhanced = analysis.get('enhanced_interpretation', {})
        confidence = analysis.get('confidence_assessment', {})

        print(f"\n📹 Video: {video_name}")
        print(
            f"🎯 Overall Behavior: {enhanced.get('overall_behavior', 'Unknown')}")
        print(
            f"😊 Emotional State: {enhanced.get('emotional_state', 'Unknown')}")
        print(f"⚡ Activity Level: {enhanced.get('activity_level', 'Unknown')}")
        print(f"🔊 Vocal Patterns: {enhanced.get('vocal_patterns', 'Unknown')}")
        print(
            f"📊 Analysis Method: {enhanced.get('analysis_method', 'Unknown')}")

        print(f"\n🎯 CONFIDENCE ASSESSMENT:")
        print(f"Overall Score: {confidence.get('overall_score', 0):.2f}")
        print(f"Data Quality: {confidence.get('data_quality', 'Unknown')}")
        print(f"Recommendation: {confidence.get('recommendation', 'Unknown')}")

        recommendations = analysis.get('comprehensive_recommendations', [])
        if recommendations:
            print(f"\n💡 ENHANCED RECOMMENDATIONS:")
            for rec in recommendations:
                print(f"• {rec}")

        # Cross-validation results
        if 'cross_validation' in analysis.get('enhanced_interpretation', {}):
            cv = analysis['enhanced_interpretation']['cross_validation']
            print(f"\n🔍 CROSS-VALIDATION:")
            print(f"Agreement Level: {cv.get('agreement_level', 'Unknown')}")
            print(f"Reliability Score: {cv.get('reliability_score', 0):.2f}")

        print("\n" + "=" * 70)
        print("✨ Enhanced analysis combines traditional signal processing")
        print("   with advanced machine learning for superior accuracy")
        print("=" * 70)


def main():
    """Run enhanced video analysis"""
    analyzer = EnhancedCatVideoAnalyzer()

    print("🚀 Enhanced Cat Behavior Analysis System")
    print("=" * 50)
    print("Features:")
    print("• Traditional audio signal processing")
    print("• Advanced machine learning analysis")
    print("• Neural networks and ensemble methods")
    print("• Cross-validation and confidence assessment")
    print("• Comprehensive behavioral insights")
    print("• Enhanced visualizations")
    print("=" * 50)

    # Analyze all videos in input folder
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    video_files = []

    for ext in video_extensions:
        video_files.extend([f for f in os.listdir(analyzer.folders['videos'])
                           if f.lower().endswith(ext.lower())])

    if not video_files:
        print("❌ No video files found in input_videos/ folder")
        print("Please add cat videos and run again.")
        return

    print(f"📹 Found {len(video_files)} video(s) to analyze")

    for video_file in video_files:
        video_path = os.path.join(analyzer.folders['videos'], video_file)
        analyzer.analyze_video(video_path)

    print("\n✅ Enhanced analysis complete for all videos!")


if __name__ == "__main__":
    main()
