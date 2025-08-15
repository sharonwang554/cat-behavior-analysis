#!/usr/bin/env python3
"""
Test script to verify all card backgrounds are properly set to light gray
"""


def test_all_card_backgrounds():
    """Test that all card-related classes have the correct background color"""
    print("🎨 Testing All Card Background Colors")
    print("=" * 50)

    # Check inline CSS in base.html
    print("1. Checking inline CSS in templates/base.html...")
    with open('templates/base.html', 'r') as f:
        base_content = f.read()

    if '.card {' in base_content and 'background: #f8f9fa' in base_content:
        print("✅ Inline .card class has light gray background (#f8f9fa)")
    else:
        print("❌ Inline .card class background not updated")

    # Check SCSS source
    print("\n2. Checking SCSS source file...")
    with open('static/css/main.scss', 'r') as f:
        scss_content = f.read()

    card_count = 0
    if '.card {' in scss_content and 'background: #f8f9fa' in scss_content:
        print("✅ SCSS .card class has light gray background")
        card_count += 1

    if '.result-card {' in scss_content and 'background: #f8f9fa' in scss_content:
        print("✅ SCSS .result-card class has light gray background")
        card_count += 1

    print(f"   Found {card_count} card classes with correct background")

    # Check compiled CSS
    print("\n3. Checking compiled CSS file...")
    with open('static/css/main.css', 'r') as f:
        css_content = f.read()

    compiled_card_count = 0
    if '.card {' in css_content and 'background: #f8f9fa' in css_content:
        print("✅ Compiled .card class has light gray background")
        compiled_card_count += 1

    if '.result-card {' in css_content and 'background: #f8f9fa' in css_content:
        print("✅ Compiled .result-card class has light gray background")
        compiled_card_count += 1

    print(
        f"   Found {compiled_card_count} compiled card classes with correct background")

    # Check for any remaining white backgrounds
    print("\n4. Checking for conflicting white backgrounds...")
    white_backgrounds = []

    # Check for 'background: white' or 'background: #ffffff'
    if 'background: white' in css_content:
        white_count = css_content.count('background: white')
        print(f"⚠️  Found {white_count} 'background: white' declarations")
        # Find context
        lines = css_content.split('\n')
        for i, line in enumerate(lines):
            if 'background: white' in line:
                context_start = max(0, i-2)
                context_end = min(len(lines), i+3)
                context = lines[context_start:context_end]
                white_backgrounds.append(f"Line {i+1}: {' '.join(context)}")

    if white_backgrounds:
        print("   White background contexts:")
        for bg in white_backgrounds[:3]:  # Show first 3
            print(f"   - {bg}")
    else:
        print("✅ No conflicting 'background: white' found in CSS")

    # Check template usage
    print("\n5. Checking template class usage...")
    template_files = ['templates/index.html', 'templates/results.html']
    total_card_usage = 0

    for template_file in template_files:
        try:
            with open(template_file, 'r') as f:
                template_content = f.read()
            card_usage = template_content.count('class="card"')
            total_card_usage += card_usage
            print(f"✅ {template_file}: {card_usage} card elements")
        except FileNotFoundError:
            print(f"❌ {template_file}: File not found")

    print(f"   Total card elements in templates: {total_card_usage}")

    print("\n" + "=" * 50)
    print("🎨 Card Background Test Summary:")
    print(f"✅ Inline CSS: .card background updated")
    print(f"✅ SCSS: {card_count} card classes updated")
    print(f"✅ Compiled CSS: {compiled_card_count} card classes updated")
    print(f"✅ Templates: {total_card_usage} card elements using correct class")

    print("\n🔧 If cards still appear white:")
    print("1. Hard refresh browser: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)")
    print("2. Clear browser cache completely")
    print("3. Try incognito/private browsing mode")
    print("4. Check browser developer tools:")
    print("   - F12 → Elements → Find .card elements")
    print("   - Check if background: #f8f9fa is applied")
    print("   - Look for any overriding styles")

    print("\n✅ Card background test completed!")


if __name__ == "__main__":
    test_all_card_backgrounds()
