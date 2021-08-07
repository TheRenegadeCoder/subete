from subete.repo import LanguageCollection
import subete

TEST_REPO = subete.load()

def test_doc_url_multiword_lang():
    language: LanguageCollection = TEST_REPO.language_collections()["Google Apps Script"]
    assert language.lang_docs_url() == "https://sample-programs.therenegadecoder.com/languages/google-apps-script"

def test_testinfo_url_multiword_lang():
    language: LanguageCollection = TEST_REPO.language_collections()["Google Apps Script"]
    assert language.testinfo_url() == "https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/g/google-apps-script/testinfo.yml"
