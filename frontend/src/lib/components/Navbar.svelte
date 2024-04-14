<script>

  import { fade } from 'svelte/transition';
  import { GET_STARTED_FADE_IN_DURATION } from '../constants';
  import TopicBlock from './TopicBlock.svelte';

  export let block;
  export let forwardStack;
  export let backStack;
  export let curriculum;
  export let curriculumHist;
  
  const toBlock = (name) => {
    block = name;
    curriculum = null;
    curriculumHist = null;
    if (name == "topic-search" || name == "resume-topic") {
      forwardStack = [];
      backStack = ["action"];
    } else if (name == "login") {
      forwardStack = [];
      backStack = [];
    }
  }
</script>

{#if block != "login" && block != "loading"}
<header in:fade={{ duration: GET_STARTED_FADE_IN_DURATION }}>
  <h1 class="logo" on:click={() => (block = "action")}>AI Tutor</h1>

  <div class='menu'>
    <svg width="25" height="25" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect class="top" x="20" y="29" width="60" height="7.85106" fill="#fff" />
      <rect class="bottom" x="20" y="62.1489" width="60" height="7.85106" fill="#fff" />
    </svg>
    <div class="menu-dropdown">
      <div
        class="btn-transparent" on:click={() => toBlock("topic-search")}>New Topic</div>
      <div class="btn-transparent" on:click={() => toBlock("resume-topic")}>Resume Topic</div>
      <!-- <div on:click={() => (block="")}>Profile</div> -->
      <div class="btn-transparent" on:click={() => toBlock("login")}>Logout</div>
    </div>
  </div>
</header>
{/if}

<style lang="scss">
  @import "../../styles/root.scss";
  @import "../../styles/navbar.scss";   
</style>