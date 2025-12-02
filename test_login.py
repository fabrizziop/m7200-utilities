#!/usr/bin/env python3
"""
Quick test script to verify login functionality
"""

from m7200_controller import M7200Controller
import json

def test_login():
    print("=" * 60)
    print("Testing M7200 Login")
    print("=" * 60)
    
    controller = M7200Controller()
    
    try:
        if controller.login():
            print("\n✅ SUCCESS! Login works!")
            
            # Try to get some basic info
            print("\nAttempting to fetch router info...")
            try:
                # Get current URL
                print(f"Current URL: {controller.driver.current_url}")
                
                # Get page title
                print(f"Page Title: {controller.driver.title}")
                
                # Try to execute some JavaScript
                js_result = controller.driver.execute_script("""
                    return {
                        url: window.location.href,
                        title: document.title
                    };
                """)
                print(f"JS Info: {json.dumps(js_result, indent=2)}")
                
            except Exception as e:
                print(f"Info gathering error: {e}")
        else:
            print("\n❌ FAILED! Login did not succeed")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.close()
        print("\nTest complete.")

if __name__ == "__main__":
    test_login()
