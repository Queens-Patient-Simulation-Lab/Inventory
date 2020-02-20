from simulation_lab.BaseTestCaseView import BaseTestCaseView


class SearchHomePageTests(BaseTestCaseView):

    # TODO, We still need to research which backend we will use before we write these tests. Whoosh is not compatible with Heroku
    def test_itemTitleIsSearchable(self):
        pass
    def test_itemTagsAreSearchable(self):
        pass
    def test_softDeletedItemsAreNotSearchable(self):
        pass

    # TODO, test what the default list is
    def test_nothingSearched_givesDefaultListOfItemsWithoutWarning(self):
        pass
    def test_noResults_givesDefaultListOfItemsWithWarning(self):
        pass
    def test_hasResults_onlyGivesResults(self):
        pass

