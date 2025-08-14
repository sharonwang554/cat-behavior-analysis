#!/usr/bin/env python3
"""
Test script to verify color assignment is working correctly
"""


def test_javascript_logic():
    """Test the JavaScript color assignment logic in Python"""
    print("🎨 Testing Color Assignment Logic")
    print("=" * 40)

    def getEmotionalStateClass(state):
        """Python version of the JavaScript function"""
        if not state:
            return "status-low"

        lowerState = state.lower()

        if "playful" in lowerState or "expressive" in lowerState:
            return "status-playful"
        if "stressed" in lowerState or "strained" in lowerState:
            return "status-stressed"
        if "calm" in lowerState or "controlled" in lowerState:
            return "status-calm"
        if "seeking" in lowerState or "attention" in lowerState:
            return "status-seeking"
        if "serious" in lowerState or "formal" in lowerState:
            return "status-serious"
        if "alert" in lowerState or "excited" in lowerState:
            return "status-alert"
        if "relaxed" in lowerState or "content" in lowerState:
            return "status-relaxed"

        return "status-medium"

    # Test cases
    test_cases = [
        ("Playful/Expressive", "status-playful", "🔵 Blue"),
        ("Stressed/Strained", "status-stressed", "🔴 Red"),
        ("Relaxed/Content", "status-relaxed", "🟣 Purple"),
        ("Calm/Controlled", "status-calm", "🟢 Green"),
        ("Seeking attention/affection", "status-seeking", "🟠 Orange"),
        ("Serious/Formal", "status-serious", "⚫ Gray"),
        ("Alert/Excited", "status-alert", "🟡 Amber"),
        ("Unknown", "status-medium", "🟡 Medium"),
    ]

    print("Testing emotional state color assignments:")
    for state, expected_class, color_desc in test_cases:
        actual_class = getEmotionalStateClass(state)
        status = "✅" if actual_class == expected_class else "❌"
        print(f"{status} '{state}' → {actual_class} ({color_desc})")

    print("\n" + "=" * 40)
    print("✅ Color assignment logic test completed!")


def test_current_results():
    """Test what colors the current results should get"""
    print("\n🧪 Testing Current Analysis Results")
    print("=" * 40)

    from web_app import WebCatAnalyzer

    analyzer = WebCatAnalyzer()
    results = analyzer.load_results()

    def getEmotionalStateClass(state):
        """Python version of the JavaScript function"""
        if not state:
            return "status-low"

        lowerState = state.lower()

        if "playful" in lowerState or "expressive" in lowerState:
            return "status-playful"
        if "stressed" in lowerState or "strained" in lowerState:
            return "status-stressed"
        if "calm" in lowerState or "controlled" in lowerState:
            return "status-calm"
        if "seeking" in lowerState or "attention" in lowerState:
            return "status-seeking"
        if "serious" in lowerState or "formal" in lowerState:
            return "status-serious"
        if "alert" in lowerState or "excited" in lowerState:
            return "status-alert"
        if "relaxed" in lowerState or "content" in lowerState:
            return "status-relaxed"

        return "status-medium"

    print("Current results and their expected colors:")
    for video_name, result in results.items():
        emotion = result.get('audio_analysis', {}).get(
            'emotional_state', 'Unknown')
        activity = result.get('visual_analysis', {}).get(
            'dominant_activity', 'Unknown')

        emotion_class = getEmotionalStateClass(emotion)

        color_map = {
            'status-playful': '🔵 Blue',
            'status-stressed': '🔴 Red',
            'status-relaxed': '🟣 Purple',
            'status-calm': '🟢 Green',
            'status-seeking': '🟠 Orange',
            'status-serious': '⚫ Gray',
            'status-alert': '🟡 Amber',
            'status-medium': '🟡 Medium'
        }

        color_desc = color_map.get(emotion_class, '❓ Unknown')

        print(f"📹 {video_name}:")
        print(
            f"   Emotional State: '{emotion}' → {emotion_class} ({color_desc})")
        print(f"   Activity Level: '{activity}'")
        print()

    print("=" * 40)
    print("✅ Current results test completed!")


if __name__ == "__main__":
    test_javascript_logic()
    test_current_results()
