<script>
	import { onMount } from 'svelte';
	
	onMount(() => {
		for (let item of document.getElementsByTagName("script")) {
			if (item.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js") {
				item.remove();
			}
		}

		let script = document.createElement('script');
		script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
		document.head.append(script);

		script.onload = () => {
			MathJax = {
				tex: {inlineMath: [['$', '$'], ['\\(', '\\)']]},
				svg: {fontCache: 'global'}
			};
			console.log("update latex")
		}
	});
</script>

<p>
	<slot />
</p>