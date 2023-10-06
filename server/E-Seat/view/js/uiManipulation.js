
const load = async (summonerName) => {
  try {
    // ... (Data Fetching 코드는 제외)
    const title = document.querySelector(`.title`);
    title.innerText = summonerName;
    for (let i = 1; i <= 20; i++) {
      const matchResult = data[i - 1];
      const matchElement = document.querySelector(`.match${i}`);
      const textElement = matchElement.querySelector(".text");
      textElement.innerText = `${matchResult.championName}   ${matchResult.kills}/${matchResult.deaths}/${matchResult.assists} 	 	 	 연속킬: ${matchResult.largestMultiKill}`;

      if (matchResult.win) {
        matchElement.closest(".match-item").classList.add("victory_bg");
        matchElement.classList.add("result_field");
        textElement.classList.add("victory_font");
      } else {
        matchElement.closest(".match-item").classList.add("defeat_bg");
        matchElement.classList.add("result_field");
        textElement.classList.add("defeat_font");
      }
    }
  } catch (error) {
    // ... (Error Handling 코드는 제외)
  }
};

const searchSummoner = async (e) => {
  // ... (Data Fetching 및 Error Handling 코드는 제외)
  document.querySelector(".login").classList.add("hide");
};

const toggle = () => {
  formType = formType === "login" ? "signup" : "login";
  document.querySelector("button").innerText =
    formType === "login" ? "검색" : "회원가입";
  document.querySelector("a").innerText =
    formType === "login" ? "회원가입 하기" : "검색 하기";
  document.querySelector('input[name="email"]').type =
    formType === "login" ? "hidden" : "email";
};
