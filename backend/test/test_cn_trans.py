from translation_module.cn_trans import translate_to_chinese

if __name__ == "__main__":
    test_query = "wireless speaker with bluetooth"
    translated = translate_to_chinese(test_query)
    print("🔍 Original:", test_query)
    print("🌐 Translated (to Chinese):", translated)
