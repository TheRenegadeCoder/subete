from subete.repo import LanguageCollection
import subete

TEST_REPO = subete.load()

def test_doc_url_multiword_lang():
    language: LanguageCollection = TEST_REPO.language_collections()["Google Apps Script"]
    assert language.lang_docs_url() == "https://sample-programs.therenegadecoder.com/languages/google-apps-script"
