<script>
  import { afterUpdate, onMount } from "svelte";
  import { fade, fly } from "svelte/transition";
  import { BACKEND_URL, QUIZ_PROMPT, BLOCK_FADE_IN_DELAY, BLOCK_FADE_IN_DURATION, BLOCK_FADE_OUT_DURATION } from "../constants";

  export let username;
  export let topic;
  export let curriculum;
  export let theme;
  export let block;
  export let finalTexts;
  export let displayTexts;
  
  let writer;
  let topicBlock;
  let userQueryInput;
  let script = document.createElement('script');
  script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";

  async function sendQuery(query) {
    finalTexts = [...finalTexts, userQueryInput];
    displayTexts = [...displayTexts, userQueryInput];
    let userQuery = userQueryInput;
    userQueryInput = "";

    let sendGptMsgResponse = await fetch(BACKEND_URL + "/sendGptMsg", {
      method: "POST",
      body: JSON.stringify({
        "topicId":  topic.topicId,
        "courseNumber": curriculum.curriculumId,
        "newMsg": userQuery,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let sendGptMsgData = await sendGptMsgResponse.json();

    if (sendGptMsgData == "Processing") {
      let latestMsg = await recursiveGetLatestMsg(curriculum.curriculumId);
      latestMsg = latestMsg.chatHistory[latestMsg.chatHistory.length - 1][1];
      finalTexts = [...finalTexts, latestMsg];
      displayTexts = [...displayTexts, ""];
    }
  }

  async function getChatHistory(curriculumId) {
    let getChatHistoryResponse = await fetch(BACKEND_URL + "/getChatHistory", {
      method: "POST",
      body: JSON.stringify({
        "topicId":  topic.topicId,
        "courseNumber": curriculumId,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let getChatHistoryData = await getChatHistoryResponse.json();
    return getChatHistoryData;
  }

  async function delay(time) {
    return new Promise(res => {
      setTimeout(res,time)
    })
  }

  async function recursiveGetLatestMsg(curriculumId) {
    console.log("getting latest msg recursively")
    let chatHistory = await getChatHistory(curriculumId);
    
    if (chatHistory.chatHistory.length == finalTexts.length - 1) {
      await delay(4000);
      chatHistory = await recursiveGetLatestMsg(curriculumId);
    }
    return chatHistory;
  }

  async function recursiveGetChatHistory(curriculumId) {
    console.log("getting ChatHistory recursively")
    let chatHistory = await getChatHistory(curriculumId);
    
    if (chatHistory == "NoHistory") {
      await delay(4000);
      chatHistory = await recursiveGetChatHistory(curriculumId);
    }
    return chatHistory;
  }

  async function getOrGenerateCurriculum(curriculumId, curriculumName) {
    let chatHistory = await getChatHistory(curriculumId);
    
    if (chatHistory.chatHistory != null) {
      return {
        curriculumId: curriculumId,
        curriculumName: curriculumName,
        chatHistory: chatHistory.chatHistory,
      }
    } else if (chatHistory == "NoHistory") {
      let generateCourseResponse = await fetch(BACKEND_URL + "/generateCourse", {
        method: "POST",
        body: JSON.stringify({
          "topicId":  topic.topicId,
          "courseNumber": curriculumId,
        }),
        headers: {
          "authorizationUserLoginToken": "qwertyuiop:" + username,
        }
      });

      let generateCourseData = await generateCourseResponse.json();
      if (generateCourseData == "Generating Course") {
        let chatHistory = await recursiveGetChatHistory(curriculumId);
        
        return {
          curriculumId: curriculumId,
          curriculumName: curriculumName,
          chatHistory: chatHistory.chatHistory,
        }
      }
    }
  }
    
  async function changeTopic(curriculumId, curriculumName) {
    block = "loading";

    curriculum = await getOrGenerateCurriculum(curriculumId, curriculumName);

    block = "topic-block";
    finalTexts = [];
    curriculum.chatHistory.forEach((msg) => {
      finalTexts = [...finalTexts, msg[1]];
    })

    if (finalTexts.length == 1) { // new chat show typewriter
      displayTexts = [""];
    } else {
      displayTexts = [...finalTexts];
    }
  }

  function updateLatex() {
    console.log("update latex")
    if (document.head.contains(script)) {
      document.head.removeChild(script);
    }
    document.head.append(script);
    
    script.onload = () => {
      MathJax = {
        tex: {inlineMath: [['$', '$'], ['\\(', '\\)']]},
        svg: {fontCache: 'global'}
      };
    };
  }

  function showText() {
    if (!curriculum) return;
    let lastIndex = displayTexts.length - 1;
    if (finalTexts[lastIndex].length > displayTexts[lastIndex].length) {
      displayTexts[lastIndex] = finalTexts[lastIndex].slice(0, displayTexts[lastIndex].length + 1);
      if (displayTexts[displayTexts[lastIndex].length - 1]) {
        setTimeout(showText, 20); // longer pause between words
      } else {
        setTimeout(showText, 5);
      }
    } else {
      writer = null
    }
  }

  afterUpdate(() => {
    if (!writer) {
      writer = setTimeout(showText, 100);
    } 
    updateLatex();
  })

  onMount(() => {
    if (!writer) {
      writer = setTimeout(showText, 500);
    }

    updateLatex();
  })
</script>

{#key curriculum}
  <div
    class="topic-block-wrapper"
    class:dark={theme == "dark"} 
    in:fade = {{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }}
    out:fade = {{ duration: BLOCK_FADE_OUT_DURATION }} 
  >
    <div
      class="glass-container topic-block"
      bind:this={topicBlock}
    >
      {#if curriculum}
        <h2 class="title">{curriculum.curriculumName}</h2>
        {#each displayTexts as displayText, i}
          {#if i % 2 == 0}
            <p>{@html displayText}</p>
          {:else if !displayText.includes(QUIZ_PROMPT)}
            <p class="color-accent-2">{displayText}</p>
          {/if}
        {/each}
        <button
          class="btn-underline quiz-button"
          on:click={() => sendQuery(QUIZ_PROMPT)}
        >
          Quiz Me
        </button>
      {:else}
        <h2 class="title">{topic.title}</h2>

        <div>
          <h4>Knowledge Requirements</h4>
          <p>{topic.prerequisites["Knowledge Requirements"]}</p>
          <h4>Suggested Preparatory Material</h4>
          <p>{topic.prerequisites["Suggested Preparatory Material"]}</p>
        </div>
        
        <div>
          <h4>Curriculum</h4>
          {#each Object.entries(topic.curriculum) as [curriculumId, curriculumName]}
          <span
            class="btn-transparent"
            on:click={() => changeTopic(curriculumId, curriculumName)}
          >
            {curriculumId} {curriculumName}
          </span>
          <br>
          {/each}
        </div>
      {/if}
    </div>

    {#if curriculum}
      <div class="text-bar">
        <input type="text" bind:value={userQueryInput} placeholder="Ask anything about the topic.." />
        <div class="go-btn" on:click={() => sendQuery()}>{">"}</div>
      </div>
    {/if}
    
  </div>
{/key}

<style lang="scss">
  @import "../../styles/root.scss";
  @import "../../styles/topicBlock.scss";
</style>