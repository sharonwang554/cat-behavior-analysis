#!/usr/bin/env python3
"""
Test script to verify refactoring works correctly
"""

import sys
import os


def test_imports():
    """Test that all refactored modules import correctly"""
    print("🧪 Testing imports...")

    try:
        from core.base_analyzer import BaseAnalyzer, AnalyzerConfig
        print("✅ BaseAnalyzer imports successfully")
    except Exception as e:
        print(f"❌ BaseAnalyzer import failed: {e}")
        return False

    try:
        from core.audio_extractor import UnifiedAudioExtractor
        print("✅ UnifiedAudioExtractor imports successfully")
    except Exception as e:
        print(f"❌ UnifiedAudioExtractor import failed: {e}")
        return False

    try:
        from core.analysis_service import AnalysisService
        print("✅ AnalysisService imports successfully")
    except Exception as e:
        print(f"❌ AnalysisService import failed: {e}")
        return False

    try:
        from video_analysis import CatVideoAnalyzer
        print("✅ Refactored CatVideoAnalyzer imports successfully")
    except Exception as e:
        print(f"❌ CatVideoAnalyzer import failed: {e}")
        return False

    try:
        from simple_video_analysis import SimpleCatVideoAnalyzer
        print("✅ Refactored SimpleCatVideoAnalyzer imports successfully")
    except Exception as e:
        print(f"❌ SimpleCatVideoAnalyzer import failed: {e}")
        return False

    try:
        from enhanced_video_analysis import EnhancedCatVideoAnalyzer
        print("✅ Refactored EnhancedCatVideoAnalyzer imports successfully")
    except Exception as e:
        print(f"❌ EnhancedCatVideoAnalyzer import failed: {e}")
        return False

    try:
        import web_app
        print("✅ Refactored web_app imports successfully")
    except Exception as e:
        print(f"❌ web_app import failed: {e}")
        return False

    return True


def test_base_analyzer():
    """Test BaseAnalyzer functionality"""
    print("\n🧪 Testing BaseAnalyzer...")

    try:
        from core.base_analyzer import BaseAnalyzer, AnalyzerConfig

        # Test configuration
        config = AnalyzerConfig()
        assert 'audio' in config.FOLDERS
        assert 'videos' in config.FOLDERS
        print("✅ AnalyzerConfig works correctly")

        # Test base analyzer (using a concrete implementation)
        from simple_video_analysis import SimpleCatVideoAnalyzer
        analyzer = SimpleCatVideoAnalyzer()

        # Test folder creation
        assert hasattr(analyzer, 'folders')
        assert analyzer.folders['audio'] == 'extracted_audio'
        print("✅ BaseAnalyzer folder setup works")

        # Test video file detection
        video_files = analyzer.get_video_files()
        assert isinstance(video_files, list)
        print("✅ Video file detection works")

        return True

    except Exception as e:
        print(f"❌ BaseAnalyzer test failed: {e}")
        return False


def test_audio_extractor():
    """Test UnifiedAudioExtractor"""
    print("\n🧪 Testing UnifiedAudioExtractor...")

    try:
        from core.audio_extractor import UnifiedAudioExtractor

        extractor = UnifiedAudioExtractor()

        # Test available methods detection
        methods = extractor.get_available_methods()
        assert isinstance(methods, list)
        print(f"✅ Available extraction methods: {methods}")

        return True

    except Exception as e:
        print(f"❌ UnifiedAudioExtractor test failed: {e}")
        return False


def test_analysis_service():
    """Test AnalysisService"""
    print("\n🧪 Testing AnalysisService...")

    try:
        from core.analysis_service import AnalysisService

        service = AnalysisService()

        # Test status
        status = service.get_status()
        assert isinstance(status, dict)
        assert 'videos_found' in status
        assert 'ml_available' in status
        print("✅ AnalysisService status works")

        # Test results loading
        results = service.load_results()
        assert isinstance(results, dict)
        print("✅ AnalysisService results loading works")

        return True

    except Exception as e:
        print(f"❌ AnalysisService test failed: {e}")
        return False


def test_inheritance():
    """Test that all analyzers properly inherit from BaseAnalyzer"""
    print("\n🧪 Testing inheritance...")

    try:
        from video_analysis import CatVideoAnalyzer
        from simple_video_analysis import SimpleCatVideoAnalyzer
        from enhanced_video_analysis import EnhancedCatVideoAnalyzer
        from core.base_analyzer import BaseAnalyzer

        # Test inheritance
        simple_analyzer = SimpleCatVideoAnalyzer()
        assert isinstance(simple_analyzer, BaseAnalyzer)
        print("✅ SimpleCatVideoAnalyzer inherits from BaseAnalyzer")

        video_analyzer = CatVideoAnalyzer()
        assert isinstance(video_analyzer, BaseAnalyzer)
        print("✅ CatVideoAnalyzer inherits from BaseAnalyzer")

        enhanced_analyzer = EnhancedCatVideoAnalyzer()
        assert isinstance(enhanced_analyzer, BaseAnalyzer)
        print("✅ EnhancedCatVideoAnalyzer inherits from BaseAnalyzer")

        # Test that they all have the same folder structure
        assert simple_analyzer.folders == video_analyzer.folders
        print("✅ All analyzers share the same folder structure")

        return True

    except Exception as e:
        print(f"❌ Inheritance test failed: {e}")
        return False


def test_web_app():
    """Test web app functionality"""
    print("\n🧪 Testing web app...")

    try:
        from web_app import app, analysis_service

        # Test Flask app creation
        assert app is not None
        print("✅ Flask app created successfully")

        # Test analysis service
        assert analysis_service is not None
        print("✅ Analysis service initialized")

        # Test that we can get status
        status = analysis_service.get_status()
        assert isinstance(status, dict)
        print("✅ Web app can get analysis status")

        return True

    except Exception as e:
        print(f"❌ Web app test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 REFACTORING VERIFICATION TESTS")
    print("=" * 50)

    tests = [
        test_imports,
        test_base_analyzer,
        test_audio_extractor,
        test_analysis_service,
        test_inheritance,
        test_web_app
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Refactoring successful!")
        return True
    else:
        print(f"\n⚠️ {failed} tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
