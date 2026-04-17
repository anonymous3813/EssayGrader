<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<nav>
	<div class="nav-inner">
		<a href="/" class="wordmark">Essay<em>Grader</em></a>
		<div class="nav-links">
			<a href="/rubrics">Rubrics</a>
			<a href="/grade" class="nav-cta">Grade Now →</a>
		</div>
	</div>
</nav>

{@render children()}

<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

	:global(*, *::before, *::after) {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}

	:global(:root) {
		--ink: #f0ede6;
		--ink-muted: #8a897f;
		--accent: #c8f55a;
		--accent-dim: #9cbf3a;
		--surface: #161a17;
		--border: rgba(255, 255, 255, 0.07);
		--font-display: 'DM Serif Display', Georgia, serif;
		--font-sans: 'DM Sans', sans-serif;
		--font-mono: 'DM Mono', monospace;
	}

	:global(body) {
		background: #0d0f0e;
		color: var(--ink);
		font-family: var(--font-sans);
	}

	nav {
		position: relative;
		z-index: 10;
		padding: 0 2rem;
		border-bottom: 1px solid var(--border);
		/*background: #0d0f0e;*/
	}
	.nav-inner {
		max-width: 1100px;
		margin: 0 auto;
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 60px;
	}
	.wordmark {
		font-family: var(--font-display);
		font-size: 1.2rem;
		letter-spacing: -0.01em;
		color: var(--ink);
		text-decoration: none;
	}
	.wordmark em {
		font-style: italic;
		color: var(--accent);
	}
	.nav-links {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}
	.nav-links a {
		color: var(--ink-muted);
		text-decoration: none;
		font-size: 0.875rem;
		transition: color 0.2s;
	}
	.nav-links a:hover {
		color: var(--ink);
	}
	.nav-cta {
		background: var(--accent) !important;
		color: #0d0f0e !important;
		padding: 0.4rem 1rem;
		border-radius: 6px;
		font-weight: 500;
		font-size: 0.875rem !important;
		transition: background 0.2s !important;
	}
	.nav-cta:hover {
		background: var(--accent-dim) !important;
	}
</style>
