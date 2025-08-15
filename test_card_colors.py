#!/usr/bin/env python3
"""
Test script to verify the card and badge color improvements
"""


def test_card_and_badge_colors():
    """Test that card and badge colors have been improved for better visibility"""
    print("🎨 Testing Card and Badge Color Improvements")
    print("=" * 50)

    # Check base.html for card background
    print("1. Checking card background color...")
    with open('templates/base.html', 'r') as f:
        base_content = f.read()

    if 'background: #f8f9fa' in base_content and '.card {' in base_content:
        print("✅ Card background changed from white to light gray (#f8f9fa)")
    else:
        print("❌ Card background not updated")

    # Check status-medium badge
    print("\n2. Checking medium badge visibility...")
    if 'background: #ffc107' in base_content and '.status-medium' in base_content:
        print("✅ Medium badge improved: bright yellow background (#ffc107)")
    else:
        print("❌ Medium badge not improved")

    # Check status-serious badge
    print("\n3. Checking serious badge visibility...")
    if 'background: #6c757d' in base_content and 'color: #ffffff' in base_content:
        print("✅ Serious badge improved: dark gray background with white text")
    else:
        print("❌ Serious badge not improved")

    # Check SCSS file
    print("\n4. Checking SCSS source file...")
    with open('static/css/main.scss', 'r') as f:
        scss_content = f.read()

    if 'background: #f8f9fa' in scss_content and '.card {' in scss_content:
        print("✅ SCSS card background updated")
    else:
        print("❌ SCSS card background not updated")

    if 'background: #ffc107' in scss_content:
        print("✅ SCSS medium badge updated")
    else:
        print("❌ SCSS medium badge not updated")

    if 'background: #6c757d' in scss_content:
        print("✅ SCSS serious badge updated")
    else:
        print("❌ SCSS serious badge not updated")

    # Check compiled CSS
    print("\n5. Checking compiled CSS...")
    with open('static/css/main.css', 'r') as f:
        css_content = f.read()

    if 'background: #f8f9fa' in css_content:
        print("✅ Compiled CSS has updated card background")
    else:
        print("❌ Compiled CSS missing card background")

    print("\n" + "=" * 50)
    print("🎨 Color Improvements Summary:")
    print("📱 Card Background: White → Light Gray (#f8f9fa)")
    print("🟡 Medium Badge: Light yellow → Bright yellow (#ffc107)")
    print("⚫ Serious Badge: Light gray → Dark gray with white text (#6c757d)")
    print("\n💡 Expected Results:")
    print("- Better contrast between cards and gradient background")
    print("- More visible Medium badges (bright yellow)")
    print("- More visible Serious/Formal badges (dark gray with white text)")
    print("- Professional appearance with improved readability")

    print("\n✅ Card and badge color test completed!")


if __name__ == "__main__":
    test_card_and_badge_colors()
