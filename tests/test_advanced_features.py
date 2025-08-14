#!/usr/bin/env python3
"""
Comprehensive test of all advanced cat meow analysis features
"""

from analysis import analyze_cat_meow, print_analysis_results
import json
import glob
import os


def test_advanced_vocal_patterns():
    """Test the advanced vocal pattern detection on various audio samples"""

    print("🐱 COMPREHENSIVE ADVANCED MEOW ANALYSIS TEST 🐱")
    print("=" * 70)

    # Get a variety of audio files to test different patterns
    audio_files = glob.glob("extracted_audio/*_meow_segment_*.wav")

    if not audio_files:
        print("❌ No meow segment files found!")
        return

    # Test different types of meows
    test_files = audio_files[:5]  # Test first 5 files

    print(
        f"Testing {len(test_files)} audio samples for advanced pattern detection...")
    print("=" * 70)

    all_results = []

    for i, file_path in enumerate(test_files, 1):
        filename = os.path.basename(file_path)
        print(f"\n📁 ANALYZING {filename.upper()} ({i}/{len(test_files)})")
        print("-" * 60)

        try:
            # Analyze the meow
            results = analyze_cat_meow(file_path)

            if results:
                # Print comprehensive results
                print_analysis_results(results)

                # Store results for summary
                all_results.append({
                    'filename': filename,
                    'results': results
                })

                # Show JSON structure for one example
                if i == 1:
                    print(f"\n📋 JSON STRUCTURE EXAMPLE:")
                    print("-" * 40)
                    print(json.dumps({
                        'vocal_patterns': results.get('vocal_patterns', []),
                        'contextual_indicators': results.get('contextual_indicators', []),
                        'health_indicators': results.get('health_indicators', []),
                        'behavioral_insights': results.get('behavioral_insights', [])
                    }, indent=2))
            else:
                print("❌ Analysis failed for this file")

        except Exception as e:
            print(f"❌ Error analyzing {filename}: {e}")

        print("\n" + "=" * 70)

    # Generate summary report
    print(f"\n📊 ANALYSIS SUMMARY REPORT")
    print("=" * 70)

    if all_results:
        # Count pattern types detected
        pattern_counts = {}
        context_counts = {}
        health_counts = {}
        insight_counts = {}

        for result in all_results:
            r = result['results']

            # Count vocal patterns
            for pattern in r.get('vocal_patterns', []):
                pattern_type = pattern['pattern']
                pattern_counts[pattern_type] = pattern_counts.get(
                    pattern_type, 0) + 1

            # Count contextual indicators
            for context in r.get('contextual_indicators', []):
                context_type = context['context']
                context_counts[context_type] = context_counts.get(
                    context_type, 0) + 1

            # Count health indicators
            for health in r.get('health_indicators', []):
                health_type = health['category']
                health_counts[health_type] = health_counts.get(
                    health_type, 0) + 1

            # Count behavioral insights
            for insight in r.get('behavioral_insights', []):
                insight_type = insight['category']
                insight_counts[insight_type] = insight_counts.get(
                    insight_type, 0) + 1

        print(f"🎵 VOCAL PATTERNS DETECTED:")
        if pattern_counts:
            for pattern, count in pattern_counts.items():
                print(
                    f"  • {pattern.replace('_', ' ').title()}: {count} occurrences")
        else:
            print("  • No specific vocal patterns detected in this sample")

        print(f"\n⏰ CONTEXTUAL INDICATORS:")
        if context_counts:
            for context, count in context_counts.items():
                print(
                    f"  • {context.replace('_', ' ').title()}: {count} occurrences")
        else:
            print("  • No specific contextual patterns detected")

        print(f"\n🏥 HEALTH INDICATORS:")
        if health_counts:
            for health, count in health_counts.items():
                print(
                    f"  • {health.replace('_', ' ').title()}: {count} occurrences")
        else:
            print("  • No health concerns detected")

        print(f"\n🧠 BEHAVIORAL INSIGHTS:")
        if insight_counts:
            for insight, count in insight_counts.items():
                print(
                    f"  • {insight.replace('_', ' ').title()}: {count} occurrences")
        else:
            print("  • Standard behavioral patterns detected")

        # Overall assessment
        total_patterns = sum(pattern_counts.values())
        total_contexts = sum(context_counts.values())
        total_health = sum(health_counts.values())
        total_insights = sum(insight_counts.values())

        print(f"\n📈 OVERALL ASSESSMENT:")
        print(f"  • Total Vocal Patterns: {total_patterns}")
        print(f"  • Total Contextual Indicators: {total_contexts}")
        print(f"  • Total Health Indicators: {total_health}")
        print(f"  • Total Behavioral Insights: {total_insights}")
        print(
            f"  • Analysis Depth Score: {total_patterns + total_contexts + total_health + total_insights}")

        if total_health > 0:
            print(f"\n⚠️ HEALTH MONITORING RECOMMENDATION:")
            print(
                f"  Health indicators were detected. Monitor cat for additional symptoms")
            print(f"  and consider veterinary consultation if patterns persist.")

    print("\n" + "=" * 70)
    print("✅ Advanced analysis test completed!")
    print("The system now provides:")
    print("  🎵 Detailed vocal pattern recognition")
    print("  ⏰ Contextual timing and urgency analysis")
    print("  🏥 Health monitoring and early warning indicators")
    print("  🧠 Comprehensive behavioral insights and recommendations")
    print("  📊 Scientific acoustic metrics with behavioral context")


if __name__ == "__main__":
    test_advanced_vocal_patterns()
