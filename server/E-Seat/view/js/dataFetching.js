
const load = async (summonerName) => {
  try {
    const data = await fetch(
      `/match?summonerName=${encodeURIComponent(summonerName)}`
    ).then((res) => res.json());
    // ... (UI Manipulation 코드는 제외)
  } catch (error) {
    console.error(error);
    alert("⚠️ 서버에서 데이터를 가져올 수 없어요! ⚠️\n" + error.message);
  }
};

const searchSummoner = async (e) => {
  e.preventDefault();
  const summonerName = e.target.summonerName.value;
  if (!summonerName) {
    alert("⚠️ 소환사명을 입력해주세요! ⚠️");
    return;
  }
  try {
    const data = await fetch(
      `/searchSummoner?summonerName=${encodeURIComponent(summonerName)}`
    );
    if (data.status !== 200) {
      alert(`⚠️ 어떻게 소환사 이름이 ${summonerName}? ⚠️`);
      return;
    }
    // ... (UI Manipulation 코드는 제외)
    await load(summonerName);
  } catch (error) {
    console.error(error);
    alert(
      `⚠️ 서버에서 ${summonerName} 데이터를 가져올 수 없어요! ⚠️\n` +
        error.message
    );
  }
};

const signup = async (e) => {
  e.preventDefault();
  const summonerName = e.target.summonerName.value;
  const password = e.target.password.value;
  const email = e.target.email.value;
  if (!summonerName || !password) {
    alert("⚠️ 아이디와 비밀번호를 입력해주세요!");
    return;
  }
  if (!email) {
    alert("⚠️ 이메일을 입력해주세요!");
    return;
  }
  try {
    const data = await fetch("/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ summonerName, password, email }),
    });
    if (data.status !== 201) {
      alert("⚠️ 회원가입에 실패했어요!");
      return;
    }
    alert("✅ 회원가입에 성공했어요!");
  } catch (error) {
    console.error(error);
    alert("⚠️ 서버에서 데이터를 가져올 수 없어요!\n" + error.message);
  }
};

