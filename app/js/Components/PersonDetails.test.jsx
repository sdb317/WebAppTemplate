import React from "react";
import PublicationDetails from "./PublicationDetails";
import PublicationStore from "../Stores/Publications";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import { Provider } from "mobx-react";
import { MemoryRouter } from "react-router-dom";

// axios mocks for api responses
const axiosMock = new MockAdapter(axios);
axiosMock.onGet(`/plus/v1/publications/?detail=false`).reply(200, {Publications: []});
// options for select fields
axiosMock.onGet("/plus/v1/options/publication/openaccess/").reply(200, [{"label": "Unknown","numeric": 0,"alphanumeric": "<Unknown>"},{"label": "No","numeric": 1,"alphanumeric": "No"},{"label": "YesGreen","numeric": 2,"alphanumeric": "Yes - Green"},{"label": "YesGold","numeric": 3,"alphanumeric": "Yes - Gold"}]);
axiosMock.onGet("/plus/v1/options/publication/type/").reply(200, [{"label": "Unknown","numeric": 0,"alphanumeric": "<Unknown>"},{"label": "ArticleInJournal","numeric": 1,"alphanumeric": "Article in Journal"},{"label": "BookOrMonograph","numeric": 2,"alphanumeric": "Book/Monograph"},{"label": "ChapterInBook","numeric": 3,"alphanumeric": "Chapter in a Book"},{"label": "PaperInConferenceOrWorkshop","numeric": 4,"alphanumeric": "Paper in Proceedings of Conference/Workshop"},{"label": "PublicationInConferenceOrContributionToBook","numeric": 5,"alphanumeric": "Publication in Conference proceeding/contribution to a book"},{"label": "PublicationInConferenceOrWorkshop","numeric": 6,"alphanumeric": "Publication in Conference proceeding/Workshop"},{"label": "ThesisOrDissertation","numeric": 7,"alphanumeric": "Thesis/Dissertation"},{"label": "Other","numeric": 100,"alphanumeric": "Other..."}]);
const fakePublication = {"Publications":[{"publisher":"Springer Nature America, Inc","open_access":0,"doi":"10.1038/s41565-018-0163-6","publication":"Nature Nanotechnology","links":[],"publication_url":"http://dx.doi.org/10.1038/s41565-018-0163-6","acknowledgement_text":null,"type_of_publication":1,"title":"Single-layer graphene modulates neuronal communication and augments membrane ion currents","share":6,"peer_reviewed":false,"saved_by":"","phase":0,"publication_date":"2018-07-10","publication_archive_url":null,"id":37,"ranked_authors":"Niccolò Paolo Pampaloni, Martin Lottner, Michele Giugliano, Alessia Matruglio, Francesco D’Amico, Maurizio Prato, Josè Antonio Garrido, Laura Ballerini, Denis Scaini","saved_on":"2018-08-24T08:57:53.483118+02:00"}]};

jest.mock("LOG_LEVEL", () => "debug", { virtual: true });

// wraps publication details in mobx provider and react router
// PublicationDetails can't tested by itself because it's tightly coupled with those
const wrapPublicationDetails = (stores, props) => {
  return (
    <Provider {...stores}>
        <MemoryRouter> 
          <PublicationDetails {...props}/> 
        </MemoryRouter>
      </Provider>
  )
};

describe("PublicationDetails handling unsaved changes tests", () => {
  const fakeID = 1;
  axiosMock.onGet(`/plus/v1/publications/${fakeID}/?detail=true`).reply(200, fakePublication);
  axiosMock.onPost("/plus/v1/publications/").reply(200, {"Success": fakeID});
  const mockedProps = {
    match: {params: {id: fakeID}},
    classes: {},   
  }
  // mobx stores
  const publicationStore = new PublicationStore();
  // use axios instance where responses for optionUrls are mocked
  publicationStore.formStore.registerAxiosInstance(axios);
  const stores = {publicationListStore: publicationStore};

  it("when there is an issue when saving in the api. Unsaved changes state should not be lost", async () => {
    const wrapper = mount(wrapPublicationDetails(stores, mockedProps));
    
    // simulate onChange
    wrapper.simulate("change");

    let publicationDetails = wrapper.find("PublicationDetails");

    // there should be unsaved changes
    expect(publicationDetails.instance().state.unsavedChanges).toBe(true);

    // api response goes wrong
    axiosMock.onPut(`/plus/v1/publications/${fakeID}/`).reply(500);

    try {
      await stores.publicationListStore.save();
    } catch(e) {
      // expected to go wrong
      console.log(e);
    }

    // there should still be unsaved changes
    expect(publicationDetails.instance().state.unsavedChanges).toBe(true);

  });


});