<script>
  import { slide, fly, fade } from 'svelte/transition';
  import { afterUpdate, onMount } from 'svelte';
  import TopicBlock from "./TopicBlock.svelte";
  import { LOGIN_FLY_IN_DURATION, LOGIN_FLY_OUT_DURATION, GET_STARTED_FADE_IN_DURATION, BLOCK_FADE_OUT_DURATION, BLOCK_FADE_IN_DELAY, BLOCK_FADE_IN_DURATION, BACKEND_URL } from '../constants';

  export let block;
  export let theme;
  export let username;
  export let backStack;
  export let forwardStack;
  export let curriculum;
  export let curriculumHist;

  let prevBlock = block;
  let displayText = "";
  let finalText = "";
  let displayTexts = [];
  let finalTexts = [];
  let topic;
  let topicIdPair;
  let topicInput = "";
  let funFact = "";

  // preserve nav hist
  const navToBlock = (name) => {
    backStack.push(block);
    if (name != forwardStack[forwardStack.length - 1]) { // if new action != forward action
      forwardStack = [];
    } else { // same action == forward -> pop forward stack
      forwardStack.pop();
    }
    block = name;
  }
  
  const back = () => {
    if (block == "topic-block" && curriculum != null) {
      curriculumHist = curriculum;
      curriculum = null;
    } else {
      forwardStack.push(block);
      block = backStack.pop();
    }
  }

  const forward = () => {
    if (block == "topic-block" && curriculumHist != null) {
      curriculum = curriculumHist;
      curriculumHist = null;
    } else {
      backStack.push(block);
      block = forwardStack.pop();
    }
  }

  function showText() {
    if (finalText.length > displayText.length) {
      displayText = finalText.slice(0, displayText.length + 1);

      if (displayText[displayText.length - 1]) {
        setTimeout(showText, 20); // longer pause between words
      } else {
        setTimeout(showText, 5);
      }
    }
  }

  async function changeFunFact(topic) {
    console.log("change fun facts");
    let getFunFactResponse = await fetch(BACKEND_URL + "/getFunFact", {
      method: "POST",
      body: JSON.stringify({
        topic: topic,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });
    funFact = await getFunFactResponse.json();
  }

  async function selectTopicBlock(selectedTopicId) {
    navToBlock("loading");
    changeFunFact(topicIdPair[selectedTopicId]);
    topic = await getTopic(selectedTopicId);
    curriculum = null;
    curriculumHist = null;
    block = "topic-block";
  }

  async function delay(time) {
    return new Promise(res => {
      setTimeout(res,time)
    })
  }

  let recursiveGetPrerequisitesDataCounter = 0;

  async function recursiveGetPrerequisitesData(topicId) {
    let getPrerequisitesResponse = await fetch(BACKEND_URL + "/getPrerequisites", {
      method: "POST",
      body: JSON.stringify({
        topicId: topicId,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let getPrerequisitesData = await getPrerequisitesResponse.json();
    if (getPrerequisitesData == "Error") {
      if (recursiveGetPrerequisitesDataCounter == 20) { // timeout - probably actual error in backend instead of processing
        recursiveGetPrerequisitesDataCounter = 0;
        return getPrerequisitesData;
      }
      await delay(4000);
      recursiveGetPrerequisitesDataCounter ++;
      console.log("waiting prerequisite data");
      getPrerequisitesData = await recursiveGetPrerequisitesData(topicId);
    }
    return getPrerequisitesData;
  }

  let recursiveGetCurriculumDataCounter = 0;

  async function recursiveGetCurriculumData(topicId) {
    let getCurriculumResponse = await fetch(BACKEND_URL + "/getCurriculum", {
      method: "POST",
      body: JSON.stringify({
        topicId: topicId,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let getCurriculumData = await getCurriculumResponse.json();
    if (getCurriculumData == "Error") {
      if (recursiveGetCurriculumDataCounter == 30) { // timeout - probably actual error in backend instead of processing
        recursiveGetCurriculumDataCounter = 0;
        return getCurriculumData;
      }
      await delay(4000);
      recursiveGetCurriculumDataCounter ++;
      console.log()
      console.log("waiting curriculum data");
      getCurriculumData = await recursiveGetCurriculumData(topicId);
    }
    return getCurriculumData;
  }

  async function getTopic(topicId) {
    let getPrerequisitesData = await recursiveGetPrerequisitesData(topicId); // get until finish generate topic

    if (getPrerequisitesData == "Error") {
      getPrerequisitesData = {"prerequisites": {
        "Knowledge Requirements": "",
        "Suggested Preparatory Material": "",
      }}
    }
    
    let getCurriculumData = await recursiveGetCurriculumData(topicId);
    if (getCurriculumData == "Error") {
      getCurriculumData = {"curriculum": {}}
    }
    console.log({
      "topicId": topicId,
      "title": topicIdPair[topicId],
      "prerequisites": getPrerequisitesData["prerequisites"],
      "curriculum": getCurriculumData["curriculum"],
    })

    return {
      "topicId": topicId,
      "title": topicIdPair[topicId],
      "prerequisites": getPrerequisitesData["prerequisites"],
      "curriculum": getCurriculumData["curriculum"],
    }
  }

  async function searchTopic() {
    navToBlock("loading");

    changeFunFact(topicInput);
    let topicId;
    let generateTopicResponse = await fetch(BACKEND_URL + "/generateTopic", {
      method: "POST",
      body: JSON.stringify({
        topic: topicInput,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let generateTopicData = await generateTopicResponse.json();

    if (generateTopicData == "Topic Exist") {
      for (let i in topicIdPair) {
        if (topicIdPair[i].toLowerCase().trim() == topicInput.toLowerCase().trim()) {
          topicId = i;
        }
      }
    } else if (generateTopicData.includes("Topic ID:")) {
      topicId = parseInt(generateTopicData.substring(9));
    } else {
      console.log("error occuring connecting to backend");
      block = "topic-search";
    }
    topicIdPair = await getTopicIdPair();
    topic = await getTopic(topicId);
    
    block = "topic-block";
    topicInput = "";
  }

  async function getTopicIdPair() {
    let getTopicIdPairResponse = await fetch(BACKEND_URL + "/getTopicIdPair", {
      method: "POST",
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let getTopicIdPairData = await getTopicIdPairResponse.json();
    return getTopicIdPairData["topicIdPair"];
  }

  async function deleteTopic(topicId) {
    let deleteTopicResponse = await fetch(BACKEND_URL + "/deleteTopic", {
      method: "POST",
      body: JSON.stringify({
        topicId: topicId,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let deleteTopicData = await deleteTopicResponse.json();
    if (deleteTopicData == "deleted") {
      topicIdPair = await getTopicIdPair();
    }
  }

  async function login() {
    block = "loading";
    topicIdPair = await getTopicIdPair();
    
    setTimeout(() => {
      block = "action"
    }, LOGIN_FLY_OUT_DURATION)
  }

  afterUpdate(() => {
    if (block != prevBlock) {
      displayText = "";

      if (block == "action") {
        finalText = "Get started"
      } else if (block == "topic-search") {
        finalText = "Search for a topic you want to learn...";
      } else if (block == "resume-topic") {
        finalText = "Pick a topic to resume...";
      }
      prevBlock = block;
      setTimeout(showText, 500);
    }
  })
</script>

<div class="content-container" class:dark={theme=="dark"}>
  {#if block != "login" && backStack.length != 0 }
    <div
      class="back-button"
      on:click={() => back()}
    >
      {"<"}
    </div>
  {/if}

  {#if block != "login" && (forwardStack.length != 0 || (block == "topic-block" && curriculumHist != null)) }
    <div
      class="forward-button"
      on:click={() => forward()}
    >
      {">"}
    </div>
  {/if}

  {#if block == "login"}
    <div class="login-block glass-container" in:fly={{ y: -70, duration: LOGIN_FLY_IN_DURATION }} out:fly={{ y: -90, duration: LOGIN_FLY_OUT_DURATION }}>
      <h2 class="logo">AI Tutor</h2>
      <p>Please login to start your learning journey</p>
      <input type="text" placeholder="Username"/>
      <input type="password" placeholder="Password"/>
      <button class="btn-underline" on:click={() => login()} style="left: 1px">Submit</button>
    </div>
  {/if}
  
  {#if block == "action"}
    <div class="block action-block" in:fade={{ duration: GET_STARTED_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
      <h3 class="condensed">Get started</h3>
      <div class="choice-container">
        <div class="glass-container card" on:click={() => navToBlock("topic-search")}>New Topic</div>
        <div class="glass-container card" on:click={() => navToBlock("resume-topic")}>Resume Topic</div>
      </div>
    </div>
  {/if}

  {#if block == "topic-search"}
    <div class="block" in:fade={{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
      <p>{displayText}</p>
      <div class="text-bar">
        <input type="text" bind:value={topicInput} placeholder="Search a topic you want to learn.." />
        <div class="go-btn" on:click={() => searchTopic()}>{">"}</div>
      </div>
    </div>
  {/if}

  {#if block == "resume-topic"}
    <div class="block resume-block" in:fade={{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
      <p>{displayText}</p>
      <ul>
        {#each Object.entries(topicIdPair) as [topicId, title]}
          {#if topicId != "1"}
          <li>
            <span class="btn-transparent" on:click={() => selectTopicBlock(topicId)}>{title}</span>
            <span class="btn-transparent remove-btn">X</span>
            <!-- on:click={() => deleteTopic(topicId)} -->
          </li>
          {/if}
        {/each}
      </ul>
    </div>
  {/if}

  {#if block == "topic-block"}
    <div class="block" in:fade={{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
      <TopicBlock
        changeFunFact = {changeFunFact}
        bind:username
        bind:topic
        bind:curriculum
        bind:theme
        bind:block
        bind:finalTexts
        bind:displayTexts
      />
    </div>
  {/if}

  {#if block == "loading"}
  <div class="block" in:fade={{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
    <div class="loading-screen">
      <div>
        <span class="loading-dot-1">.</span>
        <span class="loading-dot-2">.</span>
        <span class="loading-dot-3">.</span>
      </div>
      <div class="fun-fact" in:fade={{ delay: 5000, duration: 1000 }}>{funFact}</div>
    </div>
  </div>
  {/if}

</div>

<style lang="scss">
  @import "../../styles/root.scss";
  @import "../../styles/content.scss";    
</style>