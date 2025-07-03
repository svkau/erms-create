#!/usr/bin/env python3
"""
Enkel test av den nya ERMS-biblioteksstrukturen
==============================================

Testar grundläggande funktionalitet utan att bygga komplett dokument.
"""

import sys
import os
from datetime import datetime

def test_core():
    """Testa ERMS Core-biblioteket"""
    print("🧪 Testar ERMS Core...")
    
    try:
        # Importera core-biblioteket
        sys.path.insert(0, '../src/erms_create')
        
        from erms_create.core import Erms, Control
        from erms_create.core.elements import Dates, Agent
        from erms_create.core import value_lists
        
        print("✅ Import av core lyckades")
        
        # Testa grundläggande ERMS-skapande
        erms = Erms()
        print("✅ ERMS-objekt skapat")
        
        # Testa control-konfiguration
        erms.control.add_identification("Test Organisation", "arkivbildare")
        erms.control.add_identification("1234567890", "organisationsnummer")
        erms.control.set_classification_schema("Test Schema")
        print("✅ Control-konfiguration lyckades")
        
        # Testa aggregation
        case = erms.add_aggregation("caseFile")
        case.set_object_id("T 2024-0001")
        case.set_title("Test Ärende")
        case.set_status("closed")
        print("✅ Aggregation skapad och konfigurerad")
        
        # Testa XML-generering
        xml_output = erms.to_xml_string()
        if len(xml_output) > 100 and "erms" in xml_output:
            print("✅ XML-generering lyckades")
            print(f"   XML-längd: {len(xml_output)} tecken")
        else:
            print("❌ XML-generering producerade felaktig output")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ ERMS Core test misslyckades: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_svk_basic():
    """Testa grundläggande SVK-funktionalitet"""
    print("\n🧪 Testar SVK Ärendehandlingar...")
    
    try:
        # Importera SVK-biblioteket
        from erms_create.svk_arende import value_lists as svk_values
        from erms_create.svk_arende.validation import SVKValidator
        from erms_create.svk_arende.svk_extensions import SVKExtensions
        
        print("✅ Import av svk_arende lyckades")
        
        # Testa validator
        validator = SVKValidator()
        
        # Testa ärendenummer-validering
        valid_case = validator.validate_case_number("F 2024-0001")
        invalid_case = validator.validate_case_number("felaktigt-nummer")
        
        if valid_case and not invalid_case:
            print("✅ Ärendenummer-validering fungerar")
        else:
            print("❌ Ärendenummer-validering fungerar inte korrekt")
            return False
        
        # Testa organisationsnummer-validering
        valid_org = validator.validate_org_number("1234567890")
        invalid_org = validator.validate_org_number("123")
        
        if valid_org and not invalid_org:
            print("✅ Organisationsnummer-validering fungerar")
        else:
            print("❌ Organisationsnummer-validering fungerar inte")
            return False
        
        # Testa SVK-tillägg
        extensions = SVKExtensions("aggregation")
        extensions.set_initiative("externt")
        
        if extensions.element is not None:
            print("✅ SVK Extensions skapade")
        else:
            print("❌ SVK Extensions misslyckades")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ SVK test misslyckades: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Testa integration mellan core och SVK"""
    print("\n🧪 Testar integration...")
    
    try:
        # Detta är en förenklad test eftersom vi inte har alla klasser ännu
        from erms_create.core import Erms
        from erms_create.svk_arende.validation import SVKValidator
        
        # Skapa ett enkelt ERMS-dokument
        erms = Erms()
        erms.control.add_identification("Test Pastorat", "arkivbildare")
        erms.control.add_identification("9876543210", "organisationsnummer")
        
        case = erms.add_aggregation("caseFile")
        case.set_object_id("T 2024-0001")
        case.set_title("Integrationstest")
        
        # Generera XML
        xml_content = erms.to_xml_string()
        
        # Kontrollera att XML innehåller förväntade element
        expected_elements = [
            "erms", "control", "aggregation", "identification", 
            "objectId", "title", "caseFile"
        ]
        
        missing_elements = []
        for element in expected_elements:
            if element not in xml_content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Saknade element i XML: {missing_elements}")
            return False
        else:
            print("✅ Integration test lyckades")
            print(f"   Genererad XML innehåller alla förväntade element")
            
        return True
        
    except Exception as e:
        print(f"❌ Integration test misslyckades: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_output():
    """Testa filutskrift"""
    print("\n🧪 Testar filutskrift...")
    
    try:
        from erms_create.core import Erms
        
        # Skapa ett minimalt ERMS-dokument
        erms = Erms()
        erms.control.add_identification("Test", "arkivbildare")
        erms.control.add_identification("1111111111", "organisationsnummer")
        
        case = erms.add_aggregation("caseFile")
        case.set_object_id("TEST 2024-0001")
        case.set_title("Filtest")
        case.set_status("closed")
        
        # Spara till fil
        test_filename = "test_output.xml"
        erms.save_to_file(test_filename)
        
        # Kontrollera att filen skapades
        if os.path.exists(test_filename):
            with open(test_filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) > 100 and "TEST 2024-0001" in content:
                print("✅ Filutskrift lyckades")
                print(f"   Fil skapad: {test_filename} ({len(content)} tecken)")
                
                # Visa förhandsgranskning
                print("\n📄 Förhandsgranskning (första 300 tecken):")
                print(content[:300] + "..." if len(content) > 300 else content)
                
                return True
            else:
                print("❌ Filen har felaktigt innehåll")
                return False
        else:
            print("❌ Fil skapades inte")
            return False
            
    except Exception as e:
        print(f"❌ Filutskrift test misslyckades: {e}")
        import traceback
        traceback.print_exc()
        return False


def cleanup():
    """Rensa upp testfiler"""
    test_files = ["test_output.xml"]
    for filename in test_files:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"🗑️ Raderade testfil: {filename}")
            except:
                print(f"⚠️ Kunde inte radera: {filename}")


def main():
    """Kör alla tester"""
    print("🧪 ERMS Biblioteksstruktur - Grundtester")
    print("=" * 50)
    
    tests = [
        ("ERMS Core", test_core),
        ("SVK Basic", test_svk_basic), 
        ("Integration", test_integration),
        ("File Output", test_file_output),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 {test_name} kraschade: {e}")
            results.append((test_name, False))
    
    # Sammanfattning
    print("\n" + "=" * 50)
    print("📊 TESTRESULTAT")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:<8} {test_name}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"Resultat: {passed}/{total} tester lyckades")
    
    if passed == total:
        print("🎉 Alla tester lyckades! Grundstrukturen fungerar.")
    else:
        print("⚠️ Vissa tester misslyckades. Se detaljer ovan.")
    
    # Rensa upp
    cleanup()
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)