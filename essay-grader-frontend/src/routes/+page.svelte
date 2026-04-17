<script>
	import { onMount } from 'svelte';

	let mounted = $state(false);
	let essayText = $state('');
	let charCount = $state(0);

	onMount(() => {
		mounted = true;
	});

	function handleInput(e) {
		essayText = e.target.value;
		charCount = essayText.length;
	}

	const features = [
		{
			icon: '◈',
			title: 'Rubric-Aligned Scoring',
			desc: 'Grades against your custom rubric or standard academic criteria.'
		},
		{
			icon: '◉',
			title: 'Detailed Feedback',
			desc: 'Line-by-line annotations covering argument, evidence, and style.'
		},
		{
			icon: '◇',
			title: 'Instant Results',
			desc: 'Get a full grade report in seconds, not days.'
		}
	];
</script>

<div class="root" class:mounted>
	<!-- Ambient background -->
	<div class="bg-grid" aria-hidden="true"></div>
	<div class="bg-glow" aria-hidden="true"></div>

	<!-- Hero -->
	<header class="hero">
		<div class="hero-label">AI-Powered Grading</div>
		<h1>
			<span class="line1">Essays, graded</span>
			<span class="line2">with precision.</span>
		</h1>
		<p class="hero-sub">
			Paste any essay. Get structured feedback, a score, and actionable notes — instantly.
		</p>

		<!-- Essay input card -->
		<div class="card">
			<div class="card-header">
				<span class="card-dot red"></span>
				<span class="card-dot yellow"></span>
				<span class="card-dot green"></span>
				<span class="card-title">Paste your essay</span>
			</div>
			<textarea placeholder="Start typing or paste an essay here…" oninput={handleInput} rows="6"
			></textarea>
			<div class="card-footer">
				<span class="char-count">{charCount} characters</span>
				<a href="/grade" class="grade-btn">
					Grade this essay
					<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
						<path
							d="M3 8h10M9 4l4 4-4 4"
							stroke="currentColor"
							stroke-width="1.5"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				</a>
			</div>
		</div>
	</header>

	<!-- Features -->
	<section class="features">
		{#each features as f, i (f.title)}
			<div class="feature" style="--i:{i}">
				<div class="feature-icon">{f.icon}</div>
				<h3>{f.title}</h3>
				<p>{f.desc}</p>
			</div>
		{/each}
	</section>

	<!-- Score preview strip -->
	<section class="score-strip">
		<div class="score-strip-inner">
			<div class="score-block">
				<div class="score-num">A–</div>
				<div class="score-label">Argument</div>
			</div>
			<div class="divider"></div>
			<div class="score-block">
				<div class="score-num">B+</div>
				<div class="score-label">Evidence</div>
			</div>
			<div class="divider"></div>
			<div class="score-block">
				<div class="score-num">A</div>
				<div class="score-label">Clarity</div>
			</div>
			<div class="divider"></div>
			<div class="score-block">
				<div class="score-num">92</div>
				<div class="score-label">Overall</div>
			</div>
			<div class="strip-cta">
				<span>Sample output →</span>
			</div>
		</div>
	</section>

	<footer>
		<span>© 2026 EssayGrader</span>
		<span>Built for educators.</span>
	</footer>
</div>

<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

	:global(*, *::before, *::after) {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}
	:global(body) {
		background: #0d0f0e;
	}

	.root {
		--ink: #f0ede6;
		--ink-muted: #8a897f;
		--accent: #c8f55a;
		--accent-dim: #9cbf3a;
		--surface: #161a17;
		--border: rgba(255, 255, 255, 0.07);
		--font-display: 'DM Serif Display', Georgia, serif;
		--font-sans: 'DM Sans', sans-serif;
		--font-mono: 'DM Mono', monospace;

		min-height: 100vh;
		background: #0d0f0e;
		color: var(--ink);
		font-family: var(--font-sans);
		position: relative;
		overflow-x: hidden;
	}

	/* Background */
	.bg-grid {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: 0;
		background-image:
			linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),
			linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
		background-size: 48px 48px;
	}
	.bg-glow {
		position: fixed;
		top: -20%;
		left: 50%;
		transform: translateX(-50%);
		width: 700px;
		height: 500px;
		pointer-events: none;
		z-index: 0;
		background: radial-gradient(ellipse at center, rgba(200, 245, 90, 0.07) 0%, transparent 70%);
	}

	/* Nav */
	nav {
		position: relative;
		z-index: 10;
		padding: 0 2rem;
		border-bottom: 1px solid var(--border);
	}
	.nav-inner {
		max-width: 900px;
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

	/* Hero */
	.hero {
		position: relative;
		z-index: 5;
		max-width: 900px;
		margin: 0 auto;
		padding: 5rem 2rem 3rem;
		opacity: 0;
		transform: translateY(20px);
		transition:
			opacity 0.7s ease,
			transform 0.7s ease;
	}
	.mounted .hero {
		opacity: 1;
		transform: translateY(0);
	}

	.hero-label {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--accent);
		letter-spacing: 0.12em;
		text-transform: uppercase;
		margin-bottom: 1.5rem;
	}
	h1 {
		font-family: var(--font-display);
		font-size: clamp(3rem, 7vw, 5.5rem);
		line-height: 1.05;
		letter-spacing: -0.02em;
		margin-bottom: 1.5rem;
		display: flex;
		flex-direction: column;
	}
	.line2 {
		font-style: italic;
		color: var(--accent);
	}

	.hero-sub {
		font-size: 1.1rem;
		color: var(--ink-muted);
		max-width: 520px;
		line-height: 1.6;
		margin-bottom: 2.5rem;
		font-weight: 300;
	}

	/* Card */
	.card {
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 12px;
		overflow: hidden;
		max-width: 680px;
		box-shadow: 0 24px 60px rgba(0, 0, 0, 0.4);
		transition: box-shadow 0.3s;
	}
	.card:focus-within {
		box-shadow:
			0 24px 60px rgba(0, 0, 0, 0.5),
			0 0 0 2px rgba(200, 245, 90, 0.25);
	}
	.card-header {
		display: flex;
		align-items: center;
		gap: 6px;
		padding: 0.75rem 1rem;
		border-bottom: 1px solid var(--border);
		background: rgba(255, 255, 255, 0.02);
	}
	.card-dot {
		width: 10px;
		height: 10px;
		border-radius: 50%;
	}
	.card-dot.red {
		background: #ff5f57;
	}
	.card-dot.yellow {
		background: #febc2e;
	}
	.card-dot.green {
		background: #28c840;
	}
	.card-title {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--ink-muted);
		margin-left: 6px;
	}
	textarea {
		width: 100%;
		min-height: 160px;
		padding: 1rem;
		background: transparent;
		border: none;
		outline: none;
		color: var(--ink);
		font-family: var(--font-sans);
		font-size: 0.95rem;
		line-height: 1.65;
		resize: vertical;
		caret-color: var(--accent);
	}
	textarea::placeholder {
		color: var(--ink-muted);
	}
	.card-footer {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.75rem 1rem;
		border-top: 1px solid var(--border);
	}
	.char-count {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--ink-muted);
	}
	.grade-btn {
		display: flex;
		align-items: center;
		gap: 6px;
		background: var(--accent);
		color: #0d0f0e;
		text-decoration: none;
		padding: 0.45rem 1.1rem;
		border-radius: 6px;
		font-weight: 500;
		font-size: 0.875rem;
		transition:
			background 0.2s,
			transform 0.15s;
	}
	.grade-btn:hover {
		background: var(--accent-dim);
		transform: translateX(2px);
	}

	/* Features */
	.features {
		position: relative;
		z-index: 5;
		max-width: 900px;
		margin: 0 auto;
		padding: 4rem 2rem;
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1.5rem;
	}
	@media (max-width: 640px) {
		.features {
			grid-template-columns: 1fr;
		}
	}
	.feature {
		padding: 1.5rem;
		border: 1px solid var(--border);
		border-radius: 10px;
		background: var(--surface);
		opacity: 0;
		transform: translateY(16px);
		transition:
			opacity 0.5s ease calc(var(--i) * 0.12s),
			transform 0.5s ease calc(var(--i) * 0.12s);
	}
	.mounted .feature {
		opacity: 1;
		transform: translateY(0);
	}
	.feature-icon {
		font-size: 1.3rem;
		color: var(--accent);
		margin-bottom: 0.75rem;
	}
	.feature h3 {
		font-family: var(--font-display);
		font-size: 1.05rem;
		margin-bottom: 0.4rem;
		color: var(--ink);
	}
	.feature p {
		font-size: 0.875rem;
		color: var(--ink-muted);
		line-height: 1.55;
	}

	/* Score strip */
	.score-strip {
		position: relative;
		z-index: 5;
		border-top: 1px solid var(--border);
		border-bottom: 1px solid var(--border);
		background: var(--surface);
		padding: 2rem;
		overflow-x: auto;
	}
	.score-strip-inner {
		max-width: 900px;
		margin: 0 auto;
		display: flex;
		align-items: center;
		gap: 2rem;
		flex-wrap: nowrap;
	}
	.score-block {
		text-align: center;
		flex-shrink: 0;
	}
	.score-num {
		font-family: var(--font-display);
		font-size: 2.2rem;
		color: var(--accent);
		font-style: italic;
		line-height: 1;
		margin-bottom: 4px;
	}
	.score-label {
		font-family: var(--font-mono);
		font-size: 0.7rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: var(--ink-muted);
	}
	.divider {
		width: 1px;
		height: 48px;
		background: var(--border);
		flex-shrink: 0;
	}
	.strip-cta {
		margin-left: auto;
		flex-shrink: 0;
		font-family: var(--font-mono);
		font-size: 0.8rem;
		color: var(--accent);
		cursor: pointer;
		white-space: nowrap;
	}

	/* Footer */
	footer {
		position: relative;
		z-index: 5;
		max-width: 900px;
		margin: 0 auto;
		padding: 2rem;
		display: flex;
		justify-content: space-between;
		font-size: 0.8rem;
		color: var(--ink-muted);
		font-family: var(--font-mono);
	}
</style>
