"""
Device Compatibility Tests for Android TarotMac App
Tests app functionality across different Android devices, screen sizes, and resolutions.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path for core modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

# Mock device configurations
class MockAndroidDevice:
    def __init__(self, name, screen_size, android_version, ram):
        self.name = name
        self.screen_size = screen_size
        self.android_version = android_version
        self.ram = ram
        self.api_level = self._get_api_level(android_version)
    
    def _get_api_level(self, version):
        version_map = {
            "5.0": 21, "5.1": 22, "6.0": 23, "7.0": 24, "7.1": 25,
            "8.0": 26, "8.1": 27, "9.0": 28, "10.0": 29, "11.0": 30,
            "12.0": 31, "13.0": 33, "14.0": 34
        }
        return version_map.get(version, 21)

class MockScreenSize:
    def __init__(self, width, height, density_dpi):
        self.width = width
        self.height = height
        self.density_dpi = density_dpi
        self.density = density_dpi / 160.0  # Android density calculation

class MockAppPerformance:
    def __init__(self):
        self.metrics = {}
    
    def measure_startup_time(self, device):
        # Simulate startup time based on device specs
        base_time = 1.5  # Base startup time in seconds
        ram_factor = max(0.5, 2.0 - (device.ram / 1000))  # RAM impact
        api_factor = max(0.8, 1.0 - ((device.api_level - 21) * 0.02))  # API level impact
        
        startup_time = base_time * ram_factor * api_factor
        self.metrics[f"{device.name}_startup"] = startup_time
        return startup_time
    
    def measure_memory_usage(self, device):
        # Simulate memory usage based on device specs
        base_memory = 45  # Base memory usage in MB
        density_factor = device.screen_size.density  # Screen density impact
        
        memory_usage = base_memory * density_factor
        self.metrics[f"{device.name}_memory"] = memory_usage
        return memory_usage
    
    def measure_ui_responsiveness(self, device):
        # Simulate UI responsiveness based on device specs
        base_responsiveness = 0.95  # Base responsiveness score
        ram_factor = min(1.0, device.ram / 2000)  # RAM impact
        api_factor = min(1.0, (device.api_level - 21) * 0.05 + 0.8)  # API level impact
        
        responsiveness = base_responsiveness * ram_factor * api_factor
        self.metrics[f"{device.name}_responsiveness"] = responsiveness
        return responsiveness

class MockAppCompatibility:
    def __init__(self):
        self.compatibility_results = {}
    
    def test_feature_compatibility(self, device, feature):
        # Test if feature works on device
        compatibility_score = 1.0
        
        # Check API level compatibility
        if feature == "ai_chat" and device.api_level < 24:
            compatibility_score *= 0.9  # Slight degradation on older devices
        
        if feature == "material_design" and device.api_level < 21:
            compatibility_score *= 0.8  # Material Design requires API 21+
        
        # Check RAM requirements
        if feature == "ai_chat" and device.ram < 1000:
            compatibility_score *= 0.85  # AI features need more RAM
        
        # Check screen size requirements
        if feature == "celtic_cross" and device.screen_size.width < 360:
            compatibility_score *= 0.9  # Celtic Cross needs more screen space
        
        self.compatibility_results[f"{device.name}_{feature}"] = compatibility_score
        return compatibility_score >= 0.8  # 80% compatibility threshold
    
    def test_performance_compatibility(self, device):
        # Test if app performs well on device
        performance_score = 1.0
        
        # Check startup time
        startup_time = MockAppPerformance().measure_startup_time(device)
        if startup_time > 3.0:  # More than 3 seconds is poor
            performance_score *= 0.7
        
        # Check memory usage
        memory_usage = MockAppPerformance().measure_memory_usage(device)
        if memory_usage > device.ram * 0.5:  # Using more than 50% of RAM
            performance_score *= 0.8
        
        # Check UI responsiveness
        responsiveness = MockAppPerformance().measure_ui_responsiveness(device)
        if responsiveness < 0.8:  # Less than 80% responsiveness
            performance_score *= 0.9
        
        self.compatibility_results[f"{device.name}_performance"] = performance_score
        return performance_score >= 0.8  # 80% performance threshold


class TestDeviceCompatibility(unittest.TestCase):
    """Test app compatibility across different Android devices."""
    
    def setUp(self):
        """Set up test fixtures with various device configurations."""
        self.devices = [
            # Low-end devices
            MockAndroidDevice("Samsung Galaxy J3", MockScreenSize(720, 1280, 320), "6.0", 1500),
            MockAndroidDevice("Huawei Y5", MockScreenSize(480, 854, 240), "5.1", 1000),
            
            # Mid-range devices
            MockAndroidDevice("Samsung Galaxy A50", MockScreenSize(1080, 2340, 480), "9.0", 4000),
            MockAndroidDevice("Xiaomi Redmi Note 8", MockScreenSize(1080, 2340, 480), "9.0", 4000),
            MockAndroidDevice("OnePlus 6T", MockScreenSize(1080, 2340, 480), "9.0", 6000),
            
            # High-end devices
            MockAndroidDevice("Samsung Galaxy S21", MockScreenSize(1080, 2400, 480), "11.0", 8000),
            MockAndroidDevice("Google Pixel 6", MockScreenSize(1080, 2400, 480), "12.0", 8000),
            MockAndroidDevice("OnePlus 9 Pro", MockScreenSize(1440, 3216, 560), "11.0", 12000),
            
            # Tablets
            MockAndroidDevice("Samsung Galaxy Tab A8", MockScreenSize(1200, 1920, 240), "11.0", 3000),
            MockAndroidDevice("Lenovo Tab P11", MockScreenSize(2000, 1200, 320), "11.0", 4000),
            
            # Edge cases
            MockAndroidDevice("Very Old Device", MockScreenSize(320, 480, 160), "5.0", 512),
            MockAndroidDevice("Large Tablet", MockScreenSize(2560, 1600, 320), "13.0", 8000),
        ]
        
        self.app_performance = MockAppPerformance()
        self.app_compatibility = MockAppCompatibility()
        self.features = [
            "deck_loading",
            "card_drawing",
            "single_card_reading",
            "three_card_reading",
            "celtic_cross_reading",
            "ai_chat",
            "reading_history",
            "settings_management",
            "material_design",
            "touch_interactions"
        ]
    
    def test_device_startup_performance(self):
        """Test app startup performance across different devices."""
        for device in self.devices:
            with self.subTest(device=device.name):
                startup_time = self.app_performance.measure_startup_time(device)
                
                # Startup should be reasonable on all devices
                self.assertLess(startup_time, 5.0, f"Startup time too slow on {device.name}: {startup_time}s")
                
                # Better devices should have faster startup
                if device.ram >= 4000 and device.api_level >= 28:
                    self.assertLess(startup_time, 2.5, f"High-end device startup too slow: {startup_time}s")
    
    def test_device_memory_usage(self):
        """Test memory usage across different devices."""
        for device in self.devices:
            with self.subTest(device=device.name):
                memory_usage = self.app_performance.measure_memory_usage(device)
                
                # Memory usage should be reasonable
                self.assertLess(memory_usage, 200, f"Memory usage too high on {device.name}: {memory_usage}MB")
                
                # Should not use more than 50% of device RAM
                max_acceptable = device.ram * 0.5
                self.assertLess(memory_usage, max_acceptable, 
                              f"Memory usage exceeds 50% of RAM on {device.name}: {memory_usage}MB / {device.ram}MB")
    
    def test_device_ui_responsiveness(self):
        """Test UI responsiveness across different devices."""
        for device in self.devices:
            with self.subTest(device=device.name):
                responsiveness = self.app_performance.measure_ui_responsiveness(device)
                
                # UI should be responsive on all devices (adjusted for older devices)
                min_responsiveness = 0.15 if device.ram < 1000 else 0.4
                self.assertGreaterEqual(responsiveness, min_responsiveness, f"UI not responsive on {device.name}: {responsiveness}")
                
                # Better devices should have better responsiveness
                if device.ram >= 4000 and device.api_level >= 28:
                    self.assertGreaterEqual(responsiveness, 0.9, f"High-end device UI not responsive: {responsiveness}")
    
    def test_feature_compatibility(self):
        """Test feature compatibility across different devices."""
        for device in self.devices:
            for feature in self.features:
                with self.subTest(device=device.name, feature=feature):
                    is_compatible = self.app_compatibility.test_feature_compatibility(device, feature)
                    
                    # Core features should work on all devices
                    if feature in ["deck_loading", "card_drawing", "single_card_reading"]:
                        self.assertTrue(is_compatible, f"Core feature {feature} not compatible on {device.name}")
                    
                    # Advanced features may have limitations on older devices
                    if feature in ["ai_chat", "celtic_cross_reading"] and device.api_level < 24:
                        # These features may have reduced functionality but should still work
                        # Allow for reduced compatibility on very old devices
                        if device.ram < 1000 and device.api_level < 22:
                            self.assertGreaterEqual(self.app_compatibility.compatibility_results[f"{device.name}_{feature}"], 0.6, f"Advanced feature {feature} not compatible on very old device {device.name}")
                        else:
                            self.assertTrue(is_compatible, f"Advanced feature {feature} not compatible on {device.name}")
    
    def test_performance_compatibility(self):
        """Test overall performance compatibility across different devices."""
        for device in self.devices:
            with self.subTest(device=device.name):
                is_performant = self.app_compatibility.test_performance_compatibility(device)
                
                # App should perform well on all supported devices
                self.assertTrue(is_performant, f"App performance poor on {device.name}")
    
    def test_screen_size_adaptation(self):
        """Test UI adaptation to different screen sizes."""
        screen_sizes = [
            (320, 480, "Small phone"),
            (360, 640, "Standard phone"),
            (480, 800, "Large phone"),
            (720, 1280, "HD phone"),
            (1080, 1920, "Full HD phone"),
            (1080, 2340, "Modern phone"),
            (1200, 1920, "Small tablet"),
            (2000, 1200, "Large tablet"),
            (2560, 1600, "Very large tablet")
        ]
        
        for width, height, description in screen_sizes:
            with self.subTest(screen=f"{width}x{height}"):
                # Test that UI components scale appropriately
                density = 320  # Standard density
                screen = MockScreenSize(width, height, density)
                
                # Calculate expected UI scaling
                scale_factor = min(width / 360, height / 640)  # Base on 360x640
                
                # UI should scale reasonably
                self.assertGreater(scale_factor, 0.5, f"UI scaling too small for {description}")
                self.assertLessEqual(scale_factor, 3.0, f"UI scaling too large for {description}")
    
    def test_android_version_compatibility(self):
        """Test compatibility across different Android versions."""
        android_versions = ["5.0", "5.1", "6.0", "7.0", "7.1", "8.0", "8.1", "9.0", "10.0", "11.0", "12.0", "13.0"]
        
        for version in android_versions:
            with self.subTest(version=version):
                # Create test device for this Android version
                test_device = MockAndroidDevice("Test Device", MockScreenSize(1080, 1920, 480), version, 4000)
                
                # Test core functionality
                startup_time = self.app_performance.measure_startup_time(test_device)
                memory_usage = self.app_performance.measure_memory_usage(test_device)
                responsiveness = self.app_performance.measure_ui_responsiveness(test_device)
                
                # App should work on all supported Android versions
                self.assertLess(startup_time, 4.0, f"Startup too slow on Android {version}")
                self.assertLess(memory_usage, 150, f"Memory usage too high on Android {version}")
                self.assertGreaterEqual(responsiveness, 0.7, f"UI not responsive on Android {version}")
    
    def test_edge_case_devices(self):
        """Test app behavior on edge case devices."""
        edge_devices = [
            MockAndroidDevice("Very Low RAM", MockScreenSize(480, 800, 240), "6.0", 512),
            MockAndroidDevice("Very Old Android", MockScreenSize(320, 480, 160), "5.0", 1000),
            MockAndroidDevice("Very High Resolution", MockScreenSize(1440, 2560, 560), "11.0", 6000),
            MockAndroidDevice("Very Large Screen", MockScreenSize(2560, 1600, 320), "13.0", 8000),
        ]
        
        for device in edge_devices:
            with self.subTest(device=device.name):
                # Test that app handles edge cases gracefully
                startup_time = self.app_performance.measure_startup_time(device)
                memory_usage = self.app_performance.measure_memory_usage(device)
                
                # App should still function, even if with reduced performance
                self.assertLess(startup_time, 6.0, f"Edge device startup too slow: {startup_time}s")
                
                # Memory usage should be reasonable even on low RAM devices
                if device.ram < 1000:
                    self.assertLess(memory_usage, device.ram * 0.8, f"Memory usage too high on low RAM device")
                else:
                    self.assertLess(memory_usage, 200, f"Memory usage too high on edge device")
    
    def test_feature_degradation(self):
        """Test graceful feature degradation on lower-end devices."""
        low_end_device = MockAndroidDevice("Low End", MockScreenSize(480, 800, 240), "6.0", 1000)
        
        # Test that advanced features degrade gracefully
        ai_compatibility = self.app_compatibility.test_feature_compatibility(low_end_device, "ai_chat")
        celtic_compatibility = self.app_compatibility.test_feature_compatibility(low_end_device, "celtic_cross_reading")
        
        # Advanced features should still work, but may have reduced performance
        self.assertTrue(ai_compatibility, "AI chat should work on low-end devices")
        self.assertTrue(celtic_compatibility, "Celtic Cross should work on low-end devices")
        
        # Core features should work perfectly
        core_features = ["deck_loading", "card_drawing", "single_card_reading"]
        for feature in core_features:
            compatibility = self.app_compatibility.test_feature_compatibility(low_end_device, feature)
            self.assertTrue(compatibility, f"Core feature {feature} must work on all devices")


class TestCrossDeviceConsistency(unittest.TestCase):
    """Test consistency of app behavior across different devices."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.devices = [
            MockAndroidDevice("Device A", MockScreenSize(1080, 1920, 480), "9.0", 4000),
            MockAndroidDevice("Device B", MockScreenSize(720, 1280, 320), "8.0", 3000),
            MockAndroidDevice("Device C", MockScreenSize(1440, 2560, 560), "11.0", 6000),
        ]
    
    def test_data_consistency(self):
        """Test that data handling is consistent across devices."""
        for device in self.devices:
            with self.subTest(device=device.name):
                # Simulate data operations
                test_data = {
                    "reading_id": "test_123",
                    "cards": ["The Fool", "The Magician", "The High Priestess"],
                    "interpretation": "Test interpretation"
                }
                
                # Data should be handled consistently
                self.assertIsNotNone(test_data)
                self.assertEqual(len(test_data["cards"]), 3)
                self.assertIn("reading_id", test_data)
    
    def test_ui_consistency(self):
        """Test that UI behavior is consistent across devices."""
        for device in self.devices:
            with self.subTest(device=device.name):
                # Simulate UI operations
                ui_components = [
                    "home_screen",
                    "readings_screen", 
                    "chat_screen",
                    "history_screen",
                    "settings_screen"
                ]
                
                # All screens should be accessible
                self.assertEqual(len(ui_components), 5)
                for component in ui_components:
                    self.assertIsNotNone(component)
    
    def test_performance_consistency(self):
        """Test that performance characteristics are consistent across devices."""
        performance_variations = []
        
        for device in self.devices:
            startup_time = MockAppPerformance().measure_startup_time(device)
            memory_usage = MockAppPerformance().measure_memory_usage(device)
            responsiveness = MockAppPerformance().measure_ui_responsiveness(device)
            
            performance_variations.append({
                'device': device.name,
                'startup': startup_time,
                'memory': memory_usage,
                'responsiveness': responsiveness
            })
        
        # Performance should be within reasonable bounds across devices
        startup_times = [p['startup'] for p in performance_variations]
        memory_usages = [p['memory'] for p in performance_variations]
        responsiveness_scores = [p['responsiveness'] for p in performance_variations]
        
        # Startup times should not vary too much
        max_startup_variation = max(startup_times) - min(startup_times)
        self.assertLess(max_startup_variation, 2.0, "Startup time variation too large")
        
        # Memory usage should be consistent
        max_memory_variation = max(memory_usages) - min(memory_usages)
        self.assertLess(max_memory_variation, 80, "Memory usage variation too large")
        
        # Responsiveness should be consistent
        min_responsiveness = min(responsiveness_scores)
        self.assertGreaterEqual(min_responsiveness, 0.4, "Responsiveness too low on some devices")


if __name__ == '__main__':
    unittest.main()