<script>
  import Content from "./lib/components/Content.svelte";
  import GradientBackground from "./lib/components/GradientBackground.svelte";
  import Navbar from "./lib/components/Navbar.svelte";
  import contrastImage from "./assets/contrast.png"
  import { onMount } from "svelte";

  let block = "login";
  let theme = "light";
  let themeIconRotation = "0deg";
  let backStack = [];
  let forwardStack = [];

  const changeTheme = () => {
    theme = theme == "light" ? "dark" : "light";
    themeIconRotation = parseInt(themeIconRotation.replace("deg", "")) + 180 + "deg";
  }

  onMount(() => {
    if (theme == "dark") {
      themeIconRotation = "180deg";
    }
  })
</script>

<main>
  <Navbar bind:backStack bind:forwardStack bind:block />
  <Content bind:backStack bind:forwardStack bind:block bind:theme />
  <img class="theme-switch-btn" src={contrastImage} on:click={changeTheme} style:rotate={themeIconRotation}>
</main>

<GradientBackground bind:theme />

<style lang="scss">
  main {
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    
    & > * {
      flex: 1;
    }
  }

  .theme-switch-btn {
    position: absolute;
    cursor: pointer;
    width: 30px;
    height: 30px;
    right: 1.5rem;
    bottom: 1.5rem;
    transition: 1s;
  }
</style>
