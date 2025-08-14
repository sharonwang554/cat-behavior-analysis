#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced meow analysis
"""

from analysis import analyze_cat_meow, print_analysis_results
import glob
import os


def test_enhanced_analysis():
    """Test the enhanced analysis on existing audio files"""

    # Look for WAV files in extracted_audio directory
    audio_files = glob.glob("extracted_audio/*_meow_segment_*.wav")
    audio_files.sort()

    if not audio_files:
        print("❌ No meow segment files found in extracted_audio directory!")
        return

    # Test with first few files to show the enhanced analysis
    test_files = audio_files[:3]  # Just test first 3 files

    print("🐱 TESTING ENHANCED MEOW ANALYSIS 🐱")
    print("=" * 60)
    print(f"Testing with {len(test_files)} audio files")
    print("=" * 60)

    for i, file_path in enumerate(test_files, 1):
        filename = os.path.basename(file_path)
        print(f"\n📁 ANALYZING {filename.upper()} ({i}/{len(test_files)})")
        print("-" * 50)

        try:
            results = analyze_cat_meow(file_path)
            if results:
                print_analysis_results(results)

                # Show the new acoustic metrics
                if 'acoustic_metrics' in results:
                    print("\n🔬 DETAILED ACOUSTIC METRICS:")
                    metrics = results['acoustic_metrics']
                    print(f"  Duration: {metrics['duration_ms']} ms")
                    print(f"  Pitch: {metrics['pitch_hz']} Hz")
                    print(
                        f"  Pitch Variation: {metrics['pitch_variation_hz']} Hz")
                    print(f"  Loudness: {metrics['loudness_db']}")
                    print(
                        f"  Spectral Centroid: {metrics['spectral_centroid_hz']} Hz")
                    print(
                        f"  Zero Crossing Rate: {metrics['zero_crossing_rate']}")
            else:
                print("❌ Analysis failed for this file")

        except Exception as e:
            print(f"❌ Error analyzing {filename}: {e}")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    test_enhanced_analysis()
