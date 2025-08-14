#!/usr/bin/env python3
"""
Test script to verify the web interface fixes are working
"""

import json
import os
from web_app import WebCatAnalyzer


def test_activity_level_extraction():
    """Test that activity levels are properly extracted from enhanced analysis"""
    print("🧪 Testing Activity Level Extraction")
    print("=" * 40)

    # Create a test analyzer
    analyzer = WebCatAnalyzer()

    # Test with sample enhanced data
    enhanced_data = {
        'video_name': 'test_cat',
        'timestamp': '2025-08-14T13:34:54.578749',
        'enhanced_interpretation': {
            'overall_behavior': 'highly_active',
            'activity_level': 'high'
        },
        'ml_analysis': {
            'ml_prediction': 'excited',
            'feature_analysis': ['High activity level detected - cat is very active']
        },
        'traditional_analysis': {
            'primary_meaning': 'Test meaning',
            'emotional_state': 'Playful/Expressive',
            'acoustic_metrics': {
                'duration_ms': 30560.0
            }
        }
    }

    # Test conversion
    converted = analyzer.convert_enhanced_to_regular_format(enhanced_data)

    print(
        f"Original activity_level: {enhanced_data['enhanced_interpretation']['activity_level']}")
    print(
        f"Converted dominant_activity: {converted['visual_analysis']['dominant_activity']}")

    # Test with different scenarios
    test_cases = [
        {
            'name': 'High Activity from enhanced_interpretation',
            'data': {'enhanced_interpretation': {'activity_level': 'high'}},
            'expected': 'High'
        },
        {
            'name': 'High Activity from ML prediction (excited)',
            'data': {'ml_analysis': {'ml_prediction': 'excited'}},
            'expected': 'High'
        },
        {
            'name': 'High Activity from feature analysis',
            'data': {'ml_analysis': {'feature_analysis': ['High activity level detected']}},
            'expected': 'High'
        },
        {
            'name': 'High Activity from overall behavior',
            'data': {'enhanced_interpretation': {'overall_behavior': 'highly_active'}},
            'expected': 'High'
        },
        {
            'name': 'Low Activity from ML prediction (calm)',
            'data': {'ml_analysis': {'ml_prediction': 'calm'}},
            'expected': 'Low'
        },
        {
            'name': 'Default Medium Activity',
            'data': {},
            'expected': 'Medium'
        }
    ]

    print("\\n🧪 Testing Different Activity Level Scenarios:")
    for test_case in test_cases:
        test_data = {
            'video_name': 'test',
            'timestamp': '2025-08-14T13:34:54.578749',
            'traditional_analysis': {},
            **test_case['data']
        }

        result = analyzer.convert_enhanced_to_regular_format(test_data)
        activity = result['visual_analysis']['dominant_activity']

        status = "✅" if activity == test_case['expected'] else "❌"
        print(
            f"{status} {test_case['name']}: {activity} (expected: {test_case['expected']})")

    print("\\n" + "=" * 40)
    print("✅ Activity level extraction test completed!")


def test_existing_results():
    """Test loading and converting existing results"""
    print("\\n🧪 Testing Existing Results Loading")
    print("=" * 40)

    analyzer = WebCatAnalyzer()
    results = analyzer.load_results()

    print(f"Loaded {len(results)} results:")
    for video_name, result in results.items():
        activity = result.get('visual_analysis', {}).get(
            'dominant_activity', 'Unknown')
        emotion = result.get('audio_analysis', {}).get(
            'emotional_state', 'Unknown')
        print(f"📹 {video_name}:")
        print(f"   Activity Level: {activity}")
        print(f"   Emotional State: {emotion}")
        print()

    print("=" * 40)
    print("✅ Results loading test completed!")


if __name__ == "__main__":
    test_activity_level_extraction()
    test_existing_results()
