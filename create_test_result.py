#!/usr/bin/env python3
"""
Create a test result with Relaxed/Content emotional state to test purple color
"""

import json
import os
from datetime import datetime


def create_test_result():
    """Create a test analysis result with Relaxed/Content emotional state"""
    print("🧪 Creating Test Result with Relaxed/Content State")
    print("=" * 50)

    # Create a test result with Relaxed/Content emotional state
    test_result = {
        "video_name": "test_relaxed_cat",
        "timestamp": datetime.now().isoformat(),
        "traditional_analysis": {
            "primary_meaning": "Gentle contentment vocalization",
            "emotional_state": "Relaxed/Content",
            "urgency_level": "Very Low",
            "confidence": "High",
            "details": [
                "Soft, mellow meow indicating contentment and relaxation",
                "Low pitch variation suggesting calm state",
                "Gentle volume indicating comfortable communication"
            ],
            "acoustic_metrics": {
                "duration_ms": 2500.0,
                "pitch_hz": "180.0",
                "pitch_variation_hz": "45.0",
                "loudness_db": "0.012",
                "loudness_variation": "0.003",
                "spectral_centroid_hz": 1400.0,
                "zero_crossing_rate": 0.018
            }
        },
        "ml_analysis": {
            "timestamp": datetime.now().isoformat(),
            "ml_prediction": "calm",
            "model_confidences": {
                "random_forest": 0.8,
                "gradient_boost": 0.75,
                "svm": 0.7
            },
            "feature_analysis": [
                "Low activity level detected - cat appears calm or resting"
            ],
            "behavioral_insights": {
                "description": "Cat shows signs of contentment and relaxation",
                "indicators": [
                    "Soft vocalizations",
                    "Low movement",
                    "Calm demeanor"
                ],
                "likely_causes": [
                    "Comfortable environment",
                    "Post-meal contentment",
                    "Relaxed state"
                ]
            },
            "recommendations": [
                "Continue providing comfortable environment",
                "Maintain current care routine",
                "Cat appears well-adjusted and content"
            ],
            "confidence_score": 0.75
        },
        "enhanced_interpretation": {
            "overall_behavior": "relaxed",
            "emotional_state": "Relaxed/Content",
            "activity_level": "low",
            "vocal_patterns": "Gentle contentment vocalization",
            "behavioral_complexity": "simple",
            "analysis_method": "validated_hybrid",
            "cross_validation": {
                "agreement_level": "high",
                "conflicting_indicators": [],
                "supporting_evidence": [
                    "Both traditional and ML analysis indicate calm, content state"
                ],
                "reliability_score": 0.8
            }
        },
        "confidence_assessment": {
            "overall_score": 0.75,
            "traditional_confidence": 0.8,
            "ml_confidence": 0.75,
            "data_quality": "good",
            "recommendation": "high_confidence"
        },
        "comprehensive_recommendations": [
            "Traditional analysis: Soft, mellow meow indicating contentment and relaxation",
            "ML analysis: Continue providing comfortable environment",
            "ML analysis: Maintain current care routine",
            "ML analysis: Cat appears well-adjusted and content"
        ]
    }

    # Save the test result
    os.makedirs('combined_analysis_results', exist_ok=True)
    test_file = 'combined_analysis_results/test_relaxed_cat_enhanced_analysis.json'

    with open(test_file, 'w') as f:
        json.dump(test_result, f, indent=2)

    print(f"✅ Created test result: {test_file}")
    print(
        f"   Emotional State: {test_result['traditional_analysis']['emotional_state']}")
    print(f"   Expected Color: 🟣 Purple (status-relaxed)")

    # Test the web app loading
    print("\n🧪 Testing Web App Loading")
    print("-" * 30)

    from web_app import WebCatAnalyzer
    analyzer = WebCatAnalyzer()
    results = analyzer.load_results()

    if 'test_relaxed_cat' in results:
        result = results['test_relaxed_cat']
        emotion = result.get('audio_analysis', {}).get(
            'emotional_state', 'Unknown')
        activity = result.get('visual_analysis', {}).get(
            'dominant_activity', 'Unknown')

        print(f"✅ Test result loaded successfully:")
        print(f"   Video: test_relaxed_cat")
        print(f"   Emotional State: '{emotion}'")
        print(f"   Activity Level: '{activity}'")

        # Test color assignment
        def getEmotionalStateClass(state):
            if not state:
                return "status-low"
            lowerState = state.lower()
            if "relaxed" in lowerState or "content" in lowerState:
                return "status-relaxed"
            return "status-medium"

        color_class = getEmotionalStateClass(emotion)
        print(f"   Expected CSS Class: {color_class}")
        print(f"   Expected Color: 🟣 Purple background")

    else:
        print("❌ Test result not found in loaded results")

    print("\n" + "=" * 50)
    print("✅ Test result creation completed!")
    print("\n💡 Instructions:")
    print("1. Start the web interface: python3 web_app.py")
    print("2. Go to http://localhost:5002")
    print("3. Look for 'test_relaxed_cat' in the results")
    print("4. The emotional state should show with a purple background")


if __name__ == "__main__":
    create_test_result()
